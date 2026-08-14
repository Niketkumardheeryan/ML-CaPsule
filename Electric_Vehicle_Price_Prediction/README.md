# EV Price Prediction

A machine learning project for predicting the price of electric vehicles using vehicle specifications and categorical attributes.

## Project Overview

This project uses an electric vehicle dataset containing **103 vehicles and 14 columns**. The target variable is `PriceEuro`, representing the vehicle price in Euros.

The notebook performs:

- Data loading and exploration
- Data quality checks
- Missing-value analysis
- Duplicate-value checking
- Descriptive statistics
- Correlation analysis
- Exploratory data visualization
- Numerical and categorical feature preprocessing
- Train/test splitting
- Comparison of multiple regression algorithms
- Random Forest hyperparameter tuning using GridSearchCV
- Final model evaluation using R², MAE, and MSE

## Dataset

The dataset is loaded directly from the following CSV source:

```text
https://gist.githubusercontent.com/anu-006/2db8313ad268e9e6de0fe6eed77d7af7/raw/89974b18d63ce8faf1be5db7cc767acf53957388/electric_dataset.csv
```


### Columns

| Column | Description |
|---|---|
| `Brand` | EV manufacturer/brand |
| `Model` | Vehicle model |
| `AccelSec` | Acceleration time |
| `TopSpeed_KmH` | Maximum speed in km/h |
| `Range_Km` | Driving range in km |
| `Efficiency_WhKm` | Energy efficiency in Wh/km |
| `FastCharge_KmH` | Fast charging rate |
| `RapidCharge` | Whether rapid charging is supported |
| `PowerTrain` | Powertrain type |
| `PlugType` | Charging plug type |
| `BodyStyle` | Vehicle body style |
| `Segment` | Vehicle segment |
| `Seats` | Number of seats |
| `PriceEuro` | Vehicle price in Euros; prediction target |

## Exploratory Data Analysis

The notebook checks:

- Dataset shape and data types
- Percentage of missing values
- Duplicate records
- Descriptive statistics
- Correlation between numerical variables
- Distribution of numerical features
- Relationship between numerical features and vehicle price
- Counts of selected categorical features
- Top 10 vehicle models

The dataset contains no missing values in the initial inspection and no duplicate rows.

The notebook also converts `FastCharge_KmH` to numeric values using `pd.to_numeric(..., errors='coerce')`.

## Important Correlations

The notebook's correlation analysis shows:

- `TopSpeed_KmH` and `PriceEuro`: approximately **0.83**
- `Range_Km` and `PriceEuro`: approximately **0.67**
- `AccelSec` and `PriceEuro`: approximately **-0.63**
- `Efficiency_WhKm` and `PriceEuro`: approximately **0.40**
- `Seats` and `PriceEuro`: approximately **0.02**

These values describe relationships in this dataset and should not be interpreted as causal relationships.


Numerical preprocessing uses:

1. `SimpleImputer(strategy='mean')`
2. `StandardScaler()`


Categorical preprocessing uses `OneHotEncoder(handle_unknown='ignore')`.

A `ColumnTransformer` combines the numerical and categorical preprocessing pipelines.

## Models Compared

The notebook compares the following regression algorithms:

1. XGBoost Regressor
2. Decision Tree Regressor
3. Gradient Boosting Regressor
4. Support Vector Regressor
5. Linear Regression
6. Random Forest Regressor

The models are evaluated using:

- R² (R-squared)
- Mean Squared Error (MSE)

## Hyperparameter Tuning

Random Forest is further optimized using `GridSearchCV`.

The search includes:

- `n_estimators`: 50, 100, 150
- `max_depth`: None, 10, 20
- `min_samples_split`: 2, 5
- `min_samples_leaf`: 1, 2
- Cross-validation: 3 folds
- Scoring metric: R²
- Parallel processing: `n_jobs=-1`

The tuned model is evaluated on the test set using:

- R²
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)

## Project Structure

```text
EV-Price-Prediction/
│
├── EV_Price_prediction.ipynb
├── README.md
└── requirements.txt
```

## Installation

Clone or download the project and install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

### Jupyter Notebook

```bash
jupyter notebook EV_Price_prediction.ipynb
```

### Google Colab

The notebook is compatible with Google Colab. Upload `EV_Price_prediction.ipynb` and run the cells sequentially.

The dataset is loaded from its online CSV URL, so a working internet connection is required when executing the data-loading cell.

## Results

The notebook prints the R² and MSE for each baseline regression model. It then prints the best Random Forest hyperparameters found by GridSearchCV and evaluates the tuned model using R², MAE, and MSE.

The README intentionally does not hard-code final model scores because those values are generated when the notebook is executed and may vary with the installed library versions.

