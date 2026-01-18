# UI Integration Guide - DataDistiller 1.0 & 2.0

## Overview
The UI now supports **both** DataDistiller 1.0 and 2.0 architectures!

## Running the Hybrid UI

### Start the UI
```bash
streamlit run app_hybrid.py
```

Access at: **http://localhost:8501**

## Two Modes Available

### 🚀 Mode 1: DataDistiller 2.0 (Async API)
**Requirements:** API server + workers must be running

**Features:**
- ✅ Async document uploads (returns immediately)
- ✅ Background processing with status tracking
- ✅ Job monitoring dashboard
- ✅ Scalable architecture
- ✅ Production-ready

**How it works:**
1. Upload files → Sent to API (port 8000)
2. Workers process in background
3. Track job status in real-time
4. Query indexed documents

**To enable:**
1. Ensure Docker services are running: `docker compose ps`
2. Start API: `PYTHONPATH=/Users/gokulsreekumar/DataDistillerAI .venv/bin/python api/main.py`
3. Start workers (ingestion + embedding)
4. UI will auto-detect and show "2.0 Async API" option

### 💻 Mode 2: DataDistiller 1.0 (Direct Pipeline)
**Requirements:** Just Ollama

**Features:**
- ✅ Direct Ollama integration
- ✅ Knowledge Graph visualization
- ✅ Interactive network graphs
- ✅ Semantic flow analysis
- ✅ AI-enhanced concept progression
- ✅ Instant indexing (synchronous)

**How it works:**
1. Upload files → Processed immediately
2. Blocks UI during indexing
3. Knowledge Graph tab available
4. Query with local FAISS

**To enable:**
- No API needed
- Just start Ollama: `ollama serve`
- UI runs standalone

## Feature Comparison

| Feature | 1.0 Direct | 2.0 Async API |
|---------|------------|---------------|
| Document Upload | Sync (blocks) | Async (instant) |
| Processing | Immediate | Background workers |
| Job Tracking | No | Yes (real-time) |
| Knowledge Graph | ✅ Yes | ❌ Not yet |
| Scalability | Single instance | Multi-worker |
| Production Ready | Dev/Testing | Yes |
| Setup Complexity | Low | High |

## Current Setup Status

### Running Services:
✅ Docker infrastructure (7 services)
✅ FastAPI server (port 8000)
✅ Ingestion worker
✅ Embedding worker (should be running)
✅ Streamlit UI (port 8501)

### Available Modes:
- **2.0 Async API** - Fully operational
- **1.0 Direct** - Also works (switch in UI)

## Usage Examples

### Example 1: Use 2.0 for Production Uploads
1. Open http://localhost:8501
2. Select "🚀 2.0 Async API" in sidebar
3. Go to "📊 Documents" tab
4. Upload files → Get job IDs immediately
5. Monitor "Processing Jobs" section
6. Query when status = "completed"

### Example 2: Use 1.0 for Knowledge Graph
1. Open http://localhost:8501
2. Select "💻 1.0 Direct Pipeline" in sidebar
3. Go to "🧠 Knowledge Graph" tab
4. Explore:
   - Network visualization
   - Concept statistics
   - Semantic flow
   - AI-enhanced progression

### Example 3: Switch Between Modes
- No restart needed
- Just select different mode in sidebar
- UI adapts automatically

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│         Streamlit UI (port 8501)        │
│              app_hybrid.py              │
└─────────────┬───────────────────────────┘
              │
      ┌───────┴────────┐
      │                │
      ▼                ▼
┌──────────┐    ┌─────────────────┐
│ 1.0 Mode │    │    2.0 Mode     │
│  Direct  │    │   API Client    │
└─────┬────┘    └────────┬────────┘
      │                  │
      │                  ▼
      │         ┌────────────────┐
      │         │  FastAPI :8000 │
      │         └────────┬───────┘
      │                  │
      ▼                  ▼
┌──────────────┐  ┌──────────────────┐
│   Ollama     │  │ Kafka + Workers  │
│ FAISS Local  │  │ MinIO + Postgres │
└──────────────┘  └──────────────────┘
```

## Next Steps

### To keep both modes working:
1. **Keep running:** API + Workers + Docker
2. **Access UI:** http://localhost:8501
3. **Switch modes:** Use sidebar radio button

### To use only 1.0 (simpler):
1. Stop API and workers (Ctrl+C)
2. Stop Docker: `docker compose down`
3. Keep only: Ollama + Streamlit
4. UI auto-switches to 1.0 mode

### To use only 2.0:
1. Keep all services running
2. Use 2.0 mode in UI
3. Knowledge Graph not available (planned for Phase 4+)

## Troubleshooting

### "API not detected"
- Check: `curl http://localhost:8000/health`
- Start API if needed
- UI will work in 1.0 mode regardless

### "Knowledge Graph not available in 2.0"
- This is expected
- Switch to 1.0 mode to access KG features
- Or wait for Phase 4+ integration

### Upload fails in 2.0 mode
- Check workers are running: `python status.py`
- Check Docker services: `docker compose ps`
- View logs: `docker compose logs -f`

## Summary

✅ **UI works with both architectures!**
- **2.0:** Production async uploads + query
- **1.0:** Knowledge Graph + direct access

Choose mode based on needs:
- **Development/Analysis:** Use 1.0 for KG features
- **Production/Scale:** Use 2.0 for async processing
- **Both:** Run all services, switch as needed

Access the UI now at: **http://localhost:8501**
