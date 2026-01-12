"""
Unit tests for cover letter generation
"""
import json
from unittest.mock import patch, Mock, AsyncMock
import pytest

from app.optimization.service import OptimizationService


class TestCoverLetterGeneration:
    """Test cover letter generation functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        self.service = OptimizationService()

    @pytest.mark.asyncio
    async def test_generate_cover_letter_success(self):
        """Test successful cover letter generation"""
        resume_data = {
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com"
            },
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2020-2023"
                }
            ],
            "skills": {
                "technical": ["Python", "JavaScript", "React"]
            }
        }
        
        job_analysis = {
            "title": "Full Stack Developer",
            "company": "Startup Inc",
            "required_skills": ["Python", "React", "Node.js"],
            "technologies": ["Python", "React", "PostgreSQL"]
        }

        mock_cover_letter = """Dear Hiring Manager,

I am excited to apply for the Full Stack Developer position at Startup Inc. With my experience as a Senior Software Engineer and expertise in Python and React, I am well-positioned to contribute to your team.

My technical skills in Python and React align perfectly with your requirements. I have extensive experience building scalable applications and would bring valuable expertise to your development team.

I am particularly drawn to Startup Inc's innovative approach and would welcome the opportunity to discuss how my background can contribute to your continued success.

Best regards,
John Doe"""

        async def mock_stream_generator():
            for chunk in mock_cover_letter.split():
                yield chunk + " "

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()):
            result = await self.service.generate_cover_letter(resume_data, job_analysis)
            
            assert "Dear Hiring Manager" in result
            assert "Full Stack Developer" in result
            assert "Startup Inc" in result
            assert "Python" in result
            assert "React" in result
            assert "John Doe" in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_with_minimal_data(self):
        """Test cover letter generation with minimal resume data"""
        resume_data = {
            "personal_info": {"name": "Jane Smith"},
            "experience": [],
            "skills": {"technical": []}
        }
        
        job_analysis = {
            "title": "Software Engineer",
            "company": "Company",
            "required_skills": ["Python"],
            "technologies": ["Python"]
        }

        mock_cover_letter = "Dear Hiring Manager,\n\nI am interested in the Software Engineer position at Company.\n\nBest regards,\nJane Smith"

        async def mock_stream_generator():
            yield mock_cover_letter

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()):
            result = await self.service.generate_cover_letter(resume_data, job_analysis)
            
            assert "Jane Smith" in result
            assert "Software Engineer" in result
            assert "Company" in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_personalization(self):
        """Test cover letter personalization based on job requirements"""
        resume_data = {
            "personal_info": {"name": "Alex Johnson"},
            "experience": [
                {"title": "DevOps Engineer", "company": "Cloud Corp"}
            ],
            "skills": {"technical": ["Docker", "Kubernetes", "AWS"]}
        }
        
        job_analysis = {
            "title": "Senior DevOps Engineer",
            "company": "Scale Tech",
            "required_skills": ["Docker", "Kubernetes", "CI/CD"],
            "technologies": ["Docker", "Kubernetes", "Jenkins"]
        }

        mock_cover_letter = """Dear Hiring Manager,

I am writing to express my interest in the Senior DevOps Engineer position at Scale Tech. As a DevOps Engineer with expertise in Docker and Kubernetes, I am excited about the opportunity to contribute to your infrastructure team.

My experience with Docker and Kubernetes directly aligns with your technical requirements. I have successfully implemented CI/CD pipelines and managed containerized applications at scale.

I am particularly interested in Scale Tech's commitment to scalable infrastructure and would love to discuss how my background in cloud technologies can support your growth objectives.

