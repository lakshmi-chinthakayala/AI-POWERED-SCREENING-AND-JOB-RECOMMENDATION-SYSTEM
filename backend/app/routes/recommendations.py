"""
Job Recommendation & Skill Gap API Routes.
Runs TF-IDF + Cosine Similarity + Skill Matching engine to rank suitable jobs
and generate skill gap recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import Resume, Job
from backend.app.ml.matcher import rank_recommended_jobs

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/{resume_id}")
def get_job_recommendations(resume_id: int, top_n: int = 10, db: Session = Depends(get_db)):
    """
    Ranks suitable jobs for a candidate resume based on TF-IDF text similarity,
    skill overlap ratio, experience match, and education match.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume record not found.")

    parsed_resume = resume.parsed_json or {}
    if "raw_text" not in parsed_resume:
        parsed_resume["raw_text"] = resume.extracted_text

    # Fetch all jobs from database
    db_jobs = db.query(Job).all()
    if not db_jobs:
        raise HTTPException(status_code=404, detail="No job listings found in database.")

    jobs_list = []
    for j in db_jobs:
        jobs_list.append({
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "employment_type": j.employment_type,
            "experience_years": j.experience_years,
            "education": j.education,
            "description": j.description,
            "required_skills": j.required_skills or [],
            "preferred_skills": j.preferred_skills or [],
            "salary": j.salary
        })

    # Execute ranking algorithm
    ranked_results = rank_recommended_jobs(parsed_resume, jobs_list)
    top_recommendations = ranked_results[:top_n]

    top_role = top_recommendations[0]["job_title"] if top_recommendations else "AI / Software Specialist"
    top_match = top_recommendations[0]["match_percentage"] if top_recommendations else 0.0

    return {
        "resume_id": resume.id,
        "candidate_name": resume.candidate_name,
        "total_jobs_evaluated": len(db_jobs),
        "top_recommended_role": top_role,
        "top_match_percentage": top_match,
        "recommendations": top_recommendations
    }
