import pytest
from pydantic import ValidationError

from app.jobs.schemas import JobAnalysisRequest
from app.jobs.service import JobAnalysisService


class TestJobAnalysisRequest:
    """Test JobAnalysisRequest validation"""

    def test_valid_job_text(self):
        """Test valid request with job_text"""
        request = JobAnalysisRequest(job_text="Software Engineer position")
        assert request.job_text == "Software Engineer position"
        assert request.job_url is None

    def test_valid_job_url(self):
        """Test valid request with job_url"""
        request = JobAnalysisRequest(job_url="https://example.com/job")
        assert str(request.job_url) == "https://example.com/job"
        assert request.job_text is None

    def test_both_fields_provided(self):
        """Test request with both fields provided"""
        request = JobAnalysisRequest(
            job_text="Software Engineer",
            job_url="https://example.com/job"
        )
        assert request.job_text == "Software Engineer"
        assert str(request.job_url) == "https://example.com/job"

    def test_neither_field_provided(self):
        """Test validation error when neither field provided"""
        with pytest.raises(ValidationError):
            JobAnalysisRequest()

    def test_invalid_url(self):
        """Test validation error for invalid URL"""
        with pytest.raises(ValidationError):
            JobAnalysisRequest(job_url="not-a-url")


class TestJobAnalysisService:
    """Test JobAnalysisService methods"""

    def test_clean_job_text(self):
        """Test job text cleaning"""
        service = JobAnalysisService()

        # Test whitespace normalization
        dirty_text = "Software   Engineer\n\n\nPython    Developer"
        clean_text = service._clean_job_text(dirty_text)
        assert clean_text == "Software Engineer Python Developer"

        # Test special character removal
        dirty_text = "Software Engineer @ Company™ (Remote) [Full-time]"
        clean_text = service._clean_job_text(dirty_text)
        assert "Software Engineer" in clean_text
        assert "Company" in clean_text

    def test_clean_job_text_length_limit(self):
        """Test job text length limiting"""
        service = JobAnalysisService()
        long_text = "A" * 10000
        clean_text = service._clean_job_text(long_text)
        assert len(clean_text) <= 8000
