# Facial Expression Recognition Using PyTorch

## Overview
This project aims to develop a facial expression recognition system using PyTorch. The system classifies facial expressions into various categories using a convolutional neural network (CNN). The dataset for training and testing the model is sourced from Kaggle and includes multiple facial expressions.

## Dataset
The dataset used for this project is available on Kaggle. It contains images of faces categorized by different expressions such as happy, sad, angry, surprised, etc. 

Dataset URL: [Face Expression Recognition Dataset](https://www.kaggle.com/jonathanoheix/face-expression-recognition-dataset)

## Setup
To set up the environment and install necessary dependencies, follow these steps:

1. **Install Albumentations:** This library is used for augmenting the dataset.
   ```bash
   pip install -U git+https://github.com/albumentations-team/albumentations

2. **Install TIMM:** PyTorch image models library by Ross Wightman.
    ```bash
    pip install timm

3. **Upgrade OpenCV:** Ensure you have the latest version of OpenCV which includes contributions.
     ```bash
    pip install --upgrade opencv-contrib-python


## Model Architecture

The model architecture is based on convolutional neural networks (CNNs) designed for image classification tasks. It leverages pre-trained models from the TIMM library to enhance performance and reduce training time.


