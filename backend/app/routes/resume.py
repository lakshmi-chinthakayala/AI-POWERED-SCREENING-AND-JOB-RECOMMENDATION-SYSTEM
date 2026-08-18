"""
Resume API Routes.
Handles resume upload, PDF/DOCX parsing, NLP entity extraction, scoring, and analysis retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional
import json

from backend.app.database.connection import get_db
from backend.app.database.models import Resume, User
from backend.app.services.pdf_parser import extract_text_from_pdf
from backend.app.services.docx_parser import extract_text_from_docx
from backend.app.nlp.extractor import extract_full_resume_data
from backend.app.ml.scorer import calculate_resume_score
from backend.app.schemas.resume import ResumeAnalysisResponse

router = APIRouter(prefix="/api/resume", tags=["Resume"])

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Validates uploaded resume (PDF/DOCX), extracts text content using NLP,
    calculates Resume Score (0-100), and stores parsed data in the database.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename cannot be empty.")
        
    filename_lower = file.filename.lower()
    if not any(filename_lower.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a PDF (.pdf) or Word document (.docx)."
        )

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty (0 bytes).")
        
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File size exceeds maximum limit of 10MB.")

    # 1. Extract raw text based on extension
    if filename_lower.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_bytes)
    else:
        extracted_text = file_bytes.decode("utf-8", errors="ignore")

    if not extracted_text or len(extracted_text.strip()) < 20:
        raise HTTPException(
            status_code=422,
            detail="Unable to extract text content from document. Please ensure file is not password protected or corrupted."
        )

    # 2. Extract structured NLP candidate data
    parsed_data = extract_full_resume_data(extracted_text)
    
    # 3. Calculate Resume Score & Recommendations
    score_result = calculate_resume_score(parsed_data)
    
    parsed_data["resume_score"] = score_result["overall_score"]
    parsed_data["score_breakdown"] = score_result["breakdown"]
    parsed_data["recommendations"] = score_result["recommendations"]

    # 4. Save to Database
    candidate_info = parsed_data.get("candidate_info", {})
    new_resume = Resume(
        user_id=user_id,
        filename=file.filename,
        extracted_text=extracted_text,
        candidate_name=candidate_info.get("name"),
        candidate_email=candidate_info.get("email"),
        candidate_phone=candidate_info.get("phone"),
        candidate_location=candidate_info.get("location"),
        resume_score=score_result["overall_score"],
        parsed_json=parsed_data
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "message": "Resume analyzed successfully",
        "resume_id": new_resume.id,
        "filename": new_resume.filename,
        "resume_score": new_resume.resume_score,
        "data": parsed_data
    }

@router.get("/{resume_id}")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Retrieves resume record by ID."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume record not found.")
    return resume

@router.get("/{resume_id}/analysis")
def get_resume_analysis(resume_id: int, db: Session = Depends(get_db)):
    """Retrieves structured NLP analysis result for a resume."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume record not found.")
        
    data = resume.parsed_json or {}
    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "candidate_info": data.get("candidate_info", {}),
        "education": data.get("education", []),
        "skills_by_category": data.get("skills_by_category", {}),
        "flat_skills": data.get("flat_skills", []),
        "skill_count": data.get("skill_count", 0),
        "years_of_experience": data.get("years_of_experience", 0.0),
        "experience": data.get("experience", []),
        "projects": data.get("projects", []),
        "certifications": data.get("certifications", []),
        "resume_score": resume.resume_score,
        "score_breakdown": data.get("score_breakdown", {}),
        "recommendations": data.get("recommendations", [])
    }
