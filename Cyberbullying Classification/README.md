# Cyberbullying Classification

## Overview

This project classifies text into age, ethnicity, gender, religion, other cyberbullying, or non-cyberbullying categories. It includes a reproducible ensemble-training script and a Streamlit dashboard.

## Dataset

The training script downloads the [Cyberbullying Classification dataset](https://www.kaggle.com/datasets/andrewmvd/cyberbullying-classification) through KaggleHub. It contains more than 47,000 labelled tweets across six categories.

## Model

The classifier is a hard-voting ensemble of logistic regression, multinomial naive Bayes, and random forest models. Text is transformed using TF-IDF word and bigram features.

## Setup

From the `Cyberbullying Classification` directory, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Generate the model artifacts:

```bash
python train_model.py
```

The command downloads the dataset and creates `models/Voting.pkl` and `models/tfidf.pkl`. These generated artifacts are ignored by the repository and must be created locally.

Run the dashboard:

```bash
streamlit run app.py
```

If either artifact is missing or invalid, the dashboard shows recovery instructions instead of crashing during startup.
