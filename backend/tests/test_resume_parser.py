"""
Test suite for resume parsing functionality
Following pytest standards from .kiro/reference/pytest-standard.md
"""

import asyncio
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.resume.parser import ResumeParser
from app.resume.schemas import ResumeData


class TestResumeParser:
    """Test cases for ResumeParser class"""

    def setup_method(self):
        """Setup test fixtures"""
        self.parser = ResumeParser()

    def test_parse_pdf_basic(self):
        """Test basic PDF parsing functionality"""
        # Mock PDF content
        mock_content = b"John Doe\nSoftware Engineer\nPython, FastAPI"
        
        with patch('pdfplumber.open') as mock_pdf:
            # Setup mock PDF
            mock_page = Mock()
            mock_page.extract_text.return_value = "John Doe\nSoftware Engineer\nPython, FastAPI"
            mock_pdf.return_value.__enter__.return_value.pages = [mock_page]
            
            result = self.parser._parse_pdf(mock_content)
            
            assert isinstance(result, str)
            assert "John Doe" in result
            assert "Software Engineer" in result

    def test_parse_docx_basic(self):
        """Test basic DOCX parsing functionality"""
        mock_content = b"mock docx content"
        
        with patch('docx.Document') as mock_doc:
            # Setup mock document
            mock_paragraph = Mock()
            mock_paragraph.text = "Jane Smith\nData Scientist"
            mock_paragraph.style.name = "Normal"
            mock_doc.return_value.paragraphs = [mock_paragraph]
            
            result = self.parser._parse_docx(mock_content)
            
            assert isinstance(result, str)
            assert "Jane Smith" in result

    @pytest.mark.asyncio
    async def test_markdown_to_json_structure(self):
        """Test LLM markdown to JSON conversion"""
        markdown_text = """
        # John Doe
        Software Engineer
        
        ## Experience
        - Senior Developer at TechCorp
        - Python, FastAPI, React
        """
        
        with patch('app.resume.parser.get_llm_response') as mock_llm:
            # Mock LLM response
            mock_response = '''
            {
                "personal_info": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": null,
                    "location": null,
                    "github": null,
                    "linkedin": null
                },
                "experience": [],
                "skills": {
                    "technical": ["Python", "FastAPI"],
                    "frameworks": ["React"],
                    "tools": [],
                    "languages": []
                },
                "projects": [],
                "education": []
            }
            '''
            mock_llm.return_value = mock_response
            
            result = await self.parser._markdown_to_json(markdown_text)
            
            assert isinstance(result, dict)
            assert "personal_info" in result
            assert result["personal_info"]["name"] == "John Doe"
            assert "Python" in result["skills"]["technical"]

    @pytest.mark.asyncio
    async def test_parse_file_pdf_integration(self):
        """Integration test for complete PDF parsing workflow"""
        mock_content = b"PDF content"
        filename = "resume.pdf"
        
        with patch.object(self.parser, '_parse_pdf') as mock_parse_pdf, \
             patch.object(self.parser, '_markdown_to_json') as mock_to_json:
            
            mock_parse_pdf.return_value = "Parsed markdown content"
            mock_to_json.return_value = {
                "personal_info": {"name": "Test User", "email": "test@example.com"},
                "experience": [],
                "skills": {"technical": [], "frameworks": [], "tools": [], "languages": []},
                "projects": [],
                "education": []
            }
            
            result = await self.parser.parse_file(mock_content, filename)
            
            assert isinstance(result, dict)
            assert "personal_info" in result
            mock_parse_pdf.assert_called_once_with(mock_content)
            mock_to_json.assert_called_once()

    def test_unsupported_file_format(self):
        """Test handling of unsupported file formats"""
        mock_content = b"content"
        filename = "resume.txt"  # Supported format
        
        # This should not raise an exception for txt
        # But let's test an unsupported format
        with pytest.raises(ValueError, match="Unsupported file format"):
            import asyncio
            asyncio.run(self.parser.parse_file(mock_content, "resume.xyz"))


@pytest.mark.integration
class TestResumeParserIntegration:
    """Integration tests requiring external dependencies"""

    @pytest.mark.asyncio
    async def test_real_llm_integration(self):
        """Test with real LLM (requires API key)"""
        # Skip if no API key available
        pytest.skip("Integration test - requires Claude API key")

    def test_real_pdf_parsing(self):
        """Test with real PDF file"""
        # Skip if no test files available
        pytest.skip("Integration test - requires test PDF files")


# Unit tests for schemas
class TestResumeSchemas:
    """Test Pydantic schemas for resume data"""

    def test_resume_data_validation(self):
        """Test ResumeData schema validation"""
        valid_data = {
            "id": "test-123",
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "experience": [],
            "skills": {
                "technical": ["Python"],
                "frameworks": [],
                "tools": [],
                "languages": []
            },
            "projects": [],
            "education": []
        }
        
        resume = ResumeData(**valid_data)
        assert resume.id == "test-123"
        assert resume.personal_info.name == "John Doe"
        assert "Python" in resume.skills.technical

    def test_resume_data_invalid_email(self):
        """Test ResumeData validation with invalid email"""
        # Note: Current schema doesn't validate email format
        # This test documents current behavior
        invalid_data = {
            "id": "test-123",
            "personal_info": {
                "name": "John Doe",
                "email": "invalid-email"  # Invalid format
            },
            "experience": [],
            "skills": {"technical": [], "frameworks": [], "tools": [], "languages": []},
            "projects": [],
            "education": []
        }
        
        # Currently passes - could add email validation in future
        resume = ResumeData(**invalid_data)
        assert resume.personal_info.email == "invalid-email"
