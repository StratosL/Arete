"""
Shared test fixtures for Arete backend tests
"""
import pytest
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def mock_supabase():
    """Mock Supabase client"""
    mock_client = Mock()
    
    # Mock table operations
    mock_table = Mock()
    mock_table.select.return_value = mock_table
    mock_table.insert.return_value = mock_table
    mock_table.update.return_value = mock_table
    mock_table.eq.return_value = mock_table
    mock_table.execute.return_value = Mock(data=[])
    
    mock_client.table.return_value = mock_table
    
    # Mock storage operations
    mock_storage = Mock()
    mock_storage.upload.return_value = Mock()
    mock_client.storage.from_.return_value = mock_storage
    
    return mock_client


@pytest.fixture
def mock_llm_response():
    """Mock LLM response"""
    return AsyncMock(return_value="Mock LLM response")


@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing"""
    return {
        "id": "test-resume-123",
        "personal_info": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "location": "San Francisco, CA",
            "github": "https://github.com/johndoe",
            "linkedin": "https://linkedin.com/in/johndoe"
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
            "technical": ["Python", "JavaScript", "SQL"],
            "frameworks": ["React", "FastAPI", "Django"],
            "tools": ["Git", "Docker", "AWS"],
            "languages": ["English", "Spanish"]
        },
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Built full-stack e-commerce solution",
                "technologies": ["Python", "React", "PostgreSQL"],
                "github_url": "https://github.com/johndoe/ecommerce",
                "impact_metrics": ["Increased sales by 30%", "Reduced load time by 50%"]
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "Stanford University",
                "graduation_year": "2018",
                "gpa": "3.8"
            }
        ]
    }


@pytest.fixture
def sample_job_analysis():
    """Sample job analysis data for testing"""
    return {
        "id": "test-job-456",
        "title": "Senior Python Developer",
        "company": "Startup Inc",
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "preferred_skills": ["Docker", "AWS", "React"],
        "technologies": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "experience_level": "Senior",
        "key_requirements": [
            "5+ years Python experience",
            "Experience with FastAPI",
            "Database design skills"
        ]
    }


@pytest.fixture
def mock_pdf_content():
    """Mock PDF file content"""
    return b"Mock PDF content for testing"


@pytest.fixture
def mock_docx_content():
    """Mock DOCX file content"""
    return b"Mock DOCX content for testing"