# PCOD Detection & Explainable AI (XAI) System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/pypi-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-1.5+-green.svg)](https://xgboost.readthedocs.io/)
[![LightGBM](https://img.shields.io/badge/LightGBM-3.3+-green.svg)](https://lightgbm.readthedocs.io/)

A comprehensive machine learning pipeline for the detection of Polycystic Ovary Disease (PCOD) with a strong emphasis on **Explainability** and **Actionable Insights**. This project goes beyond simple classification by providing reasons for a diagnosis and suggesting counterfactual changes to improve health outcomes.

## 🚀 Key Features

*   **Ensemble Modeling**: Utilizes a robust soft-voting classifier combining **Random Forest**, **XGBoost**, and **LightGBM** for high-accuracy predictions.
*   **Explainable AI (XAI)**:
    *   **SHAP (SHapley Additive exPlanations)**: Provides global feature importance and local instance-level contributions.
    *   **LIME (Local Interpretable Model-agnostic Explanations)**: Generates human-readable explanations for individual predictions.
*   **Actionable Counterfactuals (DiCE)**: Leverages Diverse Counterfactual Explanations to answer "What-if" questions (e.g., "What lifestyle changes could potentially reverse the risk?").
*   **Data Preprocessing**: Automated handling of missing values, duplicate removal, feature encoding, and height string cleaning.

## 🛠️ Tech Stack

*   **Core**: Python 3.8+
*   **ML Frameworks**: Scikit-Learn, XGBoost, LightGBM
*   **Interpretability**: SHAP, LIME, DiCE (Diverse Counterfactual Explanations)
*   **Data Handling**: Pandas, NumPy
*   **Visualization**: Matplotlib

## 📦 Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Shashank1725/Fake-news-detector.git
    cd PCOD-Detection
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/scripts/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install pandas numpy scikit-learn xgboost lightgbm shap lime dice-ml matplotlib
    ```

## ⚙️ Configuration

Update the `config.py` file to point to your dataset path and define your target features:

```python
DATA_PATH = "path/to/your/dataset.csv"
TARGET_COL = 'pcod_status'
FEATURE_COLS = ['age', 'bmi', 'cycle_length', ...]  # List your features here
```

## 📂 Project Structure

*   `main.py`: Entry point for training, evaluation, and explanation generation.
*   `models.py`: Contains the logic for training the Voting Ensemble and performance metrics.
*   `preprocessing.py`: Data cleaning, encoding, and scaling pipeline.
*   `explainer.py`: Implementation of SHAP and LIME visualizations.
*   `counterfactuals.py`: Generation of actionable CFs using DiCE.
*   `config.py`: Centralized configuration for paths and hyperparameters.

## 📈 Usage

To run the complete pipeline:

```bash
python main.py
```

### Outputs:
1.  **Model Performance**: Printed to the console (Accuracy, Precision, Recall, F1-Score).
2.  **SHAP Summary**: Saved as `shap_summary.png`.
3.  **LIME Explanation**: Interactive HTML report saved as `lime_explanation.html`.
4.  **Counterfactuals**: Displayed in the console/output logs.

## 🧠 Explainability in Action

### SHAP Summary
The SHAP plot helps identify which biological factors (like BMI or Cycle Length) are the strongest drivers of PCOD risk across the entire population.

### DiCE Counterfactuals
Instead of just saying "High Risk", the system provides suggestions:
- *Current*: BMI: 30, Weight: 85kg -> **Result: Risk**
- *Counterfactual*: If BMI was 24 and Weight was 70kg -> **Result: No Risk**

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
