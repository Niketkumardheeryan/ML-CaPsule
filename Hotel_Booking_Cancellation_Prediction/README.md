Hotel Booking Cancellation Prediction

Overview

This project focuses on predicting hotel booking cancellations using machine learning classification algorithms. The objective is to build a model that can identify whether a hotel reservation is likely to be canceled based on booking-related features.

Dataset

The project uses the Hotel Booking Demand Dataset (hotel_bookings.csv).

The dataset contains information about hotel reservations, customer details, and booking characteristics.

Target Variable:

* is_canceled
    * 0: Booking is not canceled
    * 1: Booking is canceled

Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Jupyter Notebook

Project Workflow

1. Data Preprocessing and Cleaning

* Handled missing values
* Removed irrelevant features
* Converted categorical features into numerical format
* Prepared data for model training

2. Exploratory Data Analysis (EDA)

Performed data analysis and visualization to understand:

* Booking patterns
* Cancellation trends
* Feature relationships

3. Feature Engineering

* Transformed categorical variables
* Selected relevant features for model training

4. Train-Test Split

The dataset was divided into training and testing sets for model evaluation.

5. Model Training

The following machine learning classification models were implemented:

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier

6. Model Evaluation

Models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score

Model Performance Comparison

Model	Accuracy	Precision	Recall	F1 Score
Logistic Regression	81.90%	81.19%	66.56%	73.15%
Decision Tree	85.89%	80.87%	81.07%	80.97%
Random Forest	89.39%	89.33%	81.04%	84.98%

Feature Importance Analysis

Feature importance analysis was performed using the Random Forest model to identify the most influential features affecting hotel booking cancellation predictions.

Business Insights and Conclusion

The implemented models help predict booking cancellations, which can assist hotels in understanding cancellation patterns and improving reservation management strategies.

Among all models, Random Forest Classifier achieved the best performance with an accuracy of 89.39% and an F1 Score of 84.98%, making it the most effective model for this classification task.

