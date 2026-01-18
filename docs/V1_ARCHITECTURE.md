# DataDistiller 1.0 - Architecture

Technical architecture for the local RAG system.

## System Overview

DataDistiller 1.0 is a monolithic, synchronous RAG system designed for local deployment with minimal infrastructure requirements.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Streamlit  │  │     CLI      │  │ Python API   │ │
│  │   (app.py)   │  │   (cli.py)   │  │   (direct)   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                             ▼
          ┌────────────────────────────────────┐
          │      RAG Pipeline Orchestrator     │
          │   (workflows_ollama.py, etc.)      │
          └────────────┬───────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│  Document   │ │  Retrieval  │ │  Generation  │
│  Ingestion  │ │   (Search)  │ │    (LLM)     │
└─────────────┘ └─────────────┘ └──────────────┘
       │               │               │
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│   Chunker   │ │   FAISS     │ │   Ollama     │
│   Embedder  │ │VectorStore  │ │   Server     │
└─────────────┘ └─────────────┘ └──────────────┘
```

## Core Components

### 1. User Interface Layer

#### Streamlit Web App (app.py)
- **Purpose**: Interactive web interface
- **Features**: 
  - Document Q&A chat
  - Document upload/management
  - Knowledge Graph visualization
  - Chat history
- **Technology**: Streamlit
- **Port**: 8501

#### CLI (cli.py)
- **Purpose**: Command-line interface
- **Features**: Terminal-based Q&A
- **Use Case**: Scripting, automation

#### Python API
- **Purpose**: Direct programmatic access
- **Usage**: Import and use classes directly

### 2. RAG Pipeline Layer

#### RAGPipelineOllama (workflows_ollama.py)
**Responsibilities:**
- Orchestrate entire RAG workflow
- Coordinate ingestion, retrieval, generation
- Manage vector store lifecycle

**Key Methods:**
```python
def index_documents(self, path: str) -> None:
    """Load and index all documents"""
    
def query(self, question: str, top_k: int = 3) -> str:
    """Execute RAG query pipeline"""
```

**Flow:**
1. Ingest: Load → Parse → Chunk → Embed → Store
2. Query: Embed question → Search vectors → Retrieve chunks → Generate answer

#### Alternative Pipelines
- `RAGPipelineClaude` - Uses Claude for generation
- `RAGPipelineGemini` - Uses Gemini for generation

### 3. Document Ingestion

#### File Loaders (src/ingestion/)
**Supported formats:**
- TXT: Plain text
- PDF: via pypdf
- DOCX: via python-docx
- HTML: via BeautifulSoup
- MD: Markdown files

**Process:**
```
File → Loader → Raw Text → Chunker → Chunks
```

#### Semantic Chunker (src/processing/chunker.py)
**Algorithm:**
1. Split text into sentences
2. Create overlapping windows
3. Respect semantic boundaries
4. Generate metadata

**Configuration:**
```python
chunk_size = 500       # Characters per chunk
chunk_overlap = 50     # Overlap for context
```

### 4. Retrieval System

#### Vector Store (src/retrieval/)
**Implementation**: FAISS (Facebook AI Similarity Search)

**Storage**: In-memory (lifetime: process duration)

**Operations:**
```python
def add_documents(self, chunks, metadata) -> None:
    """Add documents to vector store"""
    
def search(self, query, top_k=3) -> List[Tuple]:
    """Semantic search"""
```

#### Embedding Model
**Model**: sentence-transformers/all-MiniLM-L6-v2
- **Dimensions**: 384
- **Speed**: Fast (~1000 chunks/sec)
- **Accuracy**: Good for general use
- **Size**: ~80MB

**Process:**
```
Text → Tokenize → Encode → 384-dim vector
```

### 5. Generation (LLM)

#### Ollama Integration (src/llm/llm_ollama.py)
**Architecture:**
- **Local server**: http://localhost:11434
- **API**: REST-based
- **Streaming**: Supported

**Models supported:**
- qwen2.5:3b (default, fast)
- llama3.2:3b
- mistral:7b
- Any Ollama model

**Query process:**
```
Question + Retrieved Context → Prompt Template → Ollama → Answer
```

**Prompt Template:**
```
Context: {retrieved_chunks}

Question: {user_question}

Answer based on the context above:
```

### 6. Knowledge Graph System

#### Architecture
```
Documents → spaCy NER → Concepts → NetworkX Graph → Visualization
```

#### Components

**Phase 1: Core Extraction** (src/knowledge_graph.py)
- **Tool**: spaCy (en_core_web_sm)
- **Extraction**: Named entities, noun chunks
- **Graph**: NetworkX DiGraph
- **Metrics**: Centrality, clustering, pagerank

**Phase 2: Interactive Visualization**
- **Tool**: pyvis
- **Output**: HTML with force-directed layout
- **Interactivity**: Zoom, pan, node selection
- **Physics**: Spring layout for clusters

**Phase 3: Semantic Flow Analysis**
- **Analysis**: Chunk-by-chunk concept evolution
- **Metrics**: Concept introduction/continuation
- **Visualization**: Flow diagrams, heatmaps

**Phase 4: AI-Enhanced Progression**
- **LLM**: Ollama for concept analysis
- **Output**: Logical progression summaries
- **Features**: Concept relationships, importance scoring

## Data Flow

### Document Indexing Flow
```
1. User uploads document(s)
   ↓
