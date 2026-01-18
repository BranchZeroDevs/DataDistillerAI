#!/usr/bin/env python3
"""
Kafka Producer Test - Phase 1
Sends test messages to Kafka topic
"""

import json
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC_NAME = 'doc-ingest-requests'


def create_producer():
    """Create Kafka producer with JSON serialization"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,
            max_in_flight_requests_per_connection=1  # Ensure ordering
        )
        logger.info(f"✅ Kafka producer created successfully")
        return producer
    except KafkaError as e:
        logger.error(f"❌ Failed to create Kafka producer: {e}")
        raise


def send_test_messages(producer, num_messages=10):
    """Send test document upload events"""
    logger.info(f"📤 Sending {num_messages} test messages to topic: {TOPIC_NAME}")
    
    for i in range(num_messages):
        # Create test document upload event
        job_id = str(uuid.uuid4())
        message = {
            'job_id': job_id,
            'filename': f'test_document_{i+1}.pdf',
            'file_size': 1024 * (i + 1),
            'content_type': 'application/pdf',
            's3_bucket': 'datadistiller-docs',
            's3_key': f'uploads/{job_id}/test_document_{i+1}.pdf',
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': {
                'user_id': 'test-user',
                'source': 'test-producer'
            }
        }
        
        try:
            # Send message
            future = producer.send(
                TOPIC_NAME,
                key=job_id,
                value=message
            )
            
            # Wait for send to complete (synchronous for testing)
            record_metadata = future.get(timeout=10)
            
            logger.info(
                f"✅ Message {i+1}/{num_messages} sent: "
                f"job_id={job_id}, "
                f"partition={record_metadata.partition}, "
                f"offset={record_metadata.offset}"
            )
            
            # Small delay between messages
            time.sleep(0.5)
            
        except KafkaError as e:
            logger.error(f"❌ Failed to send message {i+1}: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error sending message {i+1}: {e}")
    
    # Flush to ensure all messages are sent
    producer.flush()
    logger.info("✅ All messages flushed to Kafka")


def test_performance(producer, num_messages=100):
    """Test producer throughput"""
    logger.info(f"⚡ Performance test: Sending {num_messages} messages")
    
    start_time = time.time()
    
    for i in range(num_messages):
        message = {
            'job_id': str(uuid.uuid4()),
            'test_number': i,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        producer.send(TOPIC_NAME, value=message)
        
        if (i + 1) % 10 == 0:
            logger.info(f"Sent {i+1}/{num_messages} messages")
    
    producer.flush()
    end_time = time.time()
    
    duration = end_time - start_time
    throughput = num_messages / duration
    
    logger.info(f"✅ Performance Results:")
    logger.info(f"  Total messages: {num_messages}")
    logger.info(f"  Duration: {duration:.2f} seconds")
    logger.info(f"  Throughput: {throughput:.2f} messages/second")


def main():
    """Main test function"""
    logger.info("=" * 70)
    logger.info("KAFKA PRODUCER TEST - PHASE 1")
    logger.info("=" * 70)
    
    try:
        # Create producer
        producer = create_producer()
        
        # Test 1: Send test messages
        logger.info("\n📝 Test 1: Sending test document upload events")
        send_test_messages(producer, num_messages=5)
        
        # Test 2: Performance test
        logger.info("\n📝 Test 2: Performance test")
        test_performance(producer, num_messages=50)
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ KAFKA PRODUCER TEST COMPLETE")
        logger.info("=" * 70)
        logger.info(f"\n💡 Next steps:")
        logger.info(f"  1. Check Kafka UI: http://localhost:9000")
        logger.info(f"  2. View topic '{TOPIC_NAME}' for messages")
        logger.info(f"  3. Run consumer: python workers/test_kafka_consumer.py")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'producer' in locals():
            producer.close()
            logger.info("Producer closed")


if __name__ == "__main__":
    main()
