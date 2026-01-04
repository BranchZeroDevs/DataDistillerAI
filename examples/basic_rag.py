"""Basic RAG pipeline example."""

import logging
from pathlib import Path
from src.workflows import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run basic RAG example."""
    # Initialize pipeline
    pipeline = RAGPipeline(
        document_path="./data/documents",
        vector_db_path="./data/vector_store"
    )
    
    # Index documents (if not already indexed)
    logger.info("Indexing documents...")
    pipeline.index_documents()
    
    # Example query
    query = "What is the main topic of the documents?"
    logger.info(f"Query: {query}")
    
    response = pipeline.query(query, top_k=3)
    logger.info(f"Response:\n{response}")
    
    # Example summarization
    logger.info("Generating summary...")
    summary = pipeline.summarize()
    logger.info(f"Summary:\n{summary}")


if __name__ == "__main__":
    main()
