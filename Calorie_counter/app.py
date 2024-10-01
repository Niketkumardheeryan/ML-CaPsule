import streamlit as st
import pickle
import pandas as pd

# Load the pickled model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

def main():
    st.markdown("""
    <style>
    .title {
        font-size: 2.5em;
        color: #333;
        text-align: center;
        margin-bottom: 20px;
    }
    .input {
        width: 100%;
        padding: 10px;
        margin-bottom: 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    .button {
        background-color: #007bff;
        color: #fff;
        border: none;
        cursor: pointer;
        font-size: 1em;
        padding: 10px 20px;
        border-radius: 4px;
    }
    .button:hover {
        background-color: #0056b3;
    }
    .result {
        margin-top: 20px;
        font-size: 1.2em;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">Calorie Burnt Predictor</div>', unsafe_allow_html=True)

    # Input fields
    gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
    age = st.number_input("Age", min_value=0, max_value=120, value=25, key="age")
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170, key="height")
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, key="weight")
    duration = st.number_input("Duration (minutes)", min_value=0, max_value=180, value=30, key="duration")
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=70, key="heart_rate")
    body_temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=37.0, key="body_temp")

    if st.button("Predict", key="predict"):
        # Prepare the input data
        data = {
            'Gender': [1 if gender == "Male" else 0],
            'Age': [age],
            'Height': [height],
            'Weight': [weight],
            'Duration': [duration],
            'Heart_Rate': [heart_rate],
            'Body_Temp': [body_temp]
        }
        data_df = pd.DataFrame(data)

        # Make prediction
        prediction = model.predict(data_df)

        st.markdown(f'<div class="result">Predicted Calories: {prediction[0]:.2f}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
