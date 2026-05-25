# Crop Yield Prediction using Machine Learning 

A beginner-friendly Jupyter Notebook demonstrating a complete end-to-end Data Science pipeline for predicting agricultural crop yields based on environmental factors.

## Overview
This project uses a public dataset from Kaggle containing historical data on crop yields, rainfall, temperature, and pesticide usage. 

### Pipeline Steps Included:
1. **Data Loading & Cleaning:** Handling missing values and formatting.
2. **Exploratory Data Analysis (EDA):** Visualizing correlation heatmaps and average yields by crop type using `seaborn` and `matplotlib`.
3. **Data Preprocessing:** One-Hot Encoding categorical variables (Area and Item).
4. **Model Training:** Training and comparing two distinct algorithms:
   * **Linear Regression:** Baseline model (R2 Score: ~0.75)
   * **Random Forest Regressor:** Advanced ensemble model (R2 Score: ~0.98)

## How to Run
1. Ensure you have Jupyter and the required libraries installed:
   `pip install jupyter pandas numpy scikit-learn matplotlib seaborn`
2. Launch the notebook environment:
   `jupyter notebook`
3. Open `Crop_Yield_Prediction.ipynb` and run the cells sequentially.