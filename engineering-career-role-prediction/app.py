import streamlit as st
import joblib
import pandas as pd

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
    yes_no_mapping = {'Yes': 1, 'No': 0}

    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].map(yes_no_mapping)

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
        @import url('https://fonts.googleapis.com/css2?family=Spectral:wght@500;700&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@500;600&display=swap');

        .stApp {
            background-color: #F7F3E8;
            color: #1B2A4A;
            font-family: 'IBM Plex Sans', sans-serif;
        }
        .header {
            font-family: 'Spectral', serif;
            text-align: center;
            color: #1B2A4A;
            font-weight: 700;
            font-size: 2.3em;
            letter-spacing: 1px;
            text-transform: uppercase;
            padding-bottom: 0.4em;
            border-bottom: 3px double #1B2A4A;
            margin-bottom: 0;
        }
        .subheader {
            text-align: center;
            font-family: 'Spectral', serif;
            font-style: italic;
            color: #5B6478;
            font-size: 0.95em;
            margin-top: 0.6em;
            margin-bottom: 1.8em;
        }
        div[data-testid="stForm"] {
            background-color: #FFFDF7;
            border: 1px solid #C9CEDC;
            border-radius: 2px;
            padding: 2em 2em 1.5em;
        }
        div[data-testid="stForm"] h2 {
            font-family: 'Spectral', serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 1em;
            color: #1B2A4A;
            border-bottom: 1px solid #C9CEDC;
            padding-bottom: 0.6em;
            margin-bottom: 1em;
        }
        .stButton button {
            background-color: #1B2A4A;
            color: #F7F3E8;
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 0.85em;
            border: none;
            border-radius: 2px;
            padding: 0.6em 1.8em;
        }
        .stButton button:hover {
            background-color: #28396B;
            color: #F7F3E8;
        }
        .result-card {
            margin-top: 2em;
            display: flex;
            justify-content: center;
        }
        .stamp {
            border: 3px double #B23A2E;
            color: #B23A2E;
            font-family: 'IBM Plex Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            padding: 1em 1.6em;
            text-align: center;
            transform: rotate(-3deg);
            background: transparent;
        }
        .stamp-label {
            display: block;
            font-size: 0.7em;
            letter-spacing: 2px;
            margin-bottom: 0.3em;
            opacity: 0.85;
        }
        .stamp-value {
            display: block;
            font-size: 1.3em;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<h1 class="header">Engineering Career Role Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Based on your academic record and work habits</p>', unsafe_allow_html=True)

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

        st.markdown(f"""
            <div class="result-card">
                <div class="stamp">
                    <span class="stamp-label">Predicted Role</span>
                    <span class="stamp-value">{predicted_job_role}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()