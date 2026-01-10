
from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from pydantic import model_validator


class JobAnalysisRequest(BaseModel):
    """Request model for job analysis"""
    job_text: str | None = Field(None, description="Job description text")
    job_url: HttpUrl | None = Field(None, description="URL to job posting")

    @model_validator(mode='after')
    def validate_input(self):
        """Validate that either job_text or job_url is provided"""
        if not self.job_text and not self.job_url:
            raise ValueError("Either job_text or job_url must be provided")
        return self


class JobAnalysis(BaseModel):
    """Job analysis response model matching API contracts"""
    id: str
    title: str
    company: str
    required_skills: list[str]
    preferred_skills: list[str]
    technologies: list[str]
    experience_level: str
    key_requirements: list[str]