Sincerely,
Alex Johnson"""

        async def mock_stream_generator():
            yield mock_cover_letter

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()):
            result = await self.service.generate_cover_letter(resume_data, job_analysis)
            
            # Check personalization elements
            assert "Alex Johnson" in result
            assert "Senior DevOps Engineer" in result
            assert "Scale Tech" in result
            assert "Docker" in result
            assert "Kubernetes" in result
            assert "DevOps Engineer" in result  # Current role mentioned

    @pytest.mark.asyncio
    async def test_generate_cover_letter_streaming_error(self):
        """Test cover letter generation with streaming error"""
        resume_data = {"personal_info": {"name": "Test User"}, "experience": [], "skills": {"technical": []}}
        job_analysis = {"title": "Developer", "company": "Test Co", "required_skills": [], "technologies": []}

        async def mock_error_generator():
            raise Exception("Streaming error")
            yield  # Never reached

        with patch('app.optimization.service.stream_llm_response', return_value=mock_error_generator()):
            with pytest.raises(Exception, match="Streaming error"):
                await self.service.generate_cover_letter(resume_data, job_analysis)

    @pytest.mark.asyncio
    async def test_generate_cover_letter_empty_response(self):
        """Test cover letter generation with empty LLM response"""
        resume_data = {"personal_info": {"name": "Test User"}, "experience": [], "skills": {"technical": []}}
        job_analysis = {"title": "Developer", "company": "Test Co", "required_skills": [], "technologies": []}

        async def mock_empty_generator():
            return
            yield  # This will never execute

        with patch('app.optimization.service.stream_llm_response', return_value=mock_empty_generator()):
            result = await self.service.generate_cover_letter(resume_data, job_analysis)
            
            assert result == ""

    @pytest.mark.asyncio
    async def test_generate_cover_letter_prompt_construction(self):
        """Test that cover letter prompt includes all necessary information"""
        resume_data = {
            "personal_info": {"name": "Sarah Wilson"},
            "experience": [{"title": "Data Scientist", "company": "AI Corp"}],
            "skills": {"technical": ["Python", "Machine Learning", "TensorFlow"]}
        }
        
        job_analysis = {
            "title": "ML Engineer",
            "company": "Data Innovations",
            "required_skills": ["Python", "TensorFlow", "MLOps"],
            "technologies": ["Python", "TensorFlow", "Kubernetes"]
        }

        mock_cover_letter = "Generated cover letter content"

        async def mock_stream_generator():
            yield mock_cover_letter

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()) as mock_stream:
            await self.service.generate_cover_letter(resume_data, job_analysis)
            
            # Verify the prompt was called with correct information
            mock_stream.assert_called_once()
            call_args = mock_stream.call_args[0][0]  # Get the messages parameter
            prompt_content = call_args[0]["content"]
            
            # Check that all key information is included in the prompt
            assert "Sarah Wilson" in prompt_content
            assert "Data Scientist" in prompt_content
            assert "ML Engineer" in prompt_content
            assert "Data Innovations" in prompt_content
            assert "Python" in prompt_content
            assert "TensorFlow" in prompt_content

    @pytest.mark.asyncio
    async def test_generate_cover_letter_skills_matching(self):
        """Test cover letter emphasizes matching skills"""
        resume_data = {
            "personal_info": {"name": "Mike Chen"},
            "experience": [{"title": "Backend Developer"}],
            "skills": {"technical": ["Python", "Django", "PostgreSQL", "Redis"]}
        }
        
        job_analysis = {
            "title": "Python Developer",
            "company": "Web Solutions",
            "required_skills": ["Python", "Django", "PostgreSQL"],
            "technologies": ["Python", "Django", "PostgreSQL", "Docker"]
        }

        mock_cover_letter = """Dear Hiring Manager,

I am excited to apply for the Python Developer position at Web Solutions. My expertise in Python, Django, and PostgreSQL makes me an ideal candidate for this role.

As a Backend Developer, I have extensive experience with Python and Django, building robust web applications with PostgreSQL databases. My technical skills directly align with your requirements.

I look forward to contributing to Web Solutions' development team.

Best regards,
Mike Chen"""

        async def mock_stream_generator():
            yield mock_cover_letter

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()):
            result = await self.service.generate_cover_letter(resume_data, job_analysis)
            
            # Verify matching skills are emphasized
            assert "Python" in result
            assert "Django" in result
            assert "PostgreSQL" in result
            assert result.count("Python") >= 2  # Should mention Python multiple times