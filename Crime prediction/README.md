# Crime Data Analysis and Crime Category Prediction using Machine Learning

## Project Overview

This project analyzes crime data using Python and Machine Learning techniques to identify crime patterns and predict crime categories. The dataset is preprocessed, analyzed statistically, and used to train multiple classification models. The performance of the models is then compared to determine the most effective algorithm for crime prediction.

---

## Objectives

* Load and preprocess crime data.
* Clean and transform the dataset for analysis.
* Perform statistical and aggregate analysis.
* Generate unique identifiers for crime records.
* Classify areas into priority levels based on crime frequency.
* Build machine learning models to predict crime categories.
* Compare the performance of different classification algorithms.
* Visualize model accuracy using graphs.

---

## Dataset

**Dataset Name:** Crime_Data_from_2020_to_Present.csv

The dataset contains information about reported crime incidents, including:

* Date Reported
* Date Occurred
* Time Occurred
* Area Name
* Crime Code Description
* Victim Age
* Latitude
* Longitude
* Division Record Number (DR_NO)

---

## Technologies Used

* Python 3.x
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Matplotlib
* Seaborn
* Jupyter Notebook

---

## Project Workflow

### 1. Data Loading

* Import the crime dataset using Pandas.
* Display sample records.

### 2. Data Preprocessing

* Convert date columns into datetime format.
* Generate unique internal identifiers.
* Remove missing and invalid victim age values.
* Standardize area names.
* Extract crime categories.

### 3. Statistical Analysis

* Calculate:

  * Mean
  * Median
  * 75th Quantile
  * 90th Percentile
* Generate aggregated crime statistics by area.

### 4. Automated Priority Classification

Areas with crime counts above the 75th percentile are automatically classified as **HIGH Priority**, while the remaining areas are classified as **STANDARD Priority**.

### 5. Feature Engineering

New features are created for machine learning:

* Crime occurrence hour
* Crime occurrence month
* Day of the week
* Area
* Victim Age
* Latitude
* Longitude

### 6. Machine Learning Models

The following classification algorithms are implemented:

* Logistic Regression
* Random Forest Classifier
* XGBoost Classifier

### 7. Model Evaluation

Each model is evaluated using:

* Accuracy Score
* Classification Report
* Precision
* Recall
* F1-Score

Finally, a bar chart compares the accuracy of all models.

---

## Project Structure

```
Crime_Prediction_Project/
│
├── Crime_Data_from_2020_to_Present.csv
├── Crime_Prediction.ipynb
├── README.md
└── requirements.txt
```

---

## Installation

Install the required Python libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost
```

---

## Running the Project

1. Download the dataset.
2. Place the dataset in the project directory.
3. Open the Jupyter Notebook.
4. Execute all notebook cells sequentially.
5. View the statistical analysis, model evaluation, and visualization results.

---

## Results

The project compares three machine learning algorithms for crime prediction.

Example performance:

| Model               | Accuracy                   |
| ------------------- | -------------------------- |
| Logistic Regression | 52.01%                     |
| Random Forest       | 59.45%                     |
| XGBoost             | Generated during execution |

The visualization highlights the best-performing model based on prediction accuracy.

---

## Features

* Data cleaning and preprocessing
* Feature engineering
* Statistical analysis
* Aggregate analysis
* Automated area prioritization
* Machine learning classification
* Performance comparison
* Graphical visualization

---

## Future Improvements

* Hyperparameter tuning for improved accuracy.
* Include additional crime-related features.
* Deploy the model as a web application.
* Add crime hotspot visualization using maps.
* Perform time-series forecasting for crime trends.

---

## Conclusion

This project demonstrates a complete machine learning workflow for crime data analysis and prediction. It includes preprocessing, statistical analysis, feature engineering, model training, evaluation, and visualization. The comparison of multiple algorithms helps identify the most suitable model for predicting crime categories, making the project useful for data analysis, research, and decision support applications.

---

## Author

**Name:** *Your Name*

**Course:** *Your Course Name*

**Project:** Crime Data Analysis and Crime Category Prediction using Machine Learning
