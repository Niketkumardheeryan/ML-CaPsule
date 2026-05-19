# Fake News Detection using NLP and Logistic Regression

## Project Overview
This is a beginner-friendly Machine Learning project that builds a text classification model to detect whether a news article is Fake or Real. It uses Natural Language Processing (NLP) techniques for text preprocessing and Feature Extraction (TF-IDF), followed by a Logistic Regression model for classification.

## Folder Structure
```
Fake_News_Detection/
│
├── data/
│   ├── Fake.csv             # The Fake news dataset
│   └── True.csv             # The True news dataset
├── models/                  # Directory to save trained models
├── notebooks/
│   └── Fake_News_Detection.ipynb # Jupyter Notebook with step-by-step explanations
├── src/
│   ├── preprocess.py        # Text preprocessing functions
│   ├── train.py             # Script to train and save the model
│   └── predict.py           # Script to load the model and make predictions
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Dataset Information
The project uses the popular Fake and True News dataset. The preprocessing step automatically combines them and creates the target variable:
- `title`: The headline of the news article
- `text`: The main body of the news article
- `label`: `0` for Fake news, `1` for Real news

## Installation Steps
1. Clone or download this repository.
2. Ensure you have Python 3.7+ installed.
3. Install the required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the necessary NLTK corpora:
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('punkt')
   ```

## How to Run the Notebook
1. Navigate to the `notebooks/` directory.
2. Start Jupyter Notebook:
   ```bash
   jupyter notebook Fake_News_Detection.ipynb
   ```
3. Run the cells step-by-step to understand the workflow.

## How to Run the Python Scripts
You can also run the project using the modular scripts in the `src/` directory.
1. Train the model:
   ```bash
   python src/train.py
   ```
   This will train the model and save `model.pkl` and `vectorizer.pkl` inside the `models/` directory.
2. Make predictions on sample text:
   ```bash
   python src/predict.py
   ```

## Results Summary
The Logistic Regression model provides a strong baseline for text classification tasks. We use TF-IDF to convert text into numerical vectors and evaluate our model using Accuracy, Precision, Recall, F1-score, and a Confusion Matrix to understand false positives and false negatives.
