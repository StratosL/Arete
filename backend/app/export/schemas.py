from typing import Literal

from pydantic import BaseModel


class ExportRequest(BaseModel):
    resume_id: str
    template: Literal["classic", "modern"] = "classic"


class TemplateInfo(BaseModel):
    """Information about an available template"""
    id: str
    name: str
    description: str
    preview_image: str | None = None


AVAILABLE_TEMPLATES: list[TemplateInfo] = [
    TemplateInfo(
        id="classic",
        name="ATS Classic",
        description="Single column, maximum ATS compatibility",
        preview_image=None
    ),
    TemplateInfo(
        id="modern",
        name="Modern Professional",
        description="Clean design with accent colors and improved typography",
        preview_image=None
    ),
]