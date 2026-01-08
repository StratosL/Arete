from pydantic import BaseModel


class OptimizationRequest(BaseModel):
    """Request model for resume optimization"""
    resume_id: str
    job_id: str


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