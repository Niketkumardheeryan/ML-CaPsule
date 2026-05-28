# Pet Classification Model

## Overview

This project is a deep learning–based pet breed classification model that takes an image of a pet as input and predicts the breed present in the image.

The model is trained using the Oxford-IIIT Pet Dataset and is capable of classifying images into **37 different cat and dog breeds**.

## Dataset

The model uses the publicly available **Oxford-IIIT Pet Dataset**, which contains high-quality images of various pet breeds along with corresponding annotations.

- Total Classes: **37**
- Categories:
  - Cat Breeds
  - Dog Breeds
- Dataset Source: Kaggle-hosted Oxford Pets Dataset

## Model

The classification model is built using a **ResNet architecture** implemented with PyTorch.

### Features

- Image-based pet breed prediction
- Supports 37 cat and dog breeds
- Deep learning model trained on real-world pet images
- Built using PyTorch and TorchVision

## Workflow

1. Input a pet image
2. Preprocess the image
3. Pass the image through the trained ResNet model
4. Predict the breed with the highest confidence score

## Technologies Used

- Python
- PyTorch
- TorchVision
- NumPy
- Pandas
- Matplotlib
- Pillow
- KaggleHub## Installation

Before running the project, make sure the following libraries are installed:

- `kagglehub`
- `pandas`
- `numpy`
- `matplotlib`
- `pillow`
- `torch`
- `torchvision`

### Install Dependencies

```bash
pip install kagglehub pandas numpy matplotlib pillow torch torchvision
```

Run the main.py file to train the RESNET model on the oxford pet classification dataset. 
The model then successfully builds up the pet_model.pth, which could be used via the predict.py file. To test for any pet image which is listed in the dataset, download any image, run the predict.py file and then paste the image path.

The model successfully predicts the top 3 classes for the pet.
    