
from pydantic import BaseModel


class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str | None = None
    location: str | None = None
    github: str | None = None
    linkedin: str | None = None

class Experience(BaseModel):
    title: str
    company: str
    duration: str
    description: list[str]
    technologies: list[str]

class Skills(BaseModel):
    technical: list[str]
    frameworks: list[str]
    tools: list[str]
    languages: list[str]

class Project(BaseModel):
    name: str
    description: str
    technologies: list[str]
    github_url: str | None = None
    impact_metrics: list[str]

class Education(BaseModel):
    degree: str | None = None
    institution: str | None = None
    graduation_year: str | None = None
    gpa: str | None = None

class ResumeData(BaseModel):
    id: str
    personal_info: PersonalInfo
    experience: list[Experience]
    skills: Skills
    projects: list[Project]
    education: list[Education]

class ResumeUploadResponse(BaseModel):
    id: str
    status: str
    message: str
    data: ResumeData | None = None
