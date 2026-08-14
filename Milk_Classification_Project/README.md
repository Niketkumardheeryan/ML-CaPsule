# Milk Quality Classification Using Machine Learning

## Overview

This project classifies milk into three quality grades — **high, medium, and low** — using machine learning techniques.

The notebook uses milk-quality attributes such as pH, temperature, taste, odor, fat, turbidity, and colour to predict the `Grade` of milk.

## Dataset

The dataset contains **1,059 records and 8 columns**.

### Features

- `pH` — acidity/alkalinity of milk
- `Temprature` — milk temperature
- `Taste` — taste indicator
- `Odor` — odor indicator
- `Fat` — fat indicator
- `Turbidity` — turbidity indicator
- `Colour` — milk colour value
- `Grade` — target variable (`high`, `medium`, `low`)

The notebook loads the dataset from a CSV hosted on GitHub Gist.

## Machine Learning Models

The project compares the following classification algorithms:

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- Support Vector Classifier (SVC)
- XGBoost Classifier
- Gradient Boosting Classifier

## Evaluation

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- ROC curve

Based on the results recorded in the notebook, Random Forest and Gradient Boosting achieved the highest test accuracy (approximately **99.53%**), while Random Forest achieved a weighted multiclass ROC-AUC of **1.00**.

## Project Structure

```text
Milk-Quality-Classification/
├── Milk_classification(1).ipynb
├── README.md
└── requirements.txt
```

## Installation

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

1. Open `Milk_classification(1).ipynb` in Jupyter Notebook, JupyterLab, or Google Colab.
2. Install the dependencies.
3. Run the notebook cells sequentially.
4. The notebook loads the dataset, performs exploratory analysis, trains multiple classifiers, and compares their performance.

## Results

The notebook reports the following test accuracies:

| Model | Accuracy |
|---|---:|
| Logistic Regression | 70.75% |
| Decision Tree | 99.06% |
| Random Forest | 99.53% |
| SVC | 91.51% |
| XGBoost | 99.06% |
| Gradient Boosting | 99.53% |

## Dataset Source

The notebook uses the `milknew.csv` dataset:

https://gist.githubusercontent.com/anu-006/62e09c272b3e7b9b242bb9543fc74c2f/raw/8f88c0c6a152a1e38aaab48779cdf70fdce463bd/milknew.csv

## Note

The reported results are based on the execution recorded in the provided notebook. Very high tree-based model scores should be validated with additional cross-validation or an independent test set before treating them as general real-world performance.
