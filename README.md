# DataDistillerAI — Knowledge & Data Exploration Engine

An end-to-end AI system for ingesting, processing, and intelligently querying large knowledge bases using retrieval-augmented generation (RAG).

## Features

- **Data Ingestion**: Load documents from multiple formats (PDF, DOCX, TXT, HTML)
- **Semantic Chunking**: Intelligent text segmentation preserving context and meaning
- **Vector Indexing**: Fast similarity search using FAISS and embeddings
- **RAG Pipeline**: Ground LLM responses in source data to reduce hallucinations
- **Modular Workflows**: Query answering, summarization, and exploratory analysis
- **LLM Integration**: OpenAI API with LangChain for deterministic + probabilistic reasoning

## Architecture

```
Data Sources → Ingestion → Processing (Cleaning & Chunking) → Vector DB
                                                          ↓
                                                      Retrieval
                                                          ↓
                                                    LLM + Prompt
                                                          ↓
                                                       Response
```

## Project Structure

```
DataDistillerAI/
├── src/
│   ├── ingestion/           # Document loading & parsing
│   ├── processing/          # Cleaning, chunking, preprocessing
│   ├── retrieval/           # Vector DB & retrieval logic
│   ├── llm/                 # LLM clients & prompt engineering
│   ├── workflows/           # High-level query workflows
│   └── __init__.py
├── tests/                   # Unit & integration tests
├── config/                  # Configuration files
├── data/                    # Sample documents & datasets
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Quick Start

### 1. Setup Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
VECTOR_DB_PATH=./data/vector_store
```

### 3. Run Examples

```bash
python examples/basic_rag.py
```

## Components

### Data Ingestion (`src/ingestion/`)
- `loaders.py`: Document format handlers (PDF, DOCX, etc.)
- `parser.py`: Extract text from various document types

### Processing (`src/processing/`)
- `cleaner.py`: Text cleaning and normalization
- `chunker.py`: Semantic and fixed-size chunking strategies
- `preprocessor.py`: Tokenization and metadata enrichment

### Retrieval (`src/retrieval/`)
- `embeddings.py`: Embedding model management
- `vector_store.py`: FAISS vector database wrapper
- `retriever.py`: Similarity search and retrieval logic

### LLM (`src/llm/`)
- `client.py`: OpenAI API wrapper
- `prompts.py`: Prompt templates for different tasks
- `chains.py`: LangChain integration

### Workflows (`src/workflows/`)
- `rag.py`: Core RAG pipeline
- `qa.py`: Question answering workflow
- `summarization.py`: Document summarization
- `exploration.py`: Interactive exploration

## Usage Example

```python
from src.workflows.rag import RAGPipeline

# Initialize pipeline
pipeline = RAGPipeline(
    document_path="./data/documents/",
    vector_db_path="./data/vector_store"
)

# Index documents
pipeline.index_documents()

# Query
response = pipeline.query("What are the key findings?", top_k=3)
print(response)
```

## Configuration

Edit `config/settings.yaml` to customize:
- Chunk size and overlap
- Embedding model
- LLM parameters (temperature, max_tokens)
- Vector DB settings

## Contributing

1. Create feature branches from `main`
2. Write tests for new functionality
3. Ensure all tests pass: `pytest`
4. Submit pull requests

## License

MIT License
