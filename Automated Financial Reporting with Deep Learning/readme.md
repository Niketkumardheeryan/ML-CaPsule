# Automated Financial Reporting with Deep Learning

## Overview

This project trains a neural network to predict equity from synthetic financial data and presents test-set results in an interactive Streamlit report.

## Dataset

`financial_data.csv` contains monthly revenue, expenses, profit, assets, liabilities, and equity values. The first five numerical fields are model inputs and equity is the prediction target.

## Project structure

```text
├── app.py                 # Streamlit reporting dashboard
├── train_model.py         # Reproducible model training and export
├── financial_data.csv     # Synthetic dataset
├── requirements.txt       # Project dependencies
└── readme.md              # Project documentation
```

The generated `financial_model.keras` is excluded from Git. The previously committed `financial_model.h5` was an HTML document rather than a valid HDF5 model and could not be loaded by Keras.

## Setup

From this project directory, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Generate a valid Keras model:

```bash
python train_model.py
```

Start the dashboard:

```bash
streamlit run app.py
```

The dashboard evaluates the model on a deterministic test split, aligns predictions with their original dates, and provides downloadable prediction and summary reports.
