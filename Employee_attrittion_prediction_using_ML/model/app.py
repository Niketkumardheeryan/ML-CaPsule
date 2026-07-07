import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load the pre-trained model
model_knn = joblib.load('knn_model.pkl')

# Load label encoders for categorical variables
gender_encoder = LabelEncoder()
promotion_encoder = LabelEncoder()

# Predefined encodings for gender and promotion
gender_encoder.fit(['Male', 'Female'])
promotion_encoder.fit(['Yes', 'No'])


# Function to preprocess user input
def preprocess_input(data):
    # Encode categorical variables
    data['Gender'] = gender_encoder.transform(data['Gender'])
    data['Promotion_Last_5Years'] = promotion_encoder.transform(data['Promotion_Last_5Years'])

    # Create dummy columns for Department and Job_Title
    data = pd.get_dummies(data, columns=['Department', 'Job_Title'], drop_first=True)

    # Ensure the columns are in the same order as the training data
    X_columns = ['Age', 'Gender', 'Years_at_Company', 'Satisfaction_Level', 'Average_Monthly_Hours',
                 'Promotion_Last_5Years', 'Salary', 'Department_Finance', 'Department_HR',
                 'Department_Marketing', 'Department_Sales', 'Job_Title_Analyst',
                 'Job_Title_Engineer', 'Job_Title_HR Specialist', 'Job_Title_Manager']

    data = data.reindex(columns=X_columns, fill_value=0)
    return data


# UI elements and CSS styling
st.set_page_config(page_title="Employee Attrition Prediction", layout="centered")
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        background-image: url('https://www.transparenttextures.com/patterns/asfalt-light.png');
        background-size: cover;
    }
    .stButton button {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        color: black;
        background-color: #00c853;
        border: none;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    }
    h1 {
        text-align: center;
        font-family: Arial, sans-serif;
        color: red;
    }
    h3 {
        font-family: Arial, sans-serif;
        color: skyblue;
        font-size: 17px;
        text-align: left;
    }
    .container {
        border-radius: 15px;
        padding: 10px 20px;
        margin: 10px auto;
        width: 60%;
        max-width: 800px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        font-family: Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Employee Attrition Prediction</h1>", unsafe_allow_html=True)

# Create input form
with st.form("user_input_form"):
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    st.markdown("<h3>Enter employee information:</h3>", unsafe_allow_html=True)
    gender = st.selectbox("Gender:", ['Male', 'Female'])
    age = st.slider("Age:", 18, 70, 30)
    department = st.selectbox("Department:", ['Marketing', 'Sales', 'Engineering', 'Finance', 'HR'])
    job_title = st.selectbox("Job Title:", ['Manager', 'Engineer', 'Analyst', 'HR Specialist', 'Accountant'])
    years_at_company = st.slider("Years at Company:", 0, 30, 5)
    satisfaction_level = st.slider("Satisfaction Level (0-100):", 0, 100, 50)
    monthly_hours = st.slider("Average Monthly Hours:", 50, 300, 150)
    promotion_last_5_years = st.radio("Promotion in Last 5 Years:", ['Yes', 'No'])
    salary = st.number_input("Salary:", min_value=10000, max_value=200000, step=1000)

    submit_button = st.form_submit_button(label="Predict")

    st.markdown("</div>", unsafe_allow_html=True)

if submit_button:
    user_data = {
        'Gender': gender,
        'Age': age,
        'Department': department,
        'Job_Title': job_title,
        'Years_at_Company': years_at_company,
        'Satisfaction_Level': satisfaction_level,
        'Average_Monthly_Hours': monthly_hours,
        'Promotion_Last_5Years': promotion_last_5_years,  # Update here
        'Salary': salary
    }

    user_df = pd.DataFrame([user_data])
    user_df = preprocess_input(user_df)

    # Predict attrition
    predicted_attrition = model_knn.predict(user_df)

    # Display the result in different colored containers
    container_style = """
        <div class='container' style='background-color: {}; color: black; width: 680px; height: 60px; display: flex; justify-content: center; align-items: flex-start;'>
            <h2 style='text-align: center; margin-top: -20px;'>{}</h2>
        </div>
    """

    # Display result
    if predicted_attrition == 1:
        st.success("The Employee is likely to leave the company.")
    else:
        st.error("The Employee is likely to stay in the company.")
