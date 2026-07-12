# Convolutional Neural Network (CNN)

## Overview

This notebook demonstrates image classification using a Convolutional Neural Network (CNN) implemented with PyTorch. The notebook uses the CIFAR-10 dataset from the Hugging Face Datasets library and covers the complete deep learning workflow, including dataset loading, preprocessing, model building, training, evaluation, and prediction.

---

## Dataset

### Classification Dataset

**Dataset:** CIFAR-10

The dataset is downloaded automatically using the Hugging Face `datasets` library.

Install the required package:

```bash
pip install datasets
```

Load the dataset:

```python
from datasets import load_dataset

dataset = load_dataset("cifar10")
```

**Dataset Source:**

https://huggingface.co/datasets/cifar10

### Dataset Description

The CIFAR-10 dataset contains **60,000 RGB images** of size **32 × 32 pixels**, divided into **10 image classes**.

Classes:

- Airplane
- Automobile
- Bird
- Cat
- Deer
- Dog
- Frog
- Horse
- Ship
- Truck

Dataset Split:

- Training Images: 50,000
- Testing Images: 10,000

---

## Technologies Used

- Python
- PyTorch
- Hugging Face Datasets
- Torchvision
- NumPy
- Matplotlib

---

## Notebook Contents

The notebook includes:

- Loading the CIFAR-10 dataset using Hugging Face
- Image preprocessing and normalization
- Creating a custom PyTorch Dataset
- Creating DataLoaders
- Building a Convolutional Neural Network (CNN)
- Model training
- Loss calculation
- Model evaluation
- Image classification on unseen test data

---

## Learning Outcomes

After completing this notebook, learners will understand:

- Fundamentals of Convolutional Neural Networks (CNNs)
- Working with image datasets in PyTorch
- Loading datasets using Hugging Face Datasets
- Data preprocessing and normalization
- Building CNN architectures for image classification
- Training and evaluating deep learning models
- Performing inference on unseen images

---

## Requirements

Install the required dependencies before running the notebook:

```bash
pip install torch torchvision datasets matplotlib
```

---

## Output

After training, the notebook reports:

- Training Loss
- Test Accuracy
- Image Classification Predictions

The trained CNN learns to classify images into one of the ten CIFAR-10 object categories.