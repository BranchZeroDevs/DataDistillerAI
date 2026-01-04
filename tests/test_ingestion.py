"""Unit tests for ingestion module."""

import pytest
from pathlib import Path
import tempfile
from src.ingestion import DocumentLoader


class TestDocumentLoader:
    """Test document loading functionality."""
    
    @pytest.fixture
    def loader(self):
        """Create loader instance."""
        return DocumentLoader()
    
    @pytest.fixture
    def temp_text_file(self):
        """Create temporary text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content\nSecond line")
            return f.name
    
    def test_load_txt_file(self, loader, temp_text_file):
        """Test loading text file."""
        doc = loader.load(temp_text_file)
        assert "Test content" in doc.content
        assert doc.metadata['format'] == '.txt'
    
    def test_load_nonexistent_file(self, loader):
        """Test error handling for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            loader.load("/nonexistent/file.txt")
    
    def test_unsupported_format(self, loader):
        """Test error handling for unsupported format."""
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            f.write(b"test")
            f.flush()
            with pytest.raises(ValueError):
                loader.load(f.name)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
