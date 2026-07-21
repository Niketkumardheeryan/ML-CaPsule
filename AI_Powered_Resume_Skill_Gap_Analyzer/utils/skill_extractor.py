"""Skill extraction utilities for resume and job-description matching."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import spacy
from spacy.matcher import PhraseMatcher

logger = logging.getLogger(__name__)


def load_skills_db(path: str = "assets/skills_db.json") -> dict:
    """Load the skills taxonomy from a JSON file.

    This function attempts several sensible candidate locations so the file can be
    found whether Streamlit changes the current working directory or modules are
    imported from different places.
    """
    candidates = []

    requested = Path(path)
    # 1) If absolute path was provided, try it directly
    if requested.is_absolute():
        candidates.append(requested)

    # 2) Relative to this repository (utils parent)
    repo_root = Path(__file__).resolve().parents[1]
    candidates.append(repo_root / requested)

    # 3) Relative to current working directory (where Streamlit may run)
    candidates.append(Path.cwd() / requested)

    # 4) Walk up from this file's parent and try 'assets/skills_db.json' at each level
    for parent in repo_root.parents:
        candidates.append(parent / requested)

    # 5) As a final fallback, try a workspace-wide glob for the filename
    candidates.extend(Path(repo_root).glob("**/skills_db.json"))

    skills_path = None
    logger.debug("Checking candidate locations for skills_db.json...")
    for cand in candidates:
        try:
            candp = Path(cand)
        except Exception:
            continue
        logger.debug("Trying candidate: %s (exists=%s)", candp, candp.exists())
        if candp.exists():
            skills_path = candp
            logger.info("Using skills DB at: %s", skills_path)
            break

    if skills_path is None:
        # Show a helpful error listing the candidates we tried
        tried = "\n".join(str(p) for p in candidates[:20])
        logger.error("Skills DB not found; checked candidates: %s", tried)
        raise FileNotFoundError(
            f"Skills database not found. Checked these locations:\n{tried}\n(If your assets folder is elsewhere, pass an absolute path to load_skills_db.)"
        )

    with skills_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError("Skills database must be a JSON object.")

    return data


def _format_skill_name(skill: str) -> str:
    return " ".join(part.capitalize() for part in skill.split())


def build_phrase_matcher(nlp: Any, skills_db: Dict[str, List[str]]) -> PhraseMatcher:
    """Build a spaCy PhraseMatcher for case-insensitive multi-word skill matching."""
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    all_skills: List[str] = []
    for category_skills in skills_db.values():
        all_skills.extend(category_skills)

    patterns = [nlp.make_doc(skill) for skill in sorted(set(all_skills)) if skill]
    matcher.add("SKILLS", patterns)
    return matcher


def extract_skills(text: str, matcher: PhraseMatcher, nlp: Any) -> set[str]:
    """Match skills from a text string and return a deduplicated set of title-cased names."""
    if not text:
        return set()

    doc = nlp(text)
    matches = set()
    for _, start, end in matcher(doc):
        span = doc[start:end]
        skill_name = span.text.strip()
        if skill_name:
            matches.add(_format_skill_name(skill_name))

    return matches


def get_missing_skills(resume_skills: set[str], jd_skills: set[str]) -> list[str]:
    """Return the skills required by the job description but missing from the resume."""
    return sorted(jd_skills - resume_skills)


def get_matched_skills(resume_skills: set[str], jd_skills: set[str]) -> list[str]:
    """Return the skills shared by the resume and the job description."""
    return sorted(resume_skills & jd_skills)


if __name__ == "__main__":
    import pathlib

    sample_resume = (
        "I am a data scientist with experience in Python, SQL, pandas, scikit-learn, "
        "machine learning, deep learning, and docker. I also enjoy teamwork and communication."
    )
    sample_jd_path = pathlib.Path(__file__).resolve().parents[1] / "sample_data" / "sample_jd.txt"
    sample_jd_text = sample_jd_path.read_text(encoding="utf-8")

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        raise SystemExit("Please install the spaCy model with: python -m spacy download en_core_web_sm")

    skills_db = load_skills_db()
    matcher = build_phrase_matcher(nlp, skills_db)

    resume_skills = extract_skills(sample_resume, matcher, nlp)
    jd_skills = extract_skills(sample_jd_text, matcher, nlp)

    print("Resume skills:", sorted(resume_skills))
    print("JD skills:", sorted(jd_skills))
    print("Matched skills:", get_matched_skills(resume_skills, jd_skills))
    print("Missing skills:", get_missing_skills(resume_skills, jd_skills))
