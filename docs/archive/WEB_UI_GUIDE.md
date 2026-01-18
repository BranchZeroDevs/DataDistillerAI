# 🎨 Web UI Guide

## Running the Streamlit App

### Start the Web UI

```bash
streamlit run app.py
```

The app opens automatically at: **http://localhost:8501**

---

## 💬 Chat Interface

**Ask questions about your documents:**

1. Type your question in the input box
2. Select how many document chunks to retrieve (1-5)
3. View the answer with sources
4. Expand "Retrieved Context" to see which documents were used

**Features:**
- Real-time answers
- Relevance scoring
- Source attribution
- Chat history storage

---

## 📊 Documents Tab

**View your indexed documents:**

- Total document count
- Total chunks created
- Document size in characters
- Preview document content

---

## ℹ️ About Tab

**Learn about the system:**

- How RAG works
- Available backends
- Cost comparison
- Technology stack
- Documentation links

---

## ⚙️ Sidebar Configuration

**Select your LLM backend:**

| Backend | Best For | Cost | Speed |
|---------|----------|------|-------|
| Claude Haiku | Production | Low | ⚡⚡⚡ |
| Ollama | Privacy | Free | ⚡⚡⚡ |
| Gemini | Budget | Free | ⚡⚡ |

---

## 🔧 Setup Before Starting

### Claude Setup
```bash
# 1. Get key: https://console.anthropic.com/
# 2. Add to .env:
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### Ollama Setup
```bash
# 1. Make sure Ollama is running:
ollama serve

# 2. UI will auto-detect it
```

### Gemini Setup
```bash
# 1. Get key: https://ai.google.dev/
# 2. Add to .env:
GOOGLE_API_KEY=AIza...
```

---

## 📚 Adding Documents

1. Put files in `./data/documents/`
2. Supported: PDF, DOCX, TXT, HTML, Markdown
3. Restart app to re-index

---

## 🚀 Full Command

```bash
# Start the web UI
streamlit run app.py

# In your browser, go to:
http://localhost:8501
```

---

**Start chatting with your documents!** 🧠
