# Fake Review Detection using BERT and Explainable AI (XAI)

This project provides an end-to-end Machine Learning pipeline to detect whether online reviews are **Genuine (Truthful)** or **Fake/Spam (Deceptive)**. We use a gold-standard dataset, establish a strong baseline using **TF-IDF + Logistic Regression**, fine-tune a state-of-the-art **BERT (bert-base-uncased)** classifier, and integrate Explainable AI (**LIME** and **SHAP**) to make predictions fully interpretable.

---

## 📌 Project Overview

Online reviews are a key factor in e-commerce decision-making, which makes them prime targets for deception (e.g., promotional spam, fake negative reviews). Detecting fake reviews is challenging because deceptive reviews are often written to mimic genuine ones. 

This project aims to:
- Perform detailed Exploratory Data Analysis (EDA) on deceptive review patterns.
- Train and evaluate a fast Logistic Regression model.
- Fine-tune a deep contextual BERT model.
- Apply LIME and SHAP to explain exactly *which words* or *phrases* drove the model's predictions, addressing the black-box nature of deep neural networks.

---

## 📂 Project Structure

```directory
Fake_Review_Detection_BERT_XAI/
├── requirements.txt             # Python dependencies
├── README.md                    # Detailed documentation and walkthrough
└── fake_review_detection.ipynb  # End-to-end Jupyter Notebook (EDA, training, evaluation, XAI)
```

---

## 📊 Dataset Details

We use the **Deceptive Opinion Spam Corpus** (Ott et al.), a widely accepted NLP benchmark dataset.

- **Dataset Link:** [deceptive-opinion.csv (GitHub - shubham5351)](https://raw.githubusercontent.com/shubham5351/Fake-Review-Detection-/master/deceptive-opinion.csv)
- **Original Paper:** [Ott et al., 2011 — Finding Deceptive Opinion Spam by Any Stretch of the Imagination](https://aclanthology.org/P11-1032/)
- **Size:** 1,600 reviews.
- **Labels:** 
  - `truthful` (800 reviews from TripAdvisor) - mapped to `0`
  - `deceptive` (800 reviews generated via Mechanical Turk) - mapped to `1`
- **Balanced Class Distribution:** 50% Genuine, 50% Fake.
- **Data Columns:**
  - `deceptive`: Target category (`truthful` / `deceptive`).
  - `hotel`: The hotel name (20 Chicago hotels represented).
  - `polarity`: Sentiment direction (`positive` / `negative`).
  - `source`: Platform source (`TripAdvisor` / `MTurk` / `Web`).
  - `text`: Raw review text.

---

## ⚙️ Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.7+ installed. We recommend setting up a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate it (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies
Install all required libraries via pip:

```bash
pip install -r requirements.txt
```

### 3. Open the Notebook
Launch Jupyter Notebook or JupyterLab to run the interactive pipeline:

```bash
jupyter notebook fake_review_detection.ipynb
```

---

## 🧪 Methodology

### 1. Exploratory Data Analysis (EDA)
- **Review Length:** Analyzing character/word counts reveals that deceptive reviews tend to have a slightly tighter length distribution (since crowd workers were instructed to write ~150 words).
- **Word Frequencies:** Using custom tokenization and filtering stop words, we discover semantic differences. Truthful reviews often mention concrete nouns like spatial features (e.g., `bathroom`, `location`, `price`, specific locations), while deceptive reviews focus on generic praise, exaggerations (e.g., `wonderful`, `amazing`, `husband`, `vacation`), and subjective adjectives.

### 2. Baseline Model (TF-IDF + Logistic Regression)
- **Features:** Text representation using TF-IDF (Term Frequency-Inverse Document Frequency) extracting unigrams and bigrams, limited to the top 5,000 features.
- **Classifier:** Logistic Regression with L2 regularization. It establishes a strong baseline with fast training and low hardware requirements.

### 3. Main Model (BERT Fine-Tuning)
- **Architecture:** We load `BertForSequenceClassification` based on the pre-trained `bert-base-uncased` checkpoints.
- **Hyperparameters:**
  - Max Sequence Length: `128` (captures the core context of reviews)
  - Optimizer: `AdamW` (learning rate = `2e-5`)
  - Batch Size: `16`
  - Epochs: `3`
  - Scheduler: Linear decay scheduler with a warmup phase (10% of total steps)
- **Loss Function:** Cross-Entropy Loss.

### 4. Explainable AI (XAI)
- **LIME (Local Interpretable Model-agnostic Explanations):** Used for local, instance-level explanations of individual predictions. LIME perturbs the review text by removing words and checking how the model's confidence shifts. It returns feature weights highlighting exactly which words supported the prediction (green/deceptive vs. blue/truthful).
- **SHAP (SHapley Additive exPlanations):** Computes Shapley values for the words. We use SHAP's linear explainer on the baseline and a pipeline-based SHAP text explainer on the fine-tuned BERT model, ensuring global and local features are visualizable.

---

## 📈 Model Performance & Comparison

Typical performance comparison on the test split (20% of the dataset):

| Metric | TF-IDF + Logistic Regression | Fine-Tuned BERT |
| :--- | :---: | :---: |
| **Accuracy** | ~86.0% - 88.0% | **~93.0% - 95.0%** |
| **Precision** | ~85.0% - 87.0% | **~92.0% - 94.0%** |
| **Recall** | ~87.0% - 89.0% | **~93.0% - 95.0%** |
| **F1-Score** | ~86.0% - 88.0% | **~93.0% - 95.0%** |
| **ROC-AUC** | ~94.0% - 95.0% | **~98.0% - 99.0%** |

### Key Takeaways
1. **Context Matters:** Logistic Regression relies on single words and word pairs (bag-of-words), which misses context. BERT's multi-head self-attention mechanism models context-dependent relationships (e.g., negation, sentence-level mood), explaining its ~7% performance gain.
2. **Robustness:** BERT yields significantly fewer false positives and false negatives, as shown by its ROC-AUC curve approaching near-perfection (0.98+).

---

## 🔍 Visualizing Predictions with Explainable AI

Through LIME and SHAP, we can demystify the models' choices. Below are typical patterns found:

### Genuine Review Explanation
When explaining a truthful review, LIME highlights terms associated with logistics, hotel brands, and direct observations:
- **Contributing Words:** `chicago`, `stayed`, `husband`, `bed`, `clean`, `location`, `price`.
- **Reasoning:** Truthful reviews mention specific activities (e.g., `walking`, `breakfast voucher`, `wrigley bldg`) rather than generic luxury descriptors.

### Deceptive Review Explanation
For fake reviews, the XAI tools show that superlatives, generic pronouns, and overly subjective words carry high deceptive weights:
- **Contributing Words:** `amazing`, `wonderful`, `luxury`, `stay`, `perfect`, `hotel`.
- **Reasoning:** Deceptive writers rely on abstract praise and exaggerations because they have not actually visited the hotels, causing them to repeat standard travel verbs and generic positive adjectives.

---

## 🎓 Conclusion
This repository demonstrates that combining BERT with XAI tools gives developers the best of both worlds: high-performance text classification and human-interpretable explanations. Such interpretability is crucial for spam monitoring systems where admins need to justify *why* a review was automatically flagged or deleted.
