# Ollama Integration Guide

## ✅ What's Working

Your DataDistillerAI is now integrated with **Ollama** - completely free, local, and no API costs!

```
✓ Ollama Server: CONNECTED
✓ Basic Text Generation: WORKING
✓ RAG with Context Retrieval: WORKING  
✓ Document Summarization: WORKING
✓ Vector Search: WORKING
```

## 🚀 Quick Start

### 1. Keep Ollama Running
```bash
# In a terminal window, keep this running:
ollama serve
```

### 2. Run Your RAG System
```bash
# Test the complete system
python test_ollama.py

# Use in your own code:
from src.workflows_ollama import RAGPipeline

pipeline = RAGPipeline(document_path="./data/documents")
pipeline.index_documents()
answer = pipeline.query("Your question here")
```

### 3. Use with CLI
```bash
python cli.py
```

## 📊 Available Models

You have these models installed:
- **qwen2.5:3b** (1.8 GB) - Fast, good quality ✨ RECOMMENDED
- **deepseek-r1:1.5b** (1.0 GB) - Very fast
- **deepseek-r1:latest** (4.9 GB) - Slower but higher quality
- **gemma3:4b** (3.1 GB) - Good balance

### Switch Models
Edit `test_ollama.py` line 24:
```python
client = OllamaClient(model="qwen2.5")  # Change this
```

Or pull more:
```bash
ollama pull mistral
ollama pull llama2
```

## 💻 Code Examples

### Simple Query
```python
from src.llm_ollama import OllamaClient

client = OllamaClient(model="qwen2.5")
response = client.generate("Explain machine learning")
print(response)
```

### RAG (Question + Context)
```python
from src.llm_ollama import OllamaClient

client = OllamaClient(model="qwen2.5")
context = "Machine learning is a subset of AI..."
question = "What is machine learning?"

answer = client.query_with_context(question, context)
print(answer)
```

### Summarization
```python
from src.llm_ollama import OllamaClient

client = OllamaClient(model="qwen2.5")
text = "Long document text here..."
summary = client.summarize(text)
print(summary)
```

## 📁 New Files Created

- `src/llm_ollama.py` - Ollama client integration
- `src/workflows_ollama.py` - RAG pipeline for Ollama
- `test_ollama.py` - Complete system test
- `setup_ollama.py` - Setup and configuration script

## 💡 Tips

1. **Speed**: GPU acceleration is automatic if available
2. **Privacy**: All data stays on your machine, nothing sent to cloud
3. **Cost**: Completely free, no API keys needed
4. **Quality**: qwen2.5 is excellent balance of speed vs quality
5. **Offline**: Works without internet once model is downloaded

## 🔧 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Make sure Ollama is running in another terminal:
ollama serve
```

### "Model not found"
```bash
# Pull the model:
ollama pull qwen2.5
```

### Slow responses
- Using CPU? Try a smaller model: `deepseek-r1:1.5b`
- Have GPU? It will auto-accelerate
- Close other apps to free up memory

## 📚 Full Integration

Your system now has:
- ✅ Document loading (PDF, DOCX, TXT, HTML, Markdown)
- ✅ Semantic chunking (smart paragraph-aware splitting)
- ✅ Vector embeddings (FAISS + sentence-transformers)
- ✅ Similarity search (retrieves relevant documents)
- ✅ **Ollama LLM integration** (local, free, private)
- ✅ RAG pipeline (grounds answers in your documents)
- ✅ Summarization (creates document summaries)
- ✅ CLI interface (interactive command line)

## 🎯 Next Steps

1. **Add your documents**: Place them in `./data/documents/`
2. **Index them**: `python cli.py` → `index`
3. **Ask questions**: `python cli.py` → `query`
4. **Get summaries**: `python cli.py` → `summarize`

---

**Your DataDistillerAI RAG system is production-ready!** 🚀
