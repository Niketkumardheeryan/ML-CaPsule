import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans

# Load dataset
df = pd.read_csv('fitness_health_data.csv')

# Define pages
def home():
    st.title("Fitness and Health Tracker")
    st.write("This application provides insights into users' fitness and health data through Exploratory Data Analysis (EDA) and Machine Learning algorithms.")

def eda():
    st.title("Exploratory Data Analysis")
    
    st.write("## Dataset")
    st.write(df.head())
    
    st.write("## Descriptive Statistics")
    st.write(df.describe())
    
    st.write("## Histograms")
    fig, ax = plt.subplots()
    df.hist(bins=20, figsize=(15, 10), ax=ax)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("## Pair Plot")
    sns.pairplot(df)
    st.pyplot()
    
    st.write("## Box Plot")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)
    
    st.write("## Correlation Matrix Heatmap")
    corr_matrix = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    plt.title('Correlation Matrix Heatmap')
    st.pyplot(fig)

def calories_prediction():
    st.title("Calories Burned Prediction")
    
    st.write("## Input Features")
    steps = st.number_input('Steps', min_value=0, value=5000)
    distance = st.number_input('Distance (km)', min_value=0.0, value=4.0)
    active_minutes = st.number_input('Active Minutes', min_value=0, value=60)
    
    features = ['Steps', 'Distance', 'Active_Minutes']
    target = 'Calories'
    X = df[features]
    y = df[target]
    model = LinearRegression()
    model.fit(X, y)
    
    input_data = pd.DataFrame([[steps, distance, active_minutes]], columns=features)
    prediction = model.predict(input_data)[0]
    
    st.write(f"## Predicted Calories Burned: {prediction:.2f}")
    st.write(f"## Model Coefficients: {model.coef_}")
    st.write(f"## Mean Squared Error: {mean_squared_error(y, model.predict(X)):.2f}")

def heart_rate_clustering():
    st.title("Heart Rate Clustering")
    
    heart_rate = df[['User_ID', 'Heart_Rate']].groupby('User_ID').mean().reset_index()
    kmeans = KMeans(n_clusters=3, random_state=42)
    heart_rate['Cluster'] = kmeans.fit_predict(heart_rate[['Heart_Rate']])
    
    fig, ax = plt.subplots()
    plt.scatter(heart_rate['User_ID'], heart_rate['Heart_Rate'], c=heart_rate['Cluster'], cmap='viridis')
    plt.xlabel('User ID')
    plt.ylabel('Average Heart Rate')
    plt.title('Heart Rate Clustering')
    st.pyplot(fig)

# Streamlit navigation
pages = {
    "Home": home,
    "EDA": eda,
    "Calories Prediction": calories_prediction,
    "Heart Rate Clustering": heart_rate_clustering,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

page = pages[selection]
page()
