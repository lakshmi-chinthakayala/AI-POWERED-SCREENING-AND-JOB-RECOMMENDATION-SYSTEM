"""
Unit tests for NLP Preprocessing and Entity Extraction.
"""

import pytest
from backend.app.nlp.text_cleaner import clean_text, extract_email, extract_phone, preprocess_for_tfidf
from backend.app.nlp.skill_dictionary import ALL_SKILLS, get_canonical_skill_name
from backend.app.nlp.extractor import extract_skills, extract_candidate_name, extract_full_resume_data

def test_text_cleaning():
    raw_text = "  Hello   World!\t\nThis is a TEST resume 123.  "
    cleaned = clean_text(raw_text)
    assert "hello world!" in cleaned
    assert "\t" not in cleaned
    assert "\n" not in cleaned

def test_email_and_phone_extraction():
    sample_text = "Contact Alex Mercer at alex.mercer@example.com or call +1 (555) 019-2834 for inquiries."
    email = extract_email(sample_text)
    phone = extract_phone(sample_text)
    assert email == "alex.mercer@example.com"
    assert "555" in phone

def test_skill_dictionary_count():
    assert len(ALL_SKILLS) >= 100
    assert "python" in ALL_SKILLS
    assert "machine learning" in ALL_SKILLS
    assert "docker" in ALL_SKILLS
    assert "sql" in ALL_SKILLS

def test_skill_extraction_and_categorization():
    sample_resume = """
    Proficient in Python, Java, Machine Learning, PyTorch, Scikit-Learn, 
    FastAPI, Docker, SQL, and Pandas.
    """
    extracted = extract_skills(sample_resume)
    flat_skills = extracted["flat_skills"]
    categorized = extracted["categorized_skills"]
    
    assert "Python" in flat_skills
    assert "Machine Learning" in flat_skills
    assert "FastAPI" in flat_skills
    assert "Docker" in flat_skills
    
    assert "Python" in categorized["Programming"]
    assert "Machine Learning" in categorized["AI / ML"]
    assert "Docker" in categorized["Cloud & DevOps"]

def test_full_resume_extraction():
    sample_text = """
    Priya Sharma
    Email: priya.sharma@example.com | Phone: +1 (555) 432-8765
    Education: B.Tech in Artificial Intelligence (2024)
    Skills: Python, Scikit-Learn, Machine Learning, SQL, Pandas, Docker
    Projects: Customer Churn Model using XGBoost
    Certifications: AWS Certified Machine Learning
    """
    data = extract_full_resume_data(sample_text)
    assert data["candidate_info"]["name"] == "Priya Sharma"
    assert data["candidate_info"]["email"] == "priya.sharma@example.com"
    assert len(data["flat_skills"]) >= 5
    assert data["education"][0]["degree"] is not None
