# Image Classification with Machine Learning Models

This project contains code snippets and explanations for training and using machine learning models for image classification tasks. Four different models are included:

1. Convolutional Neural Network (CNN)
2. K-Nearest Neighbors (KNN)
3. Random Forest
4. Support Vector Machine (SVM)

## Introduction

Image classification is a fundamental task in computer vision, where the goal is to assign a label or a class to an image based on its content. Machine learning models can be trained to automatically classify images into predefined categories.

## Models

### 1. Convolutional Neural Network (CNN)

- **Description:** CNNs are deep learning models particularly well-suited for image classification tasks. They consist of multiple layers of convolutional and pooling operations, followed by fully connected layers.
- **Training:** The provided script (`cnn_image_classifier.ipynb`) demonstrates how to train a CNN model using TensorFlow/Keras. It includes data preprocessing steps, model architecture definition, compilation, training, and saving the trained model.
- **Usage:** After training, the model can classify new images as "Real" or "Fake". The script prompts the user to upload an image for classification using a file dialog.

https://github.com/vidurAgg22/ML-CaPsule/assets/165144144/dea78388-c2bd-4060-aa77-101ecea0c761

Accuracy: 0.5973266111140987

### 2. K-Nearest Neighbors (KNN)

- **Description:** KNN is a simple and intuitive machine learning algorithm used for classification tasks. It classifies new instances based on the majority class among their k nearest neighbors in the feature space.
- **Training:** The provided script (`knn_image_classifier.ipynb`) demonstrates how to train a KNN model using scikit-learn. It includes data preprocessing steps, model training, and saving the trained model.
- **Usage:** After training, the model can classify new images as "Real" or "Fake". The script prompts the user to upload an image for classification using a file dialog.

https://github.com/vidurAgg22/ML-CaPsule/assets/165144144/288c6fc7-5030-477d-ad36-f9a0438232b6

Accuracy: 0.6089563425145212

### 3. Random Forest

- **Description:** Random Forest is an ensemble learning method that constructs multiple decision trees during training and outputs the mode of the classes (classification) or the average prediction (regression) of the individual trees.
- **Training:** The provided script (`randomforest_image_classifier.ipynb`) demonstrates how to train a Random Forest model using scikit-learn. It includes data preprocessing steps, model training, and saving the trained model.
- **Usage:** After training, the model can classify new images as "Real" or "Fake". The script prompts the user to upload an image for classification using a file dialog.

https://github.com/vidurAgg22/ML-CaPsule/assets/165144144/18c447e2-b7d4-42b2-aa88-ab98f8f429ef

Accuracy: 0.6241334082818063

### 4. Support Vector Machine (SVM)

- **Description:** SVM is a supervised learning algorithm that can be used for classification or regression tasks. It finds the hyperplane that best separates the classes in the feature space.
- **Training:** The provided script (`svm_image_classifier.ipynb`) demonstrates how to train an SVM model using scikit-learn. It includes data preprocessing steps, model training, and saving the trained model.
- **Usage:** After training, the model can classify new images as "Real" or "Fake". The script prompts the user to upload an image for classification using a file dialog.

https://github.com/vidurAgg22/ML-CaPsule/assets/165144144/c474dc63-5889-45f9-8b7e-23dad457ce7e

Accuracy: 0.62619449128724

## Requirements

- Python 3.x
- TensorFlow (for CNN)
- scikit-learn
- NumPy
- PIL (Python Imaging Library)
- tkinter (for file dialog)
- Google Colab (for running the code)

## Dataset
The dataset used for training these models can be found at [this Kaggle link](https://www.kaggle.com/datasets/mgdammy/trimdataset/data).

## Usage

1. **Training Models:**
   - Update the paths to your local dataset directory in the respective scripts.
   - Run each script to train the corresponding model. The trained models will be saved locally.
   
2. **Classifying Images:**
   - For each model, there is a classification script  that takes an image file as input and classifies it as either "REAL" or "FAKE".
   - Run the classification script and follow the instructions to upload an image for classification.

If you have any Queries or Suggestions, feel free to reach out to me.

[<img height="30" src="https://img.shields.io/badge/linkedin-blue.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />][LinkedIn]
[<img height="30" src="https://img.shields.io/badge/github-black.svg?&style=for-the-badge&logo=github&logoColor=white" />][Github]
<br />

[linkedin]: https://www.linkedin.com/in/viduragarwal1/
[github]: https://github.com/vidurAgg22

<h3 align="center">Show some &nbsp;❤️&nbsp; by starring this repo! </h3>