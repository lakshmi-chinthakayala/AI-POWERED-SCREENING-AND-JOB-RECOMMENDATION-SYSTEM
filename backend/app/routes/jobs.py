"""
Jobs API Routes.
Provides job listings, job detail lookup, and multi-attribute job search and filtering.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.database.connection import get_db
from backend.app.database.models import Job
from backend.app.schemas.job import JobResponse

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("", response_model=List[JobResponse])
def get_all_jobs(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieves all job listings."""
    jobs = db.query(Job).limit(limit).all()
    return jobs

@router.get("/search")
def search_jobs(
    q: Optional[str] = Query(None, description="Search keyword in title, company, or description"),
    location: Optional[str] = Query(None, description="Filter by location"),
    skill: Optional[str] = Query(None, description="Filter by required skill"),
    employment_type: Optional[str] = Query(None, description="Filter by employment type"),
    max_experience: Optional[float] = Query(None, description="Max required experience years"),
    db: Session = Depends(get_db)
):
    """Searches and filters job descriptions based on user criteria."""
    query = db.query(Job)
    
    if q:
        search_pattern = f"%{q.lower()}%"
        query = query.filter(
            (Job.title.ilike(search_pattern)) |
            (Job.company.ilike(search_pattern)) |
            (Job.description.ilike(search_pattern))
        )
        
    if location and location != "All":
        query = query.filter(Job.location.ilike(f"%{location}%"))
        
    if employment_type and employment_type != "All":
        query = query.filter(Job.employment_type.ilike(f"%{employment_type}%"))
        
    if max_experience is not None:
        query = query.filter(Job.experience_years <= max_experience)

    jobs = query.all()
    
    # Filter by required skill in Python if specified
    if skill and skill != "All":
        skill_clean = skill.lower()
        jobs = [
            j for j in jobs
            if any(skill_clean in s.lower() for s in (j.required_skills or []) + (j.preferred_skills or []))
        ]

    return {
        "count": len(jobs),
        "query": q,
        "jobs": [JobResponse.model_validate(j) for j in jobs]
    }

@router.get("/{job_id}", response_model=JobResponse)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    """Retrieves a single job by ID."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job record not found.")
    return job
