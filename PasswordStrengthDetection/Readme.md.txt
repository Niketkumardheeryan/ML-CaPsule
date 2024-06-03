# Password Strength Checker

## Overview
This project is a simple password strength checker built using Python. The application uses a logistic regression model trained on a dataset of passwords to classify the strength of a given password as Weak, Medium, or Strong. The model uses TF-IDF vectorization for feature extraction and Gradio for the user interface.

## Features
- **Model Training**: The logistic regression model is trained to classify passwords into three categories: Weak, Medium, and Strong.
- **TF-IDF Vectorization**: The passwords are tokenized and vectorized using the TF-IDF method to convert them into numerical data suitable for model training.
- **Interactive Interface**: A user-friendly interface is created using Gradio, allowing users to input passwords and receive strength predictions.

## Dataset
The dataset (`data.csv`) should contain at least two columns:
- `password`: The actual password string.
- `strength`: An integer representing the strength of the password (0 for Weak, 1 for Medium, 2 for Strong).

## Dependencies
- pandas
- numpy
- scikit-learn
- gradio

You can install the necessary packages using:
```bash
pip install pandas numpy scikit-learn gradio
```

## Code Explanation

### Loading the Dataset
The dataset is loaded into a pandas DataFrame and cleaned by dropping any rows with missing values.

### Mapping Strength Values
The numeric values in the `strength` column are mapped to their corresponding string representations ("Weak", "Medium", "Strong").

### Tokenization Function
A custom tokenization function is defined to split each password into individual characters.

### Data Splitting and Vectorization
The passwords are vectorized using TF-IDF and split into training and test sets.

### Model Training
A logistic regression model is trained on the vectorized passwords.

### Prediction Function
A function is defined to transform an input password and use the trained model to predict its strength.

### Gradio Interface
A Gradio interface is created to provide an interactive frontend for the password strength checker.

## How to Run
1. Ensure all dependencies are installed.
2. Place the dataset (`data.csv`) in the same directory as the script.
3. Run the script:
    ```bash
    python script_name.py
    ```
4. A Gradio interface will launch in your default web browser, allowing you to input passwords and check their strength.