# 🛡️ Fake Review Detection System using BERT & Explainable AI (XAI)

A production-grade NLP pipeline that detects fake/spam reviews on online platforms using a fine-tuned **BERT (`bert-base-uncased`)** transformer model and interprets predictions using **Explainable AI (SHAP & LIME)** to highlight word-level feature contributions.

---

## Problem Statement

Online marketplaces and review platforms (Amazon, Yelp, Google Reviews) are frequently targeted by automated bot networks and fake reviewers posting deceptive feedback. Traditional keyword filtering and rule-based systems fail to handle complex semantic patterns, subtle hyperbole, and contextual spam. 

This project addresses fake review detection using **Deep Transformer Architecture (BERT)** combined with **Explainable AI (XAI)**, providing not only state-of-the-art detection accuracy but also human-understandable explanations for **why** a review was flagged as fake or genuine.

---

## Objectives

- **Binary Classification:** Classify customer reviews into `Genuine` (0) or `Fake/Spam` (1).
- **Baseline Modeling:** Build a classic TF-IDF + Logistic Regression benchmark for comparison.
- **Transformer Fine-Tuning:** Fine-tune pre-trained `bert-base-uncased` on labeled review data using PyTorch.
- **Explainable AI (XAI):** Integrate SHAP and LIME to generate word-level feature importance visualizations for individual predictions.
- **Comprehensive Evaluation:** Compare models across Accuracy, Precision, Recall, F1-Score, and AUC-ROC curves.

---

## Tech Stack

| Category | Library / Tool | Purpose |
|----------|---------------|---------|
| **Core Language** | Python 3.10+ | Primary development language |
| **Deep Learning** | PyTorch & HuggingFace Transformers | BERT model fine-tuning & sequence classification |
| **Baseline ML** | Scikit-Learn | TF-IDF vectorization, Logistic Regression, evaluation metrics |
| **Explainable AI (XAI)** | SHAP & LIME | Local and global word importance explanations |
| **Data & EDA** | Pandas, NumPy, WordCloud | Preprocessing, feature extraction, N-grams |
| **Visualization** | Matplotlib, Seaborn | Confusion matrix plots, ROC curves, SHAP summary plots |

---

## Directory Structure

```
Fake_Review_Detection/
├── fake_review_detection.ipynb   ← Main Jupyter notebook (EDA, Models, XAI, Inference)
├── README.md                     ← Project documentation & results summary
├── requirements.txt              ← Dependencies
└── data/
    └── fake_reviews.csv          ← Benchmark dataset (text, label, rating, verification)
```

---

## Dataset Overview

The dataset contains 1,200 labeled reviews with balanced target classes:

- `review_id`: Unique identifier for each review.
- `text`: Raw review text.
- `label`: `0` for Genuine Review, `1` for Fake/Spam Review.
- `rating`: Customer rating (1 to 5 stars).
- `verified_purchase`: Binary indicator (1 = Verified Buyer, 0 = Unverified).

### Key EDA Insights

1. **Length Distribution:** Genuine reviews tend to be longer with specific descriptions of product features and minor drawbacks, whereas fake reviews show a bimodal length distribution (either short repetitive spam or exaggerated reviews).
2. **Word Clouds & Vocabulary:**
   - **Genuine Reviews:** Words like *battery, quality, design, setup, days, performance, price, minor, decent*.
   - **Fake Reviews:** Words like *best, buy now, 10/10, coupon, super, discount, click link, 5 stars, cheap, scam*.

---

## Model Architecture & Methodology

### 1. Baseline Model (TF-IDF + Logistic Regression)
- Text tokenized using `TfidfVectorizer` (unigrams + bigrams, top 5,000 features).
- Logistic Regression trained with L2 regularization.

### 2. Advanced Model (Fine-Tuned BERT)
- Base checkpoint: `bert-base-uncased`.
- Architecture: 12-layer Transformer encoder with sequence classification head.
- Tokenization: `BertTokenizer` with `max_length=128`, padding, and truncation.
- Training Setup: AdamW optimizer ($lr=2\times 10^{-5}$), linear warmup scheduler, trained for 3 epochs with gradient clipping.

---

## Explainable AI (XAI) Integration

### SHAP (SHapley Additive exPlanations)
- Quantifies exact game-theoretic Shapley values for each word's contribution toward shifting the model's output probability from baseline to predicted outcome.
- **Positive SHAP values** (pushing toward Fake): `"buy now"`, `"discount"`, `"coupon"`, `"10/10"`, `"fast ship"`.
- **Negative SHAP values** (pushing toward Genuine): `"battery"`, `"weeks"`, `"decent"`, `"however"`, `"packaging"`.

### LIME (Local Interpretable Model-agnostic Explanations)
- Fits local surrogate models around specific review samples.
- Highlights word importance weights dynamically in real-time inference.

---

## Experimental Results & Performance Comparison

| Model | Accuracy | Precision | Recall | F1-Score | AUC-ROC |
|-------|----------|-----------|--------|----------|---------|
| **TF-IDF + Logistic Regression** | 98.33% | 98.35% | 98.33% | 98.33% | 0.9995 |
| **Fine-Tuned BERT (`bert-base-uncased`)** | **99.58%** | **99.59%** | **99.58%** | **99.58%** | **1.0000** |

---

## How to Run

### 1. Clone the repository and navigate to the project directory
```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd ML-CaPsule/Fake_Review_Detection
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Jupyter Notebook
```bash
jupyter notebook fake_review_detection.ipynb
```

### 4. Real-Time Inference Example
You can test custom review strings directly in the notebook using the built-in `predict_and_explain(text)` pipeline:

```python
review = "BEST PRODUCT EVER WOW AMAZING DEAL BUY NOW 10/10 FIVE STARS!"
result = predict_and_explain(review)
# Output: Label: Fake/Spam | Confidence: 99.87% | Key Drivers: 'buy now', '10/10', 'amazing'
```

---

## Why This Project Stands Out

- **Production Relevant:** Solves a major real-world security and trust problem in e-commerce.
- **Interpretability First:** Moves beyond black-box classification by incorporating Explainable AI (XAI).
- **Comprehensive Benchmarking:** Compares traditional NLP baselines against state-of-the-art Transformer models.
- **Interview-Ready:** Well-documented modular codebase suitable for machine learning portfolios.

---

## License

Distributed under the MIT License. See `LICENSE` in the root repository for details.
