import streamlit as st
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the Logistic Regression model
model = joblib.load('logistic.pkl')

# Define the job role mapping
job_role_mapping = {
    0: 'Artificial Intelligence Engineer',
    1: 'Cloud Solutions Architect',
    2: 'Cybersecurity Analyst',
    3: 'Data Scientist',
    4: 'Database Administrator',
    5: 'IT Manager',
    6: 'Network Administrator',
    7: 'Software Developer',
    8: 'Systems Analyst',
    9: 'Web Developer'
}

def preprocess_input(data):
    df = pd.DataFrame([data])
    categorical_columns = ['can work long time before system?', 'self-learning capability?', 'talent tests taken?',
                           'higher education?']
    label_encoders = {}

    for col in categorical_columns:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le

    return df

# Predict function
def predict_job_role(user_input):
    preprocessed_input = preprocess_input(user_input)
    prediction_numeric = model.predict(preprocessed_input)[0]
    predicted_job_role = job_role_mapping[prediction_numeric]
    return predicted_job_role

# Streamlit application
def main():
    st.set_page_config(page_title="Job Role Predictor", page_icon=":mag_right:")

    # Apply custom CSS
    st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
            color: #ffffff;
        }
        .input-container {
            border: 2px solid #333333;
            border-radius: 10px;
            padding: 15px;
            background-color: #1e1e1e;
        }
        .output-container {
            border: 2px solid #333333;
            border-radius: 10px;
            padding: 10px;
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .success-message {
            font-weight: bold;
            color: #ffffff;
            background-color: #4CAF50;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
        }
        .header {
            text-align: center;
            color: #90EE90; /* Light green color */
            font-weight: bold;
            font-size: 2em;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<h1 style="font-size:48px;" class="header">Job Role Predictor</h1>', unsafe_allow_html=True)

    with st.form(key='input_form'):
        st.header("Enter Your Details")
        percentage_os = st.slider('Percentage in Operating Systems', 0, 100, 85)
        percentage_daoa = st.slider('Percentage in Design and Analysis of Algorithms', 0, 100, 90)
        percentage_popl = st.slider('Percentage in Principle of Programming Languages', 0, 100, 70)
        percentage_sdam = st.slider('Percentage in Software Engineering', 0, 100, 75)
        percentage_cn = st.slider('Percentage in Computer Networks', 0, 100, 60)
        percentage_elec = st.slider('Percentage in Electronics Subjects', 0, 100, 65)
        percentage_coa = st.slider('Percentage in Computer Architecture', 0, 100, 80)
        percentage_math = st.slider('Percentage in Mathematics', 0, 100, 72)
        percentage_comms = st.slider('Percentage in Communication Skills', 0, 100, 90)
        hours_per_day = st.slider('Hours working per day', 0, 24, 8)
        hackathons = st.slider('Number of hackathons', 0, 50, 20)
        coding_skills = st.slider('Coding skills rating', 0, 100, 85)
        public_speaking = st.slider('Public speaking rating', 0, 100, 90)

        can_work_long = st.selectbox('Can you work for a long time in front of a computer system?', ['Yes', 'No'])
        self_learning = st.selectbox('Are you ready to self-learn new tech stacks and technologies?', ['Yes', 'No'])
        extra_courses = st.slider('Number of extra courses', 0, 50, 15)
        certifications = st.slider('Number of certifications', 0, 50, 10)
        workshops = st.slider('Number of workshops', 0, 100, 62)
        talent_tests = st.selectbox('Did you take the talent test?', ['Yes', 'No'])
        olympiads = st.slider('Percentage in Olympiads', 0, 100, 77)
        reading_writing_skills = st.slider('Reading and writing skills [1-5]', 1, 5, 4)
        memory_capability = st.slider('Memory capability score [1-10]', 1, 10, 8)
        higher_education = st.selectbox('Do you want to pursue higher education?', ['Yes', 'No'])

        submit_button = st.form_submit_button("Predict Job Role")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        user_input = {
            'Percentage in Operating Systems': percentage_os,
            'Percentage in Design and Analysis of Algorithms': percentage_daoa,
            'Percentage in Principle of Programming Languages': percentage_popl,
            'Percentage in Software Engineering': percentage_sdam,
            'Percentage in Computer Networks': percentage_cn,
            'Percentage in Electronics Subjects': percentage_elec,
            'Percentage in Computer Architecture': percentage_coa,
            'Percentage in Mathematics': percentage_math,
            'Percentage in Communication Skills': percentage_comms,
            'Hours working per day': hours_per_day,
            'hackathons': hackathons,
            'coding skills rating': coding_skills,
            'public speaking points': public_speaking,
            'can work long time before system?': can_work_long,
            'self-learning capability?': self_learning,
            'Extra-courses did': extra_courses,
            'certifications': certifications,
            'workshops': workshops,
            'talent tests taken?': talent_tests,
            'percentage in olympiads': olympiads,
            'reading and writing skills [1-5]': reading_writing_skills,
            'memory capability score [1-10]': memory_capability,
            'higher education?': higher_education,
        }

        predicted_job_role = predict_job_role(user_input)

        st.success(f"**Predicted Job Role:** {predicted_job_role}")

if __name__ == "__main__":
    main()
