"""
Quick Start Example - DataDistiller AI
======================================

This example shows how to use DataDistiller in just a few lines of code.
"""

from pathlib import Path
from src.workflows_ollama import RAGPipelineOllama
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def quick_start():
    """Minimal example to get started with DataDistiller."""
    
    # 1. Initialize the RAG pipeline
    logger.info("Initializing RAG pipeline...")
    pipeline = RAGPipelineOllama(
        document_path="./data/documents",
        vector_db_path="./data/vector_store"
    )
    
    # 2. Index your documents (one-time operation)
    logger.info("Indexing documents...")
    pipeline.index_documents()
    logger.info(f"✓ Indexed documents from {pipeline.document_path}")
    
    # 3. Ask questions!
    queries = [
        "What are the main topics discussed?",
        "Can you summarize the key points?",
        "What are the most important concepts?"
    ]
    
    for query in queries:
        logger.info(f"\n{'='*60}")
        logger.info(f"Q: {query}")
        logger.info(f"{'='*60}")
        
        response = pipeline.query(query, top_k=3)
        print(f"\nA: {response}\n")
    
    # 4. Generate a summary
    logger.info("\n" + "="*60)
    logger.info("Generating document summary...")
    logger.info("="*60)
    
    summary = pipeline.summarize()
    print(f"\nSummary:\n{summary}")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         DataDistiller AI - Quick Start Example          ║
    ║                                                          ║
    ║  Make sure you have:                                     ║
    ║  1. Ollama running: `ollama serve`                       ║
    ║  2. A model downloaded: `ollama pull qwen2.5:3b`         ║
    ║  3. Documents in ./data/documents/                       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        quick_start()
        print("\n✅ Success! DataDistiller is working correctly.")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        logger.error("Please check that Ollama is running and you have documents in ./data/documents/")
