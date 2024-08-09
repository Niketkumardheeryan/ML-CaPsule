#  Credit Score Classification using Machine learning

This project classifies the credit score of the user as high (good) , low (poor) or medium range (standard) based on various input features like age , occupation , annual income , number of bank accounts and credit cards , type of credits , payment behaviour , previous payment history etc. The project is hosted using a streamlit application. the model is trained on kaggle data consisting of nearly 1 lakh+ rows. Four machine learning models KNN , GBM , XGBOOST and Random Forest were applioed and KNN got the highest 87 % accuracy after stratified k-fold cross validation. also the web application provided info regarding credit score, it stats , significance , graphs and news for new users using NewsAPI Api key.


## Data Set

The below csv dataset from kaggle is used as reference which contains nearly 1lakh+ rows (ccredit_score_classificafion.csv) on which porcessing is performed to obtained a  processed data , all this processing is performed in first notebook (credit_score_notebook.ipynb) file.

The dataset link is are as follows :-
https://www.kaggle.com/datasets/clkmuhammed/creditscoreclassification

on this dataset, below processing are performed :
1) featue scaling and column reinitialization
2) errors and outliers removal using box plot
3) remove na,missing values , regularization etc
4) Drop duplicates , normalization , column dropping

(all this works ar depicted in credit_score_Classification file)

The model is trained on processed data after data processing and feature engineering  and all works associated with it are depicted in credit_score_notebook.ipynb file.

## Methodology

The project follows the below structured methodology ranging from data preprocessing pipeline to feature engineering model training, evaluation and deployment :-

1. **Data Preprocessing and feature enginnering**

2. **Exploratory Data Analysis (EDA)**:
    after Data preprocessing the next step is Exploratory  data analysis using different plotting libraries like matplotlib,pandas,seaborn and plotly.following plots were plotted in this step:-
    1) Pie chart of payment behaviour, previous payment history , type of credits and credit score each
    2) violen plot of occupation vs age using plotly (outliers and outlier removed)
    3) box plot of numerical features
    4) count plot of all occupations as well as age distrbutions
    5) heatmap or confusion matrix for four different models of machine learning
    6) ROc curve
    (refer images folder for this images and graph observation)


4. **Model Training and evaluation**: 
     The four machine learning model random forest ,XgBoost ,K-nearest neighbour, gradient boosting machine are selected for model training over the inputed processed data:
     random forest accuracy : 72 %
     GBM accuracy : 74 %
     XGBOOST accuracy : 79 %
     KNN accuracy : 87 %

     The 5 fold stratified k-fold cross validation is then performed on KNN model to obtained a final average cross validated accuracy of 87 % with 1% of deviation.

     this  K-nearest negihbours (estimated number of neighbours : 5 ) model is then loaded into streamlit application after installing and using joblib library.

5. **Inference**: 
      Deployed the model with the help streamlit web application to classify the credit score based on 15 input  features,


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

3. **Download The model from the given link and keep in the same directory**:
    ```sh
    https://drive.google.com/file/d/1_QSga1Nrb_LcbZ86jHRato9da0Lwb6-e/view?usp=sharing
    ```

4. **Obtain Your  Newsapi API Key by visiting and signing in at below website**
     ```sh
    https://newsapi.org/account
    ```
    (Replace it in app.py line number 288)


3. **Run the Model**: 
    ```python
    streamlit run app.py
    ```

4. **View Results**:  The script will allow you to classofy credit score into three categories as high(good) , medium(standard) and low (poor) based on various inputed factors. It also gives information about credit score, its stats, classsification criteria , graphs and visualizations and recent credits ,loans and finance news from NewsAPI.