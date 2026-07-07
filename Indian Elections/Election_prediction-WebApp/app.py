# Importing necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

def value_cleaner(x):
    try:
        str_temp = (x.split('Rs')[1].split('\n')[0].strip())
        str_temp_2 = ''
        for i in str_temp.split(","):
            str_temp_2 = str_temp_2 + i
        return str_temp_2
    except:
        return 0

# Function to load data
def load_data(filepath):
    try:
        return pd.read_csv(filepath)  
    except FileNotFoundError:
        st.error(f"File not found: {filepath}")
        return None
    except pd.errors.ParserError: 
        st.error(f"Error parsing file: {filepath}")
        return None


# Load the dataset
csv_file_path = 'LS_2.0.csv'
vote = load_data(csv_file_path)

if vote is not None: 
    # Data Cleaning
    if 'CRIMINAL\nCASES' in vote.columns: 
        vote['CRIMINAL\nCASES'].replace({np.NaN: 0}, inplace=True)
        vote['CRIMINAL\nCASES'] = pd.to_numeric(vote['CRIMINAL\nCASES'], errors='coerce').fillna(0).astype(np.int64)
    if 'ASSETS' in vote.columns and 'LIABILITIES' in vote.columns:
        vote['ASSETS'] = vote['ASSETS'].apply(value_cleaner).astype(np.int64)
        vote['LIABILITIES'] = vote['LIABILITIES'].apply(value_cleaner).astype(np.int64)


    # Define the main function
    def main():
        st.sidebar.title("Indian Election Prediction App") 
        # Sidebar navigation
        menu = ["About", "Dataset Overview","Visualizations", "Prediction"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        # About section
        if choice == "About":
            st.title("Indian Election Prediction App")
            st.markdown("---")
            st.write("""
            Explore and analyze the intricacies of Indian elections with intuitive web application. Leveraging data science techniques, 
            this app offers a comprehensive overview of election datasets, 
            including constituency distributions, voter demographics, and party performance. 
            Dive into visualizations showcasing state-wise trends and candidate predictions based on key factors like gender, age, and financial assets. 
            Powered by Streamlit and popular Python libraries, this user-friendly tool provides valuable insights into past elections and predicts candidate success, enabling users to understand and anticipate electoral outcomes."
            """)
            st.write("")
            st.write("")

            st.image("images.jpeg", caption="Indian Election Analysis", use_column_width=True)


        # Visualizations section
        elif choice == "Visualizations":
            st.title("Visualization")
            st.markdown("---")  
            st.subheader("State-wise Distribution of Indian Constituencies")
            st_con=vote.groupby('STATE').apply(lambda x:x['CONSTITUENCY'].nunique()).reset_index(name='# Constituency')
            # State-wise distribution of constituencies
            fig2 = px.bar(st_con, x='STATE', y='# Constituency', color='# Constituency', labels={'pop': 'Constituencies of India'})
            fig2.update_layout( template='plotly_dark')
            st.plotly_chart(fig2)
            st.markdown("---")
            # Sunburst Image of state and constituency by voters
            st.subheader("Sunburst Image of State and Constituency by Voters")
            st_con_vt = vote[['STATE', 'CONSTITUENCY', 'TOTAL ELECTORS']]
            fig3 = px.sunburst(st_con_vt, path=['STATE', 'CONSTITUENCY'], values='TOTAL ELECTORS', color='TOTAL ELECTORS', color_continuous_scale='viridis_r')
            fig3.update_layout(template='plotly_dark')
            st.plotly_chart(fig3)
            st.markdown("---")

            st_prty = vote.groupby(['PARTY', 'STATE']).apply(lambda x: x['WINNER'].sum()).reset_index(name='Wins')
            pvt_st_prty = pd.pivot(st_prty, index='PARTY', columns='STATE', values='Wins')
            st.subheader("Statewise report card for the Political Parties in India")
            # Plot the heatmap
            plt.style.use('dark_background')
            plt.figure(figsize=(15, 35))
            sns.heatmap(pvt_st_prty, annot=True, fmt='g', cmap='terrain')
            plt.xlabel('States', size=20)
            plt.ylabel('Party', size=20)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()

        # Prediction Section
        elif choice == "Prediction":
            st.title("Prediction")

            le = LabelEncoder()
            vote['GENDER'] = le.fit_transform(vote['GENDER'])
            vote['PARTY'] = le.fit_transform(vote['PARTY'])

            features = ['GENDER', 'CRIMINAL\nCASES', 'AGE', 'ASSETS', 'LIABILITIES']
            X = vote[features]
            y = vote['WINNER']

            # Handle missing values
            imputer = SimpleImputer(strategy='mean')
            X = imputer.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            model = RandomForestClassifier()
            model.fit(X_train, y_train)

            st.subheader("Input Features for Prediction")
            gender = st.selectbox("Gender", options=['Male', 'Female'])
            criminal_cases = st.number_input("Criminal Cases", min_value=0, step=1)
            age = st.number_input("Age", min_value=25, max_value=100, step=1)
            assets = st.number_input("Assets (in Rs)", min_value=0, step=1)
            liabilities = st.number_input("Liabilities (in Rs)", min_value=0, step=1)

            gender_encoded = 1 if gender == 'Female' else 0
            input_data = np.array([[gender_encoded, criminal_cases, age, assets, liabilities]])
            input_data = imputer.transform(input_data)
            prediction = model.predict(input_data)
            prediction_prob = model.predict_proba(input_data)

            if prediction[0] == 1:
                st.success(f"The candidate is likely to win with a probability of {prediction_prob[0][1]*100:.2f}%")
            else:
                st.error(f"The candidate is unlikely to win with a probability of {prediction_prob[0][0]*100:.2f}%")
            st.markdown("---")
            st.subheader("Prediction Probabilities")
            classes = model.classes_
            probabilities = prediction_prob[0]
            df_pred_prob = pd.DataFrame({"Class": classes, "Probability": probabilities})
            fig_pred_prob = px.bar(df_pred_prob, x='Class', y='Probability', color='Class', labels={'Class': 'Prediction Class', 'Probability': 'Probability'})
            fig_pred_prob.update_layout(template='plotly_dark')
            st.plotly_chart(fig_pred_prob)
        
        # Overview section
        elif choice == "Dataset Overview":
            st.title("Overview of the Dataset")
            st.write("""The dataset contains information on Indian election constituencies, including details about candidates, parties, and electoral statistics. Each entry includes data such as the state, constituency name, candidate name, party affiliation, gender, age, educational background, assets, liabilities, and voting statistics. Key features like criminal cases, gender, age, and financial status provide insights into candidate profiles, while voting metrics offer an overview of electoral participation and outcomes. With comprehensive information on candidates and constituencies, this dataset facilitates 
                     analysis of electoral trends, candidate demographics, and the electoral process's overall dynamics in India.""")
            st.markdown("---")
            st.write(vote.describe())
            st.markdown("---")
            st.subheader("Faetures in the Dataset:")
            features = [
                'STATE', 'CONSTITUENCY', 'NAME', 'WINNER', 'PARTY', 'SYMBOL', 'GENDER', 
                'CRIMINAL CASES', 'AGE', 'CATEGORY', 'EDUCATION', 'ASSETS', 'LIABILITIES', 
                'GENERAL VOTES', 'POSTAL VOTES', 'TOTAL VOTES', 'OVER TOTAL ELECTORS IN CONSTITUENCY', 
                'OVER TOTAL VOTES POLLED IN CONSTITUENCY', 'TOTAL ELECTORS'
            ]

            # Display the list of features
            st.write("### List of Features:")
            for feature in features:
                st.write("- " + feature)

    if __name__ == '__main__': 
        main()


