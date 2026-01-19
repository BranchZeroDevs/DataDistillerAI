# DataDistiller AI

> **Intelligent Document Q&A with RAG** - Available in two deployment models

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## UI
<img width="1427" height="1032" alt="image" src="https://github.com/user-attachments/assets/6292d34b-effe-45a7-96f9-622dd055e42c" />


## 🎯 Choose Your Version

DataDistiller AI offers two architectures for different use cases:

### [Version 1.0 - Local & Simple](README_V1.md) ⭐ Recommended to Start

Perfect for development, testing, and privacy-conscious users.

**Key Features:**
- ✅ 100% local processing - no cloud required
- ✅ Simple setup (just Ollama + Python)
- ✅ Knowledge Graph visualization
- ✅ Privacy-first approach
- ✅ Perfect for learning RAG concepts

**Best For:**
- Individual developers
- Privacy-sensitive projects
- Learning and experimentation
- Documents <100

[📖 Read V1 Docs →](README_V1.md) | [🚀 V1 Setup →](docs/V1_SETUP.md)

---

### [Version 2.0 - Production & Scalable](README_V2.md)

Enterprise-grade async platform for high-throughput processing.

**Key Features:**
- ✅ Async non-blocking uploads
- ✅ Event-driven architecture (Kafka)
- ✅ Horizontal scaling with workers
- ✅ RESTful API with OpenAPI
- ✅ Real-time job tracking
- ✅ Production-ready infrastructure

**Best For:**
- Production deployments
- Multiple concurrent users
- High document volume
- API integration needed

[📖 Read V2 Docs →](README_V2.md) | [🚀 V2 Setup →](docs/V2_SETUP.md)

---

## 🚀 Quick Start

### Version 1.0 (5 minutes)
```bash
# 1. Install Ollama
brew install ollama  # macOS
ollama serve
ollama pull qwen2.5:3b

# 2. Install DataDistiller
git clone <repo-url>
cd DataDistillerAI
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Run!
streamlit run app.py
```

Open http://localhost:8501

### Version 2.0 (10 minutes)
```bash
# 1. Start infrastructure
docker compose up -d

# 2. Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Start components (3 terminals)
PYTHONPATH=$PWD .venv/bin/python api/main.py              # Terminal 1
PYTHONPATH=$PWD .venv/bin/python workers/ingestion_worker.py   # Terminal 2
PYTHONPATH=$PWD .venv/bin/python workers/embedding_worker.py   # Terminal 3

# 4. Test
curl -X POST http://localhost:8000/api/v2/documents/upload \
  -F "file=@your-document.pdf"
```

API Docs: http://localhost:8000/docs

---

## 📊 Feature Comparison

| Feature | V1 Local | V2 Production |
|---------|----------|---------------|
| **Setup Complexity** | ⭐ Simple | ⭐⭐⭐ Complex |
| **Upload Response Time** | 60s (blocking) | <100ms (async) |
| **Processing** | Synchronous | Async + Parallel |
| **Infrastructure** | None (just Ollama) | Docker (8 services) |
| **API** | None | FastAPI + OpenAPI |
| **Scalability** | Single user | Multi-worker |
| **Job Tracking** | No | Yes (real-time) |
| **Knowledge Graph** | ✅ 4 visualization modes | ⏳ Coming in Phase 4 |
| **Persistence** | In-memory | PostgreSQL + MinIO |
| **Best For** | Dev/Learning | Production |

---

## 📁 Project Structure

