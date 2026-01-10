from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.optimization.schemas import (
    CoverLetterRequest,
    CoverLetterResponse,
    OptimizationRequest,
    SaveOptimizationRequest,
)
from app.optimization.service import optimization_service

router = APIRouter(prefix="/optimize", tags=["optimization"])


@router.post("")
async def optimize_resume(request: OptimizationRequest):
    """Optimize resume for job with SSE streaming"""
    
    try:
        resume_data, job_analysis = await optimization_service.get_resume_job_data(
            request.resume_id, request.job_id
        )
        
        async def generate_sse():
            async for progress in optimization_service.optimize_resume(resume_data, job_analysis):
                data = progress.model_dump_json()
                yield f"data: {data}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate_sse(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")


@router.post("/save")
async def save_optimization(request: SaveOptimizationRequest):
    """Save applied optimization results to resume"""
    
    try:
        await optimization_service.save_optimization(request.resume_id, request.optimized_data)
        return {"status": "success", "message": "Optimization saved"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save optimization: {str(e)}")


@router.post("/cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter(request: CoverLetterRequest):
    """Generate tailored cover letter based on resume and job analysis"""
    
    try:
        resume_data, job_analysis = await optimization_service.get_resume_job_data(
            request.resume_id, request.job_id
        )
        
        cover_letter = await optimization_service.generate_cover_letter(resume_data, job_analysis)
        
        return CoverLetterResponse(
            cover_letter=cover_letter,
            generated_at=datetime.now(timezone.utc)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")