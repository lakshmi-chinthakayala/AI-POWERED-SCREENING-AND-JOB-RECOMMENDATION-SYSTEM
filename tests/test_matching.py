"""
Unit tests for TF-IDF Similarity, Resume Scoring, and Multi-Factor Job Matching.
"""

import pytest
from backend.app.ml.matcher import compute_tfidf_similarity, match_resume_to_job, rank_recommended_jobs
from backend.app.ml.scorer import calculate_resume_score

def test_tfidf_similarity_calculation():
    text1 = "Python developer experienced in Machine Learning, Scikit-Learn, PyTorch, and FastAPI."
    text2 = "Looking for an AI Engineer with Python, Machine Learning, PyTorch, and FastAPI backend experience."
    similarity = compute_tfidf_similarity(text1, text2)
    assert similarity > 0.2

def test_resume_scoring():
    parsed_data = {
        "flat_skills": ["Python", "Machine Learning", "PyTorch", "FastAPI", "Docker", "SQL", "Pandas", "Scikit-Learn", "NLTK", "OpenCV"],
        "years_of_experience": 2.0,
        "experience": [{"role": "AI Engineer Intern"}],
        "projects": [{"name": "AI Resume Screener"}, {"name": "CNN Classifier"}],
        "education": [{"degree": "B.Tech in CS"}],
        "certifications": ["TensorFlow Developer Certificate"],
        "candidate_info": {
            "name": "Alex Mercer",
            "email": "alex@example.com",
            "phone": "+1 (555) 019-2834",
            "linkedin": "https://linkedin.com/in/alex",
            "github": "https://github.com/alex"
        }
    }
    score_result = calculate_resume_score(parsed_data)
    assert 70.0 <= score_result["overall_score"] <= 100.0
    assert "breakdown" in score_result

def test_job_matching_and_ranking():
    resume_data = {
        "raw_text": "Python developer with Machine Learning, Scikit-Learn, SQL, and Docker experience.",
        "flat_skills": ["Python", "Machine Learning", "Scikit-Learn", "SQL", "Docker"],
        "years_of_experience": 2.0,
        "education": [{"degree": "B.Tech in CS"}]
    }

    job1 = {
        "id": 1,
        "title": "Machine Learning Engineer",
        "company": "NeuralMetrics",
        "location": "San Francisco",
        "description": "Seeking ML Engineer skilled in Python, Machine Learning, Scikit-Learn, SQL, and Docker.",
        "required_skills": ["Python", "Machine Learning", "Scikit-Learn", "SQL", "Docker"],
        "preferred_skills": ["Kubernetes", "AWS"]
    }

    job2 = {
        "id": 2,
        "title": "React Developer",
        "company": "PixelCraft",
        "location": "Remote",
        "description": "Seeking React Frontend Developer skilled in JavaScript, HTML, CSS, React, and Redux.",
        "required_skills": ["JavaScript", "HTML", "CSS", "React", "Redux"],
        "preferred_skills": ["TypeScript"]
    }

    ranked = rank_recommended_jobs(resume_data, [job1, job2])
    assert len(ranked) == 2
    assert ranked[0]["job_title"] == "Machine Learning Engineer"
    assert ranked[0]["match_percentage"] > ranked[1]["match_percentage"]
    assert "Docker" in ranked[0]["matching_skills"]
    assert "AWS" in ranked[0]["missing_skills"]
