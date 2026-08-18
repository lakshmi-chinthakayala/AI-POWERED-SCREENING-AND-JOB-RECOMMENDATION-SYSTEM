# AI Resume Screening & Job Recommendation System

[![Project Type](https://img.shields.io/badge/B.Tech_Project-Artificial_Intelligence-indigo.svg)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-TF--IDF-orange.svg)](https://scikit-learn.org/)

An end-to-end, functional **AI Resume Screening & Job Recommendation System** designed for B.Tech Artificial Intelligence final-year project demonstration.

The system allows candidates to upload resumes in PDF or DOCX format, automatically parses structured details (skills, education, experience, projects, certifications) using NLP, calculates a transparent **Resume Score (0–100)**, and ranks the candidate against 30+ job descriptions using **TF-IDF Vectorization**, **Cosine Similarity**, and a **Multi-Factor Matching Engine**. It also generates actionable **Skill Gap Analysis** and learning recommendations for missing skills.

---

## 🚀 Key Features

1. **Document Parsing & Processing**:
   - Accepts PDF (`.pdf`) and Word (`.docx`) file formats.
   - Fast text extraction via PyMuPDF (`fitz`) and `python-docx`.
   - Built-in OCR fallback using `pytesseract` for scanned image resumes.

2. **NLP Entity & Skill Extraction Engine**:
   - Extract candidate Name, Email, Phone, Location, GitHub, and LinkedIn profiles.
   - Built-in dictionary containing **100+ technical skills** categorized across 8 core domains:
     - Programming (Python, Java, C++, JavaScript, Go...)
     - AI / Machine Learning (Scikit-learn, TensorFlow, PyTorch, XGBoost...)
     - NLP (spaCy, NLTK, Transformers, BERT, LLMs...)
     - Computer Vision (OpenCV, CNN, YOLO...)
     - Data Science (SQL, Pandas, NumPy, Power BI, Tableau...)
     - Cloud & DevOps (Docker, Kubernetes, AWS, Git, MLOps...)
     - Web Development (React, FastAPI, Flask, HTML, CSS...)
     - Databases (PostgreSQL, SQLite, MongoDB, Redis...)

3. **Application-Generated Resume Score (0–100)**:
   - Calculates a transparent weighted score:
     $$\text{Resume Score} = (30\% \times \text{Skills}) + (20\% \times \text{Experience}) + (20\% \times \text{Projects}) + (15\% \times \text{Education}) + (10\% \times \text{Certifications}) + (5\% \times \text{Completeness})$$
   - Generates personalized recommendations for score improvement.

4. **TF-IDF + Cosine Similarity Job Recommendation Engine**:
   - Multi-Factor Match Formula:
     $$\text{Final Score} = (45\% \times \text{Text Similarity}) + (35\% \times \text{Skill Match}) + (10\% \times \text{Experience Match}) + (10\% \times \text{Education Match})$$
   - Normalizes match scores to a realistic percentage ($35\% - 98\%$).

5. **Skill Gap Analysis**:
   - Categorizes **Matching Skills** (green badges) and **Missing Skills** (orange badges).
   - Maps missing skills to curated learning recommendations (e.g. Docker, AWS, PyTorch).

6. **Interactive Dashboard & Job Explorer**:
   - Visualizes skill category distributions and top job match scores using Chart.js.
   - Search and filter 30+ sample job listings by role, location, experience, skill, and employment type.

7. **One-Click Pre-loaded Demo Resumes**:
   - Includes 10 synthetic sample resumes (PDF & DOCX) in `data/sample_resumes/` for instant viva demo.

---

## 🛠️ Technology Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend** | HTML5, Tailwind CSS, JavaScript (ES6 Modules), Chart.js, FontAwesome |
| **Backend** | Python 3.13, FastAPI, Uvicorn, Pydantic |
| **AI / Machine Learning** | Scikit-learn, TF-IDF Vectorizer, Cosine Similarity, Pandas, NumPy |
| **NLP & Text Processing** | spaCy, NLTK, RegEx Entity Extraction, Custom 100+ Skill Dictionary |
| **Document Parsers** | PyMuPDF (`fitz`), `python-docx`, Tesseract OCR (`pytesseract`) |
| **Database** | SQLite via SQLAlchemy ORM (configured for easy PostgreSQL migration) |
| **Authentication** | Passlib (Bcrypt password hashing), PyJWT tokens |

---

## 📐 System Architecture & Workflow

```text
User Uploads Resume (PDF/DOCX)
       │
       ▼
Extract Text (PyMuPDF / python-docx / OCR)
       │
       ▼
NLP Processing & Skill Extraction (100+ Dictionary)
       │
       ▼
Calculate Resume Score (0-100) & Improvement Advice
       │
       ▼
TF-IDF Vectorization & Cosine Similarity Match against 30+ Jobs
       │
       ▼
Rank Recommendations & Perform Skill Gap Analysis
       │
       ▼
Display Interactive Dashboard & Learning Advice
```

---

## 📊 AI / ML Methodology & Formulas

### 1. TF-IDF Text Similarity
The text content of the candidate resume ($R$) and job description ($J$) are transformed into numerical feature vectors using Term Frequency - Inverse Document Frequency (TF-IDF):

$$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t'} f_{t', d}}$$

