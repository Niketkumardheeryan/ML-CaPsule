import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the pre-trained Random Forest model
model_rf = joblib.load('rf_student_marks_model.pkl')


# Function to predict Performance Index and categorize the grade
def predict_performance_index(hours_studied, prev_scores, extra_activities, sleep_hours, sample_papers,
                              study_efficiency, sleep_efficiency):
    # Convert yes/no to binary
    extra_activities = 1 if extra_activities.lower() == 'yes' else 0

    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'Hours Studied': [hours_studied],
        'Previous Scores': [prev_scores],
        'Extracurricular Activities': [extra_activities],
        'Sleep Hours': [sleep_hours],
        'Sample Question Papers Practiced': [sample_papers],
        'Study Efficiency': [study_efficiency],
        'Sleep Efficiency': [sleep_efficiency]
    })

    # Predict using the Random Forest model
    prediction = model_rf.predict(input_data)[0]

    # Round prediction to nearest integer
    rounded_prediction = round(prediction)

    # Determine grade
    if rounded_prediction > 90:
        grade = 'A+'
    elif rounded_prediction >= 81:
        grade = 'A'
    elif rounded_prediction >= 71:
        grade = 'B+'
    elif rounded_prediction >= 61:
        grade = 'B'
    elif rounded_prediction >= 51:
        grade = 'C+'
    elif rounded_prediction >= 41:
        grade = 'C'
    elif rounded_prediction >= 35:
        grade = 'D'
    else:
        grade = 'F'

    return rounded_prediction, grade


# Streamlit UI
st.set_page_config(page_title="Performance Predictor", page_icon=":star:", layout="centered")

# Add custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #2e2e2e;
        color: #f0f0f5;
        border-radius: 15px;
        padding: 20px;
    }
    .title {
        text-align: center;
        color: #f4a261;
        font-weight: bold;
        font-size: 36px;
    }
    .subtitle {
        text-align: center;
        color: #e9c46a;
        font-weight: bold;
        font-size: 24px;
    }
    .box {
        border: 2px solid #f4a261;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .output-box {
        border: 2px solid #e9c46a;
        border-radius: 10px;
        padding: 20px;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
    }
    .stNumberInput>div>div>input {
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">Student Performance Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter your details below to predict your marks and grade.</p>',
            unsafe_allow_html=True)

# Input fields
with st.form(key='input_form'):
    hours_studied = st.number_input("How many Hours Do you study Before Exams?", min_value=0, max_value=24, value=7)
    prev_scores = st.number_input("What was your previous Test score (0-100)?", min_value=0, max_value=100, value=50)
    extra_activities = st.selectbox("Do you participate in any extracurricular activities?", ["Yes", "No"])
    sleep_hours = st.number_input("How many Hours do you sleep?", min_value=0, max_value=24, value=7)
    sample_papers = st.number_input("Enter the total number of sample question papers that you have practiced:",
                                    min_value=0, max_value=100, value=3)
    study_efficiency = st.slider("Enter your study efficiency (0-10):", 0, 10, 5)
    sleep_efficiency = st.slider("Enter your sleep Efficiency (0-10):", 0, 10, 5)

    # Submit button
    submit_button = st.form_submit_button("Predict")

if submit_button:
    # Make prediction
    predicted_performance_index, predicted_grade = predict_performance_index(
        hours_studied, prev_scores, extra_activities, sleep_hours,
        sample_papers, study_efficiency, sleep_efficiency
    )

    # Display results
    with st.expander("Prediction Results"):
        st.success(f'Your predicted Marks out of 100 for the next Exam are: {predicted_performance_index}')
        st.error(f'Your Predicted Grade is: {predicted_grade}')
        st.markdown('</div>', unsafe_allow_html=True)
