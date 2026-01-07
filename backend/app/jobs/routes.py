import uuid

from fastapi import APIRouter
from fastapi import HTTPException

from app.core.database import get_supabase_service_client
from app.jobs.schemas import JobAnalysis
from app.jobs.schemas import JobAnalysisRequest
from app.jobs.service import job_analysis_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/analyze", response_model=JobAnalysis)
async def analyze_job(request: JobAnalysisRequest) -> JobAnalysis:
    """Analyze job description from text or URL"""

    try:
        # Get job text either from direct input or URL scraping
        if request.job_text:
            job_text = request.job_text
        elif request.job_url:
            job_text = await job_analysis_service.scrape_job_url(str(request.job_url))
        else:
            raise HTTPException(
                status_code=400,
                detail="Either job_text or job_url must be provided"
            )

        # Analyze job description with Claude API
        analysis_data = await job_analysis_service.analyze_job_description(job_text)

        # Generate unique ID for this analysis
        job_id = str(uuid.uuid4())
        analysis_data["id"] = job_id

        # Store analysis in Supabase
        supabase = get_supabase_service_client()
        supabase.table("jobs").insert({
            "id": job_id,
            "user_id": None,  # MVP: No authentication yet
            "title": analysis_data.get("title"),
            "company": analysis_data.get("company"),
            "job_text": job_text[:1000],  # Store truncated version
            "job_url": str(request.job_url) if request.job_url else None,
            "analysis": analysis_data
        }).execute()

        return JobAnalysis(**analysis_data)

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e!s}")
