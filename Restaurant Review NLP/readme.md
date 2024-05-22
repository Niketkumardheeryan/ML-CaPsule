# NLP in Restaurant Review

This project aims to perform sentiment analysis on restaurant reviews using Natural Language Processing (NLP) techniques.

## Dataset
The dataset used in this project can be found on Kaggle: [Restaurant Reviews Dataset](https://www.kaggle.com/datasets/d4rklucif3r/restaurant-reviews). It consists of 1000 reviews along with their corresponding labels (positive or negative).

## Code Overview
The provided code performs the following tasks:
1. **Data Preprocessing**:
   - Reads the dataset from the file 'Restaurant_Reviews.tsv'.
   - Removes special characters and converts text to lowercase.
   - Tokenizes the text and applies stemming using Porter Stemmer.
   - Removes stopwords from the text.
   - Constructs a corpus of preprocessed reviews.
2. **Feature Engineering**:
   - Utilizes CountVectorizer to convert text data into numerical feature vectors.
3. **Model Training**:
   - Splits the dataset into training and testing sets.
   - Trains a RandomForestClassifier model with 501 estimators and 'entropy' criterion.
4. **Model Evaluation**:
   - Predicts labels for the test set.
   - Computes the confusion matrix to evaluate the model's performance.

## Requirements
- Python 3.x
- Libraries:
  - numpy
  - pandas
  - nltk
  - scikit-learn

## Output
The output of the provided code is as follows:
- **Confusion Matrix**:
[[55 42]
[12 91]]

markdown
Copy code
- **Accuracy**: 0.73

## Usage
1. Ensure all required libraries are installed (`pip install numpy pandas nltk scikit-learn`).
2. Download the dataset from the provided Kaggle link.
3. Run the provided code to preprocess the data, train the model, and evaluate its performance.

## Author
- [Nikita]([url](https://github.com/NikitaKandwal))
