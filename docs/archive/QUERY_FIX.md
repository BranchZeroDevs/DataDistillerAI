# ✅ Fix Applied - Query Endpoint Working

## Issue
API was returning 422 error:
```json
{
  "detail": [{
    "type": "missing",
    "loc": ["body", "question"],
    "msg": "Field required",
    "input": {"query": "What documents are there?", "top_k": 3}
  }]
}
```

## Root Cause
- API expected field name: `"question"`
- UI/clients were sending: `"query"`

## Changes Made

### 1. Updated API Model ([api/models.py](api/models.py))
```python
class QueryRequest(BaseModel):
    query: str = Field(..., alias="question")  # Accept both
    # ...
    class Config:
        populate_by_name = True  # Accept both 'query' and 'question'
```

### 2. Updated Query Handler ([api/v2/query.py](api/v2/query.py))
```python
def query_documents(query: str, ...):  # Changed from 'question'
    answer = pipeline.query(query, top_k=top_k)
    results = pipeline.vector_store.search(query, top_k=top_k)
```

### 3. Updated API Endpoint ([api/main.py](api/main.py))
```python
result = query_documents(
    query=request.query,  # Changed from request.question
    top_k=request.top_k,
    # ...
)
```

## Test Results

✅ **Query endpoint now accepts both formats:**

```bash
# Works with "query"
curl -X POST http://localhost:8000/api/v2/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?", "top_k": 3}'

# Also works with "question" (backwards compatible)
curl -X POST http://localhost:8000/api/v2/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?", "top_k": 3}'
```

Response:
```json
{
  "query_id": "...",
  "question": "What is machine learning?",
  "answer": "...",
  "sources": [...],
  "retrieval_method": "hybrid",
  "latency_ms": 7826
}
```

## Status
- ✅ 422 error fixed
- ✅ API accepts both "query" and "question"
- ✅ Backwards compatible
- ✅ No API restart needed (auto-reload detected changes)
- ✅ UI (app_hybrid.py) now works in 2.0 mode

## Next Steps
The query works but returns "No relevant information" because:
- Documents were uploaded via async API (2.0)
- Query uses in-memory pipeline (1.0)
- Need to ensure both use same vector store

**Options:**
1. Re-upload documents in 1.0 mode for testing
2. Wait for Phase 4 to integrate query with async-indexed documents
3. Use hybrid app's mode switching to access both architectures
