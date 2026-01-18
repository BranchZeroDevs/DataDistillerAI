"""
FastAPI Application - DataDistiller 2.0
Asynchronous document upload and query API
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import uuid
import logging
from pathlib import Path
import tempfile
from datetime import datetime

from api.models import (
    UploadResponse, JobStatusResponse, JobListResponse,
    QueryRequest, QueryResponse, HealthResponse, ErrorResponse,
    JobStatus
)
from api.v2.upload import upload_document_to_kafka
from api.v2.query import query_documents
from storage.clients import PostgresClient, MinIOClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="DataDistiller 2.0 API",
    description="Asynchronous RAG platform with Kafka-based processing",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients (lazy loaded)
_postgres_client = None
_minio_client = None

def get_postgres_client():
    """Get or create PostgreSQL client"""
    global _postgres_client
    if _postgres_client is None:
        _postgres_client = PostgresClient()
    return _postgres_client

def get_minio_client():
    """Get or create MinIO client"""
    global _minio_client
    if _minio_client is None:
        _minio_client = MinIOClient()
    return _minio_client


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "DataDistiller 2.0 API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services = {}
    
    # Check PostgreSQL
    try:
        db = get_postgres_client()
        conn = db.get_connection()
        conn.close()
        services["postgres"] = "connected"
    except Exception as e:
        services["postgres"] = f"error: {str(e)}"
    
    # Check MinIO
    try:
        minio = get_minio_client()
        services["minio"] = "connected"
    except Exception as e:
        services["minio"] = f"error: {str(e)}"
    
    # Check Kafka (will be added)
    services["kafka"] = "not implemented"
    
    # Overall status
    status = "healthy" if all(v == "connected" or v == "not implemented" for v in services.values()) else "degraded"
    
    return HealthResponse(
        status=status,
        version="2.0.0",
        services=services
    )


@app.post("/api/v2/documents/upload", response_model=UploadResponse, status_code=202)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload document for asynchronous processing
    
    Returns 202 Accepted immediately, processing happens in background via Kafka
    """
    logger.info(f"📤 Upload request: {file.filename} ({file.content_type})")
    
    # Validate file type
    allowed_types = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: PDF, TXT, DOCX"
        )
    
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Upload to MinIO
        minio = get_minio_client()
        s3_key = f"uploads/{job_id}/{file.filename}"
        s3_info = minio.upload_bytes(file_content, s3_key, file.content_type)
        
        # Create database record
        db = get_postgres_client()
        job_data = {
            'job_id': job_id,
            'filename': file.filename,
            'file_size': file_size,
            'content_type': file.content_type,
            's3_bucket': s3_info['bucket'],
            's3_key': s3_info['key'],
            'status': 'pending'
        }
        db.create_job(job_data)
        
        # Send to Kafka (async processing)
        upload_document_to_kafka(job_id, job_data)
        
        logger.info(f"✅ Upload accepted: job_id={job_id}")
        
        return UploadResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            message="Document upload accepted. Processing will begin shortly.",
            filename=file.filename,
            file_size=file_size
        )
    
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v2/documents/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Get processing status for a job
    """
    logger.info(f"📊 Status request: job_id={job_id}")
    
    try:
        db = get_postgres_client()
        job = db.get_job_status(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return JobStatusResponse(**job)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Status query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v2/documents/list", response_model=JobListResponse)
async def list_jobs(limit: int = 100, status: str = None):
    """
    List recent document processing jobs
    """
    logger.info(f"📋 List jobs: limit={limit}, status={status}")
    
    try:
        db = get_postgres_client()
        jobs = db.list_jobs(limit=limit, status=status)
        
        job_responses = [JobStatusResponse(**job) for job in jobs]
        
        return JobListResponse(
            jobs=job_responses,
            total=len(job_responses)
        )
    
    except Exception as e:
        logger.error(f"❌ List jobs failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v2/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query indexed documents
    """
    logger.info(f"🔍 Query: {request.query}")
    
    try:
        start_time = datetime.now()
        
        # Execute query
        result = query_documents(
            query=request.query,
            top_k=request.top_k,
            retrieval_method=request.retrieval_method
        )
        
        end_time = datetime.now()
        latency = int((end_time - start_time).total_seconds() * 1000)
        
        query_id = str(uuid.uuid4())
        
        return QueryResponse(
            query_id=query_id,
            question=request.query,
            answer=result['answer'],
            sources=result['sources'],
            retrieval_method=request.retrieval_method,
            latency_ms=latency
        )
    
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Metrics endpoint (for Prometheus)
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    # TODO: Implement Prometheus metrics
    return {"message": "Metrics endpoint - to be implemented"}


def main():
    """Run the FastAPI application"""
    logger.info("=" * 70)
    logger.info("🚀 Starting DataDistiller 2.0 API")
    logger.info("=" * 70)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
