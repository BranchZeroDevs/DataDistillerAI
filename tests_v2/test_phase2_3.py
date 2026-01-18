#!/usr/bin/env python3
"""
End-to-End Test for Phase 2 & 3
Tests the complete async pipeline: Upload → Ingestion → Embedding
"""

import requests
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configuration
API_URL = "http://localhost:8000"
TEST_FILE = "data/documents/machine_learning.txt"


def test_api_health():
    """Test API health check"""
    logger.info("\n1️⃣  Testing API health...")
    
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200, f"Health check failed: {response.status_code}"
    
    data = response.json()
    logger.info(f"  Status: {data['status']}")
    logger.info(f"  Services: {data['services']}")
    logger.info("  ✅ Health check passed")


def test_document_upload():
    """Test document upload"""
    logger.info("\n2️⃣  Testing document upload...")
    
    # Prepare file
    test_file = Path(TEST_FILE)
    assert test_file.exists(), f"Test file not found: {TEST_FILE}"
    
    with open(test_file, 'rb') as f:
        files = {'file': (test_file.name, f, 'text/plain')}
        response = requests.post(f"{API_URL}/api/v2/documents/upload", files=files)
    
    assert response.status_code == 202, f"Upload failed: {response.status_code}"
    
    data = response.json()
    job_id = data['job_id']
    
    logger.info(f"  Job ID: {job_id}")
    logger.info(f"  Status: {data['status']}")
    logger.info(f"  Filename: {data['filename']}")
    logger.info(f"  Size: {data['file_size']} bytes")
    logger.info("  ✅ Upload accepted")
    
    return job_id


def test_job_status(job_id: str, max_wait: int = 60):
    """Test job status tracking"""
    logger.info(f"\n3️⃣  Tracking job status: {job_id}")
    
    start_time = time.time()
    while True:
        response = requests.get(f"{API_URL}/api/v2/documents/status/{job_id}")
        assert response.status_code == 200, f"Status check failed: {response.status_code}"
        
        data = response.json()
        status = data['status']
        progress = data['progress']
        
        logger.info(f"  Status: {status} ({progress}%)")
        
        if status == 'completed':
            logger.info(f"  Total chunks: {data.get('total_chunks')}")
            logger.info(f"  Processed: {data.get('processed_chunks')}")
            logger.info("  ✅ Job completed")
            break
        
        if status == 'failed':
            logger.error(f"  ❌ Job failed: {data.get('error_message')}")
            return False
        
        # Check timeout
        if time.time() - start_time > max_wait:
            logger.warning(f"  ⏰ Timeout waiting for completion")
            break
        
        time.sleep(2)
    
    return True


def test_job_list():
    """Test listing jobs"""
    logger.info("\n4️⃣  Testing job list...")
    
    response = requests.get(f"{API_URL}/api/v2/documents/list", params={'limit': 10})
    assert response.status_code == 200, f"List failed: {response.status_code}"
    
    data = response.json()
    logger.info(f"  Total jobs: {data['total']}")
    
    for job in data['jobs'][:3]:
        logger.info(f"    - {job['filename']}: {job['status']} ({job['progress']}%)")
    
    logger.info("  ✅ List successful")


def test_query():
    """Test querying documents"""
    logger.info("\n5️⃣  Testing query...")
    
    query_data = {
        "question": "What is machine learning?",
        "top_k": 3,
        "retrieval_method": "dense"
    }
    
    response = requests.post(f"{API_URL}/api/v2/query", json=query_data)
    assert response.status_code == 200, f"Query failed: {response.status_code}"
    
    data = response.json()
    logger.info(f"  Query ID: {data['query_id']}")
    logger.info(f"  Question: {data['question']}")
    logger.info(f"  Answer: {data['answer'][:200]}...")
    logger.info(f"  Sources: {len(data['sources'])}")
    logger.info(f"  Latency: {data['latency_ms']}ms")
    logger.info("  ✅ Query successful")


def main():
    """Run all tests"""
    logger.info("=" * 70)
    logger.info("END-TO-END TEST - PHASE 2 & 3")
    logger.info("=" * 70)
    logger.info("\n📋 Prerequisites:")
    logger.info("  1. Docker services running: docker-compose ps")
    logger.info("  2. API running: python api/main.py")
    logger.info("  3. Ingestion worker: python workers/ingestion_worker.py")
    logger.info("  4. Embedding worker: python workers/embedding_worker.py")
    logger.info("")
    
    try:
        # Run tests
        test_api_health()
        job_id = test_document_upload()
        test_job_status(job_id, max_wait=120)
        test_job_list()
        test_query()
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ ALL TESTS PASSED")
        logger.info("=" * 70)
        logger.info("\n🎉 Phase 2 & 3 Complete!")
        logger.info("\n📊 Check these UIs:")
        logger.info("  • API Docs: http://localhost:8000/docs")
        logger.info("  • Kafka UI: http://localhost:9000")
        logger.info("  • MinIO: http://localhost:9001")
        
    except AssertionError as e:
        logger.error(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
