# Migraine Type Prediction using Machine Learning

This project involves developing a Streamlit web application to predict migraine types based on user inputs, using various pre-trained machine learning models. The application allows users to enter various health parameters, such as age, gender, headache frequency, and other relevant symptoms. These inputs are preprocessed, and the model predicts a migraine type, which is then displayed to the user.

## Data Set

The below CSV dataset is used as reference for the model:
https://www.kaggle.com/datasets/ranzeet013/migraine-dataset

## Notebook

Migraine_Prediction_System.ipynb

## Methodology

1. **Data Preprocessing and Feature Engineering**:

2. **Exploratory Data Analysis (EDA)**:
    After data preprocessing, the next step is exploratory data analysis using different plotting libraries like Matplotlib, Pandas, Seaborn, and Plotly.

3. **Model Training and Evaluation**:
    The following machine learning models were selected for training over the processed data:
    - Random Forest Classifier
    The best-performing model is then loaded into the Streamlit application using the joblib library.

4. **Inference**:
    Deployed the model with the help of a Streamlit web application to predict the migraine type.

## Libraries Used

1. **Joblib**: For downloading the trained model
2. **Scikit-learn**: For machine learning processing and operations
3. **Matplotlib**: For plotting and visualizing the results
4. **Pandas**: For data manipulation
5. **Seaborn**: For advanced data visualizations
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

4. **View Results**: The script will allow you to predict the migraine type based on the input parameters.

## Demo :

https://github.com/user-attachments/assets/20343f8e-1284-4067-85ca-bd3072239860

