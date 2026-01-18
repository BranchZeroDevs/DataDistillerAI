"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):
    """Job processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    COMPLETED = "completed"
    FAILED = "failed"


class UploadResponse(BaseModel):
    """Response for document upload"""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(default=JobStatus.PENDING, description="Initial status")
    message: str = Field(default="Document upload accepted", description="Status message")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "abc-123-def-456",
                "status": "pending",
                "message": "Document upload accepted",
                "filename": "document.pdf",
                "file_size": 1048576
            }
        }


class JobStatusResponse(BaseModel):
    """Response for job status query"""
    job_id: str
    filename: str
    file_size: int
    status: JobStatus
    progress: int = Field(ge=0, le=100, description="Progress percentage")
    total_chunks: Optional[int] = None
    processed_chunks: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "abc-123",
                "filename": "document.pdf",
                "file_size": 1048576,
                "status": "processing",
                "progress": 45,
                "total_chunks": 10,
                "processed_chunks": 4,
                "created_at": "2026-01-18T12:00:00",
                "updated_at": "2026-01-18T12:05:00"
            }
        }


class JobListResponse(BaseModel):
    """Response for listing jobs"""
    jobs: list[JobStatusResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "jobs": [],
                "total": 0
            }
        }


class QueryRequest(BaseModel):
    """Request for querying documents"""
    query: str = Field(..., min_length=1, description="User question", alias="question")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of results to retrieve")
    retrieval_method: str = Field(default="hybrid", description="dense, sparse, or hybrid")
    
    class Config:
        populate_by_name = True  # Accept both 'query' and 'question'
        json_schema_extra = {
            "example": {
                "query": "What is machine learning?",
                "top_k": 3,
                "retrieval_method": "hybrid"
            }
        }


class QueryResponse(BaseModel):
    """Response for query"""
    query_id: str
    question: str
    answer: str
    sources: list[Dict[str, Any]]
    retrieval_method: str
    latency_ms: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "query-123",
                "question": "What is machine learning?",
                "answer": "Machine learning is...",
                "sources": [
                    {"content": "ML is a subset...", "score": 0.95}
                ],
                "retrieval_method": "hybrid",
                "latency_ms": 1234
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    services: Dict[str, str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "2.0.0",
                "services": {
                    "kafka": "connected",
                    "minio": "connected",
                    "postgres": "connected"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid file type",
                "detail": "Only PDF, DOCX, and TXT files are supported"
            }
        }
