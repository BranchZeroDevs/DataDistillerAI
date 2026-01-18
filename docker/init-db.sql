-- DataDistiller 2.0 Database Schema
-- Tracks document processing status and metadata

-- Document Jobs Table
CREATE TABLE IF NOT EXISTS document_jobs (
    job_id VARCHAR(36) PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    content_type VARCHAR(100),
    s3_bucket VARCHAR(100),
    s3_key VARCHAR(500),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    -- Status: pending, processing, chunking, embedding, completed, failed
    progress INTEGER DEFAULT 0,
    total_chunks INTEGER DEFAULT 0,
    processed_chunks INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Chunks Table
CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) REFERENCES document_jobs(job_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_hash VARCHAR(64),
    vector_id VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',
    -- Status: pending, embedding, indexed, failed
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_id, chunk_index)
);

-- Processing Metrics Table
CREATE TABLE IF NOT EXISTS processing_metrics (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(36) REFERENCES document_jobs(job_id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC,
    metric_unit VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query Logs Table
CREATE TABLE IF NOT EXISTS query_logs (
    query_id VARCHAR(36) PRIMARY KEY,
    query_text TEXT NOT NULL,
    retrieval_method VARCHAR(50),
    -- Method: dense, sparse, hybrid
    top_k INTEGER,
    num_results INTEGER,
    latency_ms INTEGER,
    user_feedback INTEGER,
    -- -1 (bad), 0 (neutral), 1 (good)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_document_jobs_status ON document_jobs(status);
CREATE INDEX idx_document_jobs_created ON document_jobs(created_at DESC);
CREATE INDEX idx_chunks_job_id ON document_chunks(job_id);
CREATE INDEX idx_chunks_status ON document_chunks(status);
CREATE INDEX idx_query_logs_created ON query_logs(created_at DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers
CREATE TRIGGER update_document_jobs_updated_at
    BEFORE UPDATE ON document_jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_document_chunks_updated_at
    BEFORE UPDATE ON document_chunks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing
INSERT INTO document_jobs (job_id, filename, file_size, content_type, status, progress)
VALUES ('test-job-001', 'sample.pdf', 1024000, 'application/pdf', 'completed', 100)
ON CONFLICT DO NOTHING;
