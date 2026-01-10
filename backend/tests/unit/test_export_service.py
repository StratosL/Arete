"""
Unit tests for export service
"""
from unittest.mock import patch, Mock
import pytest

from app.export.service import ExportService


class TestExportService:
    """Test ExportService methods"""

    def setup_method(self):
        """Setup test fixtures"""
        self.service = ExportService()

    def test_normalize_skill(self):
        """Test skill name normalization"""
        assert self.service._normalize_skill("javascript") == "JavaScript"
        assert self.service._normalize_skill("react.js") == "React"
        assert self.service._normalize_skill("nodejs") == "Node.js"
        assert self.service._normalize_skill("Unknown Skill") == "Unknown Skill"

    def test_quick_categorize_known_skills(self):
        """Test quick categorization of known skills"""
        assert self.service._quick_categorize("python") == "Languages"
        assert self.service._quick_categorize("react") == "Frontend"
        assert self.service._quick_categorize("docker") == "Cloud & DevOps"
        assert self.service._quick_categorize("postgresql") == "Databases"

    def test_quick_categorize_unknown_skill(self):
        """Test quick categorization returns None for unknown skills"""
        assert self.service._quick_categorize("unknown-framework") is None

    @pytest.mark.asyncio
    async def test_llm_categorize_skills_success(self):
        """Test LLM skill categorization"""
        skills = ["NewFramework", "CustomTool"]
        mock_response = """{
            "Languages": [],
            "Frontend": ["NewFramework"],
            "Tools": ["CustomTool"],
            "Other": []
        }"""

        with patch('app.export.service.get_llm_response', return_value=mock_response):
            result = await self.service._llm_categorize_skills(skills)
            
            assert "Frontend" in result
            assert "NewFramework" in result["Frontend"]
            assert "Tools" in result
            assert "CustomTool" in result["Tools"]

    @pytest.mark.asyncio
    async def test_llm_categorize_skills_parse_error(self):
        """Test LLM categorization with parse error"""
        skills = ["TestSkill"]
        
        with patch('app.export.service.get_llm_response', return_value="Invalid JSON"):
            result = await self.service._llm_categorize_skills(skills)
            
            # Should fallback to Other category
            assert result == {"Other": skills}

    @pytest.mark.asyncio
    async def test_deduplicate_and_categorize_skills(self):
        """Test skill deduplication and categorization"""
        skills_dict = {
            "technical": ["Python", "JavaScript", "python"],  # Duplicate
            "frameworks": ["React", "Django"],
            "tools": ["Git", "Docker"],
            "languages": []
        }

        result = await self.service._deduplicate_and_categorize_skills(skills_dict)
        
        # Check deduplication
        all_skills = []
        for category_skills in result.values():
            all_skills.extend(category_skills)
        assert "Python" in all_skills
        assert all_skills.count("Python") == 1  # No duplicates

        # Check categorization
        assert "Languages" in result
        assert "Frontend" in result
        assert "Cloud & DevOps" in result

    @pytest.mark.asyncio
    async def test_export_resume_not_found(self, mock_supabase):
        """Test export with resume not found"""
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = Mock(data=[])
        
        with patch('app.export.service.get_supabase_service_client', return_value=mock_supabase):
            with pytest.raises(ValueError, match="Resume .* not found"):
                await self.service.export_resume("invalid-id", "pdf")

    @pytest.mark.asyncio
    async def test_export_resume_unsupported_format(self, mock_supabase, sample_resume_data):
        """Test export with unsupported format"""
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = Mock(
            data=[{"parsed_data": sample_resume_data}]
        )
        
        with patch('app.export.service.get_supabase_service_client', return_value=mock_supabase):
            with pytest.raises(ValueError, match="Unsupported format"):
                await self.service.export_resume("resume-123", "txt")

    @pytest.mark.asyncio
    async def test_generate_pdf_success(self, sample_resume_data):
        """Test successful PDF generation"""
        with patch('app.export.service.get_supabase_service_client') as mock_supabase:
            mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value = Mock(
                data=[{"parsed_data": sample_resume_data}]
            )
            
            with patch.object(self.service, '_generate_pdf') as mock_pdf:
                mock_pdf.return_value = (b"PDF content", "application/pdf", "resume.pdf")
                
                content, content_type, filename = await self.service.export_resume("resume-123", "pdf")
                
                assert content == b"PDF content"
                assert content_type == "application/pdf"
                assert filename == "resume.pdf"

    @pytest.mark.asyncio
    async def test_generate_docx_success(self, sample_resume_data):
        """Test successful DOCX generation"""
        with patch('app.export.service.get_supabase_service_client') as mock_supabase:
            mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value = Mock(
                data=[{"parsed_data": sample_resume_data}]
            )
            
            with patch.object(self.service, '_generate_docx') as mock_docx:
                mock_docx.return_value = (b"DOCX content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "resume.docx")
                
                content, content_type, filename = await self.service.export_resume("resume-123", "docx")
                
                assert content == b"DOCX content"
                assert "wordprocessingml" in content_type
                assert filename == "resume.docx"