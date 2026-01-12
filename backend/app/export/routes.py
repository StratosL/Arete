from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import Response

from app.export.schemas import ExportRequest, AVAILABLE_TEMPLATES, TemplateInfo
from app.export.service import export_service

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/templates")
async def get_available_templates() -> list[TemplateInfo]:
    """Get list of available resume templates"""
    return AVAILABLE_TEMPLATES


@router.post("/{format}")
async def export_resume(
    format: str = Path(..., regex="^(pdf|docx)$"),
    request: ExportRequest = ...
) -> Response:
    """Export optimized resume in specified format with chosen template"""

    try:
        file_content, content_type, filename = await export_service.export_resume(
            request.resume_id, format, request.template
        )
        
        # For PDF format (which returns HTML), adjust headers for proper browser handling
        if format == "pdf" and content_type == "text/html":
            return Response(
                content=file_content,
                media_type="text/html",
                headers={
                    "Content-Disposition": f"inline; filename={filename}",
                    "Content-Type": "text/html; charset=utf-8"
                }
            )
        
        return Response(
            content=file_content,
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")