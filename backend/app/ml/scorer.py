"""
Resume Scoring Engine.
Calculates an overall application-generated Resume Score (0-100) based on weighted formula:
  - Skills (30%)
  - Experience (20%)
  - Projects (20%)
  - Education (15%)
  - Certifications (10%)
  - Resume Completeness (5%)
Includes detailed granular feedback and personalized suggestions for score improvement.
"""

from typing import Dict, Any, List

def calculate_resume_score(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes component scores, total weighted score (0-100), and improvement recommendations.
    """
    flat_skills = parsed_data.get("flat_skills", [])
    skill_count = len(flat_skills)
    
    # 1. Skills Score (30% weight) -> Target: 10+ relevant technical skills
    skills_score = min(100.0, (skill_count / 10.0) * 100.0)
    
    # 2. Experience Score (20% weight) -> Target: 2+ years or intern experience
    years_exp = parsed_data.get("years_of_experience", 0.0)
    exp_entries = parsed_data.get("experience", [])
    if years_exp >= 2.0:
        exp_score = 100.0
    elif years_exp >= 1.0:
        exp_score = 85.0
    elif len(exp_entries) > 0:
        exp_score = 70.0
    else:
        exp_score = 40.0
        
    # 3. Projects Score (20% weight) -> Target: 2+ technical projects
    projects = parsed_data.get("projects", [])
    if len(projects) >= 3:
        projects_score = 100.0
    elif len(projects) == 2:
        projects_score = 85.0
    elif len(projects) == 1:
        projects_score = 60.0
    else:
        projects_score = 30.0

    # 4. Education Score (15% weight) -> Target: Degree found
    education = parsed_data.get("education", [])
    if len(education) >= 1 and education[0].get("degree"):
        edu_score = 95.0
    else:
        edu_score = 50.0

    # 5. Certifications Score (10% weight) -> Target: 2+ certifications
    certs = parsed_data.get("certifications", [])
    if len(certs) >= 2:
        cert_score = 100.0
    elif len(certs) == 1:
        cert_score = 75.0
    else:
        cert_score = 35.0

    # 6. Completeness Score (5% weight) -> Contact Info Check
    info = parsed_data.get("candidate_info", {})
    comp_checks = [
        bool(info.get("name")),
        bool(info.get("email")),
        bool(info.get("phone")),
        bool(info.get("linkedin")),
        bool(info.get("github"))
    ]
    completeness_score = (sum(comp_checks) / len(comp_checks)) * 100.0

    # Calculate weighted total score
    total_score = round(
        (skills_score * 0.30) +
        (exp_score * 0.20) +
        (projects_score * 0.20) +
        (edu_score * 0.15) +
        (cert_score * 0.10) +
        (completeness_score * 0.05),
        1
    )

    # Generate actionable improvement recommendations
    recommendations: List[str] = []
    
    if skill_count < 8:
        recommendations.append("Add more technical skills to your profile (aim for 8+ categorized skills in AI, Web, Data, or Cloud).")
        
    if projects_score < 80:
        recommendations.append("Detail at least 2 key technical projects with technologies used and quantifiable results.")
        
    if exp_score < 75:
        recommendations.append("Elaborate on internship or project roles with specific responsibilities and key achievements.")
        
    if cert_score < 70:
        recommendations.append("Consider obtaining industry-recognized certifications (e.g., AWS, DeepLearning.AI, Coursera, TensorFlow Developer).")
        
    if not info.get("github") or info.get("github") == "https://github.com/candidate":
        recommendations.append("Include your GitHub profile link to showcase open-source code and project repositories.")
        
    if not info.get("linkedin") or info.get("linkedin") == "https://linkedin.com/in/candidate":
        recommendations.append("Add your updated LinkedIn profile URL for professional validation.")

    return {
        "overall_score": total_score,
        "breakdown": {
            "skills": {"score": round(skills_score, 1), "weight": "30%"},
            "experience": {"score": round(exp_score, 1), "weight": "20%"},
            "projects": {"score": round(projects_score, 1), "weight": "20%"},
            "education": {"score": round(edu_score, 1), "weight": "15%"},
            "certifications": {"score": round(cert_score, 1), "weight": "10%"},
            "completeness": {"score": round(completeness_score, 1), "weight": "5%"}
        },
        "recommendations": recommendations
    }
