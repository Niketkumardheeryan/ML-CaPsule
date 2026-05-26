# Spam Mail Detection Project

## Overview

Welcome to the Spam Mail Detection Project! This project uses Machine Learning and Natural Language Processing (NLP) techniques to classify emails as spam or ham (not spam).

The project is implemented using a Jupyter Notebook and demonstrates a complete text-classification workflow including:

- Data preprocessing
- Feature extraction using TF-IDF
- Model training using Logistic Regression
- Evaluation and Prediction

This project is a part of the Girl Script Summer of Code (GSSOC 2026) initiative.

## Table of Contents

1.  [Introduction](#introduction)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Installation](#installation)
5.  [How ro Run](#how-to-run)
6.  [Workflow](#workflow)
7.  [Model Training](#model-training)
8.  [License](#license)

## Introduction

Spam emails are a common problem that can lead to wasted time, cluttered inboxes, and potential security risks. This project leverages Machine Learning techniques to automatically classify emails as spam or ham.

The notebook demonstrates how textual email data can be transformed into numerical features using TF-IDF vectorization and classified using a Logistic Regression model.

## Features

- Handling missing values
- Label encoding for spam/ham classification
- TF-IDF Feature Extraction
- Model training with Logistic Regression
- Accuracy evaluation on training data and test data
- Prediction on custom email input

## Technologies Used

- Python
- NumPy
- Pandas
- Scikit-learn
- Jupyter Notebook

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
   cd ML-CaPsule
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   ```

   **To Activate:**

   Windows

   ```sh
   venv\Scripts\activate
   ```

   Linux / MacOS

   ```sh
   source venv/bin/activate
   ```

3. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```

## How to Run

1. Open the `.ipynb` notebook file using any of the following:
   - Jupyter Notebook
   - JupyterLab
   - VS Code with the Jupyter Extension

2. Dataset Setup

   The notebook expects a dataset file named: **mail_data.csv**

   Place the dataset in the project directory and update the dataset path inside the notebook if necessary.

   Current dataset loading path used in notebook:

   ```python
   raw_mail_data = pd.read_csv('/content/mail_data.csv')
   ```

   If running the project locally, you may update it to:

   ```python
   raw_mail_data = pd.read_csv('mail_data.csv')
   ```

3. Run the Notebook

   Execute the notebook cells sequentially to:
   - preprocess the dataset
   - perform TF-IDF vectorization
   - train the Logistic Regression model
   - evaluate model performance
   - test predictions on custom email input

## Workflow

The project follows this Machine Learning workflow:

1. Load and preprocess the dataset
2. Encode spam/ham labels
3. Split data into training and testing sets
4. Convert text into TF-IDF feature vectors
5. Train the Logistic Regression model
6. Evaluate model performance
7. Predict spam or ham for custom email input

## Model Training

The project uses:

- TF-IDF Vectorizer for feature extraction
- Logistic Regression for spam classification

Model performance is evaluated using training and testing accuracy

Example prediction:

_Ham mail_

## License

This project is licensed under the MIT License.

We hope this project helps beginners understand the fundamentals of NLP-based spam classification and Machine Learning workflows.

---

_This project is developed as part of the Girl Script Summer of Code (GSSOC) 2026 initiative._
