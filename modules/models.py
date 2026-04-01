from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List, Optional

class Contact(BaseModel):
    email: str # Not using EmailStr to avoid strict domain validation until we know the LLM can handle it, though it's better.
    linkedin: Optional[str] = ""
    github: Optional[str] = ""
    portfolio: Optional[str] = ""

class Experience(BaseModel):
    company: str
    role: str
    period: str
    achievements: List[str]

class Project(BaseModel):
    name: str
    tech_stack: str
    url: Optional[str] = ""
    description: str

class Education(BaseModel):
    degree: str
    institution: str
    year: str
    description: Optional[str] = ""
    hard_skills: List[str] = []

class CVData(BaseModel):
    full_name: str
    contact: Contact
    summary: str
    experience: List[Experience]
    skills: dict # {'hard': [], 'soft': []}
    projects: List[Project]
    education: List[Education]
