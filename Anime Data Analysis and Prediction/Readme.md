# Anime Data Analysis and Prediction

## Project Goal
To perform exploratory data analysis and build predictive machine learning models for Anime ratings based on features like duration, release year, and genre.

## Dataset Link
[Anime Dataset on Kaggle](https://www.kaggle.com/datasets/ayush4807/aad-dataset)

## Project Structure
```text
Anime Data Analysis and Prediction/
├── config/
│   └── config.yaml             # Pipeline configuration (data paths, hyperparams, filters)
├── Dataset/
│   └── All_Anime.csv           # Raw dataset
├── Model/
│   ├── anime_analysis_and_prediction.ipynb # Original notebook
│   ├── model_1.pkl             # Trained DecisionTreeRegressor artifact
│   └── model_2.pkl             # Trained RandomForestRegressor artifact
├── src/
│   ├── __init__.py
│   ├── utils.py                # Logging and I/O utilities
│   ├── data_ingestion.py       # Data loading, cleaning, and filtering
│   ├── feature_engineering.py  # Encoding, feature selection, and train-test split
│   └── model_training.py       # Model training, evaluation, and pickling
├── tests/
│   ├── __init__.py
│   ├── test_data_ingestion.py  # Unit tests for data ingestion
│   ├── test_feature_engineering.py # Unit tests for feature engineering
│   └── test_model_training.py # Unit tests for model training & evaluation
├── main.py                     # Central CLI execution script
└── Readme.md                   # Project documentation
```

## Modular Pipeline Features
- **Data Ingestion & Cleaning**: Robust loading, missing value imputation, string parsing for durations and years, and filtering rules.
- **Feature Engineering**: Target genre extraction, one-hot encoding categorical variables (`pd.get_dummies`), and reproducible train-test splitting.
- **Model Training & Evaluation**: Trains `LinearRegression`, `DecisionTreeRegressor`, and `RandomForestRegressor`. Evaluates model metrics (Train Score, R2 Score, MAE, MSE, RMSE).
- **Configuration-Driven**: All file paths, filtering criteria, and model output settings managed via `config/config.yaml`.
- **Logging & Utilities**: Replaced plain `print()` statements with structured, production-level logging (`src/utils.py`).

## Installation & Setup

1. **Navigate to project directory**:
   ```bash
   cd "Anime Data Analysis and Prediction"
   ```

## Running the Pipeline via CLI

To execute the end-to-end modular pipeline:

```bash
python main.py
```

You can also specify a custom configuration file path:

```bash
python main.py --config config/config.yaml
```

## Running Unit Tests

Run the test suite using `pytest`:

```bash
python -m pytest tests/
```

## Visuals
<img src="https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Box%20plot%20pr%20year.png"/>
<img src="https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Heatmap.png"/>
<img src="https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Histograms.png"/>
<img src="https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Normal%20Distributions.png"/>
<img src="https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Pairplot.png"/>

## Conclusion & Evaluation Summary
- **Linear Regression & Random Forest**: Exhibit lower training fit and higher error metrics on target genre slices.
- **Decision Tree Regressor**: Captures non-linear relationships effectively, yielding stable predictive metrics for rating forecasting. Trained models are automatically serialized to `Model/model_1.pkl` and `Model/model_2.pkl`.

## Authors
- Originally created by [@Priyankesh](https://github.com/priyankeshh), GSSoC 2024
- Modularized refactor for Issue #1696
