# Heart Disease Prediction using Logistic Regression

Welcome to the **Heart Disease Prediction** project! This repository provides an educational, beginner-friendly guide to building a machine learning pipeline that predicts whether a patient has heart disease based on their medical attributes.

---

## Introduction

### What is Heart Disease Prediction?
Heart disease prediction involves using clinical data (such as blood pressure, age, cholesterol level, and heart rate) to determine whether a patient has a cardiovascular condition. Early identification is crucial because it allows clinicians to initiate preventative care and treatment strategies, potentially saving lives.

### Why Machine Learning is Useful
In clinical practice, predicting heart disease manually requires integrating multiple complex variables. Machine learning (ML) models excel at analyzing high-dimensional datasets and identifying subtle interactions between risk factors (like cholesterol and age) that might go unnoticed by human experts. By automating this pattern recognition, ML acts as a powerful decision-support tool for healthcare professionals.

### Why Logistic Regression is Suitable
We use **Logistic Regression** for this task because:
1. **Interpretability**: Healthcare professionals need to know *why* a model made a prediction. Logistic regression provides coefficients (weights) that clearly show how much each risk factor contributes to the risk of heart disease.
2. **Efficiency**: It is simple to train, requires low computational resources, and is highly effective for binary classification tasks (where the outcome is either $0$ or $1$, i.e., "No Disease" or "Disease").
3. **Probability Estimation**: Rather than just outputting a hard label, it outputs a probability score (e.g., "75% chance of heart disease"), allowing doctors to gauge the confidence of the prediction.

---

## Dataset

