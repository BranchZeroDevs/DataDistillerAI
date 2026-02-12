# DataDistiller AI

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"/>
</p>

> **Intelligent Document Q&A powered by Retrieval-Augmented Generation (RAG) with Knowledge Graph Visualization**

## Welcome

DataDistiller AI is a **privacy-first RAG system** that transforms your documents into an intelligent knowledge base. Upload PDFs, Word docs, or text files, and ask questions in natural language — all processed **100% locally** on your machine.

## Key Highlights

- 🔒 **Privacy-First**: All processing happens locally
- 🧠 **Smart Knowledge Graphs**: Visualize document concepts  
- ⚡ **Lightning Fast**: Powered by FAISS for instant search
- 🎨 **Interactive UI**: Beautiful Streamlit interface
- 🤖 **Multi-LLM Support**: Ollama, Claude, or Gemini
- 📚 **Universal Documents**: PDF, DOCX, TXT, HTML, MD

## Quick Start

```bash
# 1. Install Ollama
brew install ollama
ollama serve
ollama pull qwen2.5:3b

# 2. Clone and setup
git clone https://github.com/BranchZeroDevs/DataDistillerAI.git
cd DataDistillerAI
python -m venv .venv
source .venv/bin/activate

# 3. Install and run
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

## Navigation

- [Quick Start Guide](getting-started/quickstart.md)
- [Architecture Overview](architecture/overview.md)
- [Examples](guides/examples.md)
- [FAQ](guides/faq.md)

## License

MIT License - see [License](about/license.md) for details.
