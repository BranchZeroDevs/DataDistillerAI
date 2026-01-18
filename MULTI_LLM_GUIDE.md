# Multi-LLM Integration Guide

Your DataDistillerAI now supports multiple LLM backends! Choose the one that best fits your needs.

## 🎯 Quick Comparison

| Feature | Ollama | Claude | Gemini |
|---------|--------|--------|--------|
| **Cost** | 🟢 FREE | 💰 Paid | 🟡 Free tier |
| **Speed** | ⚡ Fast (local) | ⚡ Fast (API) | 🔵 Medium |
| **Quality** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Privacy** | 🔐 100% Private | ☁️ Cloud | ☁️ Cloud |
| **Setup** | Easy | Easy | Easy |
| **Offline** | ✅ Yes | ❌ No | ❌ No |
| **Best For** | Local/Private | Complex Analysis | Budget-Friendly |

## 🚀 Setup Instructions

### Option 1: Ollama (100% Free, Local)

Already working! Keep running:
```bash
ollama serve
```

Test:
```bash
python test_ollama.py
```

### Option 2: Claude (Professional Quality)

**Step 1:** Get API key
- Visit: https://console.anthropic.com/
- Create account and generate API key

**Step 2:** Install and configure
```bash
python setup_claude.py
# Paste your API key when prompted
```

**Step 3:** Test
```bash
python test_claude.py
```

### Option 3: Google Gemini (Free Tier)

**Step 1:** Get API key
- Visit: https://ai.google.dev/
- Click "Get API Key" (no payment required)

**Step 2:** Install and configure
```bash
python setup_gemini.py
# Paste your API key when prompted
```

**Step 3:** Test
```bash
python test_gemini.py
```

## 💻 Code Examples

### Using Ollama (Local)
```python
from src.llm_ollama import OllamaClient

client = OllamaClient(model="qwen2.5")
response = client.generate("Explain AI")
```

### Using Claude (Professional)
```python
from src.llm_claude import ClaudeClient

client = ClaudeClient()
response = client.generate("Explain AI")
```

### Using Gemini (Free Tier)
```python
from src.llm_gemini import GeminiClient

client = GeminiClient()
response = client.generate("Explain AI")
```

### Full RAG Pipeline

#### With Ollama:
```python
from src.workflows_ollama import RAGPipeline

pipeline = RAGPipeline()
pipeline.index_documents()
answer = pipeline.query("What is machine learning?")
```

#### With Claude:
```python
from src.workflows_claude import RAGPipeline

pipeline = RAGPipeline()
pipeline.index_documents()
answer = pipeline.query("What is machine learning?")
```

#### With Gemini:
```python
from src.workflows_gemini import RAGPipeline

pipeline = RAGPipeline()
pipeline.index_documents()
answer = pipeline.query("What is machine learning?")
```

## 📁 Files Per Backend

### Ollama
- `src/llm_ollama.py` - Client
- `src/workflows_ollama.py` - RAG Pipeline
- `test_ollama.py` - Tests
- `setup_ollama.py` - Setup
- `OLLAMA_GUIDE.md` - Documentation

### Claude
- `src/llm_claude.py` - Client
- `src/workflows_claude.py` - RAG Pipeline
- `test_claude.py` - Tests
- `setup_claude.py` - Setup

### Gemini
- `src/llm_gemini.py` - Client
- `src/workflows_gemini.py` - RAG Pipeline (if created)
- `test_gemini.py` - Tests
- `setup_gemini.py` - Setup

## 🔄 Switching Backends

Just import from different modules:

```python
# Option 1: Local Ollama
from src.workflows_ollama import RAGPipeline

# Option 2: Cloud Claude  
from src.workflows_claude import RAGPipeline

# Option 3: Free Gemini
from src.workflows_gemini import RAGPipeline

# Use the same interface
pipeline = RAGPipeline()
pipeline.index_documents()
answer = pipeline.query("Your question")
```

## 💡 Recommendations

### Use Ollama If:
- ✅ Want 100% free solution
- ✅ Need complete privacy
- ✅ Have local compute resources
- ✅ Want no API key management

### Use Claude If:
- ✅ Need best quality answers
- ✅ Have complex reasoning tasks
- ✅ Want professional-grade output
- ✅ Don't mind paying for quality

### Use Gemini If:
- ✅ Want free cloud solution
- ✅ Have generous free tier needs
- ✅ OK with rate limiting
- ✅ Prefer Google's models

## ⚙️ Configuration

Add to `.env` file:

```bash
# Ollama (local, no key needed)
# Just ensure: ollama serve is running

# Claude (paid)
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Gemini (free tier)
GOOGLE_API_KEY=AIzaxxxxx

# OpenAI (paid, if using)
OPENAI_API_KEY=sk-proj-xxxxx
```

## 🧪 Test All Backends

```bash
# Test each one
python test_ollama.py    # Local
python test_claude.py    # Professional
python test_gemini.py    # Free
```

## 🎯 Common Tasks

### Question Answering with RAG
```python
from src.workflows_claude import RAGPipeline

pipeline = RAGPipeline()
pipeline.index_documents()
answer = pipeline.query("Your question", top_k=3)
print(answer)
```

### Document Summarization
```python
from src.workflows_claude import RAGPipeline

pipeline = RAGPipeline()
summary = pipeline.summarize()
print(summary)
```

### Custom Prompts
```python
from src.llm_claude import ClaudeClient

client = ClaudeClient()
response = client.generate(
    prompt="Your custom prompt",
    system_prompt="You are a helpful assistant",
    max_tokens=1024,
    temperature=0.7
)
```

## 🚀 Production Deployment

For production, consider:

1. **Ollama**: Best for on-premises, air-gapped systems
2. **Claude**: Best for professional applications that need quality
3. **Gemini**: Best for cost-conscious projects with moderate scale

All three support the same RAGPipeline interface, so switching is easy:

```python
# In production, maybe use environment variable to choose
import os

backend = os.getenv("RAG_BACKEND", "claude")

if backend == "ollama":
    from src.workflows_ollama import RAGPipeline
elif backend == "claude":
    from src.workflows_claude import RAGPipeline
else:
    from src.workflows_gemini import RAGPipeline

pipeline = RAGPipeline()
```

---

**Your DataDistillerAI supports multiple professional LLM backends!** 🚀
