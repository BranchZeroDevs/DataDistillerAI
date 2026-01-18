"""
Query handler - executes document queries
"""

import logging
from typing import Dict, List
from src.workflows_ollama import RAGPipelineOllama

logger = logging.getLogger(__name__)

# Lazy load RAG pipeline
_pipeline = None

def get_rag_pipeline():
    """Get or create RAG pipeline"""
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipelineOllama()
        logger.info("✅ RAG pipeline initialized")
    return _pipeline


def query_documents(query: str, top_k: int = 3, retrieval_method: str = "dense") -> Dict:
    """
    Query indexed documents
    
    Args:
        query: User question
        top_k: Number of results
        retrieval_method: dense, sparse, or hybrid
        
    Returns:
        Dict with answer and sources
    """
    try:
        pipeline = get_rag_pipeline()
        
        # For now, use dense retrieval (existing implementation)
        # TODO: Implement sparse and hybrid retrieval in Phase 4
        
        answer = pipeline.query(query, top_k=top_k)
        
        # Get sources
        results = pipeline.vector_store.search(query, top_k=top_k)
        sources = [
            {
                'content': content[:200] + "..." if len(content) > 200 else content,
                'score': float(score),
                'metadata': metadata
            }
            for content, metadata, score in results
        ]
        
        return {
            'answer': answer,
            'sources': sources
        }
    
    except Exception as e:
        logger.error(f"❌ Query failed: {e}")
        raise
