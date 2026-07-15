# GDP Prediction Model

Dataset: [Kaggle GDP Prediction Dataset](https://www.kaggle.com/rutikbhoyar/gdp-prediction-dataset?utm_source=chatgpt.com)

This project predicts a country's GDP per capita using Machine Learning techniques and socio-economic indicators from the dataset.

The following regression models were implemented and evaluated:

* Linear Regression
* Support Vector Machine (SVM)
* Random Forest Regressor
* Gradient Boosting Regressor

Among all models tested, the best prediction performance was achieved in the following order:

**Random Forest > Gradient Boosting > Linear Regression > SVM**

## Best Model Performance

The best results were achieved using the **Random Forest Regressor** with all features included in the dataset.

### Evaluation Metrics

| Metric   | Score   |
| -------- | ------- |
| MAE      | 2125.24 |
| RMSE     | 3051.71 |
| R² Score | 0.8873  |

## Features

* Data preprocessing and cleaning
* Missing value handling
* Exploratory Data Analysis (EDA)
* Feature correlation analysis
* Multiple regression model comparisons
* Hyperparameter tuning using GridSearchCV
* Model performance visualization

## Installation

```bash
pip install -r requirements.txt
```

## Running the Project

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/Niketkumardheeryan/ML-CaPsule/refs/heads/master/GDP%20Prediction/world.csv"
)
```

## Technologies Used

* Python
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Scikit-learn
