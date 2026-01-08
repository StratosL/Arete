import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.core.database import get_supabase_service_client
from app.optimization.schemas import OptimizationRequest, SaveOptimizationRequest
from app.optimization.service import optimization_service

router = APIRouter(prefix="/optimize", tags=["optimization"])


@router.get("")
async def optimize_resume(resume_id: str, job_id: str):
    """Optimize resume for job with SSE streaming"""
    
    try:
        supabase = get_supabase_service_client()
        
        # Fetch resume data
        resume_response = (
            supabase.table("resumes")
            .select("*")
            .eq("id", resume_id)
            .execute()
        )
        if not resume_response.data:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        resume_record = resume_response.data[0]
        resume_data = resume_record.get("parsed_data", {})
        
        # Fetch job analysis data
        job_response = supabase.table("jobs").select("*").eq("id", job_id).execute()
        if not job_response.data:
            raise HTTPException(status_code=404, detail="Job analysis not found")
        
        job_record = job_response.data[0]
        job_analysis = job_record.get("analysis", {})
        
        # Stream optimization
        async def generate_sse():
            async for progress in optimization_service.optimize_resume(resume_data, job_analysis):
                # Format as SSE
                data = progress.model_dump_json()
                yield f"data: {data}\n\n"
            
            # Send completion signal
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")


@router.post("/save")
async def save_optimization(request: SaveOptimizationRequest):
    """Save applied optimization results to resume"""
    
    try:
        supabase = get_supabase_service_client()
        
        # Update resume with optimized data
        supabase.table("resumes").update({
            "optimized_data": request.optimized_data
        }).eq("id", request.resume_id).execute()
        
        return {"status": "success", "message": "Optimization saved"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save optimization: {str(e)}")