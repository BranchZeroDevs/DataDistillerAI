# DataDistiller 2.0 - Setup Guide

Complete setup instructions for the production async RAG platform.

## System Requirements

- **OS**: macOS, Linux, or Windows with Docker
- **Docker Desktop**: Latest version
- **Python**: 3.10 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 10GB free space
- **CPU**: Multi-core recommended for workers

## Overview

DataDistiller 2.0 requires:
1. Docker infrastructure (8 services)
2. Python application (API + workers)
3. Optional: Ollama for LLM

## Step 1: Install Docker Desktop

### macOS
```bash
brew install --cask docker
```
Or download from https://www.docker.com/products/docker-desktop/

### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### Windows
Download from https://www.docker.com/products/docker-desktop/

### Verify Installation
```bash
docker --version
docker compose version
```

## Step 2: Clone and Setup

```bash
git clone <your-repository-url>
cd DataDistillerAI
```

## Step 3: Start Infrastructure

```bash
# Start all Docker services
docker compose up -d

# Verify all services are running (wait ~30 seconds)
docker compose ps

# Expected output: 7-8 services with "healthy" status
```

### Services Started
- ✅ Kafka (port 9092)
- ✅ Zookeeper (port 2181)
- ✅ Kafka UI (port 9000)
- ✅ PostgreSQL (port 5432)
- ✅ MinIO (port 9001, 9002)
- ✅ Redis (port 6379)
- ✅ Prometheus (port 9090)
- ✅ Grafana (port 3000)

### Check Services
```bash
# All services
docker compose ps

# Specific service logs
docker compose logs -f kafka
docker compose logs -f postgres

# Health check
curl http://localhost:9001  # MinIO
```

## Step 4: Python Environment

### Create Virtual Environment
```bash
python -m venv .venv

# Activate
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Verify Installation
```bash
python check_phase2_3.py
```

Expected output: All green checkmarks

## Step 5: Initialize Database

Database schema is auto-created on first run, but you can verify:

```bash
# Connect to PostgreSQL
docker exec -it datadistiller-postgres psql -U datadistiller

# Inside PostgreSQL shell:
\dt  # List tables

# Should see:
# - document_jobs
# - document_chunks
# - processing_metrics
# - query_logs

# Exit
\q
```

## Step 6: Start Application Components

You need **3 terminals** (keep all running):

### Terminal 1: API Server
```bash
source .venv/bin/activate
PYTHONPATH=$PWD .venv/bin/python api/main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Ingestion Worker
```bash
source .venv/bin/activate
PYTHONPATH=$PWD .venv/bin/python workers/ingestion_worker.py
```

Expected output:
```
✅ ingestion-worker-1 initialized
🔄 ingestion-worker-1 starting...
```

### Terminal 3: Embedding Worker
```bash
source .venv/bin/activate
PYTHONPATH=$PWD .venv/bin/python workers/embedding_worker.py
```

Expected output:
```
✅ embedding-worker-1 initialized
🔄 embedding-worker-1 starting...
```

### Optional Terminal 4: Web UI
```bash
source .venv/bin/activate
streamlit run app_hybrid.py
```

## Step 7: Verify Setup

### Check API Health
```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "services": {
    "postgres": "connected",
    "minio": "connected",
    "kafka": "not implemented"
  }
}
```

### Run Integration Test
```bash
cd tests_v2
python test_phase2_3.py
```

Or quick test:
```bash
python quick_test.py
```

### Check System Status
```bash
python status.py
```

## Step 8: First Upload

### Via API
```bash
curl -X POST http://localhost:8000/api/v2/documents/upload \
  -F "file=@data/documents/machine_learning.txt"
```

Response:
```json
{
  "job_id": "abc-123-def",
  "status": "pending",
  "filename": "machine_learning.txt",
  "file_size": 1943
}
```

### Check Status
```bash
# Replace with your job_id
curl http://localhost:8000/api/v2/documents/status/abc-123-def
```

### Via Web UI
1. Open http://localhost:8501
2. Ensure "🚀 2.0 Async API" is selected
3. Go to "📊 Documents" tab
4. Upload files
5. Monitor "Processing Jobs" section

## Configuration

### Environment Variables
Create `.env` file:
```bash
# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=datadistiller
POSTGRES_USER=datadistiller
POSTGRES_PASSWORD=datadistiller123

# MinIO
MINIO_ENDPOINT=localhost:9002
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Docker Resource Limits
Edit `docker-compose.yml` if needed:
```yaml
services:
  kafka:
    # Add resource limits
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

### Scale Workers
Add more embedding workers for parallel processing:
```bash
# Terminal 4
PYTHONPATH=$PWD .venv/bin/python workers/embedding_worker.py

# Terminal 5
PYTHONPATH=$PWD .venv/bin/python workers/embedding_worker.py

# Workers auto-join consumer group and share load
```

## Monitoring

### Web Dashboards

#### API Documentation
http://localhost:8000/docs

Interactive OpenAPI (Swagger) interface

#### Kafka UI
http://localhost:9000

- View topics
- Monitor messages
- Check consumer groups

#### MinIO Console
http://localhost:9001

- Credentials: minioadmin / minioadmin123
- Browse uploaded files
- Check buckets

#### Grafana
http://localhost:3000

- Credentials: admin / admin123
- View metrics dashboards
- (Phase 5: Configure Prometheus datasource)

### Command Line Monitoring

#### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f kafka
docker compose logs -f postgres
docker compose logs -f minio

# Tail last 100 lines
docker compose logs --tail=100 kafka
```

#### Check Kafka Topics
```bash
docker exec -it datadistiller-kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --list

# Should see:
# - doc-ingest-requests
# - chunk-processing
```

#### Check Consumer Groups
```bash
docker exec -it datadistiller-kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --describe \
  --group ingestion-workers
```

#### Query Database
```bash
# Connect
docker exec -it datadistiller-postgres psql -U datadistiller

# Check jobs
SELECT job_id, filename, status, progress 
FROM document_jobs 
ORDER BY created_at DESC 
LIMIT 10;

# Check chunks
SELECT job_id, status, COUNT(*) 
FROM document_chunks 
GROUP BY job_id, status;
```

## Troubleshooting

### Docker Issues

#### Services not starting
```bash
# Check Docker is running
docker ps

# Restart Docker Desktop
# Then restart services
docker compose down
docker compose up -d
```

#### Port conflicts
```bash
# Find process using port
lsof -i :9092  # Kafka
lsof -i :5432  # PostgreSQL

# Kill process
kill -9 <PID>

# Or change ports in docker-compose.yml
```

#### Out of disk space
```bash
# Clean up Docker
docker system prune -a --volumes

# Check space
docker system df
```

### Application Issues

#### API not responding
```bash
# Check if running
curl http://localhost:8000/health

# Check terminal for errors
# Restart API server (Ctrl+C, then restart)
```

#### Workers not processing
```bash
# Check worker logs in terminal
# Verify Kafka connection

# Check consumer groups
docker exec -it datadistiller-kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --list
```

#### Jobs stuck in "pending"
```bash
# Check ingestion worker is running
# Check Kafka topic has messages
docker exec -it datadistiller-kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic doc-ingest-requests \
  --from-beginning \
  --max-messages 1
```

#### Database connection failed
```bash
# Check PostgreSQL is running
docker compose ps postgres

# Check credentials in code match docker-compose.yml
# Restart PostgreSQL
docker compose restart postgres
```

### Performance Issues

#### Slow processing
- Add more embedding workers
- Increase worker resources
- Check CPU/memory usage: `docker stats`

#### High memory usage
```bash
# Check resource usage
docker stats

# Restart services
docker compose restart
```

## Development vs Production

### Development Setup (Current)
- Docker Compose for infrastructure
- Manual worker startup
- Local storage (Docker volumes)
- No authentication
- Single-node setup

### Production Recommendations
- Kubernetes/ECS for orchestration
- Managed Kafka (AWS MSK, Confluent Cloud)
- Managed PostgreSQL (RDS, Cloud SQL)
- S3 for storage (instead of MinIO)
- Redis Cluster
- Load balancer for API
- Authentication & rate limiting
- Multi-region deployment
- Backup & disaster recovery

## Next Steps

1. **Upload documents** via API or UI
2. **Monitor processing** in Kafka UI
3. **Query documents** via API
4. **Scale workers** as needed
5. **Read** [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md) for technical details
6. **Explore** Phase 4+ features (hybrid search, etc.)

## Stopping Services

### Stop gracefully
```bash
# Stop application (Ctrl+C in each terminal)
# API server
# Ingestion worker
# Embedding worker

# Stop Docker services
docker compose down
```

### Stop and remove data
```bash
docker compose down -v  # ⚠️ Removes volumes (data loss)
```

## Upgrading from V1

Coming from DataDistiller 1.0? Key differences:

| Aspect | V1 | V2 |
|--------|----|----|
| Setup | Simple (Ollama only) | Complex (Docker stack) |
| Upload | Blocking (60s) | Async (<100ms) |
| Processing | Sequential | Parallel |
| Storage | In-memory | Persistent |
| API | No | FastAPI |
| Scaling | No | Yes (workers) |

V1 documents need to be re-uploaded to V2 (different storage).

## Support

- Issues: [GitHub Issues]
- Docs: [README_V2.md](../README_V2.md)
- Architecture: [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md)
- API Reference: http://localhost:8000/docs
