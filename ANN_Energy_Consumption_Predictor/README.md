# ⚡ Artificial Neural Network (ANN) Energy Consumption Predictor

A machine learning solution for predicting household appliance energy consumption using environmental sensor data (temperatures, relative humidity, atmospheric pressure, windspeed, visibility) and temporal features.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Project Architecture](#project-architecture)
- [Dataset](#dataset)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
  - [Model Training](#1-model-training)
  - [Model Inference / Prediction](#2-model-inference--prediction)
  - [Jupyter Notebook](#3-jupyter-notebook)
- [Model Evaluation & Results](#model-evaluation--results)

---

## 🌟 Overview
Household energy forecasting plays a critical role in smart grid management and energy efficiency. This project utilizes a deep Artificial Neural Network (ANN) regression model built with **TensorFlow / Keras** to accurately forecast energy consumption (`Appliances` in Watt-hours).

---

## 📁 Project Architecture
```text
ANN_Energy_Consumption_Predictor/
├── dataset/
│   └── energy.csv               # Appliances Energy Prediction Dataset (19,735 rows)
├── results/                     # Output directory for artifacts & plots
│   ├── energy_model.keras       # Saved Keras ANN model
│   ├── scaler.pkl               # Fitted StandardScaler & feature names
│   ├── metrics.json             # Model evaluation performance metrics
│   └── evaluation_plots.pdf     # Consolidated PDF containing all evaluation plots
├── energy_predictor.ipynb       # Exploratory analysis and training notebook
├── train.py                     # Command-Line training and inference pipeline
└── requirements.txt             # Project dependencies
```

---

## 📊 Dataset
The **Appliances Energy Prediction Dataset** includes 4.5 months of 10-minute interval data recorded in a low-energy house:
- **Target Variable**: `Appliances` (Energy use in Wh)
- **Indoor Environment**: `T1`–`T9` (Temperatures in °C) & `RH_1`–`RH_9` (Relative Humidity in %)
- **Outdoor Weather**: `T_out`, `RH_out`, `Press_mm_hg`, `Windspeed`, `Visibility`, `Tdewpoint`
- **Random Variables**: `rv1`, `rv2`

---

## ✨ Key Features
- **Temporal & Cyclical Feature Engineering**: Extracts `hour`, `day`, `month`, `dayofweek`, along with sine and cosine hour encodings (`sin_hour`, `cos_hour`).
- **Environmental Interactions**: Computes average indoor temperature/humidity and living room interaction terms (`T1 * RH_1`).
- **Deep ANN Architecture**: Multi-layer Dense network with BatchNormalization, Dropout, and Adam optimizer.
- **Adaptive Training**: Includes `EarlyStopping` and `ReduceLROnPlateau` callbacks to prevent overfitting.
- **Artifact Persistence**: Automatically saves model weights (`.keras`) and scaler (`.pkl`) for CLI inference.

---

## 💻 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd ANN_Energy_Consumption_Predictor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

### 1. Model Training
Run `train.py` to train the ANN model on the full dataset, evaluate performance, and export all model artifacts and visualization plots:

```bash
python train.py --epochs 50 --batch_size 64
```

Custom options:
- `--dataset`: Path to input CSV (default: `dataset/energy.csv`).
- `--results_dir`: Directory to save model outputs (default: `results`).
- `--epochs`: Max training epochs (default: `50`).
- `--batch_size`: Mini-batch size (default: `64`).

---

### 2. Model Inference / Prediction
To run predictions on new data or synthetic sample inputs using the saved model:

**Run with default sample input**:
```bash
python train.py --predict
```

**Run with a custom CSV dataset**:
```bash
python train.py --predict --input_csv path/to/your_data.csv
```

---

### 3. Jupyter Notebook
You can also run the exploratory notebook interactively:
```bash
jupyter notebook energy_predictor.ipynb
```

---

## 📈 Model Evaluation & Results

The trained ANN model is evaluated using four standard regression metrics:
- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score** (Coefficient of Determination)
- **MAPE** (Mean Absolute Percentage Error)

Generated evaluation plots are compiled into a single consolidated PDF located at [results/evaluation_plots.pdf](file:///c:/Users/tanis/OneDrive/Desktop/internship%202/ML-CaPsule/ANN_Energy_Consumption_Predictor/results/evaluation_plots.pdf):

### Plot Explanations:

1. **ANN Training & Validation Loss Curve**:
   - **Purpose**: Displays the training and validation Mean Squared Error (MSE) loss across all epochs.
   - **Interpretation**: A steadily declining curve where both training and validation losses converge and stabilize indicates that the model is learning effectively. The narrow gap between train and validation losses proves that Batch Normalization and Dropout layers successfully prevented overfitting. The `EarlyStopping` callback automatically terminates training once validation loss stabilizes, ensuring optimal generalization.

2. **Actual vs. Predicted Energy Consumption Scatter Plot**:
   - **Purpose**: Correlates actual household appliance energy usage (Wh) against values predicted by the model on the test dataset.
   - **Interpretation**: The closer the data points cluster along the diagonal `y = x` dashed line (Ideal Fit), the higher the accuracy of the model. Strong density along this diagonal shows high correlation, while scattered outliers represent transient, high-energy events that are naturally more volatile to predict.

3. **Time Series Comparison Plot (Jupyter Notebook Only)**:
   - **Purpose**: Overlay comparison of actual and predicted energy values across the first 100 sequential test samples.
   - **Interpretation**: Shows how closely the model's predictions follow actual peak and baseline energy usage over time, verifying the model's transient tracking capabilities.