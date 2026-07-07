# Maternal Health Risk Prediction using Machine Learning

This project involves developing a Streamlit web application to predict maternal health risk levels based on user inputs, using various pre-trained machine learning models. The application allows users to enter various health parameters, such as age, blood pressure, blood glucose levels, body temperature, and heart rate. These inputs are preprocessed, and the model predicts a risk level, which is then displayed to the user. 

## Data Set

The below CSV dataset from Kaggle is used as reference for the model:
https://www.kaggle.com/datasets/pyuxbhatt/maternal-health-risk

## Notebook

Maternal_health_risk_prediction.ipynb

## Methodology

1. **Data Preprocessing and Feature Engineering**:

2. **Exploratory Data Analysis (EDA)**:
    After data preprocessing, the next step is exploratory data analysis using different plotting libraries like Matplotlib, Pandas, Seaborn, and Plotly. The following plots were created in this step:
    1. Pie chart
    2. Box plot of numerical features
    3. Count plot
    4. Heatmap or confusion matrix for different models of machine learning
    5. Model comparison graphs
    6. Bar graph
    7. Histogram
    8. Correlation matrix

3. **Model Training and Evaluation**:
    The following machine learning models were selected for training over the processed data:
    - Random Forest
    - Decision Tree
    - KNN
    - Gradient Boosting Machine
    - SVC
    Hyperparameter Tuning: GridSearchCV
    The best-performing model is then loaded into the Streamlit application using the joblib library.

4. **Inference**:
    Deployed the model with the help of a Streamlit web application to predict the maternal health risk level.

## Libraries Used

1. **Joblib**: For downloading the trained model
2. **Scikit-learn**: For machine learning processing and operations\
3. **Pandas**: For data manipulation
4. **NumPy**: For efficient numerical operations
5. **Seaborn**: For advanced data visualizations\
6. **Streamlit**: For creating the GUI of the web application

## How to Use

1. **Clone the Repository**:
    ```sh
    git clone url_to_this_repository
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Model**:
    ```sh
    streamlit run app.py
    ```

4. **View Results**: The script will allow you to predict the maternal health risk level based on the input parameters.

## Demo :

https://github.com/user-attachments/assets/3ded396f-4a3d-4e51-bb8c-784cd4d665d3
