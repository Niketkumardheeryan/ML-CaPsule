import streamlit as st
import pandas as pd
import joblib

# Load the trained model
gb_model = joblib.load('gradient_boosting_model.pkl')

# List of unique values for categorical columns
occupation_values = ['Account Executive', 'Accountant', 'Architect', 'Bank Teller', 'Businessman', 'Chef',
                     'Construction Worker', 'Customer Service', 'Customer Service Rep', 'Data Scientist',
                     'Dental Assistant', 'Dental Hygienist', 'Doctor', 'Electrician', 'Engineer',
                     'Event Planner', 'Financial Advisor', 'Financial Analyst', 'Graphic Artist',
                     'Graphic Design', 'Graphic Designer', 'Hair Stylist', 'Human Resources',
                     'Human Resources Manager', 'IT Manager', 'Insurance Agent', 'Lawyer',
                     'Marketing Coordinator', 'Marketing Exec', 'Marketing Manager', 'Mechanic',
                     'Mechanical Engineer', 'Mechanical Technician', 'Medical Assistant', 'Musician',
                     'Nurse', 'Other', 'Personal Trainer', 'Pharmacist', 'Photographer',
                     'Physical Education Teacher', 'Physical Therapist', 'Plumber', 'Police Officer',
                     'Project Manager', 'Real Estate Agent', 'Retail Manager', 'Sales Manager',
                     'Sales Representative', 'Salesperson', 'Social Worker', 'Software Developer',
                     'Software Engineer', 'Teacher', 'Veterinarian', 'Web Designer', 'Web Developer',
                     'Writer']

finance_status_values = ['Excellent', 'Fair', 'Good', 'Poor', 'Stable', 'Unknown', 'Unstable']
finance_history_values = ['Excellent', 'Fair', 'Good', 'Late payment', 'Missed payments', 'No issue', 'Poor']


# Function to preprocess input data similar to training data
def preprocess_input(data):
    # Example of preprocessing steps (replace with actual preprocessing steps)
    data['Occupation'] = data['Occupation'].apply(lambda x: x if x in occupation_values else 'Other')
    data['Finance Status'] = data['Finance Status'].apply(lambda x: x if x in finance_status_values else 'Unknown')
    data['Finance History'] = data['Finance History'].apply(lambda x: x if x in finance_history_values else 'Unknown')

    # One-hot encode categorical variables
    data = pd.get_dummies(data, columns=['Occupation', 'Finance Status', 'Finance History'])

    # Ensure all columns are present and in the same order as in training
    data = data.reindex(columns=model_columns, fill_value=0)

    return data


# Define the model columns based on the provided index
model_columns = ['Monthly Income', 'Credit Score', 'Years of Employment', 'Number of Children',
                 'Occupation_Account Executive', 'Occupation_Accountant', 'Occupation_Architect',
                 'Occupation_Bank Teller', 'Occupation_Businessman', 'Occupation_Chef',
                 'Occupation_Construction Worker', 'Occupation_Customer Service',
                 'Occupation_Customer Service Rep', 'Occupation_Data Scientist',
                 'Occupation_Dental Assistant', 'Occupation_Dental Hygienist',
                 'Occupation_Doctor', 'Occupation_Electrician', 'Occupation_Engineer',
                 'Occupation_Event Planner', 'Occupation_Financial Advisor',
                 'Occupation_Financial Analyst', 'Occupation_Graphic Artist',
                 'Occupation_Graphic Design', 'Occupation_Graphic Designer',
                 'Occupation_Hair Stylist', 'Occupation_Human Resources',
                 'Occupation_Human Resources Manager', 'Occupation_IT Manager',
                 'Occupation_Insurance Agent', 'Occupation_Lawyer',
                 'Occupation_Marketing Coordinator', 'Occupation_Marketing Exec',
                 'Occupation_Marketing Manager', 'Occupation_Mechanic',
                 'Occupation_Mechanical Engineer', 'Occupation_Mechanical Technician',
                 'Occupation_Medical Assistant', 'Occupation_Musician',
                 'Occupation_Nurse', 'Occupation_Other', 'Occupation_Personal Trainer',
                 'Occupation_Pharmacist', 'Occupation_Photographer',
                 'Occupation_Physical Education Teacher',
                 'Occupation_Physical Therapist', 'Occupation_Plumber',
                 'Occupation_Police Officer', 'Occupation_Project Manager',
                 'Occupation_Real Estate Agent', 'Occupation_Retail Manager',
                 'Occupation_Sales Manager', 'Occupation_Sales Representative',
                 'Occupation_Salesperson', 'Occupation_Social Worker',
                 'Occupation_Software Developer', 'Occupation_Software Engineer',
                 'Occupation_Teacher', 'Occupation_Veterinarian',
                 'Occupation_Web Designer', 'Occupation_Web Developer',
                 'Occupation_Writer', 'Finance Status_Excellent', 'Finance Status_Fair',
                 'Finance Status_Good', 'Finance Status_Poor', 'Finance Status_Stable',
                 'Finance Status_Unknown', 'Finance Status_Unstable',
                 'Finance History_Excellent', 'Finance History_Fair',
                 'Finance History_Good', 'Finance History_Late payment',
                 'Finance History_Missed payments', 'Finance History_No issue',
                 'Finance History_Poor']


# Streamlit application with custom CSS
def main():
    # Custom CSS styles
    st.markdown(
        """
        <style>
        .input-container {
            background-color: #f5f5f5;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
            color: #333;
        }

        .input-container h2 {
            font-size: 24px;
            color: #3498db;
            margin-bottom: 10px;
        }

        .input-container select, 
        .input-container input[type=number] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
        }

        .input-container select {
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            background: transparent;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23000000' height='24' viewBox='0 0 24 24' width='24'%3E%3Cpath d='M7 10l5 5 5-5H7z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position-x: calc(100% - 10px);
            background-position-y: center;
        }

        .input-container button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 4px;
        }

        .input-container button:hover {
            background-color: #2980b9;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Main page layout with input container
    st.title('Car Ownership Prediction')
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    # Input fields for user within the input container
    occupation = st.selectbox('Occupation', occupation_values)
    monthly_income = st.number_input('Monthly Income', min_value=0)
    credit_score = st.number_input('Credit Score', min_value=0)
    years_of_employment = st.number_input('Years of Employment', min_value=0)
    finance_status = st.selectbox('Finance Status', finance_status_values)
    finance_history = st.selectbox('Finance History', finance_history_values)
    number_of_children = st.number_input('Number of Children', min_value=0)

    # End of input container
    st.markdown('</div>', unsafe_allow_html=True)

    # Predict button
    if st.button('Predict'):
        # Create a dictionary with user input
        input_data = {
            'Occupation': [occupation],
            'Monthly Income': [monthly_income],
            'Credit Score': [credit_score],
            'Years of Employment': [years_of_employment],
            'Finance Status': [finance_status],
            'Finance History': [finance_history],
            'Number of Children': [number_of_children]
        }

        # Convert input data to DataFrame
        input_df = pd.DataFrame(input_data)

        # Preprocess input data
        input_processed = preprocess_input(input_df)

        # Make prediction
        prediction = gb_model.predict(input_processed)

        # Display prediction result with styling
        if prediction[0] == 1:
            st.success("You own a Car")
        else:
            st.error("You do not own a Car")


# Run the Streamlit app
if __name__ == '__main__':
    main()
