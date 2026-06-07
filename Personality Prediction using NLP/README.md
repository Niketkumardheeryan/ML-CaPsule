# Personality Prediction using NLP: Per-Axis Binary Classification

Predicts MBTI personality type from social media posts by treating each of the 4 axes as an independent binary classification problem. This approach is far more effective than predicting one of 16 types directly (which has only ~6% baseline accuracy).

## Purpose

The Myers-Briggs Type Indicator (MBTI) describes personality across 4 independent axes:

| Axis | Binary Task |
|------|-------------|
| Mind | Introversion (I) vs Extroversion (E) |
| Information | Intuition (N) vs Sensing (S) |
| Decision | Thinking (T) vs Feeling (F) |
| Lifestyle | Judging (J) vs Perceiving (P) |

One binary Logistic Regression classifier is trained per axis using TF-IDF features extracted from social media posts. Predictions from the 4 classifiers are combined to form a complete 4-letter MBTI type.

## Results (Test Set, 20% hold-out)

| Axis | Task | Accuracy | F1 | ROC-AUC |
|------|------|----------|----|---------|
| Mind | I vs E | 74.01% | 0.751 | 0.767 |
| Information | N vs S | 81.15% | 0.825 | 0.776 |
| Decision | T vs F | 78.39% | 0.784 | 0.866 |
| Lifestyle | J vs P | 67.78% | 0.680 | 0.720 |

## Dataset

[MBTI Personality Type Dataset](https://www.kaggle.com/datasets/datasnaek/mbti-type) by datasnaek on Kaggle.

Download `mbti_1.csv` and place it in this folder before running the notebook or the app.

## Project Structure

```
Personality Prediction using NLP/
├── personality_prediction_binary_axes.ipynb   # Full analysis notebook
├── app.py                                      # Streamlit web app
├── requirements.txt
├── mbti_1.csv                                  # Dataset (download from Kaggle)
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the Notebook

Open `personality_prediction_binary_axes.ipynb` in Jupyter or VS Code and run all cells top-to-bottom with `mbti_1.csv` in the same directory.

## Running the Web App

```bash
streamlit run app.py
```

The app trains all 4 classifiers on first launch (takes about 30 seconds), then lets you paste any text and get a predicted MBTI type with per-axis confidence scores.

![App screenshot showing MBTI prediction with confidence bars per axis](https://raw.githubusercontent.com/Jay-Jay-Tee/personality-prediction-mbti/main/demo.png)

## Approach Details

- **Preprocessing:** Lowercase, remove URLs, strip non-alphabetic characters, remove MBTI type mentions from posts to prevent data leakage
- **Features:** TF-IDF with unigrams and bigrams, 10,000 features, minimum document frequency of 3
- **Model:** Logistic Regression with `class_weight='balanced'` to handle skewed class distributions
- **Evaluation:** Accuracy, weighted F1, ROC-AUC, confusion matrices, and top predictive words per axis
