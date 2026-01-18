#!/bin/bash
# Quick launch script for Phase 2 & 3

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       DataDistiller 2.0 - Phase 2 & 3 Launcher              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running inside tmux/screen
if [ -n "$TMUX" ] || [ -n "$STY" ]; then
    echo "⚠️  Running inside tmux/screen. Will launch in new panes."
    
    # Launch in tmux panes
    tmux split-window -h "cd $PWD && source .venv/bin/activate && python api/main.py"
    tmux split-window -v "cd $PWD && source .venv/bin/activate && python workers/ingestion_worker.py"
    tmux split-window -v "cd $PWD && source .venv/bin/activate && python workers/embedding_worker.py"
    
    echo "✅ Launched in tmux panes"
else
    echo "📋 Manual Launch Instructions:"
    echo ""
    echo "Terminal 1 - API Server:"
    echo "  source .venv/bin/activate && python api/main.py"
    echo ""
    echo "Terminal 2 - Ingestion Worker:"
    echo "  source .venv/bin/activate && python workers/ingestion_worker.py"
    echo ""
    echo "Terminal 3 - Embedding Worker:"
    echo "  source .venv/bin/activate && python workers/embedding_worker.py"
    echo ""
    echo "Terminal 4 (Optional) - Second Embedding Worker:"
    echo "  source .venv/bin/activate && WORKER_ID=embedding-worker-2 python workers/embedding_worker.py"
    echo ""
    echo "Terminal 5 - Run Test:"
    echo "  source .venv/bin/activate && python test_phase2_3.py"
    echo ""
    echo "🌐 Web UIs:"
    echo "  • API Docs:  http://localhost:8000/docs"
    echo "  • Kafka UI:  http://localhost:9000"
    echo "  • MinIO:     http://localhost:9001"
    echo ""
fi

echo ""
echo "📖 Full guide: cat PHASE2_3_SETUP.md"
echo ""
