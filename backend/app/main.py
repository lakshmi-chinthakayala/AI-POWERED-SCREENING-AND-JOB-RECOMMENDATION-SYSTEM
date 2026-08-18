"""
FastAPI Main Application Entrypoint.
Configures REST API routers, CORS headers, static asset serving, and automatic startup database initialization.
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

from backend.app.routes import auth, resume, jobs, recommendations, dashboard
from data.generate_sample_data import seed_database_and_resumes

app = FastAPI(
    title="AI Resume Screening & Job Recommendation System",
    description="B.Tech Final Year Artificial Intelligence Project - Automated Resume Parser, NLP Skill Extractor, Resume Scorer & Job Matching Engine.",
    version="1.0.0"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(recommendations.router)
app.include_router(dashboard.router)

# Locate Frontend static directory & index.html
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
FRONTEND_INDEX_PATH = os.path.join(BASE_DIR, "frontend", "templates", "index.html")

if os.path.exists(FRONTEND_STATIC_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_STATIC_DIR), name="static")

@app.on_event("startup")
def startup_event():
    """Initializes SQLite database and populates 30+ jobs and sample resumes on server startup."""
    print("[Server Startup] Seeding database with job listings and sample resumes...")
    try:
        seed_database_and_resumes()
    except Exception as e:
        print(f"[Database Seed Warning] {e}")

@app.get("/", response_class=HTMLResponse)
async def serve_landing_page():
    """Serves the main single-page application frontend UI."""
    if os.path.exists(FRONTEND_INDEX_PATH):
        with open(FRONTEND_INDEX_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>AI Resume Screening & Recommendation System</h1><p>Frontend template initializing...</p>")

@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "online", "system": "AI Resume Screener & Recommender", "version": "1.0.0"}
