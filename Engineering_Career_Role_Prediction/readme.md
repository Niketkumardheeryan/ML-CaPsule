#  Engineering Career Role Prediction using Machine learning

This project involves developing a Streamlit web application to predict job roles based on user inputs, using a pre-trained Logistic Regression model. The application allows users to enter various academic and personal details, such as percentages in different subjects, hours worked per day, number of hackathons participated in, coding skills rating, and several other attributes. These inputs are preprocessed, with categorical features encoded using LabelEncoder. The model predicts a numeric value representing a job role, which is then mapped to a specific job title like 'Data Scientist' or 'Software Developer'. The user interface is styled with custom CSS to enhance the visual appeal, featuring a dark theme, centered light green heading, and input/output containers with specific styling. Users can submit their details through a form, and the predicted job role is displayed in a styled message upon submission, making the application user-friendly and visually engaging.


## Data Set

The below csv dataset from kaggle is used as reference for model :

https://www.kaggle.com/datasets/amitvkulkarni/hair-health


## Notebook

Engineering_career_role_prediction.ipynb

## Methodology

The project follows the below structured methodology ranging from data preprocessing pipeline to model training, evaluation and deployment :-

1. **Data Preprocessing and feature enginnering**:

2. **Exploratory Data Analysis (EDA)**:
    after Data preprocessing the next step is Exploratory  data analysis using different plotting libraries like matplotlib,pandas,seaborn and plotly.following plots were plotted in this step:-
    1) Pie chart 
    2) violin plot 
    3) box plot of numerical features
    4) count plot 
    5) heatmap or confusion matrix for four different models of machine learning
    6) model comparison graphs
    7) line plots
    8) roc curve
    9) bar graph
    10) histogram
    11) correlation matirx
    (refer images folder for this images and graph observation)


4. **Model Training and evaluation**: 
   
     The five machine learning model random forest ,logistic ,KNN, gradient boosting machine, Naive Bayes are selected for model training over the inputed processed data.
   
     The naive bayes machine model is then loaded into streamlit application after installing and using joblib library.

5. **Inference**: 
      Deployed the model with the help streamlit web application to predict the Engineering industry's most suitable role of the candidate.


## Libraries Used

1. **Joblib**: For downloading the random forest model
2. **Scikit learn**: For machine learning processing  and operations
3. **Matplotlib**: For plotting and visualizing the detection results.
4. **Pandas**: For image manipulation.
5. **NumPy**: For efficient numerical operations.
6. **Seaborn** : for advanced data visualizations
7. **plotly** : for 3D data visualizations .
8. **Streamlit** : for creating gui of the web application.



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

4. **View Results**: The script will allow you to predict Job role for the engineering student.

## Demo :


https://github.com/user-attachments/assets/7075aaf4-ed20-4f2a-a454-1d2b48c530b1


