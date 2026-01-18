#!/usr/bin/env python3
"""
Kafka Consumer Test - Phase 1
Consumes messages from Kafka topic with consumer group demonstration
"""

import json
import time
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC_NAME = 'doc-ingest-requests'
CONSUMER_GROUP = 'datadistiller-workers'

# Graceful shutdown
shutdown_flag = False

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    global shutdown_flag
    logger.info("\n🛑 Shutdown signal received, stopping consumer...")
    shutdown_flag = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def create_consumer(consumer_id="worker-1"):
    """Create Kafka consumer with auto-commit"""
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=CONSUMER_GROUP,
            auto_offset_reset='earliest',  # Start from beginning if no offset
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            consumer_timeout_ms=1000,  # Poll timeout
            client_id=consumer_id
        )
        logger.info(f"✅ Kafka consumer '{consumer_id}' created successfully")
        logger.info(f"  Consumer group: {CONSUMER_GROUP}")
        logger.info(f"  Topic: {TOPIC_NAME}")
        return consumer
    except KafkaError as e:
        logger.error(f"❌ Failed to create Kafka consumer: {e}")
        raise


def process_message(message):
    """
    Process a single message (simulates real work)
    
    Args:
        message: Kafka message object
    """
    try:
        # Extract data
        key = message.key
        value = message.value
        partition = message.partition
        offset = message.offset
        
        logger.info(f"📥 Received message:")
        logger.info(f"  Partition: {partition}, Offset: {offset}")
        logger.info(f"  Key: {key}")
        logger.info(f"  Job ID: {value.get('job_id')}")
        logger.info(f"  Filename: {value.get('filename')}")
        logger.info(f"  File size: {value.get('file_size')} bytes")
        
        # Simulate processing work
        processing_time = 0.5  # seconds
        time.sleep(processing_time)
        
        logger.info(f"✅ Processed message from partition {partition}, offset {offset}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error processing message: {e}")
        return False


def consume_messages(consumer_id="worker-1"):
    """Main consumer loop"""
    global shutdown_flag
    
    consumer = create_consumer(consumer_id)
    message_count = 0
    error_count = 0
    
    logger.info(f"🔄 Starting consumer loop for '{consumer_id}'")
    logger.info(f"Press Ctrl+C to stop")
    logger.info("=" * 70)
    
    try:
        while not shutdown_flag:
            # Poll for messages
            messages = consumer.poll(timeout_ms=1000, max_records=10)
            
            if not messages:
                continue
            
            # Process each partition's messages
            for topic_partition, records in messages.items():
                for message in records:
                    message_count += 1
                    
                    success = process_message(message)
                    
                    if not success:
                        error_count += 1
                    
                    logger.info(f"📊 Stats: Processed={message_count}, Errors={error_count}")
                    logger.info("-" * 70)
            
            # Commit offsets (already auto-committed, but can be manual)
            # consumer.commit()
        
        logger.info(f"\n✅ Consumer '{consumer_id}' stopped gracefully")
        logger.info(f"  Total processed: {message_count}")
        logger.info(f"  Total errors: {error_count}")
        
    except KafkaError as e:
        logger.error(f"❌ Kafka error: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        consumer.close()
        logger.info(f"Consumer '{consumer_id}' closed")


def test_consumer_group():
    """
    Demonstrate consumer group load balancing
    Run this multiple times in different terminals to see partitioning
    """
    import os
    
    # Get consumer ID from environment or generate
    consumer_id = os.environ.get('CONSUMER_ID', 'worker-1')
    
    logger.info("=" * 70)
    logger.info(f"KAFKA CONSUMER TEST - {consumer_id.upper()}")
    logger.info("=" * 70)
    logger.info(f"\n💡 Consumer Group Demo:")
    logger.info(f"  This consumer belongs to group: {CONSUMER_GROUP}")
    logger.info(f"  Multiple consumers in same group will share the load")
    logger.info(f"\n📝 Try this:")
    logger.info(f"  1. Run this consumer: python workers/test_kafka_consumer.py")
    logger.info(f"  2. In another terminal: CONSUMER_ID=worker-2 python workers/test_kafka_consumer.py")
    logger.info(f"  3. Send messages: python workers/test_kafka_producer.py")
    logger.info(f"  4. Watch how messages are distributed across consumers!\n")
    
    consume_messages(consumer_id)


def main():
    """Main entry point"""
    test_consumer_group()


if __name__ == "__main__":
    main()
