"""
Comprehensive unit tests for cover letter generation service
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException

from app.optimization.service import OptimizationService


class TestCoverLetterService:
    """Test cover letter generation service functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        self.service = OptimizationService()
        self.sample_resume_data = {
            "personal_info": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1-555-0123",
                "location": "San Francisco, CA"
            },
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2020-2023",
                    "description": ["Built scalable web applications", "Led team of 5 developers"],
                    "technologies": ["Python", "React", "PostgreSQL"]
                }
            ],
            "skills": {
                "technical": ["Python", "JavaScript", "React", "Node.js"],
                "frameworks": ["Django", "Express.js"],
                "tools": ["Docker", "Git"],
                "languages": ["Python", "JavaScript"]
            }
        }
        
        self.sample_job_analysis = {
            "title": "Full Stack Developer",
            "company": "Startup Inc",
            "required_skills": ["Python", "React", "Node.js"],
            "technologies": ["Python", "React", "PostgreSQL", "Docker"],
            "key_requirements": ["3+ years experience", "Full stack development", "Team leadership"]
        }

    @pytest.mark.asyncio
    async def test_generate_cover_letter_complete_data(self):
        """Test cover letter generation with complete resume and job data"""
        mock_response = """Dear Hiring Manager,

I am excited to apply for the Full Stack Developer position at Startup Inc. With my experience as a Senior Software Engineer at Tech Corp and expertise in Python, React, and Node.js, I am well-positioned to contribute to your development team.

My technical background includes extensive work with Python and React, which directly aligns with your requirements. At Tech Corp, I built scalable web applications and led a team of 5 developers, demonstrating both technical skills and leadership capabilities that match your need for team leadership experience.

I am particularly drawn to Startup Inc's innovative approach and the opportunity to work with technologies like PostgreSQL and Docker, which I have used extensively in my previous role.

I would welcome the opportunity to discuss how my full stack development experience and team leadership skills can contribute to Startup Inc's continued success.

Best regards,
John Doe"""

        async def mock_stream():
            for chunk in mock_response.split():
                yield chunk + " "

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()):
            result = await self.service.generate_cover_letter(self.sample_resume_data, self.sample_job_analysis)
            
            # Verify personalization
            assert "John Doe" in result
            assert "Full Stack Developer" in result
            assert "Startup Inc" in result
            assert "Senior Software Engineer" in result
            assert "Tech Corp" in result
            
            # Verify technical skills mentioned
            assert "Python" in result
            assert "React" in result
            assert "Node.js" in result
            
            # Verify professional structure
            assert "Dear Hiring Manager" in result
            assert "Best regards" in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_missing_personal_info(self):
        """Test cover letter generation with missing personal information"""
        incomplete_resume = {
            "personal_info": {},  # Empty personal info
            "experience": [],
            "skills": {"technical": ["Python"]}
        }
        
        mock_response = "Dear Hiring Manager,\n\nI am interested in the Full Stack Developer position at Startup Inc.\n\nBest regards,\nCandidate"

        async def mock_stream():
            yield mock_response

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()):
            result = await self.service.generate_cover_letter(incomplete_resume, self.sample_job_analysis)
            
            # Should handle missing name gracefully
            assert "Candidate" in result or "Full Stack Developer" in result
            assert "Startup Inc" in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_no_experience(self):
        """Test cover letter generation for entry-level candidate with no experience"""
        entry_level_resume = {
            "personal_info": {"name": "Jane Smith"},
            "experience": [],  # No work experience
            "skills": {"technical": ["Python", "JavaScript"]}
        }
        
        mock_response = """Dear Hiring Manager,

I am writing to express my interest in the Full Stack Developer position at Startup Inc. As a recent graduate with strong technical skills in Python and JavaScript, I am eager to begin my career in full stack development.

My technical foundation includes Python and JavaScript, which align with your requirements. While I am early in my career, I am passionate about software development and excited to contribute to your team.

I am particularly interested in Startup Inc's innovative projects and would welcome the opportunity to grow my skills while contributing to your development goals.

Best regards,
Jane Smith"""

        async def mock_stream():
            yield mock_response

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()):
            result = await self.service.generate_cover_letter(entry_level_resume, self.sample_job_analysis)
            
            assert "Jane Smith" in result
            assert "Software Engineer" in result or "recent graduate" in result or "early in my career" in result
            assert "Python" in result
            assert "JavaScript" in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_skill_matching(self):
        """Test that cover letter emphasizes matching skills between resume and job"""
        specialized_resume = {
            "personal_info": {"name": "Alex Chen"},
            "experience": [{"title": "DevOps Engineer", "company": "Cloud Corp"}],
            "skills": {"technical": ["Docker", "Kubernetes", "AWS", "Python", "Terraform"]}
        }
        
        devops_job = {
            "title": "Senior DevOps Engineer",
            "company": "Scale Tech",
            "required_skills": ["Docker", "Kubernetes", "CI/CD", "AWS"],
            "technologies": ["Docker", "Kubernetes", "Jenkins", "Terraform"]
        }
        
        mock_response = """Dear Hiring Manager,

I am excited to apply for the Senior DevOps Engineer position at Scale Tech. My experience as a DevOps Engineer with expertise in Docker, Kubernetes, and AWS makes me an ideal candidate for this role.

My technical skills include Docker and Kubernetes, which are core requirements for your position. I also have extensive experience with AWS and Terraform, technologies that align perfectly with your infrastructure needs.

I am particularly interested in Scale Tech's commitment to scalable infrastructure and would love to discuss how my DevOps expertise can support your growth objectives.

Sincerely,
Alex Chen"""

        async def mock_stream():
            yield mock_response

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()):
            result = await self.service.generate_cover_letter(specialized_resume, devops_job)
            
            # Verify matching skills are emphasized
            matching_skills = ["Docker", "Kubernetes", "AWS", "Terraform"]
            for skill in matching_skills:
                assert skill in result
            
            assert "Alex Chen" in result
            assert "Senior DevOps Engineer" in result
            assert "Scale Tech" in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_prompt_structure(self):
        """Test that the LLM prompt is properly structured with all required information"""
        async def mock_stream():
            yield "Mock cover letter"

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()) as mock_llm:
            await self.service.generate_cover_letter(self.sample_resume_data, self.sample_job_analysis)
            
            # Verify LLM was called once
            mock_llm.assert_called_once()
            
            # Get the prompt content
            call_args = mock_llm.call_args[0][0]
            prompt_content = call_args[0]["content"]
            
            # Verify all required information is in prompt
            assert "John Doe" in prompt_content
            assert "Senior Software Engineer" in prompt_content
            assert "Full Stack Developer" in prompt_content
            assert "Startup Inc" in prompt_content
            assert "Python" in prompt_content
            assert "React" in prompt_content
            
            # Verify prompt structure requirements
            assert "professional tone" in prompt_content.lower()
            assert "3-4 paragraphs" in prompt_content.lower()
            assert "no placeholder text" in prompt_content.lower()

    @pytest.mark.asyncio
    async def test_generate_cover_letter_llm_error_handling(self):
        """Test error handling when LLM service fails"""
        async def mock_error_stream():
            raise Exception("LLM service unavailable")
            yield  # Never reached

        with patch('app.optimization.service.stream_llm_response', return_value=mock_error_stream()):
            with pytest.raises(Exception, match="LLM service unavailable"):
                await self.service.generate_cover_letter(self.sample_resume_data, self.sample_job_analysis)

    @pytest.mark.asyncio
    async def test_generate_cover_letter_empty_response(self):
        """Test handling of empty LLM response"""
        async def mock_empty_stream():
            return
            yield  # Never executed

        with patch('app.optimization.service.stream_llm_response', return_value=mock_empty_stream()):
            result = await self.service.generate_cover_letter(self.sample_resume_data, self.sample_job_analysis)
            
            assert result == ""

    @pytest.mark.asyncio
    async def test_generate_cover_letter_whitespace_handling(self):
        """Test proper whitespace handling in cover letter generation"""
        mock_response = "   Dear Hiring Manager,\n\nCover letter content.\n\nBest regards,\nJohn Doe   "

        async def mock_stream():
            yield mock_response

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()):
            result = await self.service.generate_cover_letter(self.sample_resume_data, self.sample_job_analysis)
            
            # Verify whitespace is properly stripped
            assert result == mock_response.strip()
            assert not result.startswith(" ")
            assert not result.endswith(" ")

    @pytest.mark.asyncio
    async def test_generate_cover_letter_streaming_chunks(self):
        """Test proper handling of streaming response chunks"""
        chunks = ["Dear ", "Hiring ", "Manager,\n\n", "I am ", "excited ", "to apply...\n\n", "Best regards,\n", "John Doe"]

        async def mock_stream():
            for chunk in chunks:
                yield chunk

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()):
            result = await self.service.generate_cover_letter(self.sample_resume_data, self.sample_job_analysis)
            
            # Verify all chunks are properly concatenated
            expected = "".join(chunks).strip()
            assert result == expected
            assert "Dear Hiring Manager" in result
            assert "John Doe" in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_special_characters(self):
        """Test handling of special characters in resume and job data"""
        special_resume = {
            "personal_info": {"name": "José García-Smith"},
            "experience": [{"title": "Software Engineer @ Tech Co.", "company": "Tech & Innovation Ltd."}],
            "skills": {"technical": ["C++", ".NET", "Node.js"]}
        }
        
        special_job = {
            "title": "Senior C++ Developer",
            "company": "R&D Solutions Inc.",
            "required_skills": ["C++", ".NET"],
            "technologies": ["C++", ".NET", "SQL Server"]
        }
        
        mock_response = "Dear Hiring Manager,\n\nI am José García-Smith, applying for Senior C++ Developer at R&D Solutions Inc. My expertise in C++ and .NET makes me ideal for this role.\n\nBest regards,\nJosé García-Smith"

        async def mock_stream():
            yield mock_response

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()):
            result = await self.service.generate_cover_letter(special_resume, special_job)
            
            # Verify special characters are preserved
            assert "José García-Smith" in result
            assert "C++" in result
            assert ".NET" in result
            assert "R&D Solutions Inc." in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_long_response(self):
        """Test handling of very long cover letter responses"""
        # Simulate a very long response
        long_response = "Dear Hiring Manager,\n\n" + "This is a very long paragraph. " * 100 + "\n\nBest regards,\nJohn Doe"

        async def mock_stream():
            # Yield in small chunks to simulate real streaming
            chunk_size = 50
            for i in range(0, len(long_response), chunk_size):
                yield long_response[i:i + chunk_size]

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()):
            result = await self.service.generate_cover_letter(self.sample_resume_data, self.sample_job_analysis)
            
            # Verify long response is properly handled
            assert len(result) > 1000  # Should be quite long
            assert result.startswith("Dear Hiring Manager")
            assert result.endswith("John Doe")
            assert "This is a very long paragraph." in result

    @pytest.mark.asyncio
    async def test_generate_cover_letter_default_values(self):
        """Test cover letter generation with missing optional fields using defaults"""
        minimal_resume = {
            "personal_info": {"name": "Test User"},
            "experience": [],
            "skills": {}
        }
        
        minimal_job = {
            "title": "",
            "company": "",
            "required_skills": [],
            "technologies": []
        }
        
        mock_response = "Dear Hiring Manager,\n\nI am Test User applying for the Software Engineer position at Company.\n\nBest regards,\nTest User"

        async def mock_stream():
            yield mock_response

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream()) as mock_llm:
            result = await self.service.generate_cover_letter(minimal_resume, minimal_job)
            
            # Verify defaults are used in prompt
            call_args = mock_llm.call_args[0][0]
            prompt_content = call_args[0]["content"]
            
            assert "Software Engineer" in prompt_content  # Default title
            assert "Company" in prompt_content  # Default company
            assert "Test User" in result