```
DataDistillerAI/
├── README.md                  # This file
├── README_V1.md               # V1 documentation
├── README_V2.md               # V2 documentation
│
├── docs/
│   ├── V1_SETUP.md           # V1 setup guide
│   ├── V1_ARCHITECTURE.md    # V1 technical details
│   ├── V2_SETUP.md           # V2 setup guide
│   ├── V2_ARCHITECTURE.md    # V2 technical details
│   └── archive/              # Old documentation
│
├── app.py                    # V1 Streamlit UI
├── app_hybrid.py             # Hybrid UI (V1 + V2)
├── cli.py                    # V1 CLI interface
│
├── api/                      # V2 FastAPI server
│   ├── main.py              # API endpoints
│   ├── models.py            # Pydantic schemas
│   └── v2/                  # V2 handlers
│
├── workers/                  # V2 async workers
│   ├── ingestion_worker.py  # Document chunking
│   └── embedding_worker.py  # Embedding generation
│
├── storage/                  # V2 storage clients
│   └── clients.py           # MinIO + PostgreSQL
│
├── src/                      # Core shared code
│   ├── workflows_*.py       # RAG pipelines
│   ├── ingestion/           # Document loaders
│   ├── processing/          # Chunking logic
│   ├── retrieval/           # Vector store
│   ├── llm/                 # LLM integrations
│   └── knowledge_graph.py   # KG features
│
├── tests_v1/                 # V1 tests
├── tests_v2/                 # V2 tests
├── tests/                    # Shared tests
│
├── data/
│   ├── documents/           # Input documents
│   └── vector_store/        # FAISS indices
│
├── docker-compose.yml        # V2 infrastructure
└── requirements.txt          # Python dependencies
```

---

## 🎨 Key Features

### Document Processing
- **Formats**: PDF, DOCX, TXT, HTML, Markdown
- **Chunking**: Semantic-aware with overlap
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS for fast similarity search

### LLM Integration
- **Primary**: Ollama (local, privacy-first)
- **Optional**: Claude (Anthropic), Gemini (Google)
- **RAG**: Context-grounded generation
- **Streaming**: Real-time response generation

### Knowledge Graph (V1)
Four visualization modes:
1. **Network Graph** - Interactive concept relationships
2. **Statistics** - Top concepts and metrics
3. **Semantic Flow** - Chunk-wise progression
4. **AI Progression** - LLM-enhanced analysis

### Async Pipeline (V2)
- **Upload**: Non-blocking, returns job ID immediately
- **Processing**: Fan-out to multiple workers
- **Tracking**: Real-time progress updates
- **Query**: Search indexed documents via API

---

## 🧪 Testing

### V1 Tests
```bash
cd tests_v1

# Knowledge Graph phases
python test_kg_phase1.py
python test_kg_phase2.py
python test_kg_phase3.py
python test_kg_phase4.py

# LLM backends
python test_ollama.py
python test_claude.py
python test_gemini.py
```

### V2 Tests
```bash
cd tests_v2

# System check
python check_phase2_3.py

# Integration test
python test_phase2_3.py

# Quick test
python quick_test.py

# Status dashboard
python status.py
```

---

## 📚 Documentation

