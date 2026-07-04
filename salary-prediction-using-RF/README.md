# Salary Prediction Using Random Forest

## Dataset

- Source: Employee salary dataset containing information such as education level, years of experience, job role, industry, and expected CTC.
- The notebook automatically downloads the dataset as `expected_ctc.csv` using `gdown`.
- Link: https://drive.google.com/file/d/18zfwFUrcPmQVUxpJdIodGxlncMgOPacE/view?usp=sharing

This project predicts employee salaries using a **Random Forest Regression** model by leveraging employee demographic, educational, and professional attributes. The workflow includes data preprocessing, exploratory data analysis, feature engineering, model training, evaluation, and salary prediction for new employee profiles.

## Key Features
1. Automated dataset download using `gdown`
2. Data cleaning and preprocessing
3. Handling missing values and categorical variables
4. Exploratory Data Analysis (EDA) with visualizations
5. Feature engineering and transformation
6. Salary prediction using Random Forest Regression
7. Model evaluation using regression metrics
8. Prediction for new employee inputs

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Random Forest Regressor
- gdown (dataset download)

## Usage
1. Open `salary_prediction_rf_fixed.ipynb` in Jupyter Notebook or Google Colab.
2. Run all notebook cells.
3. The dataset (`expected_ctc.csv`) will be downloaded automatically using `gdown`.
4. Train the Random Forest model and evaluate its performance.
5. Use the trained model to generate salary predictions for new employee data.

## Model Evaluation
The model performance is measured using:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

These metrics provide insights into prediction accuracy, error magnitude, and the model's ability to explain variance in salary values.