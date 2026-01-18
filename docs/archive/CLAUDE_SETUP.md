# Claude (Anthropic) Setup Guide

## Quick Setup

### 1. Get Your API Key
- Visit: https://console.anthropic.com/
- Sign up or log in
- Go to Settings → API Keys
- Click "Create Key"
- Copy the key (starts with `sk-ant-`)

### 2. Add to .env
Edit `.env` file and replace:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

With your actual key:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

### 3. Install Library
Already installed! (done during setup)

### 4. Test Connection
```bash
python test_claude.py
```

## Usage Examples

### Simple Generation
```python
from src.llm_claude import ClaudeClient

client = ClaudeClient()
response = client.generate("Explain machine learning")
print(response)
```

### RAG (Question Answering)
```python
from src.llm_claude import ClaudeClient

client = ClaudeClient()
context = "Your document context..."
question = "Your question?"

answer = client.query_with_context(question, context)
print(answer)
```

### Full RAG Pipeline
```python
from src.workflows_claude import RAGPipeline

# Initialize
pipeline = RAGPipeline(document_path="./data/documents")

# Index your documents
pipeline.index_documents()

# Ask questions
answer = pipeline.query("What is machine learning?", top_k=3)
print(answer)

# Get summary
summary = pipeline.summarize()
print(summary)
```

### Using CLI
```bash
python cli.py
# Choose Claude backend when available
```

## Available Models

```python
from src.llm_claude import ClaudeClient

# Latest Sonnet (recommended, best balance)
client = ClaudeClient(model="claude-3-5-sonnet-20241022")

# Fastest
client = ClaudeClient(model="claude-3-5-haiku-20241022")

# Most Capable (slower)
client = ClaudeClient(model="claude-3-opus-20250219")
```

## Switching Between Backends

Your system supports multiple backends with the same interface:

```python
# Using Claude
from src.workflows_claude import RAGPipeline

# Using Ollama (local)
# from src.workflows_ollama import RAGPipeline

# Using Gemini (free)
# from src.workflows_gemini import RAGPipeline

pipeline = RAGPipeline()
# ... rest is the same!
```

## Pricing

Claude pricing is pay-as-you-go:
- **Input tokens**: $3 per 1M tokens (Sonnet)
- **Output tokens**: $15 per 1M tokens (Sonnet)

For reference:
- 1,000 words ≈ 1,300 tokens
- 10 page document ≈ 20,000 tokens

## Why Claude?

✅ **Excellent Reasoning** - Best at complex analysis
✅ **Long Context** - Can handle very long documents
✅ **Professional Quality** - Highest quality outputs
✅ **Reliable** - Production-ready API
✅ **Fast** - Quick response times

## Troubleshooting

### "invalid x-api-key"
- Check your key starts with `sk-ant-`
- Make sure it's copied correctly
- Verify in `.env` file has no extra spaces

### "Rate limited"
- Wait a moment and retry
- Claude has generous rate limits

### Key not found
- Ensure `.env` file has: `ANTHROPIC_API_KEY=your_key`
- Restart Python interpreter
- Check file permissions

## Comparing Backends

| Feature | Claude | Ollama | Gemini |
|---------|--------|--------|--------|
| Cost | $ | Free | Free Tier |
| Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Speed | Fast | Very Fast | Medium |
| Privacy | Cloud | Local | Cloud |
| Offline | No | Yes | No |

---

**Claude is perfect for professional RAG applications!** 🧠
