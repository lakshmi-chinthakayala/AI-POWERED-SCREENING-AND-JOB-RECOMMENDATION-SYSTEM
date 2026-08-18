"""
Pydantic Schemas for Resume Operations.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class CandidateInfoSchema(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    linkedin: str
    github: str

class EducationSchema(BaseModel):
    degree: str
    institution: str
    graduation_year: str
    specialization: str

class ExperienceSchema(BaseModel):
    role: str
    company: str
    duration: str
    responsibilities: str

class ProjectSchema(BaseModel):
    name: str
    technologies: str
    description: str

class ResumeAnalysisResponse(BaseModel):
    resume_id: int
    filename: str
    candidate_info: CandidateInfoSchema
    education: List[EducationSchema]
    skills_by_category: Dict[str, List[str]]
    flat_skills: List[str]
    skill_count: int
    years_of_experience: float
    experience: List[ExperienceSchema]
    projects: List[ProjectSchema]
    certifications: List[str]
    resume_score: float
    score_breakdown: Dict[str, Any]
    recommendations: List[str]
