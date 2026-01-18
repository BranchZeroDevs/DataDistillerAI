#!/usr/bin/env python3
"""
Simplified Phase 2 & 3 Test - Without Docker
Tests API and workers with mock infrastructure
"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if required packages are installed"""
    logger.info("\n1️⃣  Checking dependencies...")
    
    missing = []
    
    try:
        import fastapi
        logger.info("  ✅ fastapi installed")
    except ImportError:
        missing.append("fastapi")
    
    try:
        import uvicorn
        logger.info("  ✅ uvicorn installed")
    except ImportError:
        missing.append("uvicorn")
    
    try:
        import kafka
        logger.info("  ✅ kafka-python installed")
    except ImportError:
        missing.append("kafka-python")
    
    try:
        import minio
        logger.info("  ✅ minio installed")
    except ImportError:
        missing.append("minio")
    
    try:
        import psycopg2
        logger.info("  ✅ psycopg2 installed")
    except ImportError:
        missing.append("psycopg2-binary")
    
    if missing:
        logger.warning(f"  ⚠️  Missing packages: {', '.join(missing)}")
        logger.info(f"  Install with: pip install {' '.join(missing)}")
        return False
    
    logger.info("  ✅ All dependencies installed")
    return True


def check_file_structure():
    """Check if all Phase 2 & 3 files exist"""
    logger.info("\n2️⃣  Checking file structure...")
    
    required_files = [
        "api/main.py",
        "api/models.py",
        "api/v2/upload.py",
        "api/v2/query.py",
        "workers/ingestion_worker.py",
        "workers/embedding_worker.py",
        "storage/clients.py",
        "docker-compose.yml"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = Path(file_path)
        if full_path.exists():
            logger.info(f"  ✅ {file_path}")
        else:
            logger.error(f"  ❌ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist


def check_docker():
    """Check if Docker is available"""
    logger.info("\n3️⃣  Checking Docker...")
    
    import subprocess
    try:
        result = subprocess.run(['docker', 'version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            logger.info("  ✅ Docker is installed")
            
            # Check if Docker daemon is running
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logger.info("  ✅ Docker is running")
                return True
            else:
                logger.warning("  ⚠️  Docker is installed but not running")
                logger.info("  💡 Start Docker Desktop to enable full testing")
                return False
        else:
            logger.warning("  ⚠️  Docker command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        logger.warning("  ⚠️  Docker not found")
        logger.info("  💡 Install Docker Desktop to enable infrastructure testing")
        return False


def test_api_imports():
    """Test if API can be imported"""
    logger.info("\n4️⃣  Testing API imports...")
    
    try:
        import sys
        sys.path.insert(0, str(Path.cwd()))
        
        from api import models
        logger.info("  ✅ api.models imported")
        
        # Test model creation
        from api.models import UploadResponse, JobStatus
        upload = UploadResponse(
            job_id="test-123",
            status=JobStatus.PENDING,
            filename="test.pdf",
            file_size=1024
        )
        logger.info(f"  ✅ Created UploadResponse: {upload.job_id}")
        
        return True
    except Exception as e:
        logger.error(f"  ❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_worker_imports():
    """Test if workers can be imported"""
    logger.info("\n5️⃣  Testing worker imports...")
    
    try:
        # Test chunker
        from src.processing.chunker import SemanticChunker
        chunker = SemanticChunker()
        logger.info("  ✅ SemanticChunker imported")
        
        # Test vector store
        from src.retrieval import VectorStore
        logger.info("  ✅ VectorStore imported")
        
        return True
    except Exception as e:
        logger.error(f"  ❌ Import failed: {e}")
        return False


def show_next_steps(has_docker: bool):
    """Show what to do next"""
    logger.info("\n" + "=" * 70)
    logger.info("📋 NEXT STEPS")
    logger.info("=" * 70)
    
    if has_docker:
        logger.info("\n✅ Docker is available - Full testing possible!")
        logger.info("\n🚀 To start the full system:")
        logger.info("\n1. Start infrastructure:")
        logger.info("   docker compose up -d")
        logger.info("\n2. Wait 30 seconds for services to start, then open:")
        logger.info("   • Kafka UI:  http://localhost:9000")
        logger.info("   • MinIO:     http://localhost:9001 (minioadmin/minioadmin123)")
        logger.info("   • Grafana:   http://localhost:3000 (admin/admin123)")
        logger.info("\n3. Launch components (in separate terminals):")
        logger.info("   Terminal 1: python api/main.py")
        logger.info("   Terminal 2: python workers/ingestion_worker.py")
        logger.info("   Terminal 3: python workers/embedding_worker.py")
        logger.info("\n4. Run end-to-end test:")
        logger.info("   python test_phase2_3.py")
        logger.info("\n5. Or test manually:")
        logger.info("   curl -X POST http://localhost:8000/api/v2/documents/upload \\")
        logger.info("     -F 'file=@data/documents/machine_learning.txt'")
    else:
        logger.info("\n⚠️  Docker not available - Limited testing only")
        logger.info("\n💡 To enable full testing:")
        logger.info("   1. Install Docker Desktop for Mac")
        logger.info("   2. Start Docker Desktop")
        logger.info("   3. Run this test again")
        logger.info("\n📖 Alternative: Explore the code structure")
        logger.info("   • Read: PHASE2_3_SETUP.md")
        logger.info("   • Review: api/main.py")
        logger.info("   • Study: workers/ingestion_worker.py")
    
    logger.info("\n📚 Documentation:")
    logger.info("   • Setup Guide:  cat PHASE2_3_SETUP.md")
    logger.info("   • Architecture: cat DATADISTILLER_2.0_ROADMAP.md")
    logger.info("   • Quick Ref:    cat PHASE2_3_COMPLETE.md")


def main():
    """Run all checks"""
    logger.info("=" * 70)
    logger.info("PHASE 2 & 3 - SYSTEM CHECK")
    logger.info("=" * 70)
    
    results = {}
    
    # Run checks
    results['dependencies'] = check_dependencies()
    results['files'] = check_file_structure()
    results['docker'] = check_docker()
    results['api'] = test_api_imports()
    results['workers'] = test_worker_imports()
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("SUMMARY")
    logger.info("=" * 70)
    
    for check, passed in results.items():
        status = "✅" if passed else "❌"
        logger.info(f"  {status} {check.capitalize()}")
    
    # Next steps
    show_next_steps(results.get('docker', False))
    
    # Overall status
    if all([results['dependencies'], results['files'], results['api'], results['workers']]):
        logger.info("\n✅ Core system is ready!")
        if not results['docker']:
            logger.info("⚠️  Install Docker to enable full async testing")
        return True
    else:
        logger.info("\n❌ Some components need attention")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
