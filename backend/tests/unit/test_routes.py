"""
Unit tests for routes to boost coverage
"""
import pytest
from unittest.mock import patch, Mock, AsyncMock
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from main import app

client = TestClient(app)


class TestResumeRoutes:
    """Test resume routes"""

    @patch('app.resume.parser.resume_parser.parse_file', new_callable=AsyncMock)
    @patch('app.core.database.get_supabase_service_client')
    def test_upload_resume_success(self, mock_supabase, mock_parse_file):
        """Test successful resume upload"""
        # Mock parser with async return
        mock_parse_file.return_value = {
            "id": "test-123",
            "personal_info": {"name": "John Doe", "email": "john@example.com"},
            "experience": [],
            "skills": {"technical": [], "frameworks": [], "tools": [], "languages": []},
            "projects": [],
            "education": []
        }
        
        # Mock Supabase
        mock_supabase.return_value.storage.from_.return_value.upload.return_value = None
        mock_supabase.return_value.table.return_value.insert.return_value.execute.return_value = None
        
        # Create test file
        test_file = ("test.pdf", b"fake pdf content", "application/pdf")
        
        response = client.post(
            "/resume/upload",
            files={"file": test_file},
            data={"github_url": "https://github.com/test"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["personal_info"]["name"] == "John Doe"

    def test_upload_resume_no_file(self):
        """Test upload without file"""
        response = client.post("/resume/upload")
        assert response.status_code == 422

    def test_upload_resume_invalid_type(self):
        """Test upload with invalid file type"""
        test_file = ("test.xyz", b"content", "application/octet-stream")
        
        response = client.post(
            "/resume/upload",
            files={"file": test_file}
        )
        
        assert response.status_code == 400
        assert "File type not supported" in response.json()["detail"]


class TestOptimizationRoutes:
    """Test optimization routes"""

    @patch('app.optimization.service.optimization_service.get_resume_job_data', new_callable=AsyncMock)
    @patch('app.optimization.service.optimization_service.optimize_resume')
    def test_optimize_resume_success(self, mock_optimize, mock_get_data):
        """Test successful optimization"""
        # Mock get_resume_job_data
        mock_get_data.return_value = ({}, {})
        
        # Mock optimize_resume generator
        async def mock_optimize_generator():
            from app.optimization.schemas import OptimizationProgress
            yield OptimizationProgress(
                step="analyzing", 
                progress=50, 
                message="Analyzing resume content", 
                completed=False
            )
            yield OptimizationProgress(
                step="complete", 
                progress=100, 
                message="Optimization complete", 
                completed=True
            )
        
        mock_optimize.return_value = mock_optimize_generator()
        
        response = client.post("/optimize", json={
            "resume_id": "resume-123",
            "job_id": "job-456"
        })
        
        assert response.status_code == 200

    @patch('app.optimization.service.optimization_service.save_optimization', new_callable=AsyncMock)
    def test_save_optimization_success(self, mock_save):
        """Test successful optimization save"""
        mock_save.return_value = None
        
        response = client.post("/optimize/save", json={
            "resume_id": "resume-123",
            "optimized_data": {"test": "data"}
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    @patch('app.optimization.service.optimization_service.get_resume_job_data', new_callable=AsyncMock)
    @patch('app.optimization.service.optimization_service.generate_cover_letter', new_callable=AsyncMock)
    def test_generate_cover_letter_success(self, mock_generate, mock_get_data):
        """Test successful cover letter generation"""
        mock_get_data.return_value = ({}, {})
        mock_generate.return_value = "Test cover letter"
        
        response = client.post("/optimize/cover-letter", json={
            "resume_id": "resume-123",
            "job_id": "job-456"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["cover_letter"] == "Test cover letter"


class TestExportRoutes:
    """Test export routes"""

    @patch('app.export.service.export_service.export_resume', new_callable=AsyncMock)
    def test_export_pdf_success(self, mock_export):
        """Test successful PDF export"""
        mock_export.return_value = (
            b"PDF content", "application/pdf", "resume.pdf"
        )
        
        response = client.post("/export/pdf", json={
            "resume_id": "resume-123"
        })
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

    @patch('app.export.service.export_service.export_resume', new_callable=AsyncMock)
    def test_export_docx_success(self, mock_export):
        """Test successful DOCX export"""
        mock_export.return_value = (
            b"DOCX content", 
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
            "resume.docx"
        )
        
        response = client.post("/export/docx", json={
            "resume_id": "resume-123"
        })
        
        assert response.status_code == 200

    def test_export_invalid_format(self):
        """Test export with invalid format"""
        response = client.post("/export/xyz", json={
            "resume_id": "resume-123"
        })
        
        assert response.status_code == 422

    @patch('app.export.service.export_service.export_resume', new_callable=AsyncMock)
    def test_export_resume_not_found(self, mock_export):
        """Test export with resume not found"""
        mock_export.side_effect = ValueError("Resume not found")
        
        response = client.post("/export/pdf", json={
            "resume_id": "invalid-id"
        })
        
        assert response.status_code == 404


class TestGitHubRoutes:
    """Test GitHub routes"""

    @patch('app.github.service.github_service.analyze_github_profile', new_callable=AsyncMock)
    def test_analyze_github_success(self, mock_analyze):
        """Test successful GitHub analysis"""
        from app.github.schemas import GitHubAnalysisResponse, ImpactMetrics, TechStack
        
        mock_response = GitHubAnalysisResponse(
            username="testuser",
            profile_url="https://github.com/testuser",
            impact_metrics=ImpactMetrics(
                total_stars=100, total_forks=50, total_repos=25, public_repos=25,
                followers=200, following=100, contributions_last_year=500
            ),
            tech_stack=TechStack(
                primary_languages=["Python"], frameworks=["Django"], tools=["Git"]
            ),
            top_repositories=[],
            project_highlights=[],
            resume_bullet_points=["Test bullet"]
        )
        
        mock_analyze.return_value = mock_response
        
        response = client.post("/github/analyze", json={
            "username": "testuser"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    @patch('app.github.service.github_service.analyze_github_profile', new_callable=AsyncMock)
    def test_analyze_github_user_not_found(self, mock_analyze):
        """Test GitHub analysis with user not found"""
        mock_analyze.side_effect = ValueError("User not found")
        
        response = client.post("/github/analyze", json={
            "username": "invalid-user"
        })
        
        assert response.status_code == 404