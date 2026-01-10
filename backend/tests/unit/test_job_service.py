"""
Unit tests for job analysis service
"""
import json
from unittest.mock import patch, Mock
import pytest
import requests

from app.jobs.service import JobAnalysisService


class TestJobAnalysisService:
    """Test JobAnalysisService methods"""

    def setup_method(self):
        """Setup test fixtures"""
        self.service = JobAnalysisService()

    def test_clean_job_text_whitespace(self):
        """Test job text whitespace normalization"""
        dirty_text = "Software   Engineer\n\n\nPython    Developer"
        clean_text = self.service._clean_job_text(dirty_text)
        assert clean_text == "Software Engineer Python Developer"

    def test_clean_job_text_special_chars(self):
        """Test special character removal"""
        dirty_text = "Software Engineer @ Company™ (Remote) [Full-time]"
        clean_text = self.service._clean_job_text(dirty_text)
        assert "Software Engineer" in clean_text
        assert "Company" in clean_text
        assert "Remote" in clean_text

    def test_clean_job_text_length_limit(self):
        """Test job text length limiting"""
        long_text = "A" * 10000
        clean_text = self.service._clean_job_text(long_text)
        assert len(clean_text) <= 8000

    @pytest.mark.asyncio
    async def test_scrape_job_url_success(self):
        """Test successful URL scraping"""
        mock_response = Mock()
        mock_response.content = b"<html><body>Software Engineer Job Description</body></html>"
        mock_response.raise_for_status.return_value = None

        with patch('app.jobs.service.requests.get', return_value=mock_response), \
             patch('app.jobs.service.BeautifulSoup') as mock_soup:
            
            mock_soup_instance = Mock()
            mock_soup_instance.return_value = []  # Empty list for script/style elements
            mock_soup_instance.get_text.return_value = "Software Engineer Job Description"
            mock_soup.return_value = mock_soup_instance
            
            result = await self.service.scrape_job_url("https://example.com/job")
            assert "Software Engineer Job Description" in result

    @pytest.mark.asyncio
    async def test_scrape_job_url_failure(self):
        """Test URL scraping failure"""
        with patch('app.jobs.service.requests.get', side_effect=requests.RequestException("Network error")):
            with pytest.raises(Exception, match="RetryError"):
                await self.service.scrape_job_url("https://example.com/job")

    @pytest.mark.asyncio
    async def test_analyze_job_description_success(self, mock_llm_response):
        """Test successful job description analysis"""
        job_text = "Software Engineer position requiring Python and FastAPI"
        
        mock_response = json.dumps({
            "title": "Software Engineer",
            "company": "Tech Corp",
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": ["Docker"],
            "technologies": ["Python", "FastAPI"],
            "experience_level": "Mid",
            "key_requirements": ["3+ years experience"]
        })

        with patch('app.jobs.service.get_llm_response', return_value=mock_response):
            result = await self.service.analyze_job_description(job_text)
            
            assert result["title"] == "Software Engineer"
            assert result["company"] == "Tech Corp"
            assert "Python" in result["required_skills"]
            assert "FastAPI" in result["required_skills"]

    @pytest.mark.asyncio
    async def test_analyze_job_description_json_parse_error(self):
        """Test JSON parsing error handling"""
        job_text = "Software Engineer position"
        
        with patch('app.jobs.service.get_llm_response', return_value="Invalid JSON"):
            with pytest.raises(ValueError, match="Failed to parse LLM response as JSON"):
                await self.service.analyze_job_description(job_text)

    @pytest.mark.asyncio
    async def test_analyze_job_description_with_markdown(self):
        """Test analysis with markdown-wrapped JSON response"""
        job_text = "Software Engineer position"
        
        mock_response = """```json
        {
            "title": "Software Engineer",
            "company": "Unknown",
            "required_skills": ["Python"],
            "preferred_skills": [],
            "technologies": ["Python"],
            "experience_level": "Mid",
            "key_requirements": ["Python experience"]
        }
        ```"""

        with patch('app.jobs.service.get_llm_response', return_value=mock_response):
            result = await self.service.analyze_job_description(job_text)
            
            assert result["title"] == "Software Engineer"
            assert "Python" in result["required_skills"]