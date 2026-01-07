from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional, List


class JobAnalysisRequest(BaseModel):
    """Request model for job analysis"""
    job_text: Optional[str] = Field(None, description="Job description text")
    job_url: Optional[HttpUrl] = Field(None, description="URL to job posting")
    
    @field_validator('job_text')
    @classmethod
    def validate_input(cls, v, info):
        """Validate that either job_text or job_url is provided"""
        if not v and not info.data.get('job_url'):
            raise ValueError("Either job_text or job_url must be provided")
        return v


class JobAnalysis(BaseModel):
    """Job analysis response model matching API contracts"""
    id: str
    title: str
    company: str
    required_skills: List[str]
    preferred_skills: List[str]
    technologies: List[str]
    experience_level: str
    key_requirements: List[str]