$$\text{IDF}(t, D) = \log\left(\frac{N}{|\{d \in D : t \in d\}|}\right)$$

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

### 2. Cosine Similarity Score
The directional similarity between vectors $\vec{v}_R$ and $\vec{v}_J$ is computed as:

$$\text{Cosine Similarity} = \frac{\vec{v}_R \cdot \vec{v}_J}{\|\vec{v}_R\| \|\vec{v}_J\|} = \frac{\sum_{i=1}^{n} R_i J_i}{\sqrt{\sum_{i=1}^{n} R_i^2} \sqrt{\sum_{i=1}^{n} J_i^2}}$$

---

## ⚡ Quick Start & Running Instructions

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Launch Application (One-Click Runner)
```bash
python run.py
```
This script will:
- Initialize the SQLite database (`ai_resume_screener.db`).
- Seed 30+ job descriptions and 10 sample PDF/DOCX resumes.
- Start the FastAPI application server at `http://127.0.0.1:8000`.
- Automatically open your default web browser to the application dashboard.

---

## 📁 Folder Structure

```text
project-root/
├── backend/
│   └── app/
│       ├── main.py                   # FastAPI server entrypoint
│       ├── database/                 # SQLite connection & ORM models
│       ├── schemas/                  # Pydantic validation schemas
│       ├── routes/                   # API routes (Auth, Resume, Jobs, Recs, Dashboard)
│       ├── nlp/                      # Text cleaning, extraction & skill dictionary
│       ├── ml/                       # Scorer & TF-IDF Cosine Matcher engine
│       ├── services/                 # PDF, DOCX, & OCR document parsers
│       └── utils/                    # Password hashing & JWT helpers
├── frontend/
│   ├── static/                       # CSS, JS (api.js, app.js)
│   └── templates/
│       └── index.html                # Single Page Application HTML layout
├── data/
│   ├── jobs.json                     # 30+ realistic job listings dataset
│   ├── generate_sample_data.py       # Seed script
│   └── sample_resumes/               # 10 PDF/DOCX synthetic sample resumes
├── tests/                            # Pytest suite
├── requirements.txt                  # Python dependencies
├── run.py                            # One-click launcher script
└── README.md                         # Project documentation
```

---

## 🎓 Viva Presentation Q&A Guide (B.Tech AI)

**Q1: How does your system extract skills from unformatted resumes?**  
*Answer*: The system normalizes raw text using lowercasing and whitespace cleaning, then matches terms against a pre-compiled dictionary of 100+ technical skills categorized into 8 domains using bounded regular expressions and spaCy tokenization.

**Q2: What algorithm is used to rank jobs for a candidate?**  
*Answer*: We use a hybrid approach combining **TF-IDF Vectorization** and **Cosine Similarity** (45% weight), **Skill Overlap Ratio** (35% weight), **Experience Match** (10%), and **Education Match** (10%).

**Q3: How is the Resume Score (0-100) calculated?**  
*Answer*: The score is computed using a weighted formula: Skills (30%), Experience (20%), Projects (20%), Education (15%), Certifications (10%), and Profile Completeness (5%).

**Q4: How does the system perform Skill Gap Analysis?**  
*Answer*: The engine compares candidate skills against the required and preferred skills of target job roles, isolates missing skills, and queries a curated resource map to deliver specific learning advice.

---

## 🔮 Future Enhancements
- Integration of Transformer LLMs (e.g. LLaMA / Mistral) for semantic summary extraction.
- Support for multi-lingual resume parsing.
- Integration with live Job Board APIs (LinkedIn, Indeed).
