# Student performance and grade prediction using Machine learning

The updated Streamlit application for predicting a student's performance index features a sleek, dark-themed design with a central focus on usability and aesthetics. It uses a pre-trained Random Forest model, loaded via joblib, to predict performance based on user inputs such as hours studied, previous scores, extracurricular activities, and more. Inputs are collected through a form with sliders and select boxes, and predictions are displayed with rounded values and categorized grades. Custom CSS enhances the UI with contrasting colors, borders, and padding to create a visually appealing and user-friendly interface.


## Data Set

The dataset link is are as follows :-https://www.kaggle.com/datasets/nikhil7280/student-performance-multiple-linear-regression

on this dataset, below processing are performed :
1) featue scaling and column reinitialization
2) errors and outliers removal using box plot
3) remove na,missing values , regularization etc
4) Drop duplicates , normalization , column dropping


(all this works ar depicted in student_performance_predictionn.ipynb file)


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
  

4. **Model Training and evaluation**: 
     The four machine learning model Decision Tree ,SVM (linear kernel) ,Random Forest, Multiple linear regression are selected for model training over the inputed processed data:

     The most accurate Random Forest model is then loaded into streamlit application after installing and using joblib library.

5. **Inference**: 
      Deployed the model with the help streamlit web application to predict the student marks and grade using ML.

## Libraries Used

1. **Joblib**: For downloading the RF model
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


3. **Download the model and Run the Model**: 
   
    link : https://drive.google.com/file/d/1PFrcz_8IhXIudi5h-uxJo6VDZE7r058d/view?usp=sharing
    
    ```python
    streamlit run app.py
    ```


## Demo :




https://github.com/user-attachments/assets/e9ad6c27-42c7-4abc-93f9-162ac590e03c







