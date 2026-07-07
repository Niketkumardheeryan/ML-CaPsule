import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title='Maternal Health Risk Prediction', page_icon=':baby:', layout='wide')

model = joblib.load('maternal_health_risk.sav')

st.title('Maternal Health Risk Prediction')
st.markdown('## Predict the risk level of maternal health based on various health parameters.')

def user_input_features():
    age = st.slider('Age', 10, 50, 25)
    systolic_bp = st.slider('Systolic BP', 80, 200, 120)
    diastolic_bp = st.slider('Diastolic BP', 50, 120, 80)
    bs = st.slider('Blood Glucose Level (mmol/L)', 1.0, 20.0, 5.0)
    body_temp_f = st.slider('Body Temperature (°F)', 50.0, 150.0, 98.0)
    heart_rate = st.slider('Heart Rate (bpm)', 50, 150, 70)
        
    data = {
        'Age': age,
        'SystolicBP': systolic_bp,
        'DiastolicBP': diastolic_bp,
        'BS': bs,
        'BodyTemp': body_temp_f,
        'HeartRate': heart_rate
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

st.subheader('User Input Parameters')
st.write(input_df)

if st.button('Predict'):
    prediction = model.predict(input_df)
    st.subheader('Prediction')
    risk_levels = ['Low Risk', 'Mid Risk', 'High Risk']
    st.write(f"**Risk Level:** {risk_levels[prediction[0]]}")