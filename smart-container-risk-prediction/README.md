# SmartContainer Risk Engine

An AI/ML-powered shipment risk prediction system designed to identify suspicious or high-risk cargo containers using historical customs and shipment data.

The system combines:
-  Machine Learning Classification
-  Anomaly Detection
-  Explainable AI
-  Risk Analytics
-  Real-Time Shipment Monitoring

---

# Problem Statement

Traditional container inspection systems rely heavily on manual verification and static rules, making it difficult to detect suspicious shipment activities efficiently.

This project aims to build an intelligent risk engine capable of:
- Detecting fraudulent declarations
- Identifying suspicious trade routes
- Flagging risky importers/exporters
- Detecting abnormal shipment behavior
- Supporting customs and logistics security operations

---

# Features

## Advanced Feature Engineering
- Weight difference analysis
- Weight deviation percentage
- Value per KG calculation
- Trade route generation
- Night-time declaration detection
- High dwell-time risk detection

---

## Dynamic Risk Scoring
Risk scores generated using:
- Importer history
- Exporter history
- Shipping line history
- HS Code historical risk
- Port risk analysis
- Trade route risk patterns

---

## Machine Learning Models

###  Random Forest Classifier
Used for:
- Shipment risk prediction
- Risk probability estimation

###  Isolation Forest
Used for:
- Outlier detection
- Unknown anomaly identification

---

## Explainable AI
Generates human-readable risk explanations such as:
- Large weight difference detected
- Shipment stayed unusually long at port
- Importer has previous risky shipment history
- Trade route historically high risk

---

## Real-Time Risk Prediction
Outputs:
- Risk Probability
- Risk Level
- Final Risk Decision
- Risk Explanation

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Programming |
| Pandas | Data Processing |
| NumPy | Numerical Operations |
| Scikit-learn | Machine Learning |
| Random Forest | Classification |
| Isolation Forest | Anomaly Detection |

---

# Workflow

## 1️ Load Data
- Historical shipment data
- Real-time shipment data

---

## 2️ Feature Engineering
Creates intelligent features like:
- Weight_Diff
- Weight_Diff_Percent
- Value_per_KG
- Trade_Route
- Night_Declaration
- High_Dwell_Risk

---

## 3️ Safe Categorical Encoding
Encodes categorical variables using mappings built only from historical data to prevent data leakage.

---

## 4️ Aggregated Risk Features
Builds:
- Shipment frequency metrics
- Importer/exporter behavioral patterns
- Historical risk scores

---

## 5️ Model Validation
Evaluation metrics used:
- Macro F1 Score
- Weighted F1 Score
- Recall Score
- Confusion Matrix
- Classification Report

---

## 6️ Production Training
Final models trained using the complete historical dataset.

---

## 7️ Real-Time Prediction
Predicts:
- Risk Probability
- Risk Level
- Final Risk Status

---

## 8️ Explainable Risk Engine
Provides reasons behind risk predictions.

---
**Contributed by:** [Aarju Patel]
