# Bitcoin Price Prediction Web App

A Streamlit web application that predicts Bitcoin market capitalisation using **Lasso Regression**, trained on historical price data.

![App Screenshot](https://user-images.githubusercontent.com/78292851/156793113-3f6d9e91-665e-47b1-a1f6-316aaeeb2aa7.png)

## Goal

Predict the market capitalisation of Bitcoin using Lasso Regression and perform exploratory data analysis (EDA) on historical price data.

## Description

This is a regression problem where we predict Bitcoin's market cap based on features such as High, Low, Open, Close, and Volume. The model is trained using **Lasso Regression** and achieves approximately **99% accuracy**.

## How to Run

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/premdeshmane-01/ML-caPsule.git
cd "ML-caPsule/Bitcoin Price Prediction Web App"
```

### 2. Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## What Was Done

1. Performed exploratory data analysis (EDA) on the dataset
2. Loaded the dataset and viewed the top 5 rows
3. Calculated statistical data in the dataset
4. Found correlation between the features and statistical values
5. Data visualization using Matplotlib and Seaborn
6. Tested different algorithms to find the best fit
7. Calculated accuracy score of each algorithm for comparison

## Models Used

| Model | Accuracy |
|---|---|
| Lasso Regression | ~99% |

## Libraries Needed

| Library | Purpose |
|---|---|
| `streamlit` | Web app framework for the UI |
| `scikit-learn` | Lasso Regression model and utilities |
| `numpy` | Numerical computations |
| `pandas` | Data loading and manipulation |
| `scipy` | Scientific computing |
| `joblib` | Model serialisation |

## Deployment

The app is deployed using **Streamlit Share** — Streamlit turns data scripts into shareable web apps in minutes, all in Python. Simply connect your GitHub repo and deploy on Streamlit Share.

**Live App:** [Bitcoin Price Prediction Web App](https://share.streamlit.io/tandrimasingha/bitcoin-price-prediction-web-app/main/app.py)

## App Preview

![App Preview](https://user-images.githubusercontent.com/78292851/156793297-039024d7-d263-4444-9bbb-c05e8a945d47.png)

## References

- [Kaggle: Boston Housing Linear Regression](https://www.kaggle.com/patrickparsa/boston-housing-linear-regression)
- [GitHub: ML Housing Price Prediction](https://github.com/yawavi92/ML-Housing_price_predection/blob/main/melbourne_housing_data.ipynb)

## Contributed By

Tandrima Singha
