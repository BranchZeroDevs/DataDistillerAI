# DataDistiller 1.0 - Setup Guide

Complete setup instructions for the local RAG system.

## System Requirements

- **OS**: macOS, Linux, or Windows
- **Python**: 3.10 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 2GB free space

## Step 1: Install Ollama

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download from https://ollama.com/download/windows

### Start Ollama
```bash
ollama serve
```

Keep this terminal running.

### Pull a Model
In a new terminal:
```bash
# Small, fast model (recommended)
ollama pull qwen2.5:3b

# Or other options:
ollama pull llama3.2:3b
ollama pull mistral:7b
```

### Verify
```bash
curl http://localhost:11434/api/tags
```

## Step 2: Clone Repository

```bash
git clone <your-repository-url>
cd DataDistillerAI
```

## Step 3: Python Environment

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

### Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

## Step 4: Optional - Additional LLMs

### Claude (Anthropic)
```bash
# Get API key from https://console.anthropic.com/
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

### Gemini (Google)
```bash
# Get API key from https://makersuite.google.com/app/apikey
echo "GOOGLE_API_KEY=your-key-here" >> .env
```

## Step 5: Add Documents

```bash
# Create documents directory (already exists)
mkdir -p data/documents

# Add your documents (PDF, DOCX, TXT, HTML, MD)
cp /path/to/your/documents/* data/documents/
```

Sample documents are included in `data/documents/`.

## Step 6: Run the Application

### Option A: Web UI (Recommended)
```bash
streamlit run app.py
```

Open http://localhost:8501

### Option B: CLI
```bash
python cli.py
```

### Option C: Python API
```python
from src.workflows_ollama import RAGPipelineOllama

# Initialize
pipeline = RAGPipelineOllama()

# Index documents
pipeline.index_documents()

# Query
answer = pipeline.query("What is machine learning?")
print(answer)
```

## Step 7: Test Knowledge Graph

```bash
cd tests_v1

# Test each phase
python test_kg_phase1.py  # Core extraction
python test_kg_phase2.py  # Interactive visualization
python test_kg_phase3.py  # Semantic flow
python test_kg_phase4.py  # AI progression
```

## Configuration

### Change Ollama Model
Edit `src/workflows_ollama.py`:
```python
class RAGPipelineOllama:
    def __init__(self):
        self.model_name = "qwen2.5:3b"  # Change here
```

### Adjust Chunking
Edit `src/processing/chunker.py`:
```python
class SemanticChunker:
    def __init__(self):
        self.chunk_size = 500      # Characters per chunk
        self.chunk_overlap = 50    # Overlap between chunks
```

### Change Embedding Model
Edit `src/retrieval/__init__.py`:
```python
class VectorStore:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
```

## Verification

### Test Ollama Connection
```bash
cd tests_v1
python test_ollama_connection.py
```

Expected output:
```
✅ Ollama is running
✅ Model qwen2.5:3b is available
✅ Test query successful
```

### Test Full Pipeline
```bash
cd tests_v1
python test_ollama.py
```

### Test Web App
```bash
cd tests_v1
python test_webapp.py
```

## Troubleshooting

### Issue: "Ollama not responding"
**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it
ollama serve

# Check port
lsof -i :11434
```

### Issue: "Model not found"
**Solution:**
```bash
# List available models
ollama list

# Pull the model
ollama pull qwen2.5:3b
```

### Issue: "spaCy model not found"
**Solution:**
```bash
# Reinstall spaCy model
python -m spacy download en_core_web_sm --force
```

### Issue: "Out of memory"
**Solution:**
1. Use smaller model:
   ```bash
   ollama pull qwen2.5:1.5b
   ```

2. Reduce chunk size in `src/processing/chunker.py`

3. Process fewer documents at once

### Issue: "Streamlit not found"
**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall
pip install streamlit
```

### Issue: "Import errors"
**Solution:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## Performance Tips

### Faster Inference
- Use smaller models (qwen2.5:1.5b)
- Reduce `top_k` in queries (default: 3)
- Enable GPU if available (Ollama auto-detects)

### Better Accuracy
- Use larger models (mistral:7b, llama3:8b)
- Increase `top_k` for more context
- Adjust chunk size for your documents

### Knowledge Graph Performance
- Limit documents to <100 for interactive viz
- Use Phase 1 (core extraction) for large datasets
- Disable AI progression (Phase 4) for speed

## Next Steps

1. **Add your documents** to `data/documents/`
2. **Run the app**: `streamlit run app.py`
3. **Explore features**:
   - Document Q&A in Chat tab
   - Upload new documents
   - Explore Knowledge Graph
4. **Read** [V1_ARCHITECTURE.md](V1_ARCHITECTURE.md) for technical details
5. **Check out** [KNOWLEDGE_GRAPH_GUIDE.md](../KNOWLEDGE_GRAPH_GUIDE.md)

## Upgrading to V2

Want production features? See [V2_SETUP.md](V2_SETUP.md)

Key differences:
- V1: Simple, local, synchronous
- V2: Complex, scalable, asynchronous

Use V1 for:
- Development and testing
- Local privacy-first usage
- Knowledge Graph features
- Simple deployment

Use V2 for:
- Production deployments
- High document throughput
- Multiple concurrent users
- Scalable infrastructure

## Support

- Issues: [GitHub Issues]
- Docs: [README_V1.md](../README_V1.md)
- Architecture: [V1_ARCHITECTURE.md](V1_ARCHITECTURE.md)
