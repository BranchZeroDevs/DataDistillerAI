# ❓ Frequently Asked Questions (FAQ)

## General Questions

### What is DataDistiller AI?
DataDistiller AI is a privacy-first RAG (Retrieval-Augmented Generation) system that lets you upload documents and ask questions about them in natural language. It runs 100% locally on your machine, ensuring your data never leaves your computer.

### What makes it different from ChatGPT or other AI assistants?
- **Privacy**: All processing happens locally - your documents never leave your machine
- **Accuracy**: Answers are grounded in YOUR documents, not general training data
- **Citations**: Every answer includes source references
- **Knowledge Graph**: Visualize concepts and relationships in your documents
- **Free**: Uses free, local models (Ollama) - no API costs

### Is this good for a resume/portfolio?
Absolutely! This project demonstrates:
- ✅ Modern AI/ML skills (RAG, embeddings, vector search)
- ✅ Full-stack development (Python, Streamlit, FastAPI)
- ✅ System design (architecture, data pipelines)
- ✅ Production considerations (testing, CI/CD, documentation)
- ✅ Popular frameworks (LangChain, FAISS, spaCy)

---

## Technical Questions

### What programming languages/frameworks are used?
- **Language**: Python 3.10+
- **UI**: Streamlit
- **LLM Framework**: LangChain
- **Vector DB**: FAISS
- **NLP**: spaCy, sentence-transformers
- **Visualization**: NetworkX, PyVis

### What file formats are supported?
- PDF (text-based, not scanned images)
- DOCX (Microsoft Word)
- TXT (plain text)
- HTML (web pages)
- Markdown (.md files)

### Can I use cloud LLMs instead of Ollama?
Yes! DataDistiller supports:
- **Ollama** (default): Free, local, private
- **Claude** (Anthropic): High-quality, paid API
- **Gemini** (Google): Free tier available, paid for production

See [MULTI_LLM_GUIDE.md](../MULTI_LLM_GUIDE.md) for setup instructions.

### How much RAM/CPU do I need?
**Minimum**:
- 8 GB RAM
- 4 CPU cores
- 5 GB disk space

**Recommended**:
- 16 GB RAM
- 8 CPU cores
- 10 GB disk space

The embeddings model and vector store are relatively lightweight. Most compute goes to the LLM.

### Does it work on M1/M2 Macs?
Yes! Ollama has excellent Apple Silicon support. In fact, it's often faster on M-series Macs than on comparable Intel machines.

### Can I use GPU acceleration?
Yes, if using:
- **Ollama**: Automatically uses GPU if available (CUDA/Metal)
- **FAISS**: Can use GPU with `faiss-gpu` instead of `faiss-cpu`
- **Embeddings**: sentence-transformers supports CUDA

---

## Usage Questions

### How many documents can I upload?
- **V1 (local)**: Recommended <100 documents, tested up to 1000
- **V2 (production)**: No hard limit, scales horizontally

Performance depends on total text volume, not just document count.

### How long does indexing take?
Approximate times:
- 10-page PDF: ~3-5 seconds
- 50-page PDF: ~15-20 seconds
- 100-page PDF: ~30-40 seconds

Indexing is a one-time operation per document.

### Can I update documents after uploading?
Currently, you need to re-index. Future versions will support incremental updates.

### What languages are supported?
- **Documents**: Any language (Unicode text)
- **Queries**: English works best (spaCy model is English-trained)
- **LLM Responses**: Depends on the model (most support multiple languages)

### How accurate are the answers?
Accuracy depends on:
1. **Document quality**: Well-formatted, searchable text works best
2. **Query formulation**: Specific questions get better answers
3. **Context relevance**: Answers only as good as retrieved context
4. **LLM capability**: Better models (Claude) > smaller models (qwen2.5:3b)

Always verify important information against source documents.

---

## Troubleshooting

### "Ollama not responding" error
**Solution**:
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags

# If still not working, reinstall
brew reinstall ollama  # macOS
```

### "Model not found" error
**Solution**:
```bash
# Download the model
ollama pull qwen2.5:3b

# List available models
ollama list

# Try a different model
ollama pull llama2
```

### "spaCy model not found" error
**Solution**:
```bash
# Download the model
python -m spacy download en_core_web_sm

# Force reinstall if corrupted
python -m spacy download en_core_web_sm --force
```

### Slow query responses
**Causes & Solutions**:
1. **Large corpus**: Reduce `top_k` or use a GPU
2. **Slow LLM**: Try a smaller/faster model
3. **Network issues**: Ollama should be local (localhost)

### Out of memory errors
**Solutions**:
1. Use a smaller Ollama model: `qwen2.5:3b` instead of `llama2:13b`
2. Reduce chunk size in processing settings
3. Process fewer documents at once
4. Close other applications

### "Failed to create embeddings" error
**Solution**:
```bash
# Reinstall sentence-transformers
pip uninstall sentence-transformers
pip install sentence-transformers

# Clear cache
rm -rf ~/.cache/huggingface
```

---

## Performance & Optimization

### How can I make queries faster?
1. Use a smaller, faster LLM model
2. Reduce `top_k` (retrieve fewer chunks)
3. Use GPU acceleration for embeddings
4. Pre-index documents (don't re-index each time)

### How can I improve answer quality?
1. Use better LLM (Claude > Gemini > Ollama)
2. Increase `top_k` for more context
3. Improve document quality (clean formatting)
4. Use more specific queries
5. Ensure relevant documents are uploaded

### How much disk space does it use?
- Base installation: ~2 GB (dependencies)
- Ollama models: 2-7 GB each
- Vector indices: ~10-50 MB per 1000 pages
- Documents: Your original file sizes

---

## Advanced Topics

### Can I use this in production?
V1 is designed for local/development use. For production:
- See [V2 (Production)](../README_V2.md) for scalable architecture
- Implements async workers, job queues, API, persistence
- Supports multiple concurrent users

### Can I integrate this into my application?
Yes! See [examples/](../examples/) for:
- Python API usage
- REST API integration (V2)
- Custom pipeline creation

### Can I fine-tune the embeddings model?
Yes, but requires ML expertise:
1. Collect domain-specific training data
2. Fine-tune sentence-transformers model
3. Replace default model in config
4. Re-index all documents

### Can I add custom document loaders?
Yes! Implement the `BaseLoader` interface:
```python
from src.ingestion.base import BaseLoader

class CustomLoader(BaseLoader):
    def load(self, path: str) -> str:
        # Your parsing logic
        return text
```

### Is there an API?
- **V1**: No REST API (Python library only)
- **V2**: Full REST API with OpenAPI docs
  - See [V2 Setup](docs/V2_SETUP.md)

---

## Contributing & Support

### How can I contribute?
See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Where can I get help?
1. Check this FAQ
2. Read the [documentation](../docs/)
3. Search [GitHub Issues](https://github.com/BranchZeroDevs/DataDistillerAI/issues)
4. Open a new issue with details

### Can I use this commercially?
Yes! This project is MIT licensed - free for commercial use.
See [LICENSE](../LICENSE) for details.

---

## Roadmap

### What features are planned?
See [CHANGELOG.md](../CHANGELOG.md) and roadmap in [README.md](../README.md):
- Hybrid search (BM25 + dense)
- Multi-document conversations
- Better chunking strategies
- Export functionality
- Cloud deployment guides

### Can I request features?
Yes! Open a [GitHub Discussion](https://github.com/BranchZeroDevs/DataDistillerAI/discussions) or Issue.

---

Still have questions? [Open an issue](https://github.com/BranchZeroDevs/DataDistillerAI/issues/new) and we'll help!
