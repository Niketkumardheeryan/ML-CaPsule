"""Resume-to-job-description similarity scoring utilities."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def compute_tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """Compute cosine similarity between preprocessed resume and job-description text."""
    if not resume_text or not jd_text:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words=None)
    matrix = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(float(similarity * 100), 2)


def get_top_keywords(text: str, top_n: int = 15) -> list[tuple[str, float]]:
    """Return the top-N terms for a preprocessed document ranked by TF-IDF weight."""
    if not text:
        return []

    vectorizer = TfidfVectorizer(stop_words=None)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    ranked = sorted(
        ((feature_names[idx], float(scores[idx])) for idx in range(len(feature_names))),
        key=lambda item: item[1],
        reverse=True,
    )

    return ranked[:top_n]


def compare_keyword_overlap(resume_text: str, jd_text: str) -> dict:
    """Compare keyword overlap between resume and job description text."""
    if not resume_text or not jd_text:
        return {"overlap_pct": 0.0, "shared_keywords": [], "jd_only_keywords": []}

    resume_keywords = set(resume_text.split())
    jd_keywords = set(jd_text.split())

    shared_keywords = sorted(resume_keywords & jd_keywords)
    jd_only_keywords = sorted(jd_keywords - resume_keywords)
    overlap_pct = round((len(shared_keywords) / len(jd_keywords) * 100) if jd_keywords else 0.0, 2)

    return {
        "overlap_pct": overlap_pct,
        "shared_keywords": shared_keywords,
        "jd_only_keywords": jd_only_keywords,
    }


if __name__ == "__main__":
    sample_resume_path = Path(__file__).resolve().parents[1] / "sample_data" / "sample_resume.pdf"
    sample_resume_text = "data scientist python sql pandas scikit learn machine learning deep learning docker"
    sample_jd_text = (
        "data scientist python sql pandas numpy scikit learn machine learning "
        "data visualization git docker aws"
    )

    print(f"Similarity: {compute_tfidf_similarity(sample_resume_text, sample_jd_text)}%")
    print("Top keywords:", get_top_keywords(sample_jd_text, top_n=10))
    print("Keyword overlap:", compare_keyword_overlap(sample_resume_text, sample_jd_text))
