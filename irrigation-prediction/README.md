# Irrigation Need Prediction

## Dataset

- **Source:** Irrigation Need Prediction Dataset
- **Dataset Link:** https://www.kaggle.com/datasets/miadul/irrigation-water-requirement-prediction-dataset
This project predicts the irrigation requirement (**Low, Medium, or High**) using soil properties, weather conditions, crop information, and irrigation-related factors. It demonstrates an end-to-end machine learning workflow for multiclass classification to assist in efficient water management and smart agriculture.

## Key Features

1. Data preprocessing and cleaning
2. Exploratory Data Analysis (EDA)
3. Feature selection
4. Visualization of important soil, weather, and crop-related features
5. Model training and comparison
6. Irrigation need prediction for new agricultural data

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

## Project Structure

```
Projects/
└── Irrigation Need Prediction/
    ├── irrigation_prediction.ipynb
    ├── README.md
    ├── Irrigation_Prediction_Report.pdf
    └── irrigation_prediction.csv
```

## Visualizations

The notebook generates several visualizations to understand the dataset and feature relationships, including:

- Irrigation Need Class Distribution
- Distribution of Numerical Features
- Correlation Heatmap
- Soil Type vs Irrigation Need
- Crop Type vs Irrigation Need
- Crop Growth Stage vs Irrigation Need
- Soil Moisture vs Rainfall (Colored by Irrigation Need)

## Model Used
- Random Forest Classifier

## Usage

1. Open `irrigation_prediction.ipynb` in Jupyter Notebook or VS Code.
2. Install the required Python libraries.
3. Place the dataset (`irrigation_prediction.csv`) in the project directory.
4. Run all notebook cells sequentially.
5. Review the generated visualizations, evaluation metrics, and prediction results.

## Project Report

A detailed explanation of the project, preprocessing steps, model evaluation, observations, and conclusions is available in:

**`Irrigation_Prediction_Report.pdf`**

## Conclusion

This project demonstrates an end-to-end machine learning pipeline for predicting irrigation requirements using soil characteristics, weather conditions, crop information, and irrigation history. It includes data preprocessing, exploratory data analysis, model training, evaluation, and prediction. The project highlights the importance of soil moisture, rainfall, crop growth stage, and environmental conditions in determining the appropriate irrigation level, helping improve water management and agricultural productivity.

## License

MIT