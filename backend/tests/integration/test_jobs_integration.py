"""
Integration tests for jobs endpoints
"""
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from main import app
from app.jobs.service import job_analysis_service

client = TestClient(app)


@pytest.mark.integration
class TestJobsIntegration:
    """Integration tests for jobs endpoints"""

    @patch.object(job_analysis_service, 'analyze_job_description')
    @patch('app.jobs.routes.get_supabase_service_client')
    def test_analyze_job_with_text(self, mock_supabase, mock_analyze):
        """Test job analysis with direct text input"""
        # Mock LLM response
        mock_analyze.return_value = {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": ["Docker"],
            "technologies": ["Python", "FastAPI", "PostgreSQL"],
            "experience_level": "Mid",
            "key_requirements": ["3+ years experience", "Bachelor's degree"]
        }

        # Mock Supabase
        mock_supabase.return_value.table.return_value.insert.return_value.execute.return_value = None

        response = client.post("/jobs/analyze", json={
            "job_text": "Software Engineer position requiring Python and FastAPI experience"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Software Engineer"
        assert data["company"] == "Tech Corp"
        assert "Python" in data["required_skills"]
        assert "id" in data

    @patch.object(job_analysis_service, 'scrape_job_url')
    @patch.object(job_analysis_service, 'analyze_job_description')
    @patch('app.jobs.routes.get_supabase_service_client')
    def test_analyze_job_with_url(self, mock_supabase, mock_analyze, mock_scrape):
        """Test job analysis with URL scraping"""
        # Mock URL scraping
        mock_scrape.return_value = "Software Engineer job description with Python requirements"

        # Mock LLM response
        mock_analyze.return_value = {
            "title": "Software Engineer",
            "company": "Remote Corp",
            "required_skills": ["Python"],
            "preferred_skills": ["AWS"],
            "technologies": ["Python", "AWS"],
            "experience_level": "Senior",
            "key_requirements": ["5+ years experience"]
        }

        # Mock Supabase
        mock_supabase.return_value.table.return_value.insert.return_value.execute.return_value = None

        response = client.post("/jobs/analyze", json={
            "job_url": "https://example.com/job/123"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Software Engineer"
        assert mock_scrape.called

    def test_analyze_job_validation_error(self):
        """Test validation error when no input provided"""
        response = client.post("/jobs/analyze", json={})

        assert response.status_code == 422
        # Pydantic validation error message format
        assert "job_text" in response.text or "job_url" in response.text