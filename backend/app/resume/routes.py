import os
import uuid
from typing import Optional

from fastapi import APIRouter
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from app.core.config import settings
from app.core.database import get_supabase_client
from app.resume.parser import resume_parser
from app.resume.schemas import ResumeData
from app.resume.schemas import ResumeUploadResponse

router = APIRouter(prefix="/resume", tags=["resume"])

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    github_url: Optional[str] = Form(None)
):
    """Upload and parse resume file"""
    
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in settings.allowed_file_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed: {', '.join(settings.allowed_file_types)}"
        )
    
    # Validate file size
    file_content = await file.read()
    file_size_mb = len(file_content) / (1024 * 1024)
    if file_size_mb > settings.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
        )
    
    try:
        # Parse resume
        resume_id = str(uuid.uuid4())
        parsed_data = await resume_parser.parse_file(file_content, file.filename, github_url)
        
        # Add ID to parsed data
        parsed_data["id"] = resume_id
        
        # Store in Supabase
        supabase = get_supabase_client()
        
        # Store file in Supabase Storage
        storage_path = f"resumes/{resume_id}/{file.filename}"
        supabase.storage.from_("resumes").upload(storage_path, file_content)
        
        # Store parsed data in database
        supabase.table("resumes").insert({
            "id": resume_id,
            "filename": file.filename,
            "storage_path": storage_path,
            "github_url": github_url,
            "parsed_data": parsed_data,
            "status": "parsed"
        }).execute()
        
        # Create response
        resume_data = ResumeData(**parsed_data)
        
        return ResumeUploadResponse(
            id=resume_id,
            status="success",
            message="Resume parsed successfully",
            data=resume_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")
