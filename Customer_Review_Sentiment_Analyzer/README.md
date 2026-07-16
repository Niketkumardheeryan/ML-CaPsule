# Customer Review Sentiment Analyzer

A beginner-friendly, end-to-end machine learning project that classifies customer reviews as **Positive**, **Neutral**, or **Negative** using NLP and logistic regression.

##  Project Overview

This project walks you through the complete NLP pipeline for sentiment analysis on customer reviews:
- **Data Loading**: Directly from public GitHub CSV URL (no local files needed initially)
- **Text Preprocessing**: Clean text (remove URLs, HTML, punctuation, stopwords, lemmatization)
- **Exploratory Data Analysis (EDA)**: Understand dataset structure and distributions
- **Label Creation**: Map star ratings to sentiment categories (1–2 stars = Negative, 3 = Neutral, 4–5 = Positive)
- **Feature Engineering**: Convert text to numerical features using TF-IDF Vectorization
- **Model Training**: Train a Logistic Regression classifier
- **Model Evaluation**: Assess performance with accuracy, precision, recall, F1 score, and confusion matrix
- **Interactive Prediction**: Test the model with your own review text

##  Dataset

- **Name**: Amazon Product Reviews Dataset
- **Description**: Small public dataset containing 1000 real Amazon product reviews with star ratings (1-5)
- **Source**:
  - GitHub Repository: https://github.com/imsreecharan/datasets_/
  - Direct CSV URL (used by notebook): https://raw.githubusercontent.com/imsreecharan/datasets_/master/amazon_reviews.csv
- **Key Columns**:
  - `reviewText`: Full text of customer review
  - `overall`: Star rating given by the customer (1-5)

##  Installation & Usage

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Launch & Run Notebook
```bash
jupyter notebook Customer_Review_Sentiment_Analyzer.ipynb
```
- Run all cells sequentially (`Kernel → Restart & Run All`)
- The notebook will guide you through each step with explanations and visualizations

##  Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- scikit-learn
- nltk

##  Notebook Workflow

1. **Introduction**: What is sentiment analysis?
2. **Imports**: Load all required libraries and download NLTK data
3. **Data Loading**: Load dataset from public CSV URL
4. **EDA**: Explore distributions of ratings and sample reviews
5. **Preprocessing**: Define and apply text cleaning pipeline
6. **Label Creation**: Convert star ratings to sentiment labels
7. **Train-Test Split**: Split into 80% training and 20% testing data
8. **TF-IDF Vectorization**: Convert text to numerical feature vectors
9. **Model Training**: Train logistic regression model
10. **Evaluation**: Check accuracy, precision, recall, F1, and confusion matrix
11. **Prediction**: Interactive function to test custom reviews

##  Results

The model achieves strong performance on the sample dataset!

##  Future Improvements

- Train on full Amazon Reviews dataset (millions of records)
- Experiment with advanced models (Random Forest, SVM, XGBoost)
- Use transformer-based models (BERT, RoBERTa) for state-of-the-art results
- Build a web app for real-time predictions using Streamlit or Flask
- Add aspect-based sentiment analysis (e.g., detect sentiment on specific product features like "price" or "quality")
- Support multilingual reviews with multilingual transformers

##  Repository Structure

```
Customer_Review_Sentiment_Analyzer/
├── Customer_Review_Sentiment_Analyzer.ipynb  # Main, fully executed notebook
├── README.md                                   # Project documentation
└── requirements.txt                            # Python dependencies
```

##  Author

Contributed to [ML-CaPsule](https://github.com/Ananya-vastare/ML-CaPsule) under GSSoC'26.
