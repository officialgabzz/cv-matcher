"""
Tests for PDF parser module.
"""

import pytest
from pathlib import Path
from cv_matcher.pdf_parser import PDFParser


class TestPDFParser:
    """Tests for PDFParser class."""

    def test_extract_text_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        parser = PDFParser()
        with pytest.raises(FileNotFoundError):
            parser.extract_text("nonexistent.pdf")

    def test_extract_text_invalid_extension(self):
        """Test that ValueError is raised for non-PDF files."""
        parser = PDFParser()
        with pytest.raises(ValueError, match="File is not a PDF"):
            parser.extract_text("test.txt")

    def test_extract_metadata_file_not_found(self):
        """Test metadata extraction with non-existent file."""
        parser = PDFParser()
        # Should return empty dict rather than raising
        metadata = parser.extract_metadata("nonexistent.pdf")
        assert metadata == {}
