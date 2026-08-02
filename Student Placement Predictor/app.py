import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Student Placement Predictor", page_icon="🎓", layout="centered")

model = joblib.load("placement_classifier.pkl")

numeric_features = [
    "age", "cgpa", "internships_count", "projects_count", "certifications_count",
    "coding_skill_score", "aptitude_score", "communication_skill_score",
    "logical_reasoning_score", "hackathons_participated", "github_repos",
    "linkedin_connections", "mock_interview_score", "attendance_percentage",
    "backlogs", "extracurricular_score", "leadership_score",
    "sleep_hours", "study_hours_per_day"
]
categorical_features = ["gender", "branch", "college_tier", "volunteer_experience"]

st.title("🎓 Student Placement Predictor")
st.write("Fill in the student's details to predict placement likelihood.")

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 17, 30, 21)
        gender = st.selectbox("Gender", ["Male", "Female"])
        branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil"])
        college_tier = st.selectbox("College Tier", ["Tier 1", "Tier 2", "Tier 3"])
        cgpa = st.slider("CGPA", 0.0, 10.0, 7.5)
        attendance_percentage = st.slider("Attendance %", 0.0, 100.0, 85.0)
        backlogs = st.number_input("Backlogs", 0, 10, 0)
        volunteer_experience = st.selectbox("Volunteer Experience", ["Yes", "No"])
    with col2:
        internships_count = st.number_input("Internships", 0, 10, 1)
        projects_count = st.number_input("Projects", 0, 20, 3)
        certifications_count = st.number_input("Certifications", 0, 15, 2)
        hackathons_participated = st.number_input("Hackathons", 0, 10, 1)
        github_repos = st.number_input("GitHub Repos", 0, 30, 4)
        linkedin_connections = st.number_input("LinkedIn Connections", 0, 1500, 500)
        sleep_hours = st.slider("Sleep Hours/Day", 0.0, 12.0, 7.0)
        study_hours_per_day = st.slider("Study Hours/Day", 0.0, 12.0, 3.5)

    st.subheader("Skill Scores (0-100)")
    coding_skill_score = st.slider("Coding Skill Score", 0.0, 100.0, 70.0)
    aptitude_score = st.slider("Aptitude Score", 0.0, 100.0, 65.0)
    communication_skill_score = st.slider("Communication Score", 0.0, 100.0, 68.0)
    logical_reasoning_score = st.slider("Logical Reasoning Score", 0.0, 100.0, 66.0)
    mock_interview_score = st.slider("Mock Interview Score", 0.0, 100.0, 70.0)
    extracurricular_score = st.slider("Extracurricular Score", 0.0, 100.0, 60.0)
    leadership_score = st.slider("Leadership Score", 0.0, 100.0, 55.0)

    submitted = st.form_submit_button("Predict")

if submitted:
    input_data = pd.DataFrame([{
        "age": age, "cgpa": cgpa, "internships_count": internships_count,
        "projects_count": projects_count, "certifications_count": certifications_count,
        "coding_skill_score": coding_skill_score, "aptitude_score": aptitude_score,
        "communication_skill_score": communication_skill_score,
        "logical_reasoning_score": logical_reasoning_score,
        "hackathons_participated": hackathons_participated, "github_repos": github_repos,
        "linkedin_connections": linkedin_connections, "mock_interview_score": mock_interview_score,
        "attendance_percentage": attendance_percentage, "backlogs": backlogs,
        "extracurricular_score": extracurricular_score, "leadership_score": leadership_score,
        "sleep_hours": sleep_hours, "study_hours_per_day": study_hours_per_day,
        "gender": gender, "branch": branch, "college_tier": college_tier,
        "volunteer_experience": volunteer_experience
    }])[numeric_features + categorical_features]

    proba = model.predict_proba(input_data)[0][1]
    pred = model.predict(input_data)[0]

    st.divider()
    if pred == 1:
        st.success(f"✅ Likely Placed — probability: {proba:.1%}")
    else:
        st.warning(f"⚠️ Likely Not Placed — probability: {proba:.1%}")
    st.progress(float(proba))

    # ---------- WHY THIS PREDICTION ----------
    st.divider()
    st.subheader("🔍 Why this prediction?")

    # Get the preprocessing step and the trained logistic regression model
    preprocessor = model.named_steps["preprocessor"]
    logreg = model.named_steps["model"]

    # Get feature names after one-hot encoding
    feature_names = preprocessor.get_feature_names_out()

    # Transform this student's input the same way the model was trained on
    transformed_input = preprocessor.transform(input_data)
    if hasattr(transformed_input, "toarray"):
        transformed_input = transformed_input.toarray()

    # Contribution of each feature = coefficient * (scaled) feature value
    # Positive = pushes toward "Placed", Negative = pushes toward "Not Placed"
    contributions = logreg.coef_[0] * transformed_input[0]

    contrib_df = pd.DataFrame({
        "feature": feature_names,
        "contribution": contributions
    }).sort_values("contribution", ascending=False)

    top_positive = contrib_df.head(5)
    top_negative = contrib_df.tail(5).sort_values("contribution")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**⬆️ Factors helping placement:**")
        for _, row in top_positive.iterrows():
            clean_name = row["feature"].replace("num__", "").replace("cat__", "").replace("_", " ")
            st.write(f"- {clean_name}")
    with col_b:
        st.markdown("**⬇️ Factors hurting placement:**")
        for _, row in top_negative.iterrows():
            clean_name = row["feature"].replace("num__", "").replace("cat__", "").replace("_", " ")
            st.write(f"- {clean_name}")

    # ---------- HOW TO IMPROVE ----------
    st.divider()
    st.subheader("💡 How to improve")

    tips = []
    if backlogs > 0:
        tips.append("Clearing backlogs is the single strongest factor linked to placement in this dataset — prioritize this.")
    if internships_count < 2:
        tips.append("Doing more internships tends to help — aim for at least 2.")
    if projects_count < 4:
        tips.append("Adding more hands-on projects (aim for 4+) tends to help.")
    if coding_skill_score < 75:
        tips.append("Improving your coding skill score (practice DSA, coding platforms) tends to help.")
    if mock_interview_score < 75:
        tips.append("Practicing more mock interviews tends to help.")

    if tips:
        for tip in tips:
            st.write(f"- {tip}")
    else:
        st.write("This profile is already strong across the factors that matter most in this dataset.")

    with st.expander("ℹ️ About this prediction's reliability"):
        st.write(
            "This model was trained and cross-validated on 100,000 student records "
            "and reaches a test-set ROC-AUC of about 0.585 (0.5 = random guessing, "
            "1.0 = perfect). Exploratory analysis showed no single feature strongly "
            "correlates with placement in this dataset, so treat this prediction as "
            "a rough signal, not a guarantee."
        )