# Heat Stroke Risk Prediction

## Dataset

- **Source:** Heat Stroke Dataset
- **Dataset Link:** https://www.kaggle.com/datasets/tahiatazin1510997643/heat-stroke

This project predicts the risk of heat stroke using patient health indicators, environmental conditions, and lifestyle-related factors. It demonstrates an end-to-end machine learning workflow for binary classification to identify whether an individual is at risk of heat stroke.

## Key Features

1. Data preprocessing and cleaning
2. Exploratory Data Analysis (EDA)
3. Feature selection
4. Visualization of important clinical and environmental variables
5. Model training and comparison
6. Risk prediction for new patient data

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook

## Project Structure

```
Projects/
└── Heat Stroke Risk Prediction/
    ├── heat_stroke_risk_prediction.ipynb
    ├── README.md
    ├── Heat_Stroke_Risk_Prediction_Report.pdf
    └── Heat Stroke (1).csv
```

## Visualizations

The notebook generates several visualizations to understand the dataset and feature relationships, including:

- Heat Stroke Class Distribution
- Patient Temperature vs Heat Stroke
- Rectal Temperature vs Heat Stroke
- Environmental Temperature vs Heat Stroke
- Heat Index vs Heat Stroke
- Relative Humidity vs Heat Stroke
- Age vs Heat Stroke
- Physical Activity vs Heat Stroke
- Daily Water Intake vs Heat Stroke
- Feature Correlation Heatmap

## Models Used

The following machine learning models are implemented and compared:

- Logistic Regression
- Random Forest Classifier

The best-performing model is selected based on classification accuracy and used for prediction.

## Usage

1. Open `heat_stroke_risk_prediction.ipynb` in Jupyter Notebook or VS Code.
2. Install the required Python libraries.
3. Place the dataset (`Heat Stroke (1).csv`) in the project directory.
4. Run all notebook cells sequentially.
5. Review the generated visualizations, evaluation metrics, and prediction results.

## Project Report

A detailed explanation of the project, preprocessing steps, model evaluation, observations, and conclusions is available in:

**`Heat_Stroke_Risk_Prediction_Report.pdf`**

## Conclusion

This project demonstrates an end-to-end machine learning pipeline for predicting heat stroke risk using clinical and environmental data. It includes data preprocessing, exploratory analysis, model training, evaluation, and prediction. The project highlights the importance of body temperature, environmental conditions, humidity, and patient-related factors in identifying heat stroke risk.

## License

MIT