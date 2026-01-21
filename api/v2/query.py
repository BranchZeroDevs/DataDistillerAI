"""
Query handler - executes document queries
"""

import logging
from typing import Dict, List
from src.workflows_ollama import RAGPipelineOllama
from src.retrieval.hybrid_retriever import HybridRetriever

logger = logging.getLogger(__name__)

# Lazy load RAG pipeline
_pipeline = None
_retriever = None

def get_rag_pipeline():
    """Get or create RAG pipeline"""
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipelineOllama()
        logger.info("✅ RAG pipeline initialized")
    return _pipeline


def get_retriever():
    """Get or create hybrid retriever tied to vector store"""
    global _retriever
    pipeline = get_rag_pipeline()
    if _retriever is None or _retriever.vector_store is not pipeline.vector_store:
        _retriever = HybridRetriever(pipeline.vector_store)
    return _retriever


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
        retriever = get_retriever()

        retrieval_method = (retrieval_method or "dense").lower()

        if retrieval_method == "sparse":
            results = retriever.sparse_search(query, top_k=top_k)
        elif retrieval_method == "hybrid":
            results = retriever.hybrid_search(query, top_k=top_k)
        else:
            results = retriever.dense_search(query, top_k=top_k)

        if not results:
            return {
                'answer': "No relevant information found in documents.",
                'sources': []
            }

        # Build context for answer
        context = "\n\n".join([
            f"[Chunk {i+1}] {content}"
            for i, (content, metadata, score) in enumerate(results)
        ])

        answer = pipeline.llm_client.query_with_context(
            question=query,
            context=context,
            top_k_results=top_k
        )
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
