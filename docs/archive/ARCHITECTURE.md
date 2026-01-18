"""Architecture and System Design Documentation."""

# DataDistillerAI - Architecture & Design

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│              (CLI, Web, API, Jupyter)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   RAG PIPELINE                              │
│         (Orchestration & Workflow Management)               │
└────┬────────────────┬────────────────────┬─────────────────┘
     │                │                    │
     ▼                ▼                    ▼
┌─────────────┐ ┌──────────────┐ ┌──────────────┐
│ INGESTION   │ │ PROCESSING   │ │ RETRIEVAL    │
├─────────────┤ ├──────────────┤ ├──────────────┤
│ • Loaders   │ │ • Cleaner    │ │ • Embedding  │
│ • Parsers   │ │ • Chunker    │ │ • VectorDB   │
│ • Formats   │ │ • Normalizer │ │ • Search     │
└──────┬──────┘ └──────┬───────┘ └──────┬───────┘
       │               │                │
       └───────────────┬────────────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │   Data Storage      │
            ├─────────────────────┤
            │ • Vector Index      │
            │ • Document Cache    │
            │ • Metadata          │
            └────────────┬────────┘
                         │
                         │
            ┌────────────▼─────────────┐
            │  RETRIEVAL AUGMENTATION  │
            ├──────────────────────────┤
            │ Context Formatting       │
            │ Relevance Scoring        │
            │ Result Ranking           │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   LLM INTEGRATION      │
            ├────────────────────────┤
            │ • OpenAI Client        │
            │ • Prompt Templates     │
            │ • Response Generation  │
            │ • Token Management     │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Final Response       │
            │   (Grounded in Data)   │
            └────────────────────────┘
```

## Data Flow

```
Document Input
     │
     ▼
┌─────────────────────────────────────┐
│    1. LOAD & PARSE                  │
│ Detect format → Extract text        │
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │ Raw Text               │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    2. CLEAN & NORMALIZE            │
        │ Remove noise, standardize format   │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    3. CHUNK SEMANTICALLY           │
        │ Preserve meaning, manage size      │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    4. GENERATE EMBEDDINGS          │
        │ Vector representation of chunks    │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    5. INDEX IN VECTOR DATABASE     │
        │ FAISS for fast similarity search   │
        └────────────┬───────────────────────┘
                     │
                     ▼
            ┌───────────────────┐
            │ Vector Index      │
            │ Ready for Queries │
            └───────────────────┘

DURING INFERENCE:
     │
     ▼
Query Input
     │
     ▼
┌─────────────────────────────────────┐
│   1. EMBED QUERY                    │
│   Use same embedding model          │
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │ Query Vector           │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    2. SIMILARITY SEARCH            │
        │ Find top-k most similar chunks     │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    3. FORMAT CONTEXT               │
        │ Prepare retrieved chunks for LLM   │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    4. BUILD PROMPT                 │
        │ Combine context + query + rules    │
        └────────────┬───────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────┐
        │    5. LLM GENERATION               │
        │ Generate grounded response         │
        └────────────┬───────────────────────┘
                     │
                     ▼
            ┌───────────────────┐
            │ Final Answer      │
            │ (Grounded in Data)│
            └───────────────────┘
```

## Component Interactions

### 1. Ingestion → Processing
```python
# DocumentLoader extracts text
doc = loader.load("file.pdf")
# SemanticChunker breaks into pieces
chunks = chunker.chunk(doc.content, metadata=doc.metadata)
```

### 2. Processing → Retrieval
```python
# Chunks are vectorized and indexed
vector_store.add_documents(chunks)
# Stored with original content and metadata
```

### 3. Retrieval → LLM
```python
# Retrieved chunks formatted as context
results = vector_store.search(query, top_k=5)
# Context inserted into prompt template
prompt = RAG_PROMPT.format(context=context, question=query)
```

### 4. LLM → Response
```python
# LLM generates answer grounded in retrieved context
response = llm.generate(prompt, system_prompt=SYSTEM_PROMPTS["qa"])
```

## Key Design Decisions

### 1. Modular Architecture
- **Benefit**: Each component can be upgraded/replaced independently
- **Example**: Swap embedding model without changing other components

### 2. Separation of Concerns
- **Deterministic** (Loading, Chunking, Embedding): Reproducible results
- **Probabilistic** (LLM): Creative/adaptive responses
- **Benefit**: Easy debugging and optimization

### 3. Vector-First Retrieval
- **Why FAISS**: Fast approximate similarity search at scale
- **Why embeddings**: Semantic understanding vs. keyword matching
- **Benefit**: Retrieves relevant context accurately

### 4. Prompt Templates
- **Flexibility**: Easy to customize for different tasks
- **Consistency**: Ensures predictable LLM behavior
- **Extensibility**: Add new templates for new workflows

### 5. Metadata Preservation
- **Track**: Source document, chunk index, processing info
- **Use**: Answer attribution, source citation
- **Benefit**: Transparency and auditability

## Performance Characteristics

### Memory Usage
- **Vector Index**: ~1KB per chunk (for small embeddings)
- **Document Cache**: Full text of all documents
- **Optimization**: Use smaller embedding models for large corpora

### Latency
- **Embedding**: 1-10ms per chunk (batch)
- **Search**: 5-50ms for top-k (FAISS is very fast)
- **LLM**: 1-30s depending on response length
- **Total**: ~30s for typical query

### Scalability
- **Documents**: Thousands to millions (limited by storage)
- **Chunks**: Millions (FAISS handles billions)
- **Queries**: Limited by LLM rate limits, not retrieval

## Extension Points

### 1. Add New Document Format
```python
class DocumentLoader:
    def _load_custom(self, file_path: str) -> str:
        # Parse custom format
        return text
    
    self.loaders['.custom'] = self._load_custom
```

### 2. Add New Chunking Strategy
```python
class SlidingWindowChunker(SemanticChunker):
    def chunk(self, text: str) -> List[Chunk]:
        # Fixed-size sliding window
        pass
```

### 3. Add New Retrieval Method
```python
class HybridRetriever:
    def search(self, query: str):
        # Combine semantic + keyword search
        pass
```

### 4. Add New LLM Backend
```python
class LlamaClient(LLMClient):
    def _init_client(self):
        # Use local Llama model
        pass
```

### 5. Add New Workflow
```python
class ResearchWorkflow:
    def __init__(self, pipeline):
        self.pipeline = pipeline
    
    def multi_turn_analysis(self, questions):
        # Maintain conversation context
        pass
```

## Security Considerations

1. **API Keys**: Never commit `.env` file with secrets
2. **Input Validation**: Validate all file paths and user input
3. **Data Privacy**: Ensure documents don't contain sensitive info
4. **Rate Limiting**: Implement throttling for API calls
5. **Error Messages**: Don't expose sensitive info in errors

## Future Enhancements

### Short-term (Easy)
- [ ] Streaming responses for long answers
- [ ] Query caching to reduce API calls
- [ ] Better error handling and recovery
- [ ] More prompt templates for specific domains

### Medium-term (Moderate)
- [ ] Multi-modal support (images, tables)
- [ ] Fine-tuning support for custom models
- [ ] Custom vector database backends
- [ ] Query expansion and rewriting

### Long-term (Complex)
- [ ] Distributed processing for massive corpora
- [ ] Real-time document indexing
- [ ] Multi-language support
- [ ] Automatic hyperparameter tuning
- [ ] Explainability and interpretability tools
