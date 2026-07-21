"""Streamlit dashboard for resume-to-job-description analysis."""

from __future__ import annotations

import html
import logging
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import plotly.graph_objects as go
import streamlit as st
import spacy

from utils.ats_score import compute_ats_score
from utils.parser import parse_resume
from utils.preprocessing import preprocess
from utils.similarity import compare_keyword_overlap, compute_tfidf_similarity, get_top_keywords
from utils.skill_extractor import build_phrase_matcher, extract_skills, get_matched_skills, get_missing_skills, load_skills_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Resume Skill Gap Analyzer", layout="wide")


@st.cache_resource
def load_nlp_model() -> Any:
    """Load and cache the spaCy NLP model for repeated Streamlit reruns."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError as exc:
        raise RuntimeError(
            "The spaCy model 'en_core_web_sm' could not be loaded. "
            "Install it with: python -m spacy download en_core_web_sm"
        ) from exc


def render_badges(items: List[str], color: str) -> str:
    """Render a simple HTML badge list for skills."""
    if not items:
        return "<p>No items.</p>"

    badge_html = "".join(
        f'<span style="display:inline-block;padding:4px 8px;margin:4px;background:{color};color:white;border-radius:12px;">{html.escape(item)}</span>'
        for item in items
    )
    return f"<div>{badge_html}</div>"


def build_report_html(results: Dict[str, Any]) -> str:
    """Create a simple HTML report for download."""
    matched = results.get("matched_skills", [])
    missing = results.get("missing_skills", [])
    recommendations = results.get("recommendations", [])
    similarity = results.get("similarity_score", 0.0)
    ats_score = results.get("ats_score", 0.0)

    matched_html = "<br/>".join(f"- {html.escape(item)}" for item in matched) or "None"
    missing_html = "<br/>".join(f"- {html.escape(item)}" for item in missing) or "None"
    recommendations_html = "<br/>".join(f"- {html.escape(item)}" for item in recommendations) or "None"

    return f"""
    <html>
      <head><title>Resume Analysis Report</title></head>
      <body>
        <h1>AI Resume Skill Gap Analyzer Report</h1>
        <p><strong>Resume Match:</strong> {similarity:.2f}%</p>
        <p><strong>ATS Score:</strong> {ats_score:.2f}</p>
        <h2>Matched Skills</h2>
        <p>{matched_html}</p>
        <h2>Missing Skills</h2>
        <p>{missing_html}</p>
        <h2>Improvement Suggestions</h2>
        <p>{recommendations_html}</p>
      </body>
    </html>
    """


def run_analysis(resume_file: Optional[Any], jd_text: str, jd_file: Optional[Any]) -> Dict[str, Any]:
    """Run the full analysis pipeline and return a results dictionary."""
    if resume_file is None:
        raise ValueError("Please upload a resume file.")

    if not jd_text.strip() and jd_file is None:
        raise ValueError("Please provide a job description.")

    if jd_file is not None:
        jd_text = jd_file.read().decode("utf-8")

    nlp = load_nlp_model()
    # Resolve assets path relative to this file to avoid Streamlit CWD issues
    app_root = Path(__file__).resolve().parent
    assets_path = app_root / "assets" / "skills_db.json"
    skills_db = load_skills_db(str(assets_path))
    matcher = build_phrase_matcher(nlp, skills_db)

    try:
        resume_raw_text = parse_resume(resume_file)
    except Exception as exc:
        logger.exception("Failed to parse resume file")
        raise ValueError(f"Resume parsing failed: {exc}") from exc

    jd_raw_text = jd_text.strip()
    if not jd_raw_text:
        raise ValueError("Please provide a job description.")

    resume_preprocessed = preprocess(resume_raw_text)
    jd_preprocessed = preprocess(jd_raw_text)

    # Debug logging to aid investigation when zero scores occur
    logger.debug("Resume raw length: %d", len(resume_raw_text or ""))
    logger.debug("JD raw length: %d", len(jd_raw_text or ""))
    logger.debug("Resume preprocessed: %r", resume_preprocessed[:500])
    logger.debug("JD preprocessed: %r", jd_preprocessed[:500])

    resume_skills = extract_skills(resume_preprocessed, matcher, nlp)
    jd_skills = extract_skills(jd_preprocessed, matcher, nlp)

    matched = get_matched_skills(resume_skills, jd_skills)
    missing = get_missing_skills(resume_skills, jd_skills)
    similarity_score = compute_tfidf_similarity(resume_preprocessed, jd_preprocessed)
    overlap_report = compare_keyword_overlap(resume_preprocessed, jd_preprocessed)
    ats_result = compute_ats_score(resume_preprocessed, list(overlap_report.get("shared_keywords", [])))

    logger.debug("Extracted resume skills: %s", sorted(resume_skills))
    logger.debug("Extracted JD skills: %s", sorted(jd_skills))
    logger.debug("Shared keywords: %s", overlap_report.get("shared_keywords", []))

    return {
        "resume_text": resume_raw_text,
        "jd_text": jd_raw_text,
        "matched_skills": matched,
        "missing_skills": missing,
        "similarity_score": similarity_score,
        "top_keywords": get_top_keywords(jd_preprocessed, top_n=10),
        "ats_score": ats_result["ats_score"],
        "ats_formatting": ats_result["formatting"],
        "recommendations": ats_result["recommendations"],
        "keyword_density": ats_result["keyword_density"],
        "resume_preprocessed": resume_preprocessed,
        "jd_preprocessed": jd_preprocessed,
        "resume_skills": sorted(list(resume_skills)),
        "jd_skills": sorted(list(jd_skills)),
        "shared_keywords": overlap_report.get("shared_keywords", []),
    }


def main() -> None:
    """Render the Streamlit dashboard."""
    st.title("AI Resume Skill Gap Analyzer")
    st.caption("Upload a resume and compare it against a job description to see your skill gaps.")

    if "results" not in st.session_state:
        st.session_state.results = None

    left_col, right_col = st.columns([1.2, 0.8])

    with left_col:
        uploaded_resume = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="resume_uploader")

        jd_tab = st.tabs(["Paste text", "Upload .txt file"])
        with jd_tab[0]:
            jd_text = st.text_area("Job Description", height=220, key="jd_text")
        with jd_tab[1]:
            jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"], key="jd_uploader")

    with right_col:
        analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)
        if analyze_clicked:
            try:
                with st.spinner("Analyzing resume and job description..."):
                    results = run_analysis(uploaded_resume, jd_text, jd_file)
                st.session_state.results = results
            except (FileNotFoundError, RuntimeError, ValueError, OSError, UnicodeError) as exc:
                st.session_state.results = None
                st.error(f"Analysis failed: {exc}")
                logger.exception("Analysis failed")

    if st.session_state.results is not None:
        results = st.session_state.results

        st.subheader("Resume Match %")
        fig_match = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=results["similarity_score"],
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2563eb"},
                    "steps": [
                        {"range": [0, 50], "color": "lightgray"},
                        {"range": [50, 100], "color": "#dbeafe"},
                    ],
                },
            )
        )
        st.plotly_chart(fig_match, use_container_width=True)

        st.subheader("ATS Score")
        fig_ats = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=results["ats_score"],
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#10b981"},
                    "steps": [
                        {"range": [0, 50], "color": "#fef2f2"},
                        {"range": [50, 100], "color": "#dcfce7"},
                    ],
                },
            )
        )
        st.plotly_chart(fig_ats, use_container_width=True)

        col_skills, col_missing = st.columns(2)
        with col_skills:
            st.markdown("### Matched Skills")
            st.markdown(render_badges(results["matched_skills"], "#16a34a"), unsafe_allow_html=True)
        with col_missing:
            st.markdown("### Missing Skills")
            st.markdown(render_badges(results["missing_skills"], "#dc2626"), unsafe_allow_html=True)

        st.subheader("Top JD Keywords")
        keyword_names = [item[0] for item in results["top_keywords"]]
        keyword_scores = [item[1] for item in results["top_keywords"]]
        keyword_fig = go.Figure(go.Bar(x=keyword_scores, y=keyword_names, orientation="h"))
        keyword_fig.update_layout(yaxis={"autorange": "reversed"})
        st.plotly_chart(keyword_fig, use_container_width=True)

        st.subheader("Improvement Suggestions")
        for suggestion in results["recommendations"]:
            st.write(f"- {suggestion}")

        report_buffer = BytesIO()
        report_buffer.write(build_report_html(results).encode("utf-8"))
        report_buffer.seek(0)

        st.download_button(
            label="Download Report",
            data=report_buffer.getvalue(),
            file_name="resume_analysis_report.html",
            mime="text/html",
            use_container_width=True,
        )

        # Debug panel when scores are unexpectedly zero
        if results.get("similarity_score", 0) == 0 or results.get("ats_score", 0) == 0:
            with st.expander("Debug: parsed & preprocessed texts, skills", expanded=True):
                st.write("**Raw resume (truncated):**")
                st.text(results.get("resume_text", "")[:2000])
                st.write("**Raw JD (truncated):**")
                st.text(results.get("jd_text", "")[:2000])
                st.write("**Preprocessed resume:**")
                st.text(results.get("resume_preprocessed", ""))
                st.write("**Preprocessed JD:**")
                st.text(results.get("jd_preprocessed", ""))
                st.write("**Extracted resume skills:**")
                st.write(results.get("resume_skills", []))
                st.write("**Extracted JD skills:**")
                st.write(results.get("jd_skills", []))
                st.write("**Shared keywords:**")
                st.write(results.get("shared_keywords", []))


if __name__ == "__main__":
    main()
