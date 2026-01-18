# DataDistillerAI - Quick Reference

## 🚀 Getting Started (30 seconds)

### Prerequisites
- Ollama running: `ollama serve` (in another terminal)
- Documents in: `data/documents/`

### Launch Web App
```bash
streamlit run app.py
```

Then visit: `http://localhost:8501`

---

## 📋 What The App Does

### TAB 1: Chat 💬
```
┌─ Ask Questions About Your Documents
│
├─ Input your question
├─ Adjust top results slider (1-5)
├─ Press Enter or button
│
├─ Returns:
│  • Answer grounded in documents
│  • Retrieved context preview
│  • Relevance scores
│  • Chat history tracking
```

### TAB 2: Documents 📊
```
┌─ Document Statistics
│
├─ Total documents count
├─ Total chunks created
├─ Total characters indexed
│
├─ Document list with preview
│  • Filename
│  • Size in characters
│  • Content preview
```

### TAB 3: About ℹ️
```
┌─ System Information
│
├─ Feature overview
├─ How it works
├─ Backend details
├─ Tech stack
└─ Documentation links
```

---

## 🏗️ Architecture (Simple)

```
Your Documents
     ↓
Load (txt, pdf, docx, html, md)
     ↓
Split into chunks (1024 chars, 128 overlap)
     ↓
Convert to embeddings (sentence-transformers)
     ↓
Store in vector database (FAISS)
     ↓
User asks question
     ↓
Find similar chunks (semantic search)
     ↓
Pass to Ollama LLM
     ↓
Get grounded answer
```

---

## 🎯 Components

### Input
- **Supported Formats**: PDF, DOCX, TXT, HTML, Markdown
- **Location**: `data/documents/`
- **Auto-detected**: Yes

### Processing
- **Chunking**: Semantic (paragraphs → sentences)
- **Chunk Size**: 1024 characters
- **Overlap**: 128 characters
- **Embeddings**: all-MiniLM-L6-v2

### Storage
- **Vector DB**: FAISS
- **Index Location**: `data/vector_store/`
- **Indexing Speed**: ~1 sec per 100 KB

### LLM
- **Primary**: Ollama (qwen2.5:3b)
  - Local, free, private
  - URL: http://localhost:11434
- **Secondary**: Claude, Gemini (code-only)

### Interface
- **Type**: Streamlit web app
- **Tabs**: Chat, Documents, About
- **State**: Session-based chat history
- **Responsive**: Works on desktop/mobile

---

## ⚡ Quick Commands

### Setup
```bash
# Install dependencies (done once)
pip install -r requirements.txt

# Start Ollama
ollama serve

# Run webapp (new terminal)
cd /path/to/DataDistillerAI
streamlit run app.py
```

### Common Tasks
```bash
# Run simple version (lighter)
streamlit run app_simple.py

# Use CLI instead
python cli.py

# Test Ollama connection
python test_ollama_connection.py

# Test webapp components
python test_webapp.py
```

---

## 🔍 What You Can Do

### ✅ Ask Questions
- "What is machine learning?"
- "Summarize the key concepts"
- "How does deep learning work?"

### ✅ View Sources
- Click "Retrieved Context" to see source chunks
- See relevance scores
- Verify answers are grounded

### ✅ Manage Documents
- Add new files to `data/documents/`
- App auto-detects on next run
- View statistics in Documents tab

### ✅ Switch Backends (Advanced)
- Edit `app.py` line with `load_rag_pipeline("ollama")`
- Change to `"claude"` or `"gemini"`
- Requires API keys for cloud backends

---

## 🛠️ Configuration

### Default Paths
- Documents: `data/documents/`
- Vector store: `data/vector_store/`

### Default Parameters
- Ollama model: `qwen2.5:3b`
- Ollama URL: `http://localhost:11434`
- Chunk size: `1024`
- Overlap: `128`
- Top-K: `3` (adjustable in UI)

### Change Defaults
Edit `src/workflows_ollama.py` or pass parameters to `RAGPipelineOllama()`

---

## 📊 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Load app | <1s | Streamlit loads fast |
| Index docs | 5-30s | Depends on size |
| Search query | <100ms | FAISS is fast |
| Generate answer | 2-5s | Ollama inference |
| Total per question | 2-6s | Mostly LLM time |

---

## ✅ Status Check

### Verify Everything Works
```bash
# Test all components
python test_webapp.py

# Should show: ✅ ALL TESTS PASSED
```

### If Something Breaks
1. **Ollama not running**: `ollama serve`
2. **No documents**: Add files to `data/documents/`
3. **Import error**: `pip install -r requirements.txt`
4. **Port conflict**: Change port: `streamlit run app.py --server.port 8502`

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main web app (full version) |
| `app_simple.py` | Lightweight web app |
| `cli.py` | Command-line interface |
| `src/workflows_ollama.py` | RAG pipeline |
| `src/llm_ollama.py` | Ollama client |
| `src/retrieval/__init__.py` | Vector database |
| `src/ingestion/__init__.py` | Document loader |
| `src/processing/chunker.py` | Text chunking |

---

## 🎓 How It Works (Details)

### Indexing (First Time)
1. **Load** - Read PDF/DOCX/TXT/HTML/Markdown
2. **Clean** - Remove noise, normalize text
3. **Chunk** - Split by paragraphs, then sentences
4. **Embed** - Convert to 384-dimensional vectors
5. **Index** - Store in FAISS for fast search

### Querying
1. **Parse** - Read user question
2. **Embed** - Convert to same vector space
3. **Search** - Find top-K similar chunks
4. **Format** - Build context prompt
5. **Generate** - LLM produces answer
6. **Return** - Show answer + sources

---

## 🚨 Common Issues & Solutions

### "Cannot connect to Ollama"
```bash
# Make sure Ollama is running
ollama serve

# Or pull the model if not present
ollama pull qwen2.5:3b
```

### "No documents found"
```bash
# Add documents to the directory
cp your_doc.pdf data/documents/

# App will auto-detect on next run
```

### "Streamlit port already in use"
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### "Out of memory"
```bash
# Use smaller Ollama model
# Edit app.py, change model parameter to:
# model="qwen2.5:3b"  (already set)
# or try: mistral, llama2, neural-chat
```

---

## 📞 Support

See documentation files:
- `OLLAMA_GUIDE.md` - Ollama setup & models
- `README.md` - Full project documentation
- `ARCHITECTURE.md` - System design details
- `WEBAPP_VERIFICATION.md` - Detailed test results

---

**Status: ✅ Ready to Use**

Start with: `streamlit run app.py`
