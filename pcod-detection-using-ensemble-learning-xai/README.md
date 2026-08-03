# PCOD Detection Using Ensemble Learning, Explainable AI (XAI) & Counterfactual Learning

## Problem Statement

Polycystic Ovarian Disease (PCOD) is a common hormonal disorder affecting many women worldwide. Early detection is important for timely treatment and better healthcare support. Traditional prediction systems often focus only on accuracy and behave like black-box models, making it difficult to understand why a prediction was made.

In healthcare applications, interpretability and transparency are equally important along with prediction performance.

---

## Proposed Solution

This project develops an intelligent PCOD prediction system using:

* Ensemble Learning
* Deep Learning
* Explainable AI (XAI)
* Counterfactual Learning

The system predicts whether a patient is likely to have PCOD based on medical and clinical features while also explaining the reasoning behind the prediction.

---

## Models Used

### Deep Neural Network (DNN)

A Deep Neural Network built using TensorFlow/Keras is used to learn complex patterns and nonlinear relationships present in medical data.

### XGBoost

XGBoost is a gradient boosting algorithm that improves prediction performance by combining multiple weak decision trees into a strong predictive model.

### LightGBM

LightGBM is an optimized boosting algorithm that provides faster training and efficient handling of structured datasets.

### Ensemble Learning

Predictions from:

* DNN
* XGBoost
* LightGBM

are combined using weighted averaging to improve overall accuracy, robustness, and model stability.

---

## Explainable AI (SHAP)

SHAP (SHapley Additive Explanations) is used to explain model predictions by calculating the contribution of each feature toward the final output.

SHAP helps answer questions like:

* Which features influenced the prediction the most?
* Why was a patient predicted as PCOD positive or negative?

In this project, SHAP improves:

* Model transparency
* Interpretability
* Trustworthiness of AI predictions in healthcare

---

## Counterfactual Learning

Counterfactual explanations are generated using DiCE (Diverse Counterfactual Explanations).

Counterfactual learning helps identify:

> What minimal changes in input features could change the prediction outcome.

For example:

* Changes in hormone levels
* Weight-related factors
* Lifestyle-related medical attributes

This makes the AI system more actionable and understandable for real-world healthcare analysis.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* TensorFlow/Keras
* XGBoost
* LightGBM
* SHAP
* DiCE-ML

---

## Files

```bash id="u9d2vr"
PCOD_Detection_Using_Ensemble_Learning_XAI/
│
├── PCOS_data_without_infertility.xlsx
├── notebook.ipynb
└── README.md
```
