# 🎨 DataDistillerAI Web UI

## Getting Started in 30 Seconds

```bash
# Start the web UI
streamlit run app.py
```

**That's it!** The browser will open automatically at `http://localhost:8501`

---

## 🖼️ Interface Overview

### Left Sidebar
```
⚙️ Configuration
├─ Choose LLM Backend
│  ├─ Claude (Haiku) - Recommended
│  ├─ Ollama (Local) - Free
│  └─ Gemini (Free) - Budget option
└─ Costs & Info
```

### Main Tabs

#### 💬 Chat Tab
```
┌─────────────────────────────────┐
│ Ask Questions About Documents   │
├─────────────────────────────────┤
│ Your question: [input field   ] │
│ Top results: [slider 1-5]       │
├─────────────────────────────────┤
│ Answer:                         │
│ [AI response here]              │
├─────────────────────────────────┤
│ 📎 Retrieved Context (expand)   │
│ Shows which docs were used      │
├─────────────────────────────────┤
│ 💭 Chat History                 │
│ Previous Q&A stored here        │
└─────────────────────────────────┘
```

#### 📊 Documents Tab
```
┌──────────────────────────┐
│ Document Information     │
├──────────────────────────┤
│ Documents: 2             │
│ Chunks: 5                │
│ Total Characters: 4,573  │
├──────────────────────────┤
│ 📄 Indexed Documents     │
│ ├─ machine_learning.txt  │
│ │  [preview]             │
│ └─ deep_learning.txt     │
│    [preview]             │
└──────────────────────────┘
```

#### ℹ️ About Tab
```
📚 Documentation
💡 How it works
🔧 Tech stack
💰 Pricing info
📖 Links to guides
```

---

## 🚀 Common Workflows

### Workflow 1: Ask a Question
```
1. Open app.py in browser
2. Type: "What is machine learning?"
3. See answer with sources
4. Expand to see which docs were used
```

### Workflow 2: Switch Backends
```
1. Change backend in sidebar
2. (First use may index documents)
3. Ask same question
4. Compare answers from different LLMs
```

### Workflow 3: Add New Documents
```
1. Put files in ./data/documents/
2. Restart the app
3. Docs auto-index on startup
4. Ask questions about them
```

---

## 💡 Features

### 🎯 Smart Document Retrieval
- Semantic search finds relevant passages
- Shows relevance score for each chunk
- Configurable number of results (1-5)

### 🧠 Multi-Backend Support
- **Claude**: Professional quality, low cost
- **Ollama**: 100% free, runs locally
- **Gemini**: Free tier, cloud-based

### 📎 Context Attribution
- See exactly which documents were used
- Relevance scores (0-1)
- Click to expand and read full context

### 💾 Chat History
- Stores your Q&A in session
- Review previous conversations
- Save to history with one click

### 📊 Document Analytics
- Count of documents and chunks
- Total characters indexed
- Preview document content

---

## ⚙️ Configuration Guide

### Using Claude (Recommended)
```
1. Get key: https://console.anthropic.com/
2. Edit .env:
   ANTHROPIC_API_KEY=sk-ant-xxxxx
3. Select "Claude (Haiku)" in sidebar
4. Start asking questions
Cost: ~$0.80/1M tokens
```

### Using Ollama (Free)
```
1. Make sure Ollama is running:
   ollama serve
2. Select "Ollama (Local)" in sidebar
3. (App auto-detects and uses it)
Cost: $0 (runs on your machine)
```

### Using Gemini (Free)
```
1. Get key: https://ai.google.dev/
2. Edit .env:
   GOOGLE_API_KEY=AIza...
3. Select "Gemini (Free)" in sidebar
4. Keep in mind: Rate limits apply
Cost: Free tier available
```

---

## 🔧 Troubleshooting

### App won't start
```bash
# Make sure you're in the right directory
cd /Users/gokulsreekumar/Documents/DataDistillerAI

# Make sure virtual env is active
source .venv/bin/activate

# Try running again
streamlit run app.py
```

### Backend not working
- **Claude**: Check API key in .env
- **Ollama**: Check `ollama serve` is running
- **Gemini**: Check API key format

### Documents not indexing
- Files must be in `./data/documents/`
- Supported: PDF, DOCX, TXT, HTML, Markdown
- Restart app to re-index

### Slow responses
- Use fewer top_k results (try 1 or 2)
- Smaller documents = faster processing
- Ollama slower on CPU (use GPU if available)

---

## 📊 Performance Tips

| Task | Best Backend |
|------|--------------|
| **Quick responses** | Ollama (local) |
| **Best quality** | Claude Opus |
| **Lowest cost** | Claude Haiku |
| **Free option** | Ollama or Gemini |
| **Production** | Claude Haiku |

---

## 🚀 Next Steps

1. **Set up a backend** (Claude recommended)
2. **Add your documents** to `./data/documents/`
3. **Start the app** with `streamlit run app.py`
4. **Ask questions** about your documents!

---

## 💻 CLI Alternative

Don't want the web UI? Use the CLI:

```bash
python cli.py
```

---

**Ready? Run:** `streamlit run app.py` 🚀
