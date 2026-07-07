# Feedforward Neural Network on Titanic Dataset

This project involves building and training a Feedforward Neural Network to predict the survival of passengers on the Titanic using the Titanic dataset. The aim is to apply a deep learning algorithm to perform binary classification.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Model](#model)
- [Training and Evaluation](#training-and-evaluation)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

This project applies a Feedforward Neural Network to classify passengers on the Titanic as survived or not survived based on various features such as age, sex, class, and more. The goal is to explore the effectiveness of deep learning on this classic dataset.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/titanic-feedforward.git
    cd titanic-feedforward
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Preprocessing the Data

Ensure you have the Titanic dataset CSV files (`train.csv`, `test.csv`). Preprocess the data before training the model.

### Training the Model

Use the following script to train the model:
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
# Load the dataset
# Preprocess the data (handle missing values, encode categorical variables, etc.)
# Convert categorical columns to numerical
# Split the data into features and labels
# Split the data into training and testing sets
# Scale the data
# Create the model
# Train the model and capture the history
# Plot the accuracy

