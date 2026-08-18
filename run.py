"""
One-Click Application Execution Script.
Initializes the SQLite database, seeds 30+ jobs and sample resumes,
and launches the FastAPI server at http://127.0.0.1:8000 with automatic browser popup.
"""

import os
import sys
import webbrowser
import uvicorn

def main():
    print("=" * 70)
    print("  AI RESUME SCREENING & JOB RECOMMENDATION SYSTEM")
    print("  B.Tech Final Year Artificial Intelligence Project")
    print("=" * 70)
    print("\n[1/3] Initializing Database & Loading 30+ Job Listings + 10 Sample Resumes...")
    
    # Ensure current directory is in Python path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    try:
        from data.generate_sample_data import seed_database_and_resumes
        seed_database_and_resumes()
    except Exception as e:
        print(f"[Warning] Database initialization error: {e}")

    print("\n[2/3] Server starting at: http://127.0.0.1:8000")
    print("[3/3] Opening web browser automatically...\n")
    
    # Open browser after slight delay
    webbrowser.open("http://127.0.0.1:8000")

    # Launch FastAPI Server via Uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
