# 🛡️ FraudSentinel — Credit Card Anomaly Detection

## Project Overview
FraudSentinel is an end-to-end machine learning project designed to identify fraudulent credit card transactions in real-time. Operating on highly imbalanced financial data (where fraud represents a tiny fraction of total activity), the project leverages a robust pipeline combining **SMOTE** (Synthetic Minority Over-sampling Technique), **RobustScaler**, and **XGBoost** to achieve high Precision-Recall AUC without sacrificing true positive rates.

The repository includes both a deep-dive research notebook (`dric.ipynb`) detailing model training and unsupervised alternatives (like Isolation Forests), and a sleek, cyberpunk-themed **Streamlit web application** (`fraud_detection_app.py`) for real-time single transaction testing and batch CSV analysis.

---

## Dataset
The model is trained on the classic [Kaggle Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud), which contains 284,807 transactions. Among these:
* **Legitimate (Class 0):** 284,315 (99.83%)
* **Fraudulent (Class 1):** 492 (0.17%)

Because the dataset is heavily anonymized using PCA, the primary features are `V1` through `V28`, alongside `Time` (seconds elapsed between transactions) and `Amount` (transaction amount).

---

## EDA
Exploratory Data Analysis was conducted to understand the distribution of the features. Key findings include:
* Most transactions are for very small amounts, but fraudulent transactions often have specific patterns.
* Time doesn't directly indicate fraud, but scaling it helps the model process it better.
* Using `RobustScaler` on `Time` and `Amount` helps minimize the influence of extreme transaction outliers.

---

## SMOTE
Standard classification algorithms fail heavily on this data because they optimize for raw accuracy. A dummy model predicting "Normal" 100% of the time achieves 99.83% accuracy while catching zero fraud. 

To combat this, we applied **SMOTE (Synthetic Minority Over-sampling Technique)** within a stratified cross-validation pipeline. This generates synthetic fraud samples *only* on the training folds (preventing data leakage), balancing the dataset so the model can learn fraudulent patterns effectively.

---

## Isolation Forest
As part of our initial research, unsupervised anomaly detection techniques like **Isolation Forest** were explored to detect outliers without relying on labeled data. While useful for general anomaly detection, supervised methods provided better precision for this specific dataset. Details of this exploration are available in the `dric.ipynb` notebook.

---

## XGBoost
Our primary classification engine is the `XGBoostClassifier`. We trained the model using an optimized decision threshold aimed at maximizing the **PR-AUC (Precision-Recall Area Under the Curve)** rather than the standard ROC-AUC, which can be overly optimistic on highly imbalanced datasets.

---

## Results
The retrained XGBoost model running on the full dataset achieved the following metrics:
* **PR-AUC (Primary Metric):** 0.8340
* **ROC-AUC:** 0.9776
* **Recall on Fraud:** 0.90 (Successfully catching 90% of actual fraud)
* **Precision on Fraud:** 0.12

---

## How to Run

### 1. Setup Environment
Clone the repository and install the required dependencies (Python 3.8+ recommended):
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
Launch the Streamlit app locally:
```bash
streamlit run fraud_detection_app.py
```
*Note: If the trained model file `xgb_fraud_model.pkl` is not present in the directory, the app will automatically fall back to a fully interactive **Demo Mode** using a simulated score engine.*

---

## Future Improvements
* **Advanced Neural Networks:** Exploring Autoencoders for deeper unsupervised anomaly detection.
* **Real-time API:** Packaging the XGBoost model into a FastAPI microservice for integration with real payment gateways.
* **Feature Engineering:** Deriving time-based velocity features if un-anonymized data becomes available.
* **Model Ensembling:** Combining XGBoost with LightGBM and Random Forest to further boost precision.

---

## 📂 Project Structure
```
.
├── fraud_detection_app.py  # Cyberpunk Streamlit UI and inference code
├── dric.ipynb              # EDA, data preprocessing, SMOTE pipeline, and model training
├── xgb_fraud_model.pkl     # Serialized trained XGBoost classifier
├── robust_scaler.pkl       # Serialized scaler for Time/Amount normalization
├── requirements.txt        # Package dependencies
└── README.md               # You are here!
```

---

## ⚖️ License
This project is open-source. Feel free to use and adapt it for research or portfolio work.
