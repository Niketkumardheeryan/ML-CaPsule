# Heart Disease Prediction using Machine Learning

Welcome to the **Heart Disease Prediction** project! This repository provides an educational, beginner-friendly guide to building a machine learning pipeline that predicts whether a patient has heart disease based on their medical attributes.

---

## 🎯 Goal
Predict whether a patient has heart disease using machine learning classification algorithms on real-world medical data. Early identification is crucial because it allows clinicians to initiate preventative care and treatment strategies, potentially saving lives.

---

## 📊 Dataset

- **Source**: Sourced directly from Hugging Face: [`sanadf234/Heart-Disease-Prediction-dataset`](https://huggingface.co/datasets/sanadf234/Heart-Disease-Prediction-dataset) using the `datasets` library.
- **Samples**: 303 patients
- **Number of Features**: 12 medical attributes (inputs)
- **Target Variable**: `heart_disease` (binary label: `0` = No heart disease, `1` = Heart disease present)

### Feature Descriptions

| Feature Name | Type | Description |
|---|---|---|
| **Age** | Numeric | The age of the patient in years. |
| **Gender** | Categorical | The patient's gender (`Male` or `Female`). |
| **Chest Pain Type** | Categorical | Description of the pain (`Typical Angina`, `Atypical Angina`, `Non-Anginal Pain`, `Asymptomatic`). |
| **Resting BP** | Numeric | Resting blood pressure in mm Hg on admission to the hospital. |
| **Cholesterol** | Numeric | Serum cholesterol level in mg/dl. |
| **Fasting Blood Sugar** | Categorical/Binary | Fasting blood sugar > 120 mg/dl (`1` = true; `0` = false). |
| **Resting ECG** | Categorical | Electrocardiographic results (`Normal`, `Left Ventricular Hypertrophy`, `ST-T Wave Abnormality`). |
| **Max Heart Rate** | Numeric | Maximum heart rate achieved during a stress test. |
| **Exercise Angina** | Categorical/Binary | Exercise-induced angina (`Yes` or `No`). |
| **Old Peak** | Numeric | ST depression induced by exercise relative to rest. |
| **Slope** | Categorical | The slope of the peak exercise ST segment (`Upsloping`, `Flat`, `Downsloping`). |
| **Thal** | Categorical | Thalassemia type (`Normal`, `Fixed Defect`, `Reversible Defect`). |

---

## 🛠️ Project Workflow

This project follows an end-to-end Machine Learning workflow, broken down step-by-step:

### 1. Import Libraries
We import Python libraries for data processing (`pandas`, `numpy`), visualization (`matplotlib`, `seaborn`), downloading dataset (`datasets`), modeling and evaluation (`scikit-learn`), and saving the final models (`joblib`).

### 2. Load Dataset
We download the dataset directly from Hugging Face. This ensures reproducibility since anyone running the code will download the exact same version of the data automatically.

### 3. Data Cleaning
We inspect the dataset for missing/null values and handle any data type discrepancies to prepare it for exploration.

### 4. Exploratory Data Analysis (EDA)
We perform statistical analysis using `describe()` and plot distributions (like countplots for the target class and correlation heatmaps) to understand how the features relate to heart disease.

### 5. Handling Categorical Features
We identify text-based columns that represent groups or labels (like gender or chest pain types) rather than numerical measurements.

### 6. Feature Encoding
Machine learning algorithms only understand numbers. We convert categorical text fields into numeric vectors using **One-Hot Encoding** (creating dummy binary columns of 0s and 1s for each unique category).

### 7. Feature Scaling
Features like cholesterol (values ranging up to 600+) and age (ranging up to 80) have completely different ranges. We apply **Standardization (StandardScaler)** to shift the mean of each feature to $0$ and rescale the standard deviation to $1$. This ensures no feature dominates the learning process.

### 8. Train/Test Split
We split the dataset into **80% Training Data** (used to teach the model) and **20% Test Data** (kept hidden during training and used later to test how well the model generalizes to new patients).

### 9. Model Selection
We use the following algorithms:
- **Logistic Regression** - For interpretability and baseline performance
- **Random Forest Classifier** - For capturing non-linear relationships

### 10. Model Training
We call `model.fit()` to train the model weights using our training set.

### 11. Model Evaluation
We test the model's predictions on the unseen test set, calculating accuracy, precision, recall, F1-score, and plotting the Confusion Matrix and ROC Curve.

### 12. Saving Model
We save the trained model (`logistic_regression_model.pkl`) and the fitted StandardScaler (`scaler.pkl`) to disk so they can be loaded instantly in any future production script or web application.

---

## 📈 Models Used
- **Logistic Regression**
- **Random Forest Classifier**

---

## 📉 Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

## Mathematical Explanation

### What is Logistic Regression?
Unlike linear regression (which predicts continuous values, like house prices), Logistic Regression is a classification algorithm that predicts the **probability** that an input belongs to a specific class (e.g., class `1` for heart disease).

### The Mathematical Formula
We compute a weighted sum of the input features:

$$z = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_n x_n$$

Where:
- $x_1, x_2, \dots, x_n$ are the clinical features (e.g., age, cholesterol).
- $\beta_1, \beta_2, \dots, \beta_n$ are the weights (coefficients) the model learns.
- $\beta_0$ is the intercept (bias).

### The Sigmoid Function
To turn this sum $z$ (which can be any number from negative infinity to positive infinity) into a valid probability between $0$ and $1$, we pass it through the **Sigmoid Function**:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

#### Sigmoid Curve Visual