2. FileLoader reads content
   ↓
3. SemanticChunker splits into chunks
   ↓
4. Embedder generates vectors (384-dim)
   ↓
5. VectorStore stores in FAISS index
   ↓
6. Ready for queries
```

### Query Flow
```
1. User asks question
   ↓
2. Question embedded (384-dim)
   ↓
3. FAISS similarity search
   ↓
4. Top-k chunks retrieved
   ↓
5. Chunks + Question → Prompt
   ↓
6. Ollama generates answer
   ↓
7. Answer returned to user
```

### Knowledge Graph Flow
```
1. Documents loaded
   ↓
2. spaCy extracts entities
   ↓
3. NetworkX builds graph
   ↓
4. Metrics calculated
   ↓
5. pyvis generates visualization
   ↓
6. (Optional) LLM analyzes concepts
   ↓
7. Interactive HTML displayed
```

## Design Decisions

### Why Synchronous?
- **Simplicity**: Easier to understand and debug
- **Local-first**: No network complexity
- **Direct control**: Immediate feedback
- **Target audience**: Individual users, development

### Why In-Memory Storage?
- **Speed**: No I/O overhead
- **Simplicity**: No database management
- **Stateless**: Each run is fresh
- **Trade-off**: Data not persisted

### Why FAISS?
- **Performance**: Optimized for similarity search
- **Maturity**: Battle-tested by Facebook
- **Python-friendly**: Easy integration
- **Scale**: Handles millions of vectors

### Why Ollama?
- **Local**: Privacy-first
- **Free**: No API costs
- **Easy**: Simple HTTP API
- **Flexible**: Many models available

## Performance Characteristics

### Indexing Performance
- **Small docs** (<10): <5 seconds
- **Medium** (10-100): 10-30 seconds
- **Large** (100+): 1-5 minutes

**Bottlenecks:**
- Embedding generation (GPU helps)
- File parsing (PDF slowest)

### Query Performance
- **Embedding**: 10-50ms
- **Vector search**: 1-10ms (FAISS)
- **LLM generation**: 1-5s (depends on model)
- **Total**: 1-5s per query

### Memory Usage
- **Base**: ~500MB (Python + libraries)
- **Per 1000 chunks**: ~50MB (vectors + text)
- **spaCy model**: ~100MB
- **Ollama model**: 2-4GB (separate process)

## Scalability Limits

### Current Limitations
- **Concurrency**: Single user only
- **Persistence**: In-memory (no disk)
- **Documents**: Practical limit ~1000
- **Vectors**: FAISS scales to millions, but memory limited

### When to Upgrade to V2
Use V2 if you need:
- Multiple concurrent users
- Persistent storage
- Background processing
- API access
- Horizontal scaling
- Production deployment

## Technology Stack

### Core
- **Python**: 3.10+
- **Streamlit**: 1.x (UI)
- **FastAPI**: Not used (V2 only)

### NLP/ML
- **sentence-transformers**: Embeddings
- **FAISS**: Vector similarity
- **spaCy**: NER and NLP
- **NetworkX**: Graph analysis
- **pyvis**: Graph visualization

### LLM
- **Ollama**: Primary (local)
- **Anthropic SDK**: Optional (Claude)
- **Google GenAI**: Optional (Gemini)

### Utilities
- **pypdf**: PDF parsing
- **python-docx**: DOCX parsing
- **beautifulsoup4**: HTML parsing
- **matplotlib**: Plotting
- **numpy**: Numerical operations

## File Structure

```
DataDistillerAI/
├── app.py                    # Streamlit UI
├── cli.py                    # CLI interface
├── src/
│   ├── workflows_ollama.py   # RAG orchestrator
│   ├── ingestion/            # File loaders
│   ├── processing/
│   │   └── chunker.py        # Semantic chunking
│   ├── retrieval/
│   │   └── __init__.py       # Vector store
│   ├── llm/
│   │   └── llm_ollama.py     # Ollama integration
│   └── knowledge_graph.py    # KG features
├── data/
│   ├── documents/            # Input documents
│   └── vector_store/         # FAISS index (runtime)
└── tests_v1/                 # Tests
```

## Extension Points

### Add New File Format
1. Create loader in `src/ingestion/`
2. Implement `load()` method
3. Register in workflow

### Change Embedding Model
Edit `src/retrieval/__init__.py`:
```python
self.model_name = "your-model-name"
```

### Add New LLM Backend
1. Create `src/llm/llm_yourllm.py`
2. Create `src/workflows_yourllm.py`
3. Update UI to support new backend

### Customize Prompt
Edit `src/workflows_ollama.py`:
```python
def _create_prompt(self, question, context):
    return f"Your custom template here"
```

## Security Considerations

### Local-Only
- All data stays on local machine
- No external API calls (except optional Claude/Gemini)
- No authentication needed

### File Uploads
- Basic validation by extension
- No virus scanning
- Trust your input sources

### Production Warnings
⚠️ V1 is NOT production-ready:
- No authentication
- No rate limiting
- No input sanitization
- In-memory only (data loss on restart)

For production, use V2.

## Related Documentation

- [Setup Guide](V1_SETUP.md)
- [README](../README_V1.md)
- [Knowledge Graph Guide](../KNOWLEDGE_GRAPH_GUIDE.md)
- [V2 Architecture](V2_ARCHITECTURE.md) for comparison
