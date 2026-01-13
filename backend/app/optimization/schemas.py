from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class OptimizationRequest(BaseModel):
    """Request model for resume optimization"""
    resume_id: UUID
    job_id: UUID


class SaveOptimizationRequest(BaseModel):
    """Request model for saving optimization results"""
    resume_id: UUID
    optimized_data: dict


class CoverLetterRequest(BaseModel):
    """Request model for cover letter generation"""
    resume_id: UUID
    job_id: UUID


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


class KeywordMatchScore(BaseModel):
    """Keyword matching breakdown for ATS scoring"""
    matched: int
    total: int
    percentage: int
    matched_keywords: list[str] = []
    missing_keywords: list[str] = []


class SectionScore(BaseModel):
    """Individual section score for ATS"""
    name: str
    present: bool
    score: int  # 0-100


class ATSScore(BaseModel):
    """ATS compatibility score breakdown"""
    overall_score: int  # 0-100
    keyword_match: KeywordMatchScore
    section_completeness: int  # 0-100
    sections: list[SectionScore] = []
    recommendations: list[str] = []


class InterviewQuestion(BaseModel):
    """Interview preparation question"""
    category: str  # "technical", "behavioral", "system_design", "role_specific"
    question: str
    tips: str  # Brief tips for answering


class OptimizationProgress(BaseModel):
    """Progress update for SSE streaming"""
    step: str
    progress: int  # 0-100
    message: str
    suggestions: list[OptimizationSuggestion] = []
    completed: bool = False
    ats_score: Optional[ATSScore] = None
    interview_questions: list[InterviewQuestion] = []