### Getting Started
- [V1 Quick Start](README_V1.md#-quick-start)
- [V2 Quick Start](README_V2.md#-quick-start)
- [V1 Setup Guide](docs/V1_SETUP.md)
- [V2 Setup Guide](docs/V2_SETUP.md)

### Technical Details
- [V1 Architecture](docs/V1_ARCHITECTURE.md)
- [V2 Architecture](docs/V2_ARCHITECTURE.md)
- [Knowledge Graph Guide](KNOWLEDGE_GRAPH_GUIDE.md)
- [Multi-LLM Guide](MULTI_LLM_GUIDE.md)
- [Ollama Guide](OLLAMA_GUIDE.md)

### API Reference
- V2 OpenAPI Docs: http://localhost:8000/docs (when running)
- V2 ReDoc: http://localhost:8000/redoc

---

## 🛠️ Technology Stack

### Core
- **Python** 3.10+
- **Streamlit** (V1 UI)
- **FastAPI** (V2 API)

### ML/NLP
- **sentence-transformers** - Embeddings
- **FAISS** - Vector similarity
- **spaCy** - NLP and NER
- **NetworkX** - Graph analysis

### LLM
- **Ollama** - Local inference
- **Anthropic SDK** - Claude (optional)
- **Google GenAI** - Gemini (optional)

### Infrastructure (V2)
- **Docker Compose** - Service orchestration
- **Apache Kafka** - Message queue
- **PostgreSQL** - Metadata storage
- **MinIO** - S3-compatible object storage
- **Redis** - Caching
- **Prometheus** - Metrics
- **Grafana** - Dashboards

---

## 🆚 When to Use Which Version?

### Use V1 If:
- 👤 Individual user or small team
- 🏠 Running on local machine
- 🔒 Privacy is top priority
- 📚 <100 documents
- 🎓 Learning RAG concepts
- 🧪 Development and testing
- 🎨 Need Knowledge Graph features

### Use V2 If:
- 🏢 Production deployment
- 👥 Multiple concurrent users
- 📈 High document volume
- 🔌 Need API integration
- ⚡ Async processing required
- 📊 Real-time monitoring needed
- 🚀 Horizontal scaling important

### Hybrid Approach
Use `app_hybrid.py` to access **both versions** from one UI:
- Switch between V1 and V2 modes
- V1 mode: Knowledge Graph + simple upload
- V2 mode: Async API + job tracking

---

## 🔄 Migration Path

### From V1 to V2
1. Export document list from V1
2. Set up V2 infrastructure
3. Re-upload documents via V2 API
4. Update client code to use async endpoints

**Note**: V1 and V2 use different storage - data is not automatically migrated.

### From V2 to V1
Generally not recommended. V1 is for development/local use.

---

## 🐛 Troubleshooting

### V1 Issues
- **Ollama not responding**: `ollama serve` in terminal
- **Model not found**: `ollama pull qwen2.5:3b`
- **spaCy errors**: `python -m spacy download en_core_web_sm --force`

### V2 Issues
- **Docker not running**: Start Docker Desktop
- **Port conflicts**: `lsof -i :9092` and kill process
- **Workers not processing**: Check Kafka UI at http://localhost:9000

See detailed guides: [V1 Setup](docs/V1_SETUP.md) | [V2 Setup](docs/V2_SETUP.md)

---

## 🚦 Roadmap

### Completed ✅
- V1: Local RAG system with Knowledge Graph
- V2 Phase 1: Async API foundation
- V2 Phase 2: Fan-out processing
- V2 Phase 3: Worker pools and job tracking
- Hybrid UI supporting both versions

### In Progress 🔄
- V2 Phase 4: Hybrid search (BM25 + dense)
- Enhanced monitoring dashboards
- Documentation improvements

### Planned 📋
- V2 Phase 5: Production hardening
- V2 Phase 6: Performance optimization
- Knowledge Graph in V2
- Authentication & rate limiting
- Cloud deployment guides

---

## 📄 License

[Your License Here]

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

- 📖 Documentation: See docs/ folder
- 🐛 Issues: [GitHub Issues]
- 💬 Discussions: [GitHub Discussions]

---

## ⭐ Quick Links

| Link | Description |
|------|-------------|
| [V1 README](README_V1.md) | Local version docs |
| [V2 README](README_V2.md) | Production version docs |
| [V1 Setup](docs/V1_SETUP.md) | Getting started with V1 |
| [V2 Setup](docs/V2_SETUP.md) | Getting started with V2 |
| [V1 Architecture](docs/V1_ARCHITECTURE.md) | Technical details V1 |
| [V2 Architecture](docs/V2_ARCHITECTURE.md) | Technical details V2 |
| [Knowledge Graph](KNOWLEDGE_GRAPH_GUIDE.md) | KG features guide |
| [Multi-LLM](MULTI_LLM_GUIDE.md) | Using Claude/Gemini |

---

**Ready to start?**
- New users: [Start with V1 →](README_V1.md)
- Production needs: [Jump to V2 →](README_V2.md)
