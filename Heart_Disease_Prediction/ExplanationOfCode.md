# Heart Disease Prediction — Project Explanation

## What This Project Does

This project builds a machine learning model that predicts whether a patient has heart disease based on medical data. It uses **Logistic Regression**, a classic and interpretable classification algorithm, trained on a dataset sourced from Hugging Face.

---

## The Dataset

**Source:** `sanadf234/Heart-Disease-Prediction-dataset` on Hugging Face

The dataset contains 12 medical attributes per patient:

| Feature | Description |
|---|---|
| Age | Patient's age |
| Gender | Male / Female |
| Chest Pain Type | Type of chest pain experienced |
| Resting Blood Pressure | BP at rest |
| Cholesterol | Serum cholesterol level |
| Fasting Blood Sugar | Whether blood sugar > 120 mg/dl |
| Resting ECG | Electrocardiographic results |
| Max Heart Rate | Maximum heart rate achieved |
| Exercise Angina | Chest pain induced by exercise |
| Old Peak | ST depression from exercise |
| Slope | Slope of the peak exercise ST segment |
| Thalassemia | Blood disorder type |

**Target:** `heart_disease` — `0` (No disease) or `1` (Disease present)

---

## Step-by-Step Workflow

### 1. Loading Data
The dataset is loaded directly from Hugging Face using the `datasets` library. This avoids manual CSV downloads and ensures reproducibility.

### 2. Exploratory Data Analysis (EDA)
Before modeling, the data is inspected using `df.info()`, `df.describe()`, and `df.isnull().sum()` to understand:
- Data types of each column
- Any missing values
- Statistical distribution of features
- Whether the target classes are balanced

### 3. Target Distribution
A count plot (`sns.countplot`) visualizes how many patients do or do not have heart disease. This reveals potential class imbalance that could affect model reliability.

### 4. Correlation Heatmap
A heatmap (`sns.heatmap`) displays pairwise correlations between numerical features. Correlation ranges from **−1 to +1**:
- **+1** → Strong positive relationship
- **−1** → Strong negative relationship
- **0** → No relationship

This helps identify which features are most predictive of heart disease.

### 5. Feature and Target Separation
The input features `X` and target `y` are separated:
```python
X = df.drop("heart_disease", axis=1)
y = df["heart_disease"]
```

### 6. Encoding Categorical Features
Machine learning models require numerical input. Text columns (e.g., Male/Female, Yes/No, chest pain categories) are converted using **One-Hot Encoding** via `pd.get_dummies()`. This creates binary (0/1) columns for each category.

**Example:**

| Gender | Male |
|---|---|
| Male | 1 |
| Female | 0 |

### 7. Train-Test Split
The data is split **80% training / 20% testing** using `train_test_split()`. The model learns from the training set and is evaluated on the unseen test set, simulating real-world performance.

### 8. Feature Scaling
Features have very different numerical ranges (e.g., Age: 20–80, Cholesterol: hundreds). Without scaling, larger-valued features can unfairly dominate the model. **StandardScaler** normalizes all features using:

```
z = (x − μ) / σ
```

Where:
- `x` = original value
- `μ` = mean of the feature
- `σ` = standard deviation

After scaling, every feature has **mean = 0** and **standard deviation = 1**.

---

## The Algorithm — Logistic Regression

### How It Works
Logistic Regression predicts the **probability** that a patient has heart disease using the **sigmoid function**:

```
σ(z) = 1 / (1 + e^(−z))
```

Where `z` is the weighted sum of all input features. The output always lies between 0 and 1.

### Decision Rule
- Predicted probability **> 0.5** → Heart disease present (class 1)
- Predicted probability **≤ 0.5** → No heart disease (class 0)

### Training
During `model.fit()`, the algorithm adjusts its weights to minimize prediction error and find the optimal decision boundary separating the two classes.

---

## Model Evaluation

### Accuracy: ~91%
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```
91% of predictions were correct overall.

### Confusion Matrix

|  | Predicted: No Disease | Predicted: Disease |
|---|---|---|
| **Actual: No Disease** | 1737 ✅ | 582 ❌ |
| **Actual: Disease** | 380 ❌ | 8281 ✅ |

- **1737** healthy patients correctly identified
- **8281** diseased patients correctly identified
- **582** false alarms (healthy predicted as diseased)
- **380** missed cases (diseased predicted as healthy) — the most critical error in healthcare

### Precision, Recall, and F1-Score

| Metric | Formula | Meaning |
|---|---|---|
| **Precision** | TP / (TP + FP) | Of predicted positives, how many are truly positive? |
| **Recall** | TP / (TP + FN) | Of actual positives, how many did the model catch? |
| **F1-Score** | 2 × (Precision × Recall) / (Precision + Recall) | Harmonic mean balancing both |

In medical applications, **Recall** is especially important — missing a disease case (false negative) is more dangerous than a false alarm.

### ROC-AUC Score: 0.85
The **ROC Curve** plots the True Positive Rate vs. False Positive Rate across all decision thresholds. An **AUC of 0.85** indicates strong ability to distinguish between healthy and diseased patients (1.0 = perfect, 0.5 = random guessing).

---

## Model Saving

The trained model and scaler are saved using `joblib.dump()`. This allows the model to be:
- Reloaded without retraining
- Deployed in a web or clinical application
- Integrated into a healthcare analytics pipeline

---

## Final Results Summary

| Metric | Value |
|---|---|
| Model | Logistic Regression |
| Dataset | Hugging Face (`sanadf234/Heart-Disease-Prediction-dataset`) |
| Accuracy | ~91% |
| ROC-AUC Score | 0.85 |

---

## Key Takeaways

- A complete ML pipeline was built end-to-end: data loading → preprocessing → training → evaluation → saving.
- Logistic Regression proved effective for this binary classification task, achieving strong accuracy and a good AUC score.
- Proper preprocessing (encoding, scaling) was critical for model performance.
- The model can serve as a foundation for a medical decision-support tool for early heart disease detection.