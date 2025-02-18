# Toxic Comment Classification

This project focuses on classifying toxic comments into multiple categories using machine learning techniques.

## Dataset
- The dataset consists of comments labeled as `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, and `identity_hate`.
- `non_toxic` comments are also included as a control group.

## Preprocessing
- Text cleaning and tokenization
- Removing stopwords and special characters
- Vectorization using TF-IDF

## Model Development
- The model was trained using a machine learning classifier (e.g., Logistic Regression, Naïve Bayes, or a neural network).
- Multi-label classification approach was used to predict multiple toxic categories for each comment.

## Model Performance
### Accuracy
- Model Accuracy: **0.7325**

### Classification Report
```
                precision    recall  f1-score   support

identity_hate       0.00      0.14      0.00        14
       insult       0.00      0.06      0.00        68
    non_toxic       0.99      0.75      0.85    146921
      obscene       0.00      0.15      0.00        65
 severe_toxic       0.00      0.00      0.00         0
       threat       0.00      0.17      0.00         6
        toxic       0.10      0.41      0.16      6090

     accuracy                           0.73    153164
    macro avg       0.16      0.24      0.15    153164
 weighted avg       0.95      0.73      0.82    153164
```

## Observations
- The model performs well for `non_toxic` comments, achieving high precision and recall.
- The `toxic` class has a moderate recall (0.41) but a low precision (0.10), indicating false positives.
- Other toxic categories (`identity_hate`, `insult`, `obscene`, `threat`) have very low precision and recall.
- The `severe_toxic` category has no true samples in the test set, leading to undefined recall.

## Future Improvements
- Address class imbalance by oversampling underrepresented categories or undersampling the dominant class.
- Experiment with deep learning models like LSTMs or transformers for better text representation.
- Fine-tune the threshold for classification to reduce false positives.
- Improve feature engineering techniques, such as word embeddings (e.g., Word2Vec, GloVe, BERT).

## Dependencies
- Python 3.11
- Scikit-learn
- Numpy
- Pandas
- Matplotlib
- NLTK

## Running the Code
```bash
python train.py  # Train the model
python evaluate.py  # Evaluate the model
```

## Image Section
![image](https://github.com/user-attachments/assets/1799675a-b3a4-4cb9-9926-1299568a6601)


## Acknowledgments
This project is inspired by Kaggle's toxic comment classification challenge.

