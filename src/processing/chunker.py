"""Semantic and fixed-size text chunking."""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Chunk:
    """Represents a text chunk with metadata."""
    
    def __init__(self, content: str, metadata: Dict[str, Any], chunk_id: str = None):
        self.content = content
        self.metadata = metadata
        self.chunk_id = chunk_id or f"chunk_{hash(content) % 10000}"
    
    def __repr__(self) -> str:
        return f"Chunk(id={self.chunk_id}, length={len(self.content)})"


class SemanticChunker:
    """Intelligent text chunking preserving semantic boundaries."""
    
    def __init__(self, chunk_size: int = 1024, overlap: int = 128, min_length: int = 100):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Target size of each chunk
            overlap: Number of characters to overlap between chunks
            min_length: Minimum chunk length
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_length = min_length
    
    def chunk(self, text: str, metadata: Dict[str, Any] = None) -> List[Chunk]:
        """
        Split text into semantic chunks.
        
        Strategy:
        1. Split by paragraphs (double newlines)
        2. If paragraph too large, split by sentences
        3. Merge small chunks to reach target size
        """
        metadata = metadata or {}
        
        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If single paragraph exceeds size, split by sentences
            if len(paragraph) > self.chunk_size:
                # Flush current chunk
                if current_chunk.strip():
                    chunk_obj = Chunk(current_chunk.strip(), metadata)
                    chunks.append(chunk_obj)
                    current_chunk = ""
                
                # Split paragraph into sentences
                sentences = self._split_sentences(paragraph)
                chunk_text = ""
                
                for sentence in sentences:
                    if len(chunk_text) + len(sentence) <= self.chunk_size:
                        chunk_text += " " + sentence if chunk_text else sentence
                    else:
                        if chunk_text and len(chunk_text) >= self.min_length:
                            chunk_obj = Chunk(chunk_text.strip(), metadata)
                            chunks.append(chunk_obj)
                        chunk_text = sentence
                
                if chunk_text and len(chunk_text) >= self.min_length:
                    chunk_obj = Chunk(chunk_text.strip(), metadata)
                    chunks.append(chunk_obj)
            else:
                # Try to add paragraph to current chunk
                test_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
                
                if len(test_chunk) <= self.chunk_size:
                    current_chunk = test_chunk
                else:
                    if current_chunk and len(current_chunk) >= self.min_length:
                        chunk_obj = Chunk(current_chunk.strip(), metadata)
                        chunks.append(chunk_obj)
                    current_chunk = paragraph
        
        # Add final chunk
        if current_chunk and len(current_chunk) >= self.min_length:
            chunk_obj = Chunk(current_chunk.strip(), metadata)
            chunks.append(chunk_obj)
        
        # Add overlap information to metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_index'] = i
            chunk.metadata['total_chunks'] = len(chunks)
        
        logger.info(f"Created {len(chunks)} chunks from text ({len(text)} chars)")
        return chunks
    
    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        """Split text into sentences."""
        sentences = []
        current = ""
        
        for char in text:
            current += char
            if char in '.!?' and len(current) > 1:
                sentences.append(current.strip())
                current = ""
        
        if current.strip():
            sentences.append(current.strip())
        
        return sentences
