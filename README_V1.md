# DataDistiller 1.0 - Local RAG System

**Version 1.0** - Synchronous, local-first document Q&A with Knowledge Graph visualization

## 🎯 Overview

DataDistiller 1.0 is a fully local RAG (Retrieval Augmented Generation) system with advanced Knowledge Graph features. Perfect for privacy-conscious users who want complete control over their data.

### Key Features
- ✅ **100% Local** - All processing happens on your machine
- ✅ **Privacy-First** - No data leaves your computer
- ✅ **Knowledge Graph** - Visual network of concepts and relationships
- ✅ **Semantic Analysis** - AI-powered concept progression
- ✅ **Multi-LLM Support** - Ollama (primary), Claude, Gemini
- ✅ **Simple Setup** - No Docker or infrastructure needed

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Ollama installed and running

### 1. Install Ollama
```bash
# macOS
brew install ollama

# Start Ollama
ollama serve

# Pull a model (in another terminal)
ollama pull qwen2.5:3b
```

### 2. Install DataDistiller
```bash
# Clone and setup
git clone <your-repo>
cd DataDistillerAI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 3. Run the App
```bash
streamlit run app.py
```

Open http://localhost:8501

## 📚 Documentation

- **Setup Guide**: [docs/V1_SETUP.md](docs/V1_SETUP.md)
- **Architecture**: [docs/V1_ARCHITECTURE.md](docs/V1_ARCHITECTURE.md)
- **Knowledge Graph Guide**: [KNOWLEDGE_GRAPH_GUIDE.md](KNOWLEDGE_GRAPH_GUIDE.md)

## 🎨 Features

### 1. Document Q&A
- Upload documents (PDF, DOCX, TXT, HTML, MD)
- Ask questions in natural language
- Get AI-generated answers with sources

### 2. Knowledge Graph
Four visualization modes:
- **Network Graph** - Interactive concept network
- **Statistics** - Top concepts and relationships
- **Semantic Flow** - Chunk-wise concept progression
- **AI Progression** - LLM-enhanced logical flow

### 3. Chat Interface
- Context-aware conversations
- Chat history
- Source highlighting

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │
│   (app.py)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   RAGPipelineOllama     │
│  (workflows_ollama.py)  │
└────────┬────────────────┘
         │
    ┌────┴─────┐
    ▼          ▼
┌────────┐  ┌──────────┐
│ Ollama │  │  FAISS   │
│  LLM   │  │  Vector  │
│        │  │  Store   │
└────────┘  └──────────┘
```

### Components
- **UI**: Streamlit web interface
- **LLM**: Ollama (local inference)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS (in-memory)
- **Knowledge Graph**: NetworkX + spaCy + pyvis

## 🧪 Testing

```bash
# Test Knowledge Graph phases
cd tests_v1
python test_kg_phase1.py  # Core extraction
python test_kg_phase2.py  # Interactive viz
python test_kg_phase3.py  # Semantic flow
python test_kg_phase4.py  # AI progression

# Test LLM backends
python test_ollama.py
python test_claude.py     # Requires ANTHROPIC_API_KEY
python test_gemini.py     # Requires GOOGLE_API_KEY
```

## 📝 Usage Examples

### Upload and Query
1. Start the app: `streamlit run app.py`
2. Go to "📊 Documents" tab
3. Upload your documents
4. Go to "💬 Chat" tab
5. Ask questions!

### Explore Knowledge Graph
1. Upload and index documents
2. Go to "🧠 Knowledge Graph" tab
3. Explore:
   - Network visualization
   - Concept statistics
   - Semantic flow patterns
   - AI-enhanced progression

## 🔧 Configuration

### Change LLM Model
Edit `src/workflows_ollama.py`:
```python
self.model_name = "qwen2.5:3b"  # Change to your preferred model
```

### Adjust Chunk Size
Edit `src/processing/chunker.py`:
```python
self.chunk_size = 500  # Adjust as needed
```

## 🆚 Version Comparison

| Feature | V1 | V2 |
|---------|----|----|
| Processing | Synchronous | Async |
| Setup | Simple | Complex |
| Scale | Single doc | Multi-doc |
| Infrastructure | None | Docker |
| Knowledge Graph | ✅ Yes | ⏳ Coming |
| Best For | Development | Production |

## 📖 Related Guides

- [Multi-LLM Guide](MULTI_LLM_GUIDE.md) - Using Claude/Gemini
- [Ollama Guide](OLLAMA_GUIDE.md) - Ollama setup details
- [Knowledge Graph Guide](KNOWLEDGE_GRAPH_GUIDE.md) - KG features

## 🐛 Troubleshooting

### Ollama not responding
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart Ollama
killall ollama
ollama serve
```

### Knowledge Graph errors
```bash
# Reinstall spaCy model
python -m spacy download en_core_web_sm --force
```

### Out of memory
- Use smaller model: `ollama pull qwen2.5:1.5b`
- Reduce chunk size in configuration
- Process fewer documents at once

## 🚦 Next Steps

- Explore [DataDistiller 2.0](README_V2.md) for production features
- Read [V1_ARCHITECTURE.md](docs/V1_ARCHITECTURE.md) for technical details
- Check [KNOWLEDGE_GRAPH_GUIDE.md](KNOWLEDGE_GRAPH_GUIDE.md) for KG usage

## 📄 License

[Your License]

---

**Need production features?** → See [DataDistiller 2.0](README_V2.md)
