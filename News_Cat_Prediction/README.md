# News Article Classification Streamlit App

## Overview

This Streamlit application classifies news articles into five predefined categories: Business, Entertainment, Politics, Sports, and Technology. By leveraging advanced machine learning techniques, including Non-Negative Matrix Factorization (NMF) and Support Vector Classifier (SVC), this app provides users with an intuitive interface to input articles and receive instant predictions.

## Table of Contents

- [News Article Classification Streamlit App](#news-article-classification-streamlit-app)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Dataset](#dataset)
  - [Jupyter Notebook](#jupyter-notebook)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Model Training](#model-training)
  - [Model Evaluation](#model-evaluation)
  - [Model Tuning](#model-tuning)
  - [Predicting Test Dataset](#predicting-test-dataset)
  - [Contributing](#contributing)

## Features

- **Interactive Article Classification**: Users can input any news article and receive a predicted category.
- **Visualization Tools**: Display model performance metrics and confusion matrices to analyze classification results.
- **Multiple Models**: Benchmark and compare different classification models to determine the best-performing algorithm.
- **User-Friendly Interface**: Designed with simplicity in mind, making it easy for users to navigate and understand the results.

## Technologies Used

- [Streamlit](https://streamlit.io/) - Framework for building the web application.
- [scikit-learn](https://scikit-learn.org/stable/) - For machine learning algorithms and evaluation metrics.
- [pandas](https://pandas.pydata.org/) - Data manipulation and analysis.
- [numpy](https://numpy.org/) - Numerical computations and array handling.
- [matplotlib](https://matplotlib.org/) - Data visualization library for creating static, animated, and interactive visualizations.
- [seaborn](https://seaborn.pydata.org/) - Statistical data visualization built on top of Matplotlib.

## Dataset

The application uses a public dataset from the BBC, comprising 2,225 articles labeled under five categories: Business, Entertainment, Politics, Sports, and Technology. The dataset is split into 1,490 records for training and 735 records for testing.

The dataset can be downloaded from its original source or is provided in the repository for local use.

## Jupyter Notebook

The accompanying Jupyter Notebook (`news-classification.ipynb`) serves as the foundation for the Streamlit app. It includes the following key components:

- **Data Preprocessing**: Load the dataset, encode categorical labels, and apply text preprocessing techniques such as tokenization, stemming, and stopword removal.
- **Feature Extraction**: Utilize Term Frequency-Inverse Document Frequency (TF-IDF) to convert text data into numerical feature vectors suitable for machine learning models.
- **Model Training**: Implement various machine learning algorithms, including Logistic Regression, Naive Bayes, and Support Vector Classifier (SVC), while evaluating their performance.
- **Model Evaluation**: Generate classification reports and confusion matrices to assess model accuracy, precision, recall, and F1-score.
- **Hyperparameter Tuning**: Optimize model parameters using techniques like GridSearch to improve performance.

The notebook provides a detailed analysis and visualization of the data, serving as the basis for the classification logic implemented in the Streamlit app.

## Installation

To run the app locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

2. **Open your web browser and navigate to** `http://localhost:8501`.

3. **Input your news article** in the provided text area and click on the "Classify" button to see the predicted category.

4. **Explore visualizations** of model performance, including accuracy metrics and confusion matrices.

## Model Training

The app employs various machine learning models to classify articles, including:

- **Logistic Regression**: A statistical method that models the relationship between features and class probabilities.
- **Naive Bayes**: A probabilistic classifier that assumes independence among features.
- **Support Vector Classifier (SVC)**: A model that finds the optimal hyperplane to separate classes.

These models are evaluated using cross-validation, and the SVC model is chosen based on its superior accuracy.

## Model Evaluation

Model performance is assessed using metrics such as accuracy, precision, recall, and F1-score. A confusion matrix is visualized to identify misclassifications and analyze model behavior.

## Model Tuning

By examining the top words from the feature extraction phase, we assess whether to adjust model parameters (e.g., number of topics, initialization methods) or preprocessing steps (e.g., stop words, n-grams) to improve the quality of the topics and overall model performance.

## Predicting Test Dataset

Based on benchmark results, the SVC model is selected to predict the test dataset. The app creates the SVC model with the best hyperparameters identified through GridSearch, then applies this model to the test dataset for final predictions.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report bugs, please create an issue or submit a pull request.

1. **Fork the repository.**
2. **Create a new branch:**

   ```bash
   git checkout -b feature-branch
   ```

3. **Make your changes and commit them:**

   ```bash
   git commit -m 'Add new feature'
   ```

4. **Push to the branch:**

   ```bash
   git push origin feature-branch
   ```
