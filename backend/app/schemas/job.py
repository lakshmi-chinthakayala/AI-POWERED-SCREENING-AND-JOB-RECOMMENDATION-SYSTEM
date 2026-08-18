"""
Pydantic Schemas for Jobs, Recommendations, and Skill Gap Analysis.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    employment_type: str
    experience_years: float
    education: str
    description: str
    required_skills: List[str]
    preferred_skills: List[str]
    salary: str
    application_url: str

    class Config:
        from_attributes = True

class SkillRecommendationItem(BaseModel):
    skill: str
    recommendation: str

class JobMatchResponse(BaseModel):
    job_id: int
    job_title: str
    company: str
    location: str
    employment_type: str
    salary: str
    match_percentage: float
    matching_skills: List[str]
    missing_skills: List[str]
    skill_gap_recommendations: List[SkillRecommendationItem]
    score_details: Dict[str, float]

class RecommendationListResponse(BaseModel):
    resume_id: int
    total_jobs_evaluated: int
    top_recommended_role: str
    top_match_percentage: float
    recommendations: List[JobMatchResponse]

class DashboardStatsResponse(BaseModel):
    resume_score: float
    skills_count: int
    projects_count: int
    certifications_count: int
    years_of_experience: float
    top_recommended_role: str
    top_match_percentage: float
    skills_distribution: Dict[str, int]
    top_matching_jobs: List[Dict[str, Any]]
    skill_gap_summary: Dict[str, Any]