- **Source**: Sourced directly from Hugging Face: [`sanadf234/Heart-Disease-Prediction-dataset`](https://huggingface.co/datasets/sanadf234/Heart-Disease-Prediction-dataset) using the `datasets` library.
- **Number of Features**: 12 medical attributes (inputs).
- **Target Variable**: `heart_disease` (binary label: `0` = No heart disease, `1` = Heart disease present).

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

## Project Workflow

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

### 9. Logistic Regression
We initialize a Logistic Regression classifier, which will search for the optimal decision boundary between the two classes.

### 10. Model Training
We call `model.fit()` to train the Logistic Regression weights using our training set.

### 11. Model Evaluation
We test the model's predictions on the unseen test set, calculating accuracy, precision, recall, F1-score, and plotting the Confusion Matrix and ROC Curve.

### 12. Saving Model
We save the trained Logistic Regression model (`logistic_regression_model.pkl`) and the fitted StandardScaler (`scaler.pkl`) to disk so they can be loaded instantly in any future production script or web application.

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
```
    Probability (y)
      1.0 |          .-------
          |         /
      0.5 |    ----/----
          |       /
      0.0 |______/____________ Input (z)
                 0
```

- When $z$ is highly positive, $e^{-z}$ approaches $0$, so $\sigma(z)$ approaches $1$.
- When $z$ is highly negative, $e^{-z}$ is huge, so $\sigma(z)$ approaches $0$.
- When $z = 0$, $\sigma(0) = 0.5$.

### Decision Boundary
To make a final decision, we set a threshold (usually $0.5$):

- If $\sigma(z) \ge 0.5$, we predict class **`1`** (Heart Disease).
- If $\sigma(z) < 0.5$, we predict class **`0`** (No Heart Disease).

The line or boundary where $\sigma(z) = 0.5$ (or $z = 0$) is called the **Decision Boundary**.

---

## Model Evaluation Metrics

Understanding these metrics is vital for evaluating models in healthcare contexts:

```
                      PREDICTED CLASS
                    No Disease  Disease
                  .-----------.-----------.
      No Disease  |    TN     |    FP     |  (False Alarm)
                  |-----------|-----------|
ACTUAL   Disease  |    FN     |    TP     |  (Missed Case)
                  '-----------'-----------'
```

### 1. Accuracy
- **Definition**: The proportion of total predictions that were correct.
- **Formula**: $\frac{TP + TN}{TP + TN + FP + FN}$
- **Healthcare Interpretation**: Out of all patients, what percentage did we diagnose correctly? While useful, accuracy can be misleading if the dataset has many more healthy patients than sick ones.

### 2. Precision
- **Definition**: The proportion of predicted positive cases that were actually positive.
- **Formula**: $\frac{TP}{TP + FP}$
- **Healthcare Interpretation**: If the model predicts a patient has heart disease, how likely is it that they *really* have it? High precision prevents unnecessary patient anxiety and medical tests.

### 3. Recall (Sensitivity)
- **Definition**: The proportion of actual positive cases that were correctly caught by the model.
- **Formula**: $\frac{TP}{TP + FN}$
- **Healthcare Interpretation**: Out of all patients who *actually* have heart disease, what percentage did the model detect? **Recall is the most critical metric in healthcare**—missing a sick patient (False Negative) is much more dangerous than raising a false alarm (False Positive).

### 4. F1 Score
- **Definition**: The harmonic mean of Precision and Recall.
- **Formula**: $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$
- **Healthcare Interpretation**: A balanced score that is high only if *both* precision and recall are high.

### 5. Confusion Matrix
- **Definition**: A table showing the breakdown of correct and incorrect predictions across both classes.
- **Healthcare Interpretation**: Visualizes the exact number of True Negatives (TN), False Positives (FP), False Negatives (FN), and True Positives (TP).

### 6. ROC Curve & ROC-AUC
- **Definition**: The **Receiver Operating Characteristic (ROC)** curve plots the True Positive Rate (Recall) against the False Positive Rate at different classification thresholds. The **Area Under the Curve (AUC)** measures overall performance.
- **Healthcare Interpretation**:
  - $\text{AUC} = 0.5$ means the model performs no better than a random coin flip.
  - $\text{AUC} = 1.0$ is a perfect model.
  - $\text{AUC} \ge 0.8$ indicates a strong ability to distinguish between sick and healthy patients.

---

## Results

After training the Logistic Regression model on the heart disease dataset, the evaluation yields the following performance metrics:

- **Accuracy**: **~91%** (91% of predictions on the test set were correct).
- **ROC-AUC**: **0.85** (strong diagnostic capability).
- **Confusion Matrix Interpretation**:
  - High True Positive (TP) count indicates the model is highly effective at diagnosing patients who have heart disease.
  - The low False Negative (FN) count demonstrates strong recall, indicating very few missed cases.

---

## How to Run

### Step 1: Clone the Repository
Open your terminal and clone the repository:
```bash
git clone https://github.com/Randomlyclueless/ML-CaPsule.git
cd ML-CaPsule/Heart_Disease_Prediction
```

### Step 2: Install Requirements
Install all dependencies listed in the requirements file:
```bash
pip install -r requirements.txt
```
*(Ensure you have Jupyter notebook or JupyterLab installed: `pip install jupyter`)*

### Step 3: Run the Notebook
Launch Jupyter:
```bash
jupyter notebook
```
Open **`heart_disease_prediction.ipynb`** and run the cells from top to bottom.

### Expected Outputs
- Correlation heatmap and distribution visualizations.
- Classification reports containing accuracy, precision, and recall scores.
- Generated model and scaler binary files inside the `models/` directory.

---

## Folder Structure

The final files are structured as follows:

```
Heart_Disease_Prediction/
│
├── README.md                          # Comprehensive beginner-friendly documentation
├── heart_disease_prediction.ipynb     # Jupyter Notebook containing the code and pipeline
├── requirements.txt                   # List of project dependencies
└── models/                            # Directory containing saved artifacts
    ├── logistic_regression_model.pkl  # Trained Scikit-Learn Logistic Regression model
    └── scaler.pkl                     # Saved StandardScaler instance
```

---

## Future Improvements

To build upon this project, future enhancements could include:
1. **Hyperparameter Tuning**: Use grid search or random search to tune regularized weights ($C$ parameter) in Logistic Regression.
2. **Cross Validation**: Implement $K$-fold cross-validation to ensure the model performance is consistent across different data partitions.
3. **Model Comparisons**:
   - Compare performance with a **Random Forest Classifier** (handles non-linear relationships).
   - Compare with **XGBoost** (extreme gradient boosting) to see if accuracy can be pushed higher.
4. **Web App Deployment**: Wrap the saved models in a **Streamlit** user interface, enabling users to enter their medical stats in a web form and receive real-time prediction probabilities.
