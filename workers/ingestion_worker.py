"""
Ingestion Worker - Consumes upload events and splits documents into chunks
Phase 3: Fan-Out Processing
"""

import json
import logging
import signal
import sys
import uuid
import hashlib
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
from storage.clients import PostgresClient, MinIOClient
from src.processing.chunker import SemanticChunker
import tempfile
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
UPLOAD_TOPIC = 'doc-ingest-requests'
CHUNK_TOPIC = 'chunk-processing'
CONSUMER_GROUP = 'ingestion-workers'
DLQ_TOPIC = 'doc-ingest-dlq'

# Graceful shutdown
shutdown_flag = False

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    global shutdown_flag
    logger.info("\n🛑 Shutdown signal received...")
    shutdown_flag = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


class IngestionWorker:
    """Worker that processes document uploads and fans out to chunks"""
    
    def __init__(self, worker_id="ingestion-worker-1"):
        """Initialize worker"""
        self.worker_id = worker_id
        self.consumer = self._create_consumer()
        self.producer = self._create_producer()
        self.db = PostgresClient()
        self.minio = MinIOClient()
        self.chunker = SemanticChunker(chunk_size=1024, overlap=128)
        
        logger.info(f"✅ {self.worker_id} initialized")
    
    def _create_consumer(self):
        """Create Kafka consumer"""
        return KafkaConsumer(
            UPLOAD_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=CONSUMER_GROUP,
            auto_offset_reset='earliest',
            enable_auto_commit=False,  # Manual commit for reliability
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            consumer_timeout_ms=1000,
            client_id=self.worker_id
        )
    
    def _create_producer(self):
        """Create Kafka producer"""
        return KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',
            retries=3
        )
    
    def process_document(self, job_data: dict) -> bool:
        """
        Process a document: download, split into chunks, fan-out to Kafka
        
        Args:
            job_data: Job metadata
            
        Returns:
            True if successful, False otherwise
        """
        job_id = job_data['job_id']
        
        try:
            logger.info(f"📄 Processing job: {job_id}")
            
            # Update status to processing
            self.db.update_job_status(job_id, 'processing', progress=10)
            
            # Download file from MinIO
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(job_data['filename']).suffix) as tmp_file:
                tmp_path = tmp_file.name
            
            self.minio.download_file(job_data['s3_key'], tmp_path)
            logger.info(f"✅ Downloaded: {job_data['s3_key']}")
            
            # Read file content
            with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Update status to chunking
            self.db.update_job_status(job_id, 'chunking', progress=30)
            
            # Split into chunks
            chunks = self.chunker.chunk(content, metadata={'job_id': job_id, 'filename': job_data['filename']})
            total_chunks = len(chunks)
            
            logger.info(f"✂️  Split into {total_chunks} chunks")
            
            # Update job with chunk count
            self.db.get_connection().cursor().execute("""
                UPDATE document_jobs 
                SET total_chunks = %s 
                WHERE job_id = %s
            """, (total_chunks, job_id))
            self.db.get_connection().commit()
            
            # Fan-out: Send each chunk to chunk-processing topic
            for i, chunk in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                content_hash = hashlib.sha256(chunk.content.encode()).hexdigest()
                
                # Create chunk record in DB
                chunk_data = {
                    'chunk_id': chunk_id,
                    'job_id': job_id,
                    'chunk_index': i,
                    'content': chunk.content,
                    'content_hash': content_hash,
                    'status': 'pending'
                }
                self.db.create_chunk(chunk_data)
                
                # Send to Kafka for embedding
                chunk_message = {
                    'chunk_id': chunk_id,
                    'job_id': job_id,
                    'chunk_index': i,
                    'content': chunk.content,
                    'metadata': chunk.metadata
                }
                
                self.producer.send(
                    CHUNK_TOPIC,
                    key=chunk_id,
                    value=chunk_message
                )
                
                # Update progress
                progress = 30 + int((i + 1) / total_chunks * 40)
                self.db.update_job_status(job_id, 'chunking', progress=progress)
            
            self.producer.flush()
            
            # Update status to embedding (workers will process chunks)
            self.db.update_job_status(job_id, 'embedding', progress=70)
            
            logger.info(f"✅ Fanned out {total_chunks} chunks for job {job_id}")
            
            # Clean up temp file
            Path(tmp_path).unlink()
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error processing job {job_id}: {e}")
            self.db.update_job_status(job_id, 'failed', error=str(e))
            
            # Send to DLQ
            try:
                self.producer.send(DLQ_TOPIC, value=job_data)
                logger.info(f"📮 Sent to DLQ: {job_id}")
            except:
                pass
            
            return False
    
    def run(self):
        """Main worker loop"""
        global shutdown_flag
        
        logger.info(f"🔄 {self.worker_id} starting...")
        logger.info(f"   Consuming from: {UPLOAD_TOPIC}")
        logger.info(f"   Producing to: {CHUNK_TOPIC}")
        logger.info(f"   Consumer group: {CONSUMER_GROUP}")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 70)
        
        processed = 0
        failed = 0
        
        try:
            while not shutdown_flag:
                # Poll for messages
                messages = self.consumer.poll(timeout_ms=1000, max_records=1)
                
                if not messages:
                    continue
                
                # Process each message
                for topic_partition, records in messages.items():
                    for message in records:
                        job_data = message.value
                        
                        logger.info(f"\n📥 Received: job_id={job_data['job_id']}")
                        
                        # Process document
                        success = self.process_document(job_data)
                        
                        if success:
                            processed += 1
                            # Commit offset only after successful processing
                            self.consumer.commit()
                            logger.info(f"✅ Committed offset for {job_data['job_id']}")
                        else:
                            failed += 1
                        
                        logger.info(f"📊 Stats: Processed={processed}, Failed={failed}")
                        logger.info("-" * 70)
            
            logger.info(f"\n✅ {self.worker_id} stopped gracefully")
            logger.info(f"   Total processed: {processed}")
            logger.info(f"   Total failed: {failed}")
        
        except Exception as e:
            logger.error(f"❌ Worker error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.consumer.close()
            self.producer.close()
            logger.info(f"{self.worker_id} closed")


def main():
    """Main entry point"""
    import os
    worker_id = os.environ.get('WORKER_ID', 'ingestion-worker-1')
    
    logger.info("=" * 70)
    logger.info(f"INGESTION WORKER - {worker_id.upper()}")
    logger.info("=" * 70)
    
    worker = IngestionWorker(worker_id)
    worker.run()


if __name__ == "__main__":
    main()
