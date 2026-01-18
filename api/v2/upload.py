"""
Upload handler - sends documents to Kafka for async processing
"""

import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
from typing import Dict

logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
UPLOAD_TOPIC = 'doc-ingest-requests'

# Lazy load producer
_producer = None

def get_kafka_producer():
    """Get or create Kafka producer"""
    global _producer
    if _producer is None:
        try:
            _producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1
            )
            logger.info("✅ Kafka producer initialized")
        except KafkaError as e:
            logger.error(f"❌ Failed to create Kafka producer: {e}")
            raise
    return _producer


def upload_document_to_kafka(job_id: str, job_data: Dict):
    """
    Send document upload event to Kafka
    
    Args:
        job_id: Unique job identifier
        job_data: Job metadata
    """
    try:
        producer = get_kafka_producer()
        
        # Create event message
        message = {
            'job_id': job_id,
            'filename': job_data['filename'],
            'file_size': job_data['file_size'],
            'content_type': job_data['content_type'],
            's3_bucket': job_data['s3_bucket'],
            's3_key': job_data['s3_key'],
            'timestamp': job_data.get('timestamp', None)
        }
        
        # Send to Kafka
        future = producer.send(
            UPLOAD_TOPIC,
            key=job_id,
            value=message
        )
        
        # Wait for confirmation (can be async in production)
        record_metadata = future.get(timeout=10)
        
        logger.info(
            f"✅ Sent to Kafka: job_id={job_id}, "
            f"partition={record_metadata.partition}, "
            f"offset={record_metadata.offset}"
        )
        
    except KafkaError as e:
        logger.error(f"❌ Kafka send failed for job {job_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error sending to Kafka: {e}")
        raise
