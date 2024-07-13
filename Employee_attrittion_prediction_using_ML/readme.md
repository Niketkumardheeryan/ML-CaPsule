# Employee Attrittion prediction using Machine Learning

This project involves creating a user-friendly Streamlit application for predicting employee attrition using a pre-trained KNN model. The application gathers relevant employee information such as age, gender, department, job title, years at the company, satisfaction level, average monthly hours, promotion history, and salary through a well-designed form. The app preprocesses the input data, including label encoding for categorical variables and one-hot encoding for specific features. Upon submission, the app predicts whether an employee is likely to leave or stay at the company, displaying the results in aesthetically pleasing colored containers—green for high attrition risk and red for low attrition risk. The project emphasizes enhanced UI/UX, incorporating custom CSS for styling, centered bold headers, and a background pattern to ensure a visually appealing interface. The final product is a comprehensive, intuitive tool for HR departments to anticipate and address employee attrition effectively.


## Data Set

The dataset link is are as follows :-https://www.kaggle.com/datasets/mrsimple07/employee-attrition-data-prediction

on this dataset, below processing are performed :
1) featue scaling and column reinitialization
2) errors and outliers removal using box plot
3) remove na,missing values , regularization etc
4) Drop duplicates , normalization , column dropping
5) Oversampling

(all this works ar depicted in employee_attrityion_prediction.ipynb file)


## Methodology

The project follows the below structured methodology ranging from data preprocessing pipeline to feature engineering model training, evaluation and deployment :-

1. **Data Preprocessing and feature enginnering**

2. **Exploratory Data Analysis (EDA)**:
    after Data preprocessing the next step is Exploratory  data analysis using different plotting libraries like matplotlib,pandas,seaborn and plotly.following plots were plotted in this step:-
    1) Pie charts
    2) violen plots
    3) box plot of numerical features
    4) count plots
    5) histogram
    6) model comparison graphs
    7) confusion matrix
    8) Correlation metrices
    (refer images folder for this images and graph observation)


4. **Model Training and evaluation**: 
     The four machine learning model Naive Bayes ,XgBoost ,KNN, gradient boosting machine are selected for model training over the inputed processed data:

     The most accurate KNN model is then loaded into streamlit application after installing and using joblib library.

5. **Inference**: 
      Deployed the model with the help streamlit web application to predict the atttrition level of employee

## Libraries Used

1. **Joblib**: For downloading the KNN model
2. **Scikit learn**: For machine learning processing  and operations
3. **Matplotlib**: For plotting and visualizing the detection results.
4. **Pandas**: For Data manipulation.
5. **NumPy**: For efficient numerical operations.
6. **Seaborn** : for advanced data visualizations
7. **plotly** : for 3D data visualizations .
8. **Streamlit** : for creating gui of the web application.
9. **requests** : requests for creating Htttp requests

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
    ```python
    streamlit run app.py
    ```

4. **View Results**:  The script will allow you to predict whether the employee is going to stay in the company or leave the company  based on various parametrs like work of experience, age , promoted in the past , position held, sector in which employee works , satisfaction level and average monthly hours the employee works in the company using machine learning models and result is outputted on the streamlit based application using python as shown in the demo.

## Demo 


https://github.com/user-attachments/assets/d7f232d6-ac43-4075-8691-eba04b99a5d4

