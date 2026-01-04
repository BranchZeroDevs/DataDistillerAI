# Quick Start Guide - DataDistillerAI

## 🎯 5-Minute Quick Start

### 1. Initial Setup

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data/documents data/vector_store
cp .env.example .env
python examples/sample_data.py
```

### 2. Configure API Key

Edit `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Index Documents

```bash
# Create sample documents (already done by setup.sh)
python examples/sample_data.py

# Or add your own documents to data/documents/
# Supported formats: PDF, DOCX, TXT, HTML, MD
```

### 4. Run Basic Example

```bash
python examples/basic_rag.py
```

Expected output:
```
INFO:root:Indexing documents...
INFO:root:Loaded document: ml_fundamentals.txt (...)
INFO:root:Created X chunks from text
INFO:root:Added X chunks to vector store
INFO:root:Query: What is the main topic of the documents?
INFO:root:Response:
The documents discuss machine learning and deep learning fundamentals...
```

### 5. Interactive CLI

```bash
python cli.py
```

Commands:
- `setup` - Initialize pipeline
- `index` - Index documents
- `query` - Ask a question
- `summarize` - Generate summary
- `help` - Show help
- `exit` - Exit

Example session:
```
> setup
Enter document path (default: ./data/documents): 
> index
> query
Enter your question: What is deep learning?
> summarize
```

---

## 📚 Using the Python API

### Basic Query

```python
from src.workflows import RAGPipeline

pipeline = RAGPipeline(
    document_path="./data/documents",
    vector_db_path="./data/vector_store"
)

# Index documents
pipeline.index_documents()

# Ask a question
answer = pipeline.query("What is machine learning?")
print(answer)
```

### Summarize Documents

```python
summary = pipeline.summarize()
print(summary)
```

### Work with Components

```python
from src.ingestion import DocumentLoader
from src.processing.chunker import SemanticChunker
from src.retrieval import VectorStore

# Load documents
loader = DocumentLoader()
documents = loader.load_directory("./data/documents")

# Chunk them
chunker = SemanticChunker(chunk_size=1024)
chunks = []
for doc in documents:
    chunks.extend(chunker.chunk(doc.content, metadata=doc.metadata))

# Index in vector store
vector_store = VectorStore()
vector_store.add_documents(chunks)

# Search
results = vector_store.search("your query", top_k=5)
```

---

## 🛠️ Project Structure

```
DataDistillerAI/
├── src/
│   ├── ingestion/         # Document loading
│   ├── processing/        # Chunking & cleaning
│   ├── retrieval/         # Vector DB
│   ├── llm/               # LLM integration
│   └── workflows/         # High-level pipelines
├── examples/
│   ├── basic_rag.py       # Simple example
│   ├── usage_examples.py  # Detailed examples
│   └── sample_data.py     # Create sample docs
├── tests/                 # Unit tests
├── config/                # Settings
├── data/                  # Documents & vector DB
├── cli.py                 # Interactive CLI
├── requirements.txt       # Dependencies
├── .env.example          # Template env file
├── README.md             # Full documentation
└── DEVELOPMENT.md        # Development guide
```

---

## 🔧 Configuration

All settings are in `.env`:

```env
# API
OPENAI_API_KEY=sk-your-key

# Paths
VECTOR_DB_PATH=./data/vector_store
DATA_PATH=./data

# LLM
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500

# Processing
CHUNK_SIZE=1024
CHUNK_OVERLAP=128
MIN_CHUNK_LENGTH=100

# Retrieval
TOP_K_RETRIEVALS=5
SIMILARITY_THRESHOLD=0.5

# Logging
LOG_LEVEL=INFO
```

See `config/settings.py` for defaults.

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_ingestion.py::TestDocumentLoader::test_load_txt_file

# Run with coverage
pytest --cov=src tests/
```

---

## 📖 Common Tasks

### Add More Documents

```bash
# Copy your documents to data/documents/
cp my_docs/*.pdf data/documents/
cp my_docs/*.txt data/documents/

# Re-index
python -c "
from src.workflows import RAGPipeline
p = RAGPipeline()
p.index_documents()
"
```

### Change Embedding Model

Edit `.env`:
```env
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

Or in code:
```python
pipeline = RAGPipeline(
    embedding_model="sentence-transformers/all-mpnet-base-v2"
)
```

### Adjust Chunk Size

Edit `.env`:
```env
CHUNK_SIZE=2048
CHUNK_OVERLAP=256
```

Smaller chunks = more precise but more API calls
Larger chunks = fewer API calls but less precise

### Change LLM Model

Edit `.env`:
```env
LLM_MODEL=gpt-4
```

Or in code:
```python
pipeline = RAGPipeline(llm_model="gpt-4")
```

---

## ❓ FAQ

**Q: How do I use my own documents?**
A: Place them in `data/documents/` (supports PDF, DOCX, TXT, HTML, MD), then run `pipeline.index_documents()`

**Q: What if I get "API rate limit" error?**
A: Add delays between requests or use a different API key with higher rate limits

**Q: How can I improve answer quality?**
A: Adjust `CHUNK_SIZE`, use a better embedding model, or fine-tune prompts in `src/llm/__init__.py`

**Q: Can I use local LLMs instead of OpenAI?**
A: Yes, modify `src/llm/__init__.py` to use Llama, Mistral, or other local models

**Q: How do I persist the vector database?**
A: Already saved to `VECTOR_DB_PATH`. Load with: `vector_store.load("./data/vector_store")`

---

## 🚀 Next Steps

1. **Explore Examples**: Check `examples/` for more detailed usage patterns
2. **Read Documentation**: See `README.md` and `DEVELOPMENT.md`
3. **Customize**: Modify components for your use case
4. **Deploy**: Package as service or integrate into applications
5. **Contribute**: Improve and extend functionality

---

## 📞 Support

For issues or questions:
1. Check `DEVELOPMENT.md` troubleshooting section
2. Review example code in `examples/`
3. Check test files for usage patterns
4. Read docstrings in source files

Happy coding! 🎉
