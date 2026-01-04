"""Core RAG pipeline implementation."""

import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Complete retrieval-augmented generation pipeline."""
    
    def __init__(
        self,
        document_path: str = None,
        vector_db_path: str = "./data/vector_store",
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "gpt-3.5-turbo",
        api_key: str = None,
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            document_path: Path to documents directory or file
            vector_db_path: Path to vector database
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            embedding_model: Embedding model name
            llm_model: LLM model name
            api_key: OpenAI API key
        """
        self.document_path = document_path
        self.vector_db_path = vector_db_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Import here to avoid circular dependencies
        from src.ingestion.loaders import DocumentLoader
        from src.processing.chunker import SemanticChunker
        from src.retrieval import VectorStore
        from src.llm import LLMClient
        
        self.loader = DocumentLoader()
        self.chunker = SemanticChunker(chunk_size, chunk_overlap)
        self.vector_store = VectorStore(embedding_model)
        self.llm = LLMClient(api_key=api_key, model=llm_model)
    
    def index_documents(self) -> None:
        """Load, chunk, and index documents."""
        if not self.document_path:
            logger.warning("No document path specified")
            return
        
        path = Path(self.document_path)
        
        # Load documents
        if path.is_file():
            documents = [self.loader.load(str(path))]
        else:
            documents = self.loader.load_directory(str(path))
        
        # Chunk documents
        all_chunks = []
        for doc in documents:
            metadata = doc.metadata.copy()
            chunks = self.chunker.chunk(doc.content, metadata)
            all_chunks.extend(chunks)
        
        # Add to vector store
        self.vector_store.add_documents(all_chunks)
        
        # Save vector store
        Path(self.vector_db_path).mkdir(parents=True, exist_ok=True)
        self.vector_store.save(self.vector_db_path)
    
    def query(self, question: str, top_k: int = 3) -> str:
        """
        Query the knowledge base.
        
        Args:
            question: User question
            top_k: Number of relevant chunks to retrieve
        
        Returns:
            Generated answer grounded in source documents
        """
        # Retrieve relevant chunks
        results = self.vector_store.search(question, top_k=top_k)
        
        if not results:
            return "No relevant documents found."
        
        # Format context from retrieved chunks
        context_parts = []
        for content, metadata, score in results:
            source = metadata.get('source', 'Unknown')
            context_parts.append(f"[{source}]\n{content}\n")
        
        context = "\n---\n".join(context_parts)
        
        # Generate answer using LLM
        from src.llm import RAG_PROMPT, SYSTEM_PROMPTS
        
        prompt = RAG_PROMPT.format(context=context, question=question)
        
        try:
            answer = self.llm.generate(prompt, system_prompt=SYSTEM_PROMPTS["qa"])
            return answer
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "Error generating response."
    
    def summarize(self, document_path: str = None) -> str:
        """
        Summarize a document.
        
        Args:
            document_path: Path to document (uses indexed docs if None)
        
        Returns:
            Generated summary
        """
        if document_path:
            doc = self.loader.load(document_path)
            text = doc.content
        else:
            # Use all chunks from vector store
            text = "\n".join(doc['content'] for doc in self.vector_store.documents.values())
        
        from src.llm import SUMMARIZATION_PROMPT, SYSTEM_PROMPTS
        
        # Truncate if too long
        if len(text) > 4000:
            text = text[:4000]
        
        prompt = SUMMARIZATION_PROMPT.format(document=text)
        
        try:
            summary = self.llm.generate(prompt, system_prompt=SYSTEM_PROMPTS["summarization"])
            return summary
        except Exception as e:
            logger.error(f"Error summarizing: {e}")
            return "Error generating summary."
