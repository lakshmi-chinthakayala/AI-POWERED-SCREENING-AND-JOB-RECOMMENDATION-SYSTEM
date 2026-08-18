"""
Dashboard Analytics API Routes.
Aggregates statistics and prepares dynamic chart datasets for the frontend dashboard.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.database.models import Resume, Job
from backend.app.ml.matcher import rank_recommended_jobs

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats/{resume_id}")
def get_dashboard_stats(resume_id: int, db: Session = Depends(get_db)):
    """
    Computes key metrics and chart dataset JSON for dashboard rendering.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume record not found.")

    parsed_resume = resume.parsed_json or {}
    if "raw_text" not in parsed_resume:
        parsed_resume["raw_text"] = resume.extracted_text

    # Compute skills category distribution
    skills_by_cat = parsed_resume.get("skills_by_category", {})
    skills_distribution = {cat: len(skills) for cat, skills in skills_by_cat.items() if len(skills) > 0}

    # Fetch top job recommendations
    db_jobs = db.query(Job).all()
    jobs_list = [
        {
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
        } for j in db_jobs
    ]

    ranked = rank_recommended_jobs(parsed_resume, jobs_list)
    top_5_jobs = ranked[:5]

    top_role = top_5_jobs[0]["job_title"] if top_5_jobs else "Software Specialist"
    top_match = top_5_jobs[0]["match_percentage"] if top_5_jobs else 0.0

    # Aggregate skill gaps across top 5 jobs
    missing_skill_counts = {}
    for j in top_5_jobs:
        for skill in j.get("missing_skills", []):
            missing_skill_counts[skill] = missing_skill_counts.get(skill, 0) + 1

    top_missing_skills = sorted(missing_skill_counts.items(), key=lambda x: x[1], reverse=True)[:6]

    return {
        "resume_score": resume.resume_score,
        "skills_count": parsed_resume.get("skill_count", 0),
        "projects_count": len(parsed_resume.get("projects", [])),
        "certifications_count": len(parsed_resume.get("certifications", [])),
        "years_of_experience": parsed_resume.get("years_of_experience", 0.0),
        "top_recommended_role": top_role,
        "top_match_percentage": top_match,
        "skills_distribution": skills_distribution,
        "top_matching_jobs": top_5_jobs,
        "skill_gap_summary": {
            "top_missing_skills": dict(top_missing_skills),
            "recommendations": top_5_jobs[0]["skill_gap_recommendations"] if top_5_jobs else []
        }
    }
