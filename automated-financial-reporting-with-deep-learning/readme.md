# Automated Financial Reporting with Deep Learning

## Overview
This project aims to automate the generation of financial reports using deep learning, reducing manual effort and errors. The project involves creating a synthetic dataset, training a deep learning model, and generating financial reports.

## Dataset
The dataset contains the following columns:
- `Date`: The date of the observation.
- `Revenue`: The revenue for the period.
- `Expenses`: The expenses for the period.
- `Profit`: The profit for the period.
- `Assets`: The total assets value.
- `Liabilities`: The total liabilities value.
- `Equity`: The total equity value.

## Project Structure
- `financial_data.csv`: The synthetic dataset file.
- `generate_dataset.py`: Script to generate the synthetic dataset.
- `train_model.py`: Script to train the deep learning model.
- `evaluate_model.py`: Script to evaluate the trained model.
- `generate_report.py`: Script to generate financial reports.

## Setup
1. Install the required packages:
   ```bash
   pip install pandas numpy scikit-learn tensorflow
