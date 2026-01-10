from datetime import datetime
from pydantic import BaseModel


class OptimizationRequest(BaseModel):
    """Request model for resume optimization"""
    resume_id: str
    job_id: str


class SaveOptimizationRequest(BaseModel):
    """Request model for saving optimization results"""
    resume_id: str
    optimized_data: dict


class CoverLetterRequest(BaseModel):
    """Request model for cover letter generation"""
    resume_id: str
    job_id: str


class CoverLetterResponse(BaseModel):
    """Response model for cover letter generation"""
    cover_letter: str
    generated_at: datetime


class OptimizationSuggestion(BaseModel):
    """Individual optimization suggestion"""
    section: str  # "experience", "skills", "projects", etc.
    type: str     # "add_keyword", "enhance_description", "quantify_impact"
    original: str
    suggested: str
    reason: str
    impact: str   # "high", "medium", "low"


class OptimizationProgress(BaseModel):
    """Progress update for SSE streaming"""
    step: str
    progress: int  # 0-100
    message: str
    suggestions: list[OptimizationSuggestion] = []
    completed: bool = False