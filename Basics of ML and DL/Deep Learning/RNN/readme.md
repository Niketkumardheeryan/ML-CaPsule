# Recurrent Neural Network (RNN) for IMDb Sentiment Analysis

## Overview
This notebook demonstrates how to build, train, and evaluate a **Recurrent Neural Network (RNN)** for **sentiment analysis** using the **IMDb Movie Reviews** dataset. RNNs are designed to process sequential data by maintaining information from previous time steps, making them well-suited for natural language processing tasks.

## About the IMDb Dataset
The IMDb dataset contains **50,000 movie reviews** labeled as either **positive** or **negative** sentiment.

The dataset is split into:
- **25,000** training reviews
- **25,000** testing reviews

Each review is represented as a sequence of integer-encoded words.

## Dataset

The notebook uses the **IMDb Movie Reviews** dataset.

### Download using gdown

```bash
pip install gdown
gdown --id 1LL4rJU6xtgn1fUHTO7TmdrXNhz0A19CG
```

### Direct Google Drive Link

https://drive.google.com/file/d/1LL4rJU6xtgn1fUHTO7TmdrXNhz0A19CG/view?usp=sharing

After downloading, place the file as:

`IMDB Dataset.csv`

in the same directory as the notebook.

## Topics Covered
- Introduction to Recurrent Neural Networks (RNNs)
- Loading the IMDb dataset
- Text preprocessing and sequence padding
- Word Embedding
- Building an RNN model
- Model training and validation
- Performance evaluation
- Sentiment prediction on movie reviews

## Learning Objectives
- Understand the fundamentals of Recurrent Neural Networks.
- Learn how text data is represented for deep learning models.
- Build and train an RNN for binary text classification.
- Evaluate model performance using classification metrics.
- Predict the sentiment of unseen movie reviews.

## Model Architecture
The RNN model typically consists of:
- Embedding Layer
- SimpleRNN Layer
- Dropout Layer (optional)
- Dense Hidden Layer
- Sigmoid Output Layer

## Evaluation Metrics
- Accuracy
- Loss
- Precision
- Recall
- F1-Score
- Confusion Matrix

## Applications
- Sentiment Analysis
- Spam Detection
- Text Classification
- Language Modeling
- Customer Feedback Analysis

## Requirements
- Python 3.x
- NumPy
- Matplotlib
- TensorFlow / Keras
- Scikit-learn

## Expected Outcome
After completing this notebook, you will be able to:
- Preprocess textual data for deep learning.
- Train an RNN on the IMDb dataset.
- Classify movie reviews as positive or negative.
- Interpret training and validation accuracy/loss curves.

## References
- TensorFlow/Keras Documentation
- IMDb Large Movie Review Dataset
- Deep Learning by Ian Goodfellow, Yoshua Bengio, and Aaron Courville
- Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow