import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import requests

# Load the trained KNN model
model = joblib.load('knn_model.pkl')

# Define model columns for preprocessing
model_columns = ['Age', 'Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card',
                 'Interest_Rate', 'Num_of_Loan', 'Num_of_Delayed_Payment',
                 'Num_Credit_Inquiries', 'Total_Debt', 'Credit_Utilization_Ratio',
                 'Occupation_Architect', 'Occupation_Developer',
                 'Occupation_Doctor', 'Occupation_Engineer', 'Occupation_Entrepreneur',
                 'Occupation_Journalist', 'Occupation_Lawyer', 'Occupation_Manager',
                 'Occupation_Mechanic', 'Occupation_Media_Manager',
                 'Occupation_Musician', 'Occupation_Scientist', 'Occupation_Teacher',
                 'Occupation_Writer', 'Type_of_Credits_Low', 'Type_of_Credits_Medium',
                 'Previous_Payment_history_Unpaid',
                 'Payment_Behaviour_High Spent and Medium value payments',
                 'Payment_Behaviour_High Spent and Small value payments',
                 'Payment_Behaviour_Low Spent and Large value payments',
                 'Payment_Behaviour_Low Spent and Medium value payments',
                 'Payment_Behaviour_Low Spent and Small value payments']


# Function to preprocess input data
def preprocess_input(df):
    # Encode categorical variables if necessary
    categorical_cols = ['Occupation', 'Type_of_Credits', 'Previous_Payment_history', 'Payment_Behaviour']
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    # Ensure all columns are present and in the same order as in training
    df_encoded = df_encoded.reindex(columns=model_columns, fill_value=0)
    return df_encoded


# Function to predict credit score
def predict_credit_score(input_data):
    # Preprocess input data
    input_df = pd.DataFrame([input_data])
    input_df_processed = preprocess_input(input_df)

    # Make prediction
    prediction = model.predict(input_df_processed)

    return prediction[0]  # Return the predicted class index


# Function to display semi-circular gauge chart with Plotly
def display_gauge(predicted_score):
    plot_bgcolor = "#28282B"  # Dark gray background
    quadrant_colors = [plot_bgcolor, "#f25829", "#eff229", "#2bad4e"]
    quadrant_text = ["", "<b>High</b>", "<b>Medium</b>", "<b>Low</b>"]
    n_quadrants = len(quadrant_colors) - 1

    min_value = 0
    max_value = 2  # Maximum value for predicted_score
    hand_length = np.sqrt(2) / 6

    # Calculate hand angle based on predicted score
    if predicted_score == 0:
        hand_angle = np.pi * 0.25  # 45 degrees
    elif predicted_score == 1:
        hand_angle = np.pi * 0.5  # 90 degrees
    elif predicted_score == 2:
        hand_angle = np.pi * 0.75  # 135 degrees

    fig = go.Figure(
        data=[
            go.Pie(
                values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                rotation=90,
                hole=0.5,
                marker_colors=quadrant_colors,
                text=quadrant_text,
                textinfo="text",
                hoverinfo="skip",
            ),
        ],
        layout=go.Layout(
            showlegend=False,
            margin=dict(b=0, t=0, l=10, r=10),
            width=650,
            height=450,
            paper_bgcolor=plot_bgcolor,
            shapes=[
                go.layout.Shape(
                    type="circle",
                    x0=0.48, x1=0.52,
                    y0=0.48, y1=0.52,
                    fillcolor="#ffffff",
                    line_color="#ffffff",
                ),
                go.layout.Shape(
                    type="line",
                    x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                    y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                    line=dict(color="#ffffff", width=4)
                )
            ]
        )
    )
    return fig  # Return the Plotly figure object


# Function to fetch credit score information from a mock API
def fetch_credit_score_info():
    # Example data, replace this with actual API call
    credit_info = {
        "average_credit_score": 690,
        "highest_credit_score": 850,
        "lowest_credit_score": 300,
        "credit_score_distribution": {
            "Excellent": 20,
            "Very Good": 25,
            "Good": 30,
            "Fair": 15,
            "Poor": 10
        }
    }
    return credit_info


# Function to fetch recent news about credit scores
# Function to fetch recent news about credit scores and banking
def fetch_recent_news(api_key):
    url = f"https://newsapi.org/v2/everything?q=credit+score+banking&apiKey={api_key}&pageSize=10"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get('articles', [])

    # Filter articles with missing content or images
    valid_articles = []
    for article in articles:
        if article.get("description") and article.get("urlToImage"):
            valid_articles.append(article)
        if len(valid_articles) >= 6:
            break

    return valid_articles[:6]


# Streamlit App
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Credit Score Classification", "Credit Score Information"])

    if selection == "Credit Score Classification":
        st.title('Credit Score Classification App')

        # Collect user inputs
        age = st.number_input('Age', min_value=18, max_value=100, value=30)
        occupation = st.selectbox('Occupation',
                                  ['Scientist', 'Teacher', 'Engineer', 'Entrepreneur', 'Developer', 'Lawyer',
                                   'Media_Manager', 'Doctor', 'Journalist', 'Manager', 'Accountant', 'Musician',
                                   'Mechanic', 'Writer', 'Architect'])
        annual_income = st.number_input('Annual Income', min_value=0, value=50000)
        num_bank_accounts = st.number_input('Number of Bank Accounts', min_value=0, value=1)
        num_credit_cards = st.number_input('Number of Credit Cards', min_value=0, value=1)
        interest_rate = st.number_input('Interest Rate', min_value=0, value=10)
        num_of_loan = st.number_input('Number of Loans', min_value=0, value=1)
        num_of_delayed_payment = st.number_input('Number of Delayed Payments', min_value=0, value=0)
        num_credit_inquiries = st.number_input('Number of Credit Inquiries', min_value=0, value=1)
        type_of_credits = st.selectbox('Type of Credits', ['High', 'Medium', 'Low'])
        total_debt = st.number_input('Total Debt', min_value=0, value=10000)
        credit_utilization_ratio = st.number_input('Credit Utilization Ratio', min_value=0.0, value=30.0)
        previous_payment_history = st.selectbox('Previous Payment History', ['Paid', 'Unpaid'])
        payment_behaviour = st.selectbox('Payment Behaviour', ['High Spent and Small value payments',
                                                               'Low Spent and Large value payments',
                                                               'Low Spent and Medium value payments',
                                                               'Low Spent and Small value payments',
                                                               'High Spent and Medium value payments',
                                                               'High Spent and Large value payments'])

        # Create a dictionary of user inputs
        input_data = {
            'Age': age,
            'Occupation': occupation,
            'Annual_Income': annual_income,
            'Num_Bank_Accounts': num_bank_accounts,
            'Num_Credit_Card': num_credit_cards,
            'Interest_Rate': interest_rate,
            'Num_of_Loan': num_of_loan,
            'Num_of_Delayed_Payment': num_of_delayed_payment,
            'Num_Credit_Inquiries': num_credit_inquiries,
            'Type_of_Credits': type_of_credits,
            'Total_Debt': total_debt,
            'Credit_Utilization_Ratio': credit_utilization_ratio,
            'Previous_Payment_history': previous_payment_history,
            'Payment_Behaviour': payment_behaviour
        }

        # Predict credit score on button click
        if st.button('Predict', key='prediction_button'):
            predicted_score = predict_credit_score(input_data)

            # Display result with styled messages
            st.subheader('Prediction')
            if predicted_score == 0:
                st.success(f'**Good Credit Score**')
            elif predicted_score == 1:
                st.warning(f'**Standard Credit Score**')
            elif predicted_score == 2:
                st.error(f'**Poor Credit Score**')

            # Display gauge chart in the center
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.plotly_chart(display_gauge(predicted_score), use_container_width=True)

    elif selection == "Credit Score Information":
        st.title('Credit Score Information')

        # Fetch credit score information
        credit_info = fetch_credit_score_info()

        # Display credit score information in a paragraph
        st.header("About Credit Scores")
        st.write("""
            A credit score is a numerical expression based on a level analysis of a person's credit files, 
            to represent the creditworthiness of an individual. Lenders, such as banks and credit card companies, 
            use credit scores to evaluate the potential risk posed by lending money to consumers and to mitigate losses 
            due to bad debt. Credit scores are determined by credit bureaus, who gather information about consumers' 
            financial history and provide that information in a numerical format.
        """)

        # Display credit score classification range table
        st.header("Credit Score Classification")
        classification_data = {
            "Credit Score Range": ["300-579", "580-669", "670-739", "740-799", "800-850"],
            "Classification": ["Poor", "Fair", "Good", "Very Good", "Excellent"],
            "Significance": [
                "Considered a poor credit score. Likely to be declined for loans and credit cards.",
                "Below average. Might qualify for some loans, but with higher interest rates.",
                "Average. Should qualify for most loans and credit cards with average interest rates.",
                "Above average. Likely to qualify for loans and credit cards with favorable terms.",
                "Excellent. Should have no problems getting approved for loans and credit cards with the best terms."
            ]
        }
        classification_df = pd.DataFrame(classification_data)
        st.table(classification_df)

        # Display credit score statistics
        st.header("Credit Score Statistics")
        st.metric("Average Credit Score", credit_info["average_credit_score"])
        st.metric("Highest Credit Score", credit_info["highest_credit_score"])
        st.metric("Lowest Credit Score", credit_info["lowest_credit_score"])

        # Display credit score distribution
        st.header("Credit Score Distribution")
        distribution = pd.DataFrame(list(credit_info["credit_score_distribution"].items()),
                                    columns=["Category", "Percentage"])
        fig = px.bar(distribution, x="Category", y="Percentage", title="Credit Score Distribution",
                     labels={"Percentage": "Percentage (%)"})
        st.plotly_chart(fig)

        # Display more organized graphs about credit scores
        st.header("Additional Credit Score Insights")

        # Example graphs (these should be based on actual data from the API)
        example_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Average Credit Score": [680, 685, 690, 695, 700, 705, 710, 715, 720, 725, 730, 735]
        })
        fig1 = px.line(example_data, x="Month", y="Average Credit Score", title="Average Credit Score Over the Year")
        st.plotly_chart(fig1)

        example_data2 = pd.DataFrame({
            "Credit Score Range": ["300-579", "580-669", "670-739", "740-799", "800-850"],
            "Number of People": [50, 100, 200, 150, 75]
        })
        fig2 = px.pie(example_data2, values="Number of People", names="Credit Score Range",
                      title="Credit Score Range Distribution")
        st.plotly_chart(fig2)

        example_data3 = pd.DataFrame({
            "Credit Score": ["Poor", "Fair", "Good", "Very Good", "Excellent"],
            "Interest Rate": [25, 20, 15, 10, 5]
        })
        fig3 = px.bar(example_data3, x="Credit Score", y="Interest Rate",
                      title="Average Interest Rates by Credit Score")
        st.plotly_chart(fig3)

        st.header("Recent News")
        api_key = "ENTER_YOUR_NewsAPI_Key"  # Replace with your NewsAPI key obtained from NewsAPI.com
        news_articles = fetch_recent_news(api_key)

        for i, article in enumerate(news_articles):
            if i % 2 == 0:
                col1, col2 = st.columns(2)
            with col1 if i % 2 == 0 else col2:
                st.subheader(article["title"])
                st.image(article["urlToImage"], use_column_width=True)
                st.write(article["description"])
                st.write(f"[Read more]({article['url']})")


if __name__ == '__main__':
    main()
