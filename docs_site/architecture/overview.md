# 🏗️ DataDistiller AI - System Architecture

## Overview

DataDistiller AI is a **Retrieval-Augmented Generation (RAG)** system that combines document retrieval with large language models to provide intelligent question-answering capabilities.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│                    (Streamlit Web App)                          │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RAG Pipeline Core                          │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │  Document   │  │  Processing  │  │   Knowledge Graph   │   │
│  │  Ingestion  │→ │  & Chunking  │→ │   Construction      │   │
│  └─────────────┘  └──────────────┘  └─────────────────────┘   │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ Embedding   │  │ Vector Store │  │   LLM Integration   │   │
│  │ Generation  │→ │   (FAISS)    │→ │     (Ollama)        │   │
│  └─────────────┘  └──────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Document Ingestion (`src/ingestion/`)

**Purpose**: Load and parse documents from various formats

**Components**:
- PDF Loader (PyPDF)
- DOCX Loader (python-docx)
- Text Loader
- HTML Loader (BeautifulSoup4)
- Markdown Loader

**Flow**:
```
Documents → Format Detection → Content Extraction → Text Output
```

### 2. Text Processing (`src/processing/`)

**Purpose**: Split documents into semantic chunks for better retrieval

**Components**:
- Semantic Chunker
- Overlap Strategy
- Metadata Preservation

**Flow**:
```
Raw Text → Semantic Splitting → Chunks with Context → Metadata Tagging
```

**Parameters**:
- Chunk Size: ~500 tokens
- Overlap: ~50 tokens
- Strategy: Sentence-aware splitting

### 3. Embedding Generation

**Purpose**: Convert text chunks into vector representations

**Model**: `sentence-transformers/all-MiniLM-L6-v2`
- Dimensions: 384
- Speed: ~1000 sentences/sec on CPU
- Quality: Optimized for semantic similarity

**Flow**:
```
Text Chunks → Sentence Transformer → 384-dim Vectors → Normalized
```

### 4. Vector Store (`src/retrieval/`)

**Purpose**: Efficient similarity search over document embeddings

**Technology**: FAISS (Facebook AI Similarity Search)
- Index Type: Flat (exact search)
- Distance Metric: Cosine similarity
- Persistence: Local disk storage

**Flow**:
```
Query → Embedding → FAISS Search → Top-K Results → Re-ranking
```

### 5. Knowledge Graph (`src/knowledge_graph.py`)

**Purpose**: Extract and visualize concept relationships

**Components**:
- Entity Extraction (spaCy NER)
- Relationship Detection
- Graph Construction (NetworkX)
- Visualization (PyVis)

**Modes**:
1. **Network Graph**: Interactive concept network
2. **Statistics**: Entity frequencies and metrics
3. **Semantic Flow**: Concept progression through documents
4. **AI Progression**: LLM-enhanced concept relationships

**Flow**:
```
Documents → NER (spaCy) → Entity Pairs → Graph → Visualization
```

### 6. LLM Integration (`src/llm/`)

**Purpose**: Generate natural language answers from retrieved context

**Supported Backends**:
- **Ollama** (Primary): Local, privacy-first
  - Models: qwen2.5:3b, llama2, mistral, etc.
  - API: REST (localhost:11434)
- **Claude** (Optional): Anthropic cloud API
- **Gemini** (Optional): Google cloud API

**Flow**:
```
Query + Context → Prompt Template → LLM → Answer + Citations
```

### 7. RAG Pipeline (`src/workflows/`)

**Purpose**: Orchestrate the end-to-end RAG process

**Steps**:
1. **Index Phase**:
   ```
   Documents → Ingestion → Chunking → Embedding → Vector Store
   ```

2. **Query Phase**:
   ```
   User Query → Embedding → Retrieval → Context Assembly → LLM → Answer
   ```

**Prompt Template**:
```
Context: [Retrieved document chunks]
Question: [User query]
Instructions: Answer based on context, cite sources
```

## Data Flow

### Document Indexing

```
1. User uploads documents (PDF, DOCX, TXT, etc.)
   ↓
2. Document Loader extracts text
   ↓
3. Text Chunker splits into semantic units
   ↓
4. Sentence Transformer creates embeddings
   ↓
5. FAISS indexes vectors for fast search
   ↓
6. spaCy extracts entities for Knowledge Graph
   ↓
7. Metadata stored for source tracking
```

### Query Processing

```
1. User submits natural language question
   ↓
2. Question embedded into vector
   ↓
3. FAISS finds top-K similar chunks
   ↓
4. Context assembled from retrieved chunks
   ↓
5. Prompt constructed with context + question
   ↓
6. LLM generates answer
   ↓
7. Sources cited in response
   ↓
8. Answer displayed to user
```

## Technology Stack

### NLP & ML
- **sentence-transformers**: Semantic embeddings
- **FAISS**: Vector similarity search
- **spaCy**: Named Entity Recognition (NER)
- **NetworkX**: Graph analysis
- **LangChain**: LLM orchestration

### LLM
- **Ollama**: Local model serving
- **Anthropic SDK**: Claude integration
- **Google GenAI**: Gemini integration

### UI & API
- **Streamlit**: Interactive web interface
- **FastAPI**: REST API (V2)

### Document Processing
- **PyPDF**: PDF parsing
- **python-docx**: DOCX parsing
- **BeautifulSoup4**: HTML parsing

## Performance Characteristics

### Indexing (V1)
- PDF: ~2-3 pages/sec
- DOCX: ~5-10 pages/sec
- TXT: ~20-30 pages/sec

### Query (V1)
- Embedding: ~50ms
- Vector search: ~10-50ms (depends on corpus size)
- LLM generation: ~2-5 sec (depends on model)
- **Total**: ~2-6 seconds per query

### Scalability
- **V1**: Up to ~1000 documents, single user
- **V2**: Unlimited documents, multiple concurrent users

## Security & Privacy

### V1 (Local)
- ✅ 100% local processing
- ✅ No data sent to cloud
- ✅ Ollama models run on-device
- ✅ FAISS index stored locally

### V2 (Production)
- ⚠️ Data stored in PostgreSQL/MinIO
- ⚠️ Cloud LLMs send data to API providers
- ✅ Can use Ollama for privacy
- ✅ Secure by design (auth pending)

## Directory Structure

```
src/
├── __init__.py
├── ingestion/              # Document loaders
│   ├── pdf_loader.py
│   ├── docx_loader.py
│   └── text_loader.py
├── processing/             # Text chunking
│   └── chunker.py
├── retrieval/              # Vector store
│   └── vector_store.py
├── llm/                    # LLM integrations
│   ├── base.py
│   ├── ollama_client.py
│   ├── claude_client.py
│   └── gemini_client.py
├── workflows/              # RAG orchestration
│   └── rag_pipeline.py
├── knowledge_graph.py      # Graph features
├── workflows_ollama.py     # Ollama workflow
├── workflows_claude.py     # Claude workflow
└── workflows_gemini.py     # Gemini workflow
```

## Future Enhancements

### Planned
- [ ] Hybrid search (BM25 + dense)
- [ ] Multi-document conversations
- [ ] Better chunking strategies
- [ ] Query expansion
- [ ] Answer quality metrics
- [ ] Caching layer
- [ ] Batch processing

### Under Consideration
- [ ] Multi-modal support (images, tables)
- [ ] Real-time document updates
- [ ] Distributed vector stores
- [ ] Fine-tuned embeddings
- [ ] Custom LLM integration

---

For implementation details, see the [source code](../src/) and [examples](../examples/).
