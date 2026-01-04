"""Unit tests for processing module."""

import pytest
from src.processing.chunker import SemanticChunker


class TestSemanticChunker:
    """Test text chunking functionality."""
    
    @pytest.fixture
    def chunker(self):
        """Create chunker instance."""
        return SemanticChunker(chunk_size=200, overlap=20, min_length=30)
    
    def test_basic_chunking(self, chunker):
        """Test basic text chunking."""
        text = """This is the first paragraph. It contains multiple sentences.

This is the second paragraph. It also has content."""
        
        chunks = chunker.chunk(text)
        assert len(chunks) > 0
        assert all(len(c.content) >= 30 for c in chunks)
    
    def test_empty_text(self, chunker):
        """Test chunking empty text."""
        chunks = chunker.chunk("")
        assert len(chunks) == 0
    
    def test_metadata_preservation(self, chunker):
        """Test that metadata is preserved."""
        text = "Sample text for chunking."
        metadata = {"source": "test.txt"}
        
        chunks = chunker.chunk(text, metadata)
        assert all(c.metadata.get("source") == "test.txt" for c in chunks)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
