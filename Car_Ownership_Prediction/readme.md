#  Car ownership prediction using Machine learning

This project predicts whether the user has a capability to own a car or not based on many input features like occupation,monthly income, credit score ,year of eployement, financial status, financial history , car and number of children.

This project could be useful source in financial field for asset predictability and to measure its association with different input features.

## Data Set

The below csv dataset from kaggle is used as reference which contains nearly 600+ rows (car_ownership.csv) on which porcessing is performed to obtained a  processed data processed_data_car.csv , all this processing is performed in first notebook (car_ownership_data_preprocessing.ipynb) file.

The dataset link is are as follows :-
https://www.kaggle.com/datasets/rkiattisak/car-ownership-predictionbeginner-intermediate

on this dataset, below processing are performed :
1) featue scaling and column reinitialization
2) errors and outliers removal
3) remove na,missing values , regularization etc
(all this works ar depicted in car-ownership_data_preprocessing file)

The model is trained on processed_data_car.csv file and all works associated with it are depicted in car_ownership_model_training.ipynb file.

## Methodology

The project follows the below structured methodology ranging from data preprocessing pipeline to model training, evaluation and deployment :-

1. **Data Preprocessing and feature enginnering**: 
2. **Exploratory Data Analysis (EDA)**:
    after Data preprocessing the next step is Exploratory  data analysis using different plotting libraries like matplotlib,pandas,seaborn and plotly.following plots were plotted in this step:-
    1) Pie chart of financial history and financial status types
    2) violen plot of credit scores
    3) box plot of numerical features
    4) count plot of all occupations
    5) heatmap or confusion matrix for four different models of machine learning
    6) model comparison graphs
    (refer images folder for this images and graph observation)
    along with these in model training and evaluation below graphs are plotted :

4. **Model Training and evaluation**: 
     The four machine learning model random forest ,decision trees ,logistic regression, gradient boosting machine are selected for model training over the inputed processed data:
     random forest accuracy : 95 %
     GBM accuracy : 96 %
     decision trees accuracy : 93 %
     logisitic regression accuracy : 85 %

     The 10 fold cross validation is then performed on GBM model to obtained a final average cross validated accuracy of 95 % with 3% of deviation.

     this Gradient boosting machine model is then loaded into streamlit application after installig and using joblib library.

5. **Inference**: 
      Deployed the model with the help streamlit web application to detect car ownership using input features.


## Libraries Used

1. **Joblib**: For downloading the random forest model
2. **Scikit learn**: For machine learning processing  and operations
3. **Matplotlib**: For plotting and visualizing the detection results.
4. **Pandas**: For image manipulation.
5. **NumPy**: For efficient numerical operations.
6. **Seaborn** : for advanced data visualizations
7. **plotly** : for 3D data visualizations .
8. **Streamlit** : for creating gui of the web application.

## Tesla (Car company) Stock price Prediction

Along wiht these you can see Tesla stock price prediction in carcompnay_tesla_stock_prediction.ipynb file and its dataset scrapped from yahoo fianance in csv file of TLSA_historic_data.csv.

The stock price for next day , next month and next year is predicted using LSTM. A detailed analysis of Data as well as EDA is performed.


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

4. **View Results**: The script will allow you to predict whether the person has the capability to own a car or not.
