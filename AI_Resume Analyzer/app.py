import streamlit as st
import pdfplumber
from skills import job_roles
import matplotlib.pyplot as plt
from nlp_utils import extract_entities
from ai_suggestions import generate_suggestions

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------------------
# FUNCTIONS
# ---------------------------

def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text.lower()


def analyze_resume(text, selected_role):

    required_skills = job_roles[selected_role]

    found_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in text:
            found_skills.append(skill)

        else:
            missing_skills.append(skill)

    return found_skills, missing_skills


def calculate_score(found, total):

    if total == 0:
        return 0

    score = int((len(found) / total) * 100)

    return score


# ---------------------------
# SIDEBAR
# ---------------------------

st.sidebar.title("📌 About")

st.sidebar.info(
    """
    AI Resume Analyzer helps users:

    ✅ Analyze resume skills  
    ✅ Calculate ATS score  
    ✅ Detect missing skills  
    ✅ Improve resume quality  
    ✅ Generate AI suggestions  
    """
)

# ---------------------------
# MAIN TITLE
# ---------------------------

st.title("📄 AI Resume Analyzer")

st.markdown(
    "### Upload your resume and analyze ATS compatibility"
)

# ---------------------------
# JOB ROLE SELECTION
# ---------------------------

selected_role = st.selectbox(
    "Select Target Job Role",
    list(job_roles.keys())
)

# ---------------------------
# FILE UPLOAD
# ---------------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# ---------------------------
# ANALYSIS SECTION
# ---------------------------

if uploaded_file:

    st.success("Resume uploaded successfully!")

    # ---------------------------
    # EXTRACT RESUME TEXT
    # ---------------------------

    resume_text = extract_text(uploaded_file)

    # ---------------------------
    # AI FEEDBACK
    # ---------------------------

    st.subheader("🤖 AI Resume Feedback")

    ai_feedback = generate_suggestions(
        resume_text
    )

    st.write(ai_feedback)

    # ---------------------------
    # NLP ENTITY EXTRACTION
    # ---------------------------

    entities = extract_entities(resume_text)

    st.subheader("📌 Extracted Entities")

    for ent, label in entities:
        st.write(f"{ent} → {label}")

    # ---------------------------
    # SKILL ANALYSIS
    # ---------------------------

    found_skills, missing_skills = analyze_resume(
        resume_text,
        selected_role
    )

    total_skills = len(
        job_roles[selected_role]
    )

    # ---------------------------
    # SCORE CALCULATION
    # ---------------------------

    score = calculate_score(
        found_skills,
        total_skills
    )

    # ---------------------------
    # ATS SCORE SECTION
    # ---------------------------

    st.subheader("📊 ATS Resume Score")

    st.progress(score / 100)

    st.metric(
        "ATS Score",
        f"{score}%"
    )

    # ---------------------------
    # SKILLS DETECTED
    # ---------------------------

    st.subheader("✅ Skills Detected")

    if found_skills:

        for skill in found_skills:
            st.success(skill)

    else:

        st.warning(
            "No matching skills found."
        )

    # ---------------------------
    # MISSING SKILLS
    # ---------------------------

    st.subheader("❌ Missing Skills")

    if missing_skills:

        for skill in missing_skills:
            st.error(skill)

    else:

        st.success(
            "No missing skills!"
        )

    # ---------------------------
    # SUGGESTIONS
    # ---------------------------

    st.subheader("💡 Suggestions")

    if score < 50:

        st.warning(
            """
            Add more relevant skills,
            projects, and certifications
            to improve your ATS score.
            """
        )

    elif score < 80:

        st.info(
            """
            Your resume is decent,
            but can still be improved.
            """
        )

    else:

        st.success(
            """
            Excellent ATS-friendly resume!
            """
        )

    # ---------------------------
    # PIE CHART
    # ---------------------------

    st.subheader("📈 Skill Analysis")

    labels = [
        "Detected",
        "Missing"
    ]

    values = [
        len(found_skills),
        len(missing_skills)
    ]

    fig, ax = plt.subplots()

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)