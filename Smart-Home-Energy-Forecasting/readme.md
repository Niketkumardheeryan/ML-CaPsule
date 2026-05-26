# AI-Based Smart Home Energy Consumption Forecasting & Waste Pattern Analysis

A complete end-to-end Machine Learning project for predicting energy consumption and detecting wasteful usage patterns in smart homes.

## Project Structure

```
energy/
├── dataset/
│   └── energydata_complete.csv       # 100K-row dataset
├── notebooks/
│   └── python.py                     # Full ML pipeline (EDA → Models → Forecast)
│   └── plots/                        # Auto-generated EDA & analysis plots
├── models/                           # Saved models, scaler, forecast CSV
├── flask_app/
│   ├── app.py                        # Flask web application
│   ├── static/style.css              # Styling
│   └── templates/
│       ├── index.html                # Input form
│       └── result.html               # Prediction results
└── readme.md
```

## Setup

```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels flask joblib xgboost
```

## Usage

### 1. Run the ML Pipeline
```bash
cd notebooks
python python.py
```
This will:
- Perform full EDA and save 17+ plots to `notebooks/plots/`
- Train 5 models before and after feature engineering
- Run KMeans clustering for waste detection
- Run ARIMA forecasting for 30 days
- Save the best model to `models/`

### 2. Launch the Flask Web App
```bash
cd flask_app
python app.py
```
Open `http://127.0.0.1:5000` → fill the form → get prediction + forecast chart.

## Models Used
| Model | Type |
|-------|------|
| Linear Regression | Baseline |
| Decision Tree | Tree-based |
| Random Forest | Ensemble |
| KNN | Instance-based |
| XGBoost | Gradient Boosting |

## Key Features
- **13-section pipeline** covering the full ML lifecycle
- **Before vs After** feature engineering comparison
- **PCA** with explained variance analysis
- **KMeans clustering** for waste detection (Efficient / Moderate / Wasteful)
- **ARIMA** time-series forecasting (30-day)
- **Flask web app** with prediction + forecast visualization
