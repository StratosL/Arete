from fastapi import APIRouter
from fastapi import HTTPException

from app.github.schemas import GitHubAnalysisResponse
from app.github.schemas import GitHubAnalyzeRequest
from app.github.service import github_service

router = APIRouter(prefix="/github", tags=["github"])


@router.post("/analyze", response_model=GitHubAnalysisResponse)
async def analyze_github_profile(request: GitHubAnalyzeRequest):
    """Analyze GitHub profile and generate resume insights"""
    
    try:
        analysis = await github_service.analyze_github_profile(request.username)
        return analysis
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub analysis failed: {e!s}")