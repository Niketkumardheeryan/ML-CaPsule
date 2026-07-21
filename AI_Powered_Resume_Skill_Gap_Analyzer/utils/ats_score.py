"""Estimate ATS-friendliness of a resume based on formatting and keyword coverage."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

KEYWORD_WEIGHT = 0.6
FORMAT_WEIGHT = 0.4
REQUIRED_SECTIONS = ["experience", "education", "skills", "summary", "contact"]
SECTION_PATTERNS = {
    "experience": [r"\bexperience\b", r"\bwork history\b", r"\bprofessional experience\b"],
    "education": [r"\beducation\b", r"\bacademics\b", r"\bqualifications\b"],
    "skills": [r"\bskills\b", r"\btechnical skills\b", r"\bcore competencies\b"],
    "summary": [r"\bsummary\b", r"\bobjective\b", r"\bprofessional summary\b"],
    "contact": [r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", r"\b\+?\d[\d\s().-]{7,}\b"],
}


def check_formatting(resume_text: str) -> dict:
    """Detect whether a resume contains standard ATS-friendly sections."""
    if not resume_text:
        return {section: False for section in REQUIRED_SECTIONS}

    normalized_text = resume_text.lower()
    formatting: dict = {}
    for section in REQUIRED_SECTIONS:
        patterns = SECTION_PATTERNS.get(section, [])
        found = any(re.search(pattern, normalized_text) for pattern in patterns)
        formatting[section] = found

    return formatting


def keyword_density_score(resume_text: str, jd_keywords: list[str]) -> float:
    """Measure how many job-description keywords appear in the resume text."""
    if not resume_text or not jd_keywords:
        return 0.0

    normalized_text = resume_text.lower()
    matched = 0
    for keyword in jd_keywords:
        if keyword and re.search(rf"\b{re.escape(keyword.lower())}\b", normalized_text):
            matched += 1

    return round((matched / len(jd_keywords)) * 100, 2)


def compute_ats_score(resume_text: str, jd_keywords: list[str]) -> dict:
    """Compute a weighted ATS friendliness score and return practical recommendations."""
    formatting = check_formatting(resume_text)
    required_sections_found = sum(formatting.values())
    formatting_completeness = round((required_sections_found / len(REQUIRED_SECTIONS)) * 100, 2)

    keyword_density = keyword_density_score(resume_text, jd_keywords)
    ats_score = round((KEYWORD_WEIGHT * keyword_density) + (FORMAT_WEIGHT * formatting_completeness), 2)

    recommendations: list[str] = []
    for section, found in formatting.items():
        if not found:
            recommendations.append(f"Add a clear '{section}' section to improve ATS readability.")

    if keyword_density < 70:
        recommendations.append("Increase keyword coverage by including more job-description terms naturally in the resume.")

    if not recommendations:
        recommendations.append("Resume structure and keyword coverage look strong for ATS parsing.")

    return {
        "ats_score": ats_score,
        "formatting": formatting,
        "keyword_density": keyword_density,
        "recommendations": recommendations,
    }


if __name__ == "__main__":
    sample_resume_path = Path(__file__).resolve().parents[1] / "sample_data" / "sample_resume.pdf"
    sample_resume_text = (
        "Summary: Data scientist with experience in Python, SQL, pandas, scikit-learn, "
        "machine learning, and deep learning. Contact: john.doe@example.com | +1 555-123-4567. "
        "Skills: Python SQL Pandas Scikit-learn Machine Learning Docker. Education: BSc Computer Science. "
        "Experience: Worked on data pipelines and analytics models."
    )
    sample_jd_keywords = ["python", "sql", "pandas", "numpy", "scikit-learn", "machine learning", "data visualization", "git", "docker", "aws"]

    print(compute_ats_score(sample_resume_text, sample_jd_keywords))
