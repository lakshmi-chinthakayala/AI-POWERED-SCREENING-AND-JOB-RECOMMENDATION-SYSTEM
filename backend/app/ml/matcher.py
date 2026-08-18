"""
Job Matching & Recommendation Engine.
Calculates realistic match scores between Candidate Resume and Job Descriptions using:
  - TF-IDF Vectorization & Cosine Similarity (45%)
  - Skill Overlap Match Ratio (35%)
  - Experience Requirement Match (10%)
  - Education Requirement Match (10%)
Provides Skill Gap Analysis and actionable learning recommendations.
"""

from typing import Dict, Any, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.nlp.text_cleaner import preprocess_for_tfidf
from backend.app.nlp.skill_dictionary import get_canonical_skill_name

# Curated Learning Resource Database for Skill Gap Analysis
SKILL_LEARNING_RECOMMENDATIONS = {
    "docker": "Learn Docker fundamentals, containerization, image creation, multi-stage builds, and Docker Compose.",
    "kubernetes": "Study Kubernetes architecture, pods, deployments, services, and cluster orchestration.",
    "aws": "Explore AWS core services: EC2, S3, Lambda, IAM, and SageMaker for ML deployments.",
    "gcp": "Learn Google Cloud Platform components, BigQuery, Vertex AI, and Cloud Run.",
    "azure": "Master Azure AI services, Azure ML studio, Blob storage, and App Services.",
    "pytorch": "Practice PyTorch tensors, autograd, neural network modules, CUDA GPU acceleration, and Torchvision.",
    "tensorflow": "Learn TensorFlow 2.x, Keras Sequential API, custom layers, and TF Lite deployment.",
    "transformers": "Study Hugging Face Transformers library, BERT fine-tuning, and LLM tokenization.",
    "llm": "Understand Large Language Model architectures, RAG pipelines, fine-tuning, and LangChain integration.",
    "langchain": "Build LLM applications using LangChain, prompt templates, memory, and vector indices.",
    "opencv": "Master OpenCV image processing, feature detection, object tracking, and video stream manipulation.",
    "yolo": "Learn YOLO object detection models, custom dataset annotation, and real-time detection inference.",
    "sql": "Practice advanced SQL queries, JOINs, window functions, indexing, and query performance tuning.",
    "mongodb": "Learn MongoDB document schema design, aggregation pipelines, and indexing.",
    "fastapi": "Master FastAPI async endpoint development, Pydantic data validation, and OpenAPI documentation.",
    "react": "Study React hooks, state management, component lifecycles, and API integration.",
    "tableau": "Learn Tableau dashboard design, data modeling, calculated fields, and interactive analytics.",
    "power bi": "Master Power BI data modeling, DAX expressions, interactive reports, and data transformation.",
    "mlops": "Explore MLOps tools: MLflow model tracking, DVC data versioning, and automated CI/CD for ML models.",
    "ci/cd": "Study CI/CD pipelines with GitHub Actions, automated testing, and deployment workflows."
}

DEFAULT_LEARNING_ADVICE = "Review documentation, complete hands-on mini projects, and practice implementing core real-world applications."

def compute_tfidf_similarity(resume_text: str, job_text: str) -> float:
    """Calculates Cosine Similarity between resume text and job description via TF-IDF."""
    clean_resume = preprocess_for_tfidf(resume_text)
    clean_job = preprocess_for_tfidf(job_text)
    
    if not clean_resume or not clean_job:
        return 0.0
        
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_job])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(sim)
    except Exception:
        return 0.0

def match_resume_to_job(resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes precise multi-factor match score and skill gap analysis.
    Formula:
      Final Match = (0.45 * Text Similarity) + (0.35 * Skill Match) + (0.10 * Experience Match) + (0.10 * Education Match)
    """
    resume_text = resume_data.get("raw_text", "")
    job_description = f"{job_data.get('title', '')} {job_data.get('description', '')} {' '.join(job_data.get('required_skills', []))} {' '.join(job_data.get('preferred_skills', []))}"
    
    # 1. Text Similarity (45% weight)
    similarity = compute_tfidf_similarity(resume_text, job_description)
    text_similarity_score = min(100.0, similarity * 100.0 * 1.6) # Scaled for practical overlap
    
    # 2. Skill Match (35% weight)
    candidate_skills = set([s.lower() for s in resume_data.get("flat_skills", [])])
    required_skills = [s.lower() for s in job_data.get("required_skills", [])]
    preferred_skills = [s.lower() for s in job_data.get("preferred_skills", [])]
    all_job_skills = list(set(required_skills + preferred_skills))
    
    if all_job_skills:
        matching_skills_raw = [s for s in all_job_skills if s in candidate_skills]
        missing_skills_raw = [s for s in all_job_skills if s not in candidate_skills]
        skill_match_ratio = len(matching_skills_raw) / len(all_job_skills)
    else:
        matching_skills_raw = list(candidate_skills)[:5]
        missing_skills_raw = []
        skill_match_ratio = 0.70

    skill_match_score = skill_match_ratio * 100.0

    # 3. Experience Match (10% weight)
    cand_exp = resume_data.get("years_of_experience", 0.0)
    req_exp = job_data.get("experience_years", 1.0)
    
    if cand_exp >= req_exp:
        exp_score = 100.0
    elif cand_exp > 0:
        exp_score = (cand_exp / max(1.0, req_exp)) * 100.0
    else:
        exp_score = 50.0

    # 4. Education Match (10% weight)
    candidate_edu = resume_data.get("education", [])
    edu_score = 90.0 if len(candidate_edu) > 0 else 60.0

    # Compute final weighted match score
    final_match_percentage = round(
        (text_similarity_score * 0.45) +
        (skill_match_score * 0.35) +
        (exp_score * 0.10) +
        (edu_score * 0.10),
        1
    )
    
    # Ensure realistic range 35% - 98%
    final_match_percentage = max(35.0, min(98.0, final_match_percentage))

    # Format matching and missing skills canonically
    matching_skills = [get_canonical_skill_name(s) for s in matching_skills_raw]
    missing_skills = [get_canonical_skill_name(s) for s in missing_skills_raw]

    # Generate skill gap learning recommendations
    skill_gap_recommendations = []
    for skill_raw in missing_skills_raw:
        skill_clean = skill_raw.lower()
        rec_text = SKILL_LEARNING_RECOMMENDATIONS.get(skill_clean, f"Master {get_canonical_skill_name(skill_raw)} fundamentals: {DEFAULT_LEARNING_ADVICE}")
        skill_gap_recommendations.append({
            "skill": get_canonical_skill_name(skill_raw),
            "recommendation": rec_text
        })

    return {
        "job_id": job_data.get("id"),
        "job_title": job_data.get("title"),
        "company": job_data.get("company"),
        "location": job_data.get("location"),
        "employment_type": job_data.get("employment_type", "Full-time"),
        "salary": job_data.get("salary", "$80,000 - $120,000"),
        "match_percentage": final_match_percentage,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "skill_gap_recommendations": skill_gap_recommendations,
        "score_details": {
            "text_similarity": round(text_similarity_score, 1),
            "skill_match": round(skill_match_score, 1),
            "experience_match": round(exp_score, 1),
            "education_match": round(edu_score, 1)
        }
    }

def rank_recommended_jobs(resume_data: Dict[str, Any], jobs_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Calculates match scores for all jobs in dataset and ranks them from highest match to lowest."""
    results = []
    for job in jobs_list:
        match_result = match_resume_to_job(resume_data, job)
        results.append(match_result)
        
    # Sort descending by match percentage
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results
