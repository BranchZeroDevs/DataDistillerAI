# DataDistiller 2.0 - Async Production RAG Platform

**Version 2.0** - Event-driven, scalable document processing with async API

## 🎯 Overview

DataDistiller 2.0 is a production-ready, event-driven RAG platform built on microservices architecture. Designed for high-throughput document processing with real-time job tracking.

### Key Features
- ✅ **Async Processing** - Non-blocking document uploads
- ✅ **Event-Driven** - Kafka-based message queue
- ✅ **Scalable** - Horizontal worker scaling
- ✅ **Job Tracking** - Real-time progress monitoring
- ✅ **Production Ready** - Docker Compose infrastructure
- ✅ **RESTful API** - FastAPI with OpenAPI docs

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Python 3.10+
- 8GB+ RAM recommended

### 1. Start Infrastructure
```bash
# Clone repository
git clone <your-repo>
cd DataDistillerAI

# Start Docker services
docker compose up -d

# Verify services (wait ~30 seconds)
docker compose ps
```

### 2. Setup Python Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Application
```bash
# Terminal 1: API Server
PYTHONPATH=$PWD .venv/bin/python api/main.py

# Terminal 2: Ingestion Worker
PYTHONPATH=$PWD .venv/bin/python workers/ingestion_worker.py

# Terminal 3: Embedding Worker
PYTHONPATH=$PWD .venv/bin/python workers/embedding_worker.py

# Terminal 4: Web UI (optional)
.venv/bin/streamlit run app_hybrid.py
```

## 📚 Documentation

- **Setup Guide**: [docs/V2_SETUP.md](docs/V2_SETUP.md)
- **Architecture**: [docs/V2_ARCHITECTURE.md](docs/V2_ARCHITECTURE.md)
- **API Reference**: http://localhost:8000/docs (when running)

## 🏗️ Architecture

```
┌──────────────┐
│  FastAPI     │ ← POST /upload (202 Accepted)
│  Server      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Kafka     │ ← doc-ingest-requests topic
│  Message Q   │
└──────┬───────┘
       │
       ├─────────────────┐
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ Ingestion   │   │ Embedding   │
│  Worker     │→──│  Workers    │
│             │   │  (Pool)     │
└──────┬──────┘   └──────┬──────┘
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│   MinIO     │   │ PostgreSQL  │
│  S3 Store   │   │  Metadata   │
└─────────────┘   └─────────────┘
```

## 🎨 Components

### Infrastructure (Docker)
- **Kafka** (port 9092) - Message queue
- **Zookeeper** (port 2181) - Kafka coordination
- **PostgreSQL** (port 5432) - Job metadata
- **MinIO** (port 9001/9002) - S3-compatible storage
- **Redis** (port 6379) - Caching
- **Prometheus** (port 9090) - Metrics
- **Grafana** (port 3000) - Dashboards
- **Kafka UI** (port 9000) - Topic monitoring

### Application
- **FastAPI Server** - REST API endpoints
- **Ingestion Worker** - Document chunking & fan-out
- **Embedding Workers** - Parallel embedding generation
- **Storage Clients** - MinIO and PostgreSQL abstractions

## 🔌 API Endpoints

### Upload Document
```bash
curl -X POST http://localhost:8000/api/v2/documents/upload \
  -F "file=@document.pdf"

# Response (202 Accepted)
{
  "job_id": "abc-123-def-456",
  "status": "pending",
  "filename": "document.pdf",
  "file_size": 1048576
}
```

### Check Status
```bash
curl http://localhost:8000/api/v2/documents/status/abc-123-def-456

# Response
{
  "job_id": "abc-123-def-456",
  "status": "completed",
  "progress": 100,
  "total_chunks": 15,
  "processed_chunks": 15
}
```

### Query Documents
```bash
curl -X POST http://localhost:8000/api/v2/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 3
  }'

# Response
{
  "answer": "Machine learning is...",
  "sources": [...],
  "latency_ms": 245
}
```

