# 🚀 DataDistiller 2.0 - Architecture Upgrade Roadmap

## Vision: From Script to Platform

**Current (1.0):** Synchronous RAG with local processing  
**Target (2.0):** Asynchronous, distributed, production-grade RAG platform

---

## 🎯 Core Improvements

### 1. Asynchronous Ingestion Pipeline
- **Event-Driven:** Kafka-based message queue
- **Parallel Processing:** Fan-out pattern (1 PDF → 50 workers)
- **Fault Tolerance:** DLQ, retries, idempotency
- **Response:** Immediate 202 Accepted (no waiting)

### 2. Hybrid Retrieval Engine
- **Dense Search:** Vector similarity (existing FAISS)
- **Sparse Search:** BM25 keyword matching (new)
- **Re-ranking:** Cross-encoder for precision (new)
- **Result:** Better accuracy on specific queries

### 3. Infrastructure
- **Message Queue:** Kafka
- **Storage:** S3/MinIO for raw files
- **Databases:** Vector DB + Keyword Index
- **Monitoring:** Metrics, logs, traces

---

## 📋 Implementation Phases

### Phase 1: Infrastructure Setup (Week 1-2)
**Goal:** Get Kafka running locally

**Tasks:**
- [ ] Docker Compose setup (Kafka + Zookeeper)
- [ ] Simple producer/consumer test
- [ ] Consumer groups demonstration
- [ ] Health check endpoints

**Deliverables:**
- `docker-compose.yml` with Kafka stack
- Test producer (`test_kafka_producer.py`)
- Test consumer (`test_kafka_consumer.py`)
- Documentation

**Tech Stack:**
- Kafka (event streaming)
- Zookeeper (coordination)
- Python kafka-python library

---

### Phase 2: Asynchronous Upload API (Week 3-4)
**Goal:** Non-blocking document ingestion

**Tasks:**
- [ ] FastAPI upload endpoint (replaces Streamlit upload)
- [ ] S3/MinIO integration for file storage
- [ ] Kafka producer for upload events
- [ ] Background worker for processing
- [ ] Status tracking (pending/processing/complete)

**Deliverables:**
- `api/upload.py` - FastAPI endpoint
- `workers/ingestion_worker.py` - Kafka consumer
- `storage/s3_client.py` - MinIO integration
- Status tracking DB (SQLite/PostgreSQL)

**API Design:**
```python
POST /api/v2/documents/upload
Response: {"job_id": "abc-123", "status": "accepted"}

GET /api/v2/documents/status/{job_id}
Response: {"status": "processing", "progress": "45%"}
```

---

### Phase 3: Fan-Out Processing (Week 5-6)
**Goal:** Parallel chunk processing

**Tasks:**
- [ ] PDF splitter (unstructured.io integration)
- [ ] Fan-out to chunk-processing topic
- [ ] Embedding worker pool
- [ ] Progress tracking per chunk
- [ ] Graceful shutdown handling

**Deliverables:**
- `workers/splitter_worker.py` - PDF → chunks
- `workers/embedding_worker.py` - Chunk → vector
- Kafka topic architecture
- Worker scaling guide

**Architecture:**
```
Upload → Kafka[doc-requests] 
       → Splitter Worker 
       → Kafka[chunk-processing] (50 messages)
       → Embedding Workers (5 instances)
       → Vector DB
```

---

### Phase 4: Hybrid Search Engine (Week 7-8)
**Goal:** Better retrieval accuracy

**Tasks:**
- [ ] BM25 indexer integration (Elasticsearch or rank-bm25)
- [ ] Parallel dense + sparse retrieval
- [ ] Result merger (deduplication)
- [ ] Cross-encoder re-ranking
- [ ] A/B testing framework

**Deliverables:**
- `retrieval/hybrid_retriever.py`
- `retrieval/bm25_index.py`
- `retrieval/reranker.py` (Cohere API or local model)
- Performance benchmarks

**Query Flow:**
```
Question → [Dense Search (FAISS) → Top 20]
        ↓ [Sparse Search (BM25)  → Top 20]
        → Merge + Dedupe (40 chunks)
        → Cross-Encoder Re-rank
        → Top 5 → LLM
```

---

### Phase 5: Fault Tolerance & Monitoring (Week 9-10)
**Goal:** Production-ready reliability

**Tasks:**
- [ ] Dead Letter Queue setup
- [ ] Retry logic with exponential backoff
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Alert rules
- [ ] Circuit breaker pattern

