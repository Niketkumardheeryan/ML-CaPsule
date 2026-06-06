# Customer Review Sentiment Analyzer

## Overview

This project classifies Amazon product reviews into Positive, Neutral, and Negative sentiments using Natural Language Processing (NLP) and Machine Learning.

The idea is to help users quickly understand the sentiment behind customer reviews without having to read hundreds of comments manually.

## Features

* Text preprocessing and cleaning
* Sentiment classification into Positive, Neutral, and Negative
* TF-IDF based feature extraction
* Logistic Regression model
* Interactive Streamlit interface for real-time predictions

## Dataset

The model is trained on an Amazon Product Reviews dataset obtained from Kaggle.

Star ratings are converted into sentiment labels as follows:

| Rating | Sentiment |
| ------ | --------- |
| 4-5    | Positive  |
| 3      | Neutral   |
| 1-2    | Negative  |

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-Learn
* Streamlit
* Joblib

## Project Structure

```text
Customer_Review_Sentiment_Analyzer/
│
├── app.py
├── train.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
├── README.md
├── dataset/
└── screenshots/
```

## Model Pipeline

1. Load and preprocess review data
2. Convert ratings into sentiment labels
3. Clean review text
4. Transform text using TF-IDF Vectorization
5. Train a Logistic Regression classifier
6. Evaluate model performance
7. Save the trained model and vectorizer
8. Use Streamlit for real-time sentiment prediction

## Performance

Model: Logistic Regression

Feature Extraction: TF-IDF Vectorization

Accuracy Achieved: **88.78%**

Classification Report:

```text
Negative  -> Precision: 0.69 | Recall: 0.59
Neutral   -> Precision: 0.37 | Recall: 0.12
Positive  -> Precision: 0.92 | Recall: 0.98
```

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python train.py
```

Run the application:

```bash
streamlit run app.py
```

## Sample Predictions

Input:

```text
This product exceeded my expectations and works perfectly.
```

Output:

```text
Positive
```

Input:

```text
Worst purchase I have made. Completely disappointed.
```

Output:

```text
Negative
```

## Future Improvements

* Experiment with XGBoost and LightGBM
* Improve Neutral sentiment detection
* Fine-tune transformer-based models such as BERT
* Deploy the application online

## Author

Built as part of an open-source contribution to ML-CaPsule.

