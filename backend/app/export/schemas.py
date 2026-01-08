from pydantic import BaseModel


class ExportRequest(BaseModel):
    resume_id: str