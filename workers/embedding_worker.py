"""
Embedding Worker - Consumes chunk events and generates embeddings
Phase 3: Fan-Out Processing
"""

import json
import logging
import signal
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from storage.clients import PostgresClient
from src.retrieval import VectorStore
from src.processing.chunker import Chunk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
CHUNK_TOPIC = 'chunk-processing'
CONSUMER_GROUP = 'embedding-workers'
DLQ_TOPIC = 'chunk-processing-dlq'

# Graceful shutdown
shutdown_flag = False

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    global shutdown_flag
    logger.info("\n🛑 Shutdown signal received...")
    shutdown_flag = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


class EmbeddingWorker:
    """Worker that generates embeddings and indexes chunks"""
    
    def __init__(self, worker_id="embedding-worker-1"):
        """Initialize worker"""
        self.worker_id = worker_id
        self.consumer = self._create_consumer()
        self.db = PostgresClient()
        self.vector_store = VectorStore()
        
        logger.info(f"✅ {self.worker_id} initialized")
    
    def _create_consumer(self):
        """Create Kafka consumer"""
        return KafkaConsumer(
            CHUNK_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=CONSUMER_GROUP,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            consumer_timeout_ms=1000,
            client_id=self.worker_id
        )
    
    def process_chunk(self, chunk_data: dict) -> bool:
        """
        Process a chunk: generate embedding and index
        
        Args:
            chunk_data: Chunk metadata
            
        Returns:
            True if successful, False otherwise
        """
        chunk_id = chunk_data['chunk_id']
        job_id = chunk_data['job_id']
        
        try:
            logger.info(f"🔢 Processing chunk: {chunk_id} (job: {job_id})")
            
            # Update chunk status
            self.db.update_chunk_status(chunk_id, 'embedding')
            
            # Create Chunk object
            chunk = Chunk(
                content=chunk_data['content'],
                metadata=chunk_data.get('metadata', {})
            )
            
            # Add to vector store (generates embedding)
            self.vector_store.add_documents([chunk])
            
            # Update chunk status
            self.db.update_chunk_status(chunk_id, 'indexed', vector_id=chunk_id)
            
            # Update job progress
            conn = self.db.get_connection()
            with conn.cursor() as cur:
                # Increment processed count
                cur.execute("""
                    UPDATE document_jobs 
                    SET processed_chunks = processed_chunks + 1
                    WHERE job_id = %s
                    RETURNING processed_chunks, total_chunks
                """, (job_id,))
                
                result = cur.fetchone()
                if result:
                    processed, total = result
                    progress = int((processed / total) * 100) if total > 0 else 100
                    
                    # Update progress
                    cur.execute("""
                        UPDATE document_jobs 
                        SET progress = %s
                        WHERE job_id = %s
                    """, (progress, job_id))
                    
                    # If all chunks done, mark as completed
                    if processed >= total:
                        cur.execute("""
                            UPDATE document_jobs 
                            SET status = 'completed', completed_at = NOW()
                            WHERE job_id = %s
                        """, (job_id,))
                        logger.info(f"🎉 Job {job_id} completed!")
                
                conn.commit()
            conn.close()
            
            logger.info(f"✅ Indexed chunk: {chunk_id}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Error processing chunk {chunk_id}: {e}")
            self.db.update_chunk_status(chunk_id, 'failed', error=str(e))
            return False
    
    def run(self):
        """Main worker loop"""
        global shutdown_flag
        
        logger.info(f"🔄 {self.worker_id} starting...")
        logger.info(f"   Consuming from: {CHUNK_TOPIC}")
        logger.info(f"   Consumer group: {CONSUMER_GROUP}")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 70)
        
        processed = 0
        failed = 0
        
        try:
            while not shutdown_flag:
                # Poll for messages
                messages = self.consumer.poll(timeout_ms=1000, max_records=5)
                
                if not messages:
                    continue
                
                # Process each chunk
                for topic_partition, records in messages.items():
                    for message in records:
                        chunk_data = message.value
                        
                        logger.info(f"\n📥 Received chunk: {chunk_data['chunk_id']}")
                        
                        # Process chunk
                        success = self.process_chunk(chunk_data)
                        
                        if success:
                            processed += 1
                            # Commit offset
                            self.consumer.commit()
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
            # Save vector store
            self.vector_store.save("./data/vector_store")
            logger.info(f"{self.worker_id} closed")


def main():
    """Main entry point"""
    import os
    worker_id = os.environ.get('WORKER_ID', 'embedding-worker-1')
    
    logger.info("=" * 70)
    logger.info(f"EMBEDDING WORKER - {worker_id.upper()}")
    logger.info("=" * 70)
    
    worker = EmbeddingWorker(worker_id)
    worker.run()


if __name__ == "__main__":
    main()
