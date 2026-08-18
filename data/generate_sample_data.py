"""
Sample Data Generation and Database Seeding Script.
Initializes SQLite database, inserts 30+ jobs, 100+ skills, and generates
10 synthetic candidate resumes (.pdf & .docx) in data/sample_resumes/.
"""

import os
import json
import docx
import fitz  # PyMuPDF

from backend.app.database.connection import engine, SessionLocal, Base
from backend.app.database.models import User, Job, Skill, Resume
from backend.app.nlp.skill_dictionary import SKILL_CATEGORIES
from backend.app.nlp.extractor import extract_full_resume_data
from backend.app.ml.scorer import calculate_resume_score
from backend.app.utils.auth_utils import hash_password

SAMPLE_RESUMES_DIR = os.path.join(os.path.dirname(__file__), "sample_resumes")
JOBS_JSON_PATH = os.path.join(os.path.dirname(__file__), "jobs.json")

SAMPLE_PROFILES = [
    {
        "filename": "sample_ai_engineer.pdf",
        "name": "Alex Mercer",
        "email": "alex.mercer@example.com",
        "title": "AI Engineer Candidate",
        "text": """
Alex Mercer
Email: alex.mercer@example.com | Phone: +1 (555) 019-2834 | Location: Bangalore, India
LinkedIn: linkedin.com/in/alex-mercer-ai | GitHub: github.com/alex-mercer-ai

PROFESSIONAL SUMMARY
Innovative Artificial Intelligence Engineer with 2 years of experience developing machine learning models, deep neural networks, and scalable FastAPI backend services.

EDUCATION
B.Tech in Computer Science & Engineering (Specialization in Artificial Intelligence)
Tech University of Engineering | 2024 | GPA: 3.9/4.0

TECHNICAL SKILLS
- Programming: Python, Java, C++, JavaScript
- AI / ML: Machine Learning, Deep Learning, Scikit-Learn, TensorFlow, PyTorch, Keras, Neural Networks
- NLP & Vision: NLP, spaCy, NLTK, OpenCV, CNN
- Cloud & Data: Docker, AWS, SQL, PostgreSQL, Pandas, NumPy, FastAPI, Git

EXPERIENCE
AI Engineer Intern | Apex AI Systems | 2023 - Present
- Designed deep neural network architectures using PyTorch and TensorFlow for pattern classification.
- Built async FastAPI REST endpoints for real-time model inference and deployed containerized services using Docker.
- Optimized feature extraction pipelines reducing inference latency by 35%.

PROJECTS
AI Resume Screening & Job Recommendation System
- Built end-to-end NLP resume parser with TF-IDF similarity score calculation and skill-gap recommendations.
- Technologies: Python, FastAPI, Scikit-Learn, PyMuPDF, SQLite, React

Deep Learning Image Classifier
- Developed a CNN image classifier using PyTorch achieving 94% validation accuracy on custom dataset.

CERTIFICATIONS
- Machine Learning Specialization - DeepLearning.AI
- TensorFlow Developer Certificate - Google
"""
    },
    {
        "filename": "sample_ml_engineer.docx",
        "name": "Priya Sharma",
        "email": "priya.sharma@example.com",
        "title": "Machine Learning Candidate",
        "text": """
Priya Sharma
Email: priya.sharma@example.com | Phone: +1 (555) 432-8765 | Location: San Francisco, CA
LinkedIn: linkedin.com/in/priya-sharma-ml | GitHub: github.com/priya-sharma-ml

OBJECTIVE
Motivated Machine Learning Engineer focused on predictive modeling, hyperparameter optimization, and data engineering.

EDUCATION
B.Tech in Artificial Intelligence & Data Science
National Institute of Technology | 2024

TECHNICAL SKILLS
- Machine Learning: Scikit-Learn, XGBoost, Random Forest, SVM, Decision Trees, Gradient Boosting, Hyperparameter Tuning
- Data Science: Python, SQL, Pandas, NumPy, SciPy, Matplotlib, Seaborn
- Cloud & MLOps: Docker, Git, Linux, MLOps, MLflow

EXPERIENCE
ML Developer Intern | NeuralMetrics Labs | 2023 - 2024
- Built tabular classification and regression pipelines using XGBoost and Scikit-Learn.
- Performed extensive exploratory data analysis and feature engineering on 500k+ record datasets.
- Tracked model experiments using MLflow and deployed Docker containers to AWS.

PROJECTS
Predictive Customer Churn Analytics
- Developed churn prediction model with XGBoost achieving 89% AUC-ROC score.
- Technologies: Python, Pandas, XGBoost, Scikit-Learn, Matplotlib

Automated Data Preprocessing Pipeline
- Engineered reusable data cleaning and outlier detection modules in Python.

CERTIFICATIONS
- AWS Certified Machine Learning - Specialty
- Python for Data Science and AI - IBM
"""
    },
    {
        "filename": "sample_data_scientist.pdf",
        "name": "David Chen",
        "email": "david.chen@example.com",
        "title": "Data Scientist Candidate",
        "text": """
David Chen
Email: david.chen@example.com | Phone: +1 (555) 987-6543 | Location: New York, NY
LinkedIn: linkedin.com/in/david-chen-ds | GitHub: github.com/david-chen-ds

SUMMARY
Data Scientist with background in statistics, SQL analytics, data visualization, and predictive modeling.

EDUCATION
B.Sc in Statistics & Computer Science | Columbia University | 2024

TECHNICAL SKILLS
- Analytics & Stats: SQL, Python, Pandas, NumPy, Statistics, Data Analysis, Exploratory Data Analysis, R
- Visualization: Power BI, Tableau, Matplotlib, Seaborn, Excel
- ML & DB: Scikit-Learn, PostgreSQL, MySQL, SQLite, Git

EXPERIENCE
Data Analyst Intern | DataPulse Analytics | 2023 - 2024
- Authored complex SQL queries and window functions to aggregate key performance indicators.
- Created interactive executive Power BI dashboards displaying monthly sales forecasts.

PROJECTS
Sales Forecasting & Time Series Model
- Applied ARIMA and Prophet models to predict quarterly retail sales trends.
- Technologies: Python, Pandas, Statsmodels, Power BI

Statistical Customer Segmentation
- Implemented K-Means clustering in Python to segment users into distinct personas.

CERTIFICATIONS
- Google Data Analytics Professional Certificate
- Microsoft Certified: Power BI Data Analyst Associate
"""
    },
    {
        "filename": "sample_python_dev.docx",
        "name": "Sarah Jenkins",
        "email": "sarah.j@example.com",
        "title": "Python Backend Candidate",
        "text": """
Sarah Jenkins
Email: sarah.j@example.com | Phone: +1 (555) 234-5678 | Location: Austin, TX
LinkedIn: linkedin.com/in/sarah-jenkins-dev | GitHub: github.com/sarah-jenkins-dev

SUMMARY
Backend Software Developer specializing in Python microservices, FastAPI REST APIs, and containerized deployment.

EDUCATION
B.Tech in Computer Science & Engineering | University of Texas | 2024

TECHNICAL SKILLS
- Languages & Web: Python, FastAPI, Flask, Django, REST API, HTML, CSS, JavaScript
- Databases: PostgreSQL, SQLite, MySQL, Redis, SQLAlchemy
- DevOps: Docker, Git, Linux, Bash Scripting, CI/CD, AWS

EXPERIENCE
Python Backend Developer Intern | PyCloud Systems | 2023 - 2024
- Built async REST APIs using FastAPI and Pydantic validation schemas.
- Integrated SQLAlchemy ORM with PostgreSQL database and configured Docker Compose environments.

PROJECTS
Microservice Authentication & Payment Gateway
- Developed JWT authentication middleware and integrated Stripe REST API.
- Technologies: Python, FastAPI, PostgreSQL, Docker, Redis

Task Scheduling Queue System
- Implemented async background tasks using Celery and Redis message broker.

CERTIFICATIONS
- Certified Entry-Level Python Programmer (PCEP)
- Docker Essentials: Developer Certificate
"""
    },
    {
        "filename": "sample_nlp_engineer.pdf",
        "name": "Rohan Gupta",
        "email": "rohan.gupta@example.com",
        "title": "NLP & LLM Candidate",
        "text": """
Rohan Gupta
Email: rohan.gupta@example.com | Phone: +1 (555) 876-5432 | Location: Bangalore, India
LinkedIn: linkedin.com/in/rohan-gupta-nlp | GitHub: github.com/rohan-gupta-nlp

SUMMARY
NLP Engineer focused on Large Language Models, Transformer fine-tuning, RAG architecture, and text parsing pipelines.

EDUCATION
B.Tech in Computer Science (Artificial Intelligence) | IIT Bangalore | 2024

TECHNICAL SKILLS
- NLP & AI: NLP, spaCy, NLTK, Transformers, BERT, Hugging Face, LLM, Large Language Models, LangChain, Tokenization, Named Entity Recognition
- Deep Learning: PyTorch, TensorFlow, Scikit-Learn
- Backend: Python, FastAPI, Docker, SQL, Vector Databases, Git

EXPERIENCE
NLP Research Intern | LingoAI Technologies | 2023 - 2024
- Built Named Entity Recognition (NER) models using spaCy and BERT fine-tuning.
- Engineered Retrieval-Augmented Generation (RAG) pipelines with LangChain and vector databases.

PROJECTS
Automated Resume Skill Extractor
- Built custom NLP extraction engine identifying 100+ technical skills from raw resume text.
- Technologies: Python, spaCy, NLTK, Transformers, FastAPI

Multilingual Sentiment Classifier
- Fine-tuned BERT model for multi-class sentiment detection with 91% F1-score.

CERTIFICATIONS
- Natural Language Processing Specialization - DeepLearning.AI
"""
    },
    {
        "filename": "sample_cv_engineer.pdf",
        "name": "Elena Rostova",
        "email": "elena.rostova@example.com",
        "title": "Computer Vision Candidate",
        "text": """
Elena Rostova
Email: elena.rostova@example.com | Phone: +1 (555) 345-6789 | Location: Boston, MA
LinkedIn: linkedin.com/in/elena-rostova-cv | GitHub: github.com/elena-rostova-cv

SUMMARY
Computer Vision Developer experienced in real-time object detection, OpenCV, CNNs, and YOLO models.

EDUCATION
B.Tech in Computer Engineering | Boston Tech | 2024

TECHNICAL SKILLS
- Vision & AI: Computer Vision, OpenCV, CNN, Convolutional Neural Networks, YOLO, Object Detection, Image Processing, PyTorch
- Core: Python, C++, NumPy, Matplotlib, Docker, Git, Linux

EXPERIENCE
Vision Systems Intern | Visionary Robotics | 2023 - 2024
- Trained YOLOv8 object detection models for real-time video stream inspection.
- Implemented OpenCV spatial transformation and edge detection algorithms.

PROJECTS
Real-Time Object Detection & Tracking System
- Implemented YOLOv8 detector processing 60 FPS video feeds with OpenCV.
- Technologies: Python, OpenCV, YOLO, PyTorch, CUDA

Autonomous Lane Keeping Prototype
- Built CNN model in PyTorch for camera-based steering control.

CERTIFICATIONS
- Deep Learning for Computer Vision - Coursera
"""
    },
    {
        "filename": "sample_fullstack_dev.docx",
        "name": "Michael Chang",
        "email": "michael.chang@example.com",
        "title": "Full Stack Web Candidate",
        "text": """
Michael Chang
Email: michael.chang@example.com | Phone: +1 (555) 654-3210 | Location: Seattle, WA
LinkedIn: linkedin.com/in/michael-chang-fs | GitHub: github.com/michael-chang-fs

SUMMARY
Full Stack Web Developer proficient in React, JavaScript, HTML5, CSS3, Python, and FastAPI backend development.

EDUCATION
B.Tech in Information Technology | Washington State University | 2024

TECHNICAL SKILLS
- Frontend: JavaScript, React, HTML, HTML5, CSS, CSS3, Tailwind CSS, Bootstrap
- Backend: Python, FastAPI, Node.js, REST API, SQL, PostgreSQL, SQLite
- Tools: Git, GitHub, Docker, JSON

EXPERIENCE
Full Stack Developer Intern | OmniStack Cloud | 2023 - 2024
- Built responsive user dashboards in React and Tailwind CSS.
- Developed scalable REST APIs using FastAPI and integrated SQLite database schemas.

PROJECTS
Interactive SaaS Dashboard Platform
- Created full-stack web app with authentication, dark mode UI, and Chart.js metrics.
- Technologies: React, JavaScript, FastAPI, Python, SQLite, Tailwind CSS

E-Commerce Web Application
- Built React frontend with shopping cart state management and REST API backend.

CERTIFICATIONS
- Meta Front-End Developer Professional Certificate
"""
    },
    {
        "filename": "sample_data_analyst.pdf",
        "name": "Samantha Reed",
        "email": "samantha.reed@example.com",
        "title": "Data Analyst Candidate",
        "text": """
Samantha Reed
Email: samantha.reed@example.com | Phone: +1 (555) 789-0123 | Location: Remote
LinkedIn: linkedin.com/in/samantha-reed-da | GitHub: github.com/samantha-reed-da

SUMMARY
Detail-oriented Data Analyst proficient in SQL query writing, Power BI dashboard generation, and Excel data modeling.

EDUCATION
B.Sc in Data Analytics | State University | 2024

TECHNICAL SKILLS
- Analytics & DB: SQL, PostgreSQL, Data Analysis, Exploratory Data Analysis, Excel
- Visualization: Power BI, Tableau, Data Visualization, Matplotlib
- Code: Python, Pandas, NumPy, Git

EXPERIENCE
Junior Data Analyst | InsightTech Solutions | 2023 - Present
- Created automated weekly performance reports using SQL and Power BI.
- Cleaned and normalized client relational datasets eliminating duplicates.

PROJECTS
Executive Business Intelligence Dashboard
- Constructed Power BI dashboard connecting 5 SQL database tables for revenue analysis.

Customer Satisfaction Survey Analysis
- Conducted sentiment and statistical analysis on survey feedback data using Pandas.

CERTIFICATIONS
- Google Data Analytics Certificate
"""
    },
    {
        "filename": "sample_ai_intern.pdf",
        "name": "Aryan Patel",
        "email": "aryan.patel@example.com",
        "title": "AI Final Year Student",
        "text": """
Aryan Patel
Email: aryan.patel@example.com | Phone: +1 (555) 890-1234 | Location: Bangalore, India
LinkedIn: linkedin.com/in/aryan-patel-ai | GitHub: github.com/aryan-patel-ai

OBJECTIVE
Final-year B.Tech Artificial Intelligence student seeking an AI / ML Internship to apply machine learning skills.

EDUCATION
B.Tech in Artificial Intelligence & Machine Learning
VTU Engineering College | Expected Graduation: 2024 | GPA: 3.8/4.0

TECHNICAL SKILLS
- Programming: Python, C++, Java, Data Structures
- AI / ML: Machine Learning, Scikit-Learn, Pandas, NumPy, Matplotlib, Neural Networks
- Web & Tools: HTML, CSS, FastAPI, SQL, Git, GitHub

ACADEMIC PROJECTS
B.Tech Final Year Project: AI Resume Screening & Recommendation System
- Designed an automated resume analysis engine with TF-IDF similarity calculation and skill gap advice.
- Technologies: Python, Scikit-Learn, FastAPI, React, SQLite

Handwritten Digit Classifier
- Implemented a baseline neural network in PyTorch achieving 98% accuracy on MNIST dataset.

CERTIFICATIONS
- Python for Data Science - NPTEL
"""
    },
    {
        "filename": "sample_backend_dev.docx",
        "name": "Jason Vance",
        "email": "jason.vance@example.com",
        "title": "Backend Microservices Candidate",
        "text": """
Jason Vance
Email: jason.vance@example.com | Phone: +1 (555) 901-2345 | Location: Chicago, IL
LinkedIn: linkedin.com/in/jason-vance-be | GitHub: github.com/jason-vance-be

SUMMARY
Backend Software Developer skilled in Python, Java, REST API design, PostgreSQL, and Docker containerization.

EDUCATION
B.Tech in Computer Science | Illinois Tech | 2024

TECHNICAL SKILLS
- Languages: Python, Java, C++, SQL
- Frameworks & DB: FastAPI, Flask, PostgreSQL, Redis, SQLite, SQLAlchemy, REST API
- DevOps: Docker, Git, Linux, CI/CD, Bash

EXPERIENCE
Software Engineering Intern | ServerScale Systems | 2023 - 2024
- Built high-speed API endpoints and integrated Redis caching layer.
- Wrote automated unit tests with Pytest achieving 88% code coverage.

PROJECTS
Distributed Rate Limiter Microservice
- Designed token-bucket rate limiter API using Redis and FastAPI.

API Gateway & Load Balancer Simulator
- Implemented load balancing logic in Python with Docker deployment scripts.

CERTIFICATIONS
- Oracle Certified Associate, Java SE Programmer
"""
    }
]

