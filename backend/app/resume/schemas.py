from pydantic import BaseModel
from typing import List, Optional

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None

class Experience(BaseModel):
    title: str
    company: str
    duration: str
    description: List[str]
    technologies: List[str]

class Skills(BaseModel):
    technical: List[str]
    frameworks: List[str]
    tools: List[str]
    languages: List[str]

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]
    github_url: Optional[str] = None
    impact_metrics: List[str]

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: str
    gpa: Optional[str] = None

class ResumeData(BaseModel):
    id: str
    personal_info: PersonalInfo
    experience: List[Experience]
    skills: Skills
    projects: List[Project]
    education: List[Education]

class ResumeUploadResponse(BaseModel):
    id: str
    status: str
    message: str
    data: Optional[ResumeData] = None