**Deliverables:**
- DLQ consumer with retry logic
- Metrics endpoints
- Grafana dashboard JSON
- Alerting rules
- Runbook documentation

**Metrics:**
- Ingestion rate (docs/min)
- Processing latency (p50, p95, p99)
- Error rate
- Queue depth
- Worker utilization

---

### Phase 6: API & UI Upgrade (Week 11-12)
**Goal:** Modern interface

**Tasks:**
- [ ] FastAPI backend (replace Streamlit backend)
- [ ] REST API documentation (OpenAPI)
- [ ] React/Next.js frontend (optional)
- [ ] WebSocket for real-time updates
- [ ] API authentication (JWT)

**Deliverables:**
- Full REST API
- Swagger/OpenAPI spec
- Modern UI (or keep Streamlit as admin panel)
- Authentication system

---

## 🛠️ Technology Stack

### Current (1.0)
```
Frontend:    Streamlit
Processing:  Synchronous Python
Storage:     Local FAISS + files
LLM:         Ollama (local)
```

### Target (2.0)
```
Frontend:    Streamlit (admin) + React (optional)
API:         FastAPI
Queue:       Kafka + Zookeeper
Storage:     MinIO (S3-compatible) + PostgreSQL
Vector DB:   FAISS → Qdrant/Weaviate (upgrade path)
Keyword:     BM25 (rank-bm25) or Elasticsearch
Reranking:   Cohere API or BAAI/bge-reranker
LLM:         Ollama (primary) + OpenAI (secondary)
Monitoring:  Prometheus + Grafana
Deployment:  Docker Compose → Kubernetes (future)
```

---

## 📊 Success Metrics

### Performance
- Upload response time: < 200ms (vs current: 5-60s)
- Processing throughput: 100 docs/min (vs current: ~5/min)
- Query latency: < 2s (with reranking)

### Reliability
- Uptime: 99.9%
- Message loss: 0% (Kafka guarantees)
- Failed job recovery: 100%

### Quality
- Retrieval precision: +30% (with hybrid search)
- User satisfaction: Measurable via feedback

---

## 🎓 Interview Talking Points

### Architecture
✅ Event-driven microservices  
✅ Asynchronous processing  
✅ Horizontal scaling  
✅ Fault tolerance (DLQ, retries)  

### Distributed Systems
✅ Message queue (Kafka)  
✅ Consumer groups  
✅ Fan-out pattern  
✅ Idempotency  

### AI/ML Engineering
✅ Hybrid retrieval (dense + sparse)  
✅ Re-ranking with cross-encoders  
✅ Vector database optimization  
✅ A/B testing framework  

### DevOps
✅ Docker Compose orchestration  
✅ Monitoring & alerting  
✅ Health checks  
✅ Graceful degradation  

---

## 🚦 Quick Start (Phase 1)

```bash
# Start Kafka infrastructure
docker-compose up -d

# Test producer
python workers/test_kafka_producer.py

# Test consumer (in another terminal)
python workers/test_kafka_consumer.py

# Check Kafka UI
open http://localhost:9000
```

---

## 📁 New Directory Structure

```
DataDistillerAI/
├── api/                    # FastAPI endpoints
│   ├── v2/
│   │   ├── upload.py
│   │   ├── query.py
│   │   └── status.py
│   └── middleware/
├── workers/                # Kafka consumers
│   ├── ingestion_worker.py
│   ├── splitter_worker.py
│   ├── embedding_worker.py
│   └── dlq_worker.py
├── retrieval/             # Hybrid search
│   ├── hybrid_retriever.py
│   ├── bm25_index.py
│   └── reranker.py
├── storage/               # External storage
│   ├── s3_client.py
│   └── db_client.py
├── monitoring/            # Observability
│   ├── metrics.py
│   └── logging.py
├── docker/                # Infrastructure
│   ├── docker-compose.yml
│   ├── kafka.yml
│   └── monitoring.yml
└── tests/                 # E2E tests
    ├── integration/
    └── load/
```

---

## 🎯 Next Steps

1. **Review this roadmap** - Any changes?
2. **Start Phase 1** - Kafka setup
3. **Weekly iterations** - One phase every 1-2 weeks
4. **Document everything** - For interviews

**Estimated Timeline:** 12 weeks to production-ready 2.0  
**Time Investment:** 10-15 hours/week

---

Ready to start Phase 1? 🚀
