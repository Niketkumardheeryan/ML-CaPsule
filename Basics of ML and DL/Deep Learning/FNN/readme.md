# Feedforward Neural Network (FNN)

## Overview

This project demonstrates the implementation of **Feedforward Neural Networks (FNNs)** for both **classification** and **regression** tasks using TensorFlow/Keras. It introduces the complete deep learning workflow, including data preprocessing, model building, training, evaluation, and prediction on unseen data.

---

## Datasets

### Classification Dataset

**Source:** Date Fruit Dataset

The notebook downloads the dataset as **`DateFruit_Dataset.csv`** using **gdown**.

**Download Link:**
`https://drive.google.com/uc?id=1dZIaL-O9ZRrk4cwFwEHorW10E2io3XyS`

This dataset contains numerical features describing the physical characteristics of different varieties of date fruits. It is used to train a Feedforward Neural Network (FNN) for a multiclass classification task.

### Regression Dataset

**Source:** Combined Cycle Power Plant Dataset

The notebook downloads the dataset as **`powerplant_data.csv`** using **gdown**.

**Download Link:**
`https://drive.google.com/uc?id=1SSt6XdVJg7B8VS4R1dWYStz1uj5cDDfB`

This dataset contains environmental variables such as Ambient Temperature (AT), Exhaust Vacuum (V), Ambient Pressure (AP), and Relative Humidity (RH). The objective is to predict the Electrical Power Output (PE) using a Feedforward Neural Network.

---

## Files Included

### `FNN_Classification.ipynb`

This notebook demonstrates the implementation of a Feedforward Neural Network for **multiclass classification**.

**The notebook covers:**

* Downloading and loading the dataset
* Data preprocessing and feature scaling
* Label encoding
* Splitting the dataset into training and testing sets
* Building an FNN using TensorFlow/Keras
* Training the model
* Evaluating the model using Accuracy, Precision, Recall, F1-Score, and Confusion Matrix
* Predicting classes for unseen samples

This notebook helps beginners understand how neural networks learn to classify data from input features.

---

### `FNN_Regression.ipynb`

This notebook demonstrates the implementation of a Feedforward Neural Network for **regression**.

**The notebook covers:**

* Downloading and loading the dataset
* Data preprocessing and feature normalization
* Splitting the dataset into training and testing sets
* Building an FNN regression model
* Training the model
* Evaluating the model using MAE, MSE, RMSE, and R² Score
* Predicting continuous numerical values

This notebook helps beginners understand how neural networks predict continuous outputs using regression techniques.

---

## Key Features

* Feedforward Neural Network implementation using TensorFlow/Keras
* Classification using the Date Fruit Dataset
* Regression using the Combined Cycle Power Plant Dataset
* Automatic dataset download using gdown
* Data preprocessing and feature scaling
* Model training and evaluation
* Prediction on unseen data
* Beginner-friendly implementation with practical examples

---

## How the Algorithm Works

Both notebooks follow the same workflow:

1. Load the dataset.
2. Preprocess and normalize the input data.
3. Split the dataset into training and testing sets.
4. Build a Feedforward Neural Network with input, hidden, and output layers.
5. Train the model using backpropagation and the Adam optimizer.
6. Evaluate the trained model using appropriate performance metrics.
7. Use the trained model to make predictions on unseen data.

---

## Tech Stack

* Python
* TensorFlow / Keras
* NumPy
* Pandas
* Matplotlib
* Scikit-learn
* gdown (Dataset Download)

---

## Usage

1. Open `FNN_Classification.ipynb` or `FNN_Regression.ipynb` in **Jupyter Notebook** or **Google Colab**.
2. Run all notebook cells.
3. If the datasets are not available locally, they will be downloaded automatically using **gdown**.
4. Review the training process, evaluation metrics, and model predictions.

---

## References

* TensorFlow Documentation
* Keras Documentation
* Deep Learning by Ian Goodfellow, Yoshua Bengio, and Aaron Courville
* Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow by Aurélien Géron