### List Documents
```bash
curl http://localhost:8000/api/v2/documents/list

# Response
{
  "documents": [...],
  "total": 10
}
```

## 🧪 Testing

```bash
# Quick system check
python check_phase2_3.py

# Full integration test
cd tests_v2
python test_phase2_3.py

# Quick upload test
python quick_test.py

# System status
python status.py
```

## 📊 Monitoring

### Web UIs
- **API Docs**: http://localhost:8000/docs
- **Kafka UI**: http://localhost:9000
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin123)
- **Grafana**: http://localhost:3000 (admin/admin123)

### Check Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f kafka
docker compose logs -f postgres

# Application logs (check terminal outputs)
```

## 🔄 Workflow

1. **Upload** → Client sends file to API
2. **Accept** → API stores in MinIO, creates job in PostgreSQL, sends to Kafka
3. **Ingest** → Worker downloads, chunks, fans out to Kafka
4. **Embed** → Workers generate embeddings in parallel
5. **Complete** → Update job status, ready for queries

## ⚡ Performance

- **Async uploads**: Returns in <100ms
- **Fan-out processing**: 1 doc → N chunks processed in parallel
- **Horizontal scaling**: Add more embedding workers as needed
- **Progress tracking**: Real-time status updates

## 🔧 Configuration

### Scale Workers
```bash
# Add more embedding workers (in separate terminals)
PYTHONPATH=$PWD .venv/bin/python workers/embedding_worker.py
PYTHONPATH=$PWD .venv/bin/python workers/embedding_worker.py
# Workers auto-join consumer group and share load
```

### Environment Variables
Create `.env`:
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
```

## 🆚 Version Comparison

| Feature | V1 | V2 |
|---------|----|----|
| Architecture | Monolithic | Microservices |
| Upload Response | 60s (blocking) | <100ms (async) |
| Processing | Sequential | Parallel |
| Scalability | Single instance | Multi-worker |
| Infrastructure | None | Docker (8 services) |
| Job Tracking | No | Yes (real-time) |
| Storage | In-memory | MinIO + PostgreSQL |
| API | No | FastAPI + OpenAPI |
| Best For | Development | Production |

## 🐛 Troubleshooting

### Docker not running
```bash
# Check Docker
docker ps

# Start Docker Desktop
# Restart services
docker compose down
docker compose up -d
```

### Port conflicts
```bash
# Find process using port
lsof -i :9092

# Kill process
kill -9 <PID>
```

### Worker not processing
```bash
# Check Kafka topics
docker exec -it datadistiller-kafka kafka-topics \
  --bootstrap-server localhost:9092 --list

# Check consumer groups
docker exec -it datadistiller-kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 --list
```

### Database issues
```bash
# Connect to PostgreSQL
docker exec -it datadistiller-postgres psql -U datadistiller

# Check tables
\dt

# Query jobs
SELECT * FROM document_jobs ORDER BY created_at DESC LIMIT 10;
```

## 🚦 What's Next

### Implemented (Phase 2 & 3)
- ✅ Async API with FastAPI
- ✅ Kafka message queue
- ✅ Fan-out processing pattern
- ✅ Job tracking with PostgreSQL
- ✅ MinIO storage
- ✅ Worker pools

### Planned (Phase 4+)
- ⏳ Hybrid search (BM25 + dense)
- ⏳ Enhanced monitoring dashboards
- ⏳ Rate limiting & auth
- ⏳ Knowledge Graph integration
- ⏳ Advanced error handling
- ⏳ Load testing & optimization

## 📖 Related Guides

- [V2 Setup Guide](docs/V2_SETUP.md) - Detailed setup instructions
- [V2 Architecture](docs/V2_ARCHITECTURE.md) - Technical deep dive
- [Phase 2 & 3 Complete](docs/archive/PHASE2_3_COMPLETE.md) - Implementation details

## 📄 License

[Your License]

---

**Want simpler local setup?** → See [DataDistiller 1.0](README_V1.md)
