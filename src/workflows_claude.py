"""
RAG Pipeline with Anthropic Claude
"""

import logging
from pathlib import Path
from typing import Optional, List

# Import components
from src.ingestion import DocumentLoader
from src.processing.chunker import SemanticChunker
from src.retrieval import VectorStore

logger = logging.getLogger(__name__)


class RAGPipelineClaude:
    """
    RAG Pipeline using Claude (cloud-based, professional quality)
    
    Usage:
        pipeline = RAGPipelineClaude(document_path="./data/documents")
        pipeline.index_documents()
        answer = pipeline.query("What is machine learning?")
    """
    
    def __init__(
        self,
        document_path: str = "./data/documents",
        vector_store_path: str = "./data/vector_store",
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        model: str = "claude-3-5-haiku-20241022"
    ):
        """
        Initialize RAG pipeline with Claude
        
        Args:
            document_path: Path to documents directory
            vector_store_path: Path to save/load vector store
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            model: Claude model to use (default: claude-3-5-sonnet - best balance)
        """
        self.document_path = Path(document_path)
        self.vector_store_path = Path(vector_store_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = model
        
        # Initialize components
        self.loader = DocumentLoader()
        self.chunker = SemanticChunker(
            chunk_size=chunk_size,
            overlap=chunk_overlap
        )
        self.vector_store = VectorStore()
        
        # Lazy load LLM client
        self._llm_client = None
        
        logger.info(f"Initialized RAG Pipeline with Claude ({model})")
    
    @property
    def llm_client(self):
        """Lazy load Claude client"""
        if self._llm_client is None:
            try:
                from src.llm_claude import ClaudeClient
                self._llm_client = ClaudeClient(model=self.model)
            except Exception as e:
                logger.error(f"Failed to initialize Claude: {e}")
                raise
        return self._llm_client
    
    def index_documents(self) -> int:
        """
        Index all documents in the document directory
        
        Returns:
            Number of chunks created
        """
        logger.info(f"Loading documents from {self.document_path}")
        
        # Load documents
        documents = self.loader.load_directory(str(self.document_path))
        if not documents:
            logger.warning(f"No documents found in {self.document_path}")
            return 0
        
        logger.info(f"Loaded {len(documents)} documents")
        
        # Chunk documents
        all_chunks = []
        for doc in documents:
            chunks = self.chunker.chunk(
                doc.content,
                metadata=doc.metadata
            )
            all_chunks.extend(chunks)
        
        logger.info(f"Created {len(all_chunks)} semantic chunks")
        
        # Index chunks
        self.vector_store.add_documents(all_chunks)
        logger.info(f"Indexed {len(all_chunks)} chunks in vector store")
        
        # Save vector store
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        self.vector_store.save(str(self.vector_store_path))
        logger.info(f"Saved vector store to {self.vector_store_path}")
        
        return len(all_chunks)
    
    def query(self, question: str, top_k: int = 3) -> str:
        """
        Query the RAG system with a question
        
        Args:
            question: User question
            top_k: Number of relevant chunks to retrieve
        
        Returns:
            Generated answer grounded in documents
        """
        logger.info(f"Processing query: {question}")
        
        # Retrieve relevant chunks
        results = self.vector_store.search(question, top_k=top_k)
        
        if not results:
            return "No relevant information found in documents."
        
        # Build context from retrieved chunks
        context = "\n\n".join([
            f"[Chunk {i+1}] {content}"
            for i, (content, metadata, score) in enumerate(results)
        ])
        
        logger.info(f"Retrieved {len(results)} relevant chunks")
        
        try:
            # Generate answer using Claude
            answer = self.llm_client.query_with_context(
                question=question,
                context=context,
                top_k_results=top_k
            )
            return answer
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"Error generating response: {e}"
    
    def summarize(self) -> str:
        """
        Summarize all indexed documents
        
        Returns:
            Summary of documents
        """
        logger.info("Summarizing indexed documents")
        
        # Get all chunks
        all_chunks = self.vector_store.get_all_documents()
        if not all_chunks:
            return "No documents to summarize."
        
        # Combine all chunks
        full_text = "\n\n".join([chunk.content for chunk in all_chunks])
        
        try:
            # Summarize using Claude
            summary = self.llm_client.summarize(full_text)
            return summary
        except Exception as e:
            logger.error(f"Error summarizing: {e}")
            return f"Error generating summary: {e}"


# For backward compatibility
RAGPipeline = RAGPipelineClaude

__all__ = ['RAGPipelineClaude', 'RAGPipeline']