def generate_pdf_resume(filepath: str, text: str):
    """Generates a text-extractable PDF using PyMuPDF (fitz)."""
    doc = fitz.open()
    page = doc.new_page()
    rect = fitz.Rect(50, 50, 550, 800)
    page.insert_textbox(rect, text, fontsize=10, fontname="helv")
    doc.save(filepath)
    doc.close()

def generate_docx_resume(filepath: str, text: str):
    """Generates a text-extractable DOCX file using python-docx."""
    doc = docx.Document()
    for paragraph_str in text.strip().split('\n'):
        if paragraph_str.strip():
            doc.add_paragraph(paragraph_str.strip())
    doc.save(filepath)

def seed_database_and_resumes():
    """Builds database, loads 30+ jobs, 100+ skills, and generates sample resume files."""
    os.makedirs(SAMPLE_RESUMES_DIR, exist_ok=True)
    
    # 1. Create SQLite database tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 2. Seed Default User
    demo_user = db.query(User).filter(User.email == "demo@example.com").first()
    if not demo_user:
        demo_user = User(
            name="AI Project Demo User",
            email="demo@example.com",
            hashed_password=hash_password("demopassword123")
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

    # 3. Seed Skills
    for cat, skill_list in SKILL_CATEGORIES.items():
        for sk in skill_list:
            existing = db.query(Skill).filter(Skill.name == sk).first()
            if not existing:
                db.add(Skill(name=sk, category=cat))
    db.commit()

    # 4. Seed Jobs from jobs.json
    if os.path.exists(JOBS_JSON_PATH):
        with open(JOBS_JSON_PATH, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
            
        for j in jobs_data:
            existing_job = db.query(Job).filter(Job.id == j["id"]).first()
            if not existing_job:
                db.add(Job(
                    id=j["id"],
                    title=j["title"],
                    company=j["company"],
                    location=j["location"],
                    employment_type=j.get("employment_type", "Full-time"),
                    experience_years=j.get("experience_years", 1.0),
                    education=j.get("education", "B.Tech in CS/AI"),
                    description=j["description"],
                    required_skills=j["required_skills"],
                    preferred_skills=j.get("preferred_skills", []),
                    salary=j.get("salary", "$80,000 - $120,000")
                ))
        db.commit()

    # 5. Generate Sample Resume Files & Seed Resumes Table
    print("[Seed Data] Generating sample PDF and DOCX resume files...")
    for prof in SAMPLE_PROFILES:
        filepath = os.path.join(SAMPLE_RESUMES_DIR, prof["filename"])
        if prof["filename"].endswith(".pdf"):
            generate_pdf_resume(filepath, prof["text"])
        elif prof["filename"].endswith(".docx"):
            generate_docx_resume(filepath, prof["text"])
            
        # Parse data using NLP extractor
        parsed = extract_full_resume_data(prof["text"])
        score_res = calculate_resume_score(parsed)
        parsed["resume_score"] = score_res["overall_score"]
        parsed["score_breakdown"] = score_res["breakdown"]
        parsed["recommendations"] = score_res["recommendations"]

        existing_res = db.query(Resume).filter(Resume.filename == prof["filename"]).first()
        if not existing_res:
            db.add(Resume(
                user_id=demo_user.id,
                filename=prof["filename"],
                extracted_text=prof["text"],
                candidate_name=prof["name"],
                candidate_email=prof["email"],
                candidate_phone="+1 (555) 019-2834",
                candidate_location="Bangalore, India",
                resume_score=score_res["overall_score"],
                parsed_json=parsed
            ))
    db.commit()
    db.close()
    print("[Seed Data] Database populated successfully with 30+ jobs and 10 sample resumes!")

if __name__ == "__main__":
    seed_database_and_resumes()
