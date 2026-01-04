"""Vector database and retrieval operations."""

from typing import List, Tuple, Dict, Any
import logging
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """Wrapper for embedding generation."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize embedding model."""
        self.model_name = model_name
        self.model = self._load_model()
    
    def _load_model(self):
        """Load embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer(self.model_name)
        except ImportError:
            raise ImportError("sentence-transformers not installed. Use: pip install sentence-transformers")
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings."""
        return self.model.encode(texts, convert_to_numpy=True)


class VectorStore:
    """FAISS-based vector database for efficient similarity search."""
    
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize vector store.
        
        Args:
            embedding_model: Name of embedding model to use
        """
        self.embedding_model = EmbeddingModel(embedding_model)
        self.index = None
        self.documents = {}
        self.document_count = 0
    
    def add_documents(self, chunks: List[Any]) -> None:
        """
        Add chunks to vector store.
        
        Args:
            chunks: List of Chunk objects with content and metadata
        """
        if not chunks:
            logger.warning("No chunks to add")
            return
        
        # Extract texts and create embeddings
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_model.encode(texts)
        
        # Initialize FAISS index if needed
        if self.index is None:
            self._init_index(embeddings.shape[1])
        
        # Add to index
        self.index.add(embeddings.astype('float32'))
        
        # Store metadata
        for i, chunk in enumerate(chunks):
            doc_id = self.document_count + i
            self.documents[doc_id] = {
                'content': chunk.content,
                'metadata': chunk.metadata,
            }
        
        self.document_count += len(chunks)
        logger.info(f"Added {len(chunks)} chunks to vector store")
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Search for similar documents.
        
        Args:
            query: Query text
            top_k: Number of results to return
        
        Returns:
            List of (content, metadata, score) tuples
        """
        if self.index is None or self.document_count == 0:
            logger.warning("Vector store is empty")
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Search index
        distances, indices = self.index.search(query_embedding.astype('float32').reshape(1, -1), top_k)
        
        # Format results
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx >= 0:  # FAISS returns -1 for invalid indices
                doc = self.documents.get(idx)
                if doc:
                    # Convert distance to similarity score (L2 distance to cosine-like similarity)
                    similarity = 1 / (1 + distance)
                    results.append((doc['content'], doc['metadata'], similarity))
        
        logger.info(f"Found {len(results)} similar documents for query")
        return results
    
    def _init_index(self, dimension: int) -> None:
        """Initialize FAISS index."""
        try:
            import faiss
            self.index = faiss.IndexFlatL2(dimension)
        except ImportError:
            raise ImportError("faiss-cpu not installed. Use: pip install faiss-cpu")
    
    def save(self, path: str) -> None:
        """Save vector store to disk."""
        import pickle
        import json
        
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        try:
            import faiss
            faiss.write_index(self.index, str(path / "index.faiss"))
        except ImportError:
            raise ImportError("faiss-cpu not installed")
        
        with open(path / "documents.json", 'w') as f:
            json.dump(self.documents, f)
        
        logger.info(f"Saved vector store to {path}")
    
    def load(self, path: str) -> None:
        """Load vector store from disk."""
        import json
        
        path = Path(path)
        
        try:
            import faiss
            self.index = faiss.read_index(str(path / "index.faiss"))
        except ImportError:
            raise ImportError("faiss-cpu not installed")
        
        with open(path / "documents.json", 'r') as f:
            self.documents = json.load(f)
            self.document_count = len(self.documents)
        
        logger.info(f"Loaded vector store from {path}")
