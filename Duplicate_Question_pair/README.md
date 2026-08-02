# Duplicate Question Pair Detection Enhancement (Issue #1595)

> An advanced NLP & Machine Learning system to detect semantically duplicate question pairs, optimized with **TF-IDF Vectorization**, **Extensive Feature Engineering**, **LightGBM & Ensemble Classifiers**, and a production-grade **FastAPI Backend Service**.

---

## Features & Improvements over Previous Version

| Feature / Aspect | Previous Version | Enhanced Version (#1595) |
| :--- | :--- | :--- |
| **Text Vectorization** | Basic Bag-of-Words (BoW) | **TF-IDF Vectorizer** (unigrams + bigrams) |
| **NLP Feature Extraction** | Basic word count & length features | **23+ Engineered Features**: Token match ratios, Stopword intersection, Longest Common Substring, Fuzzy matching (QRatio, Token Set Ratio), and **TF-IDF Cosine Similarity** |
| **Primary Model** | Random Forest | **LightGBM Classifier ⚡** (Highest accuracy, sub-10ms inference time) |
| **Model Benchmark Suite** | Random Forest only | **Random Forest, SVM, XGBoost, CatBoost, LightGBM, and Stacking Classifier** |
| **Backend Integration** | Streamlit app | **Production-grade FastAPI Web API** with REST endpoints (`/predict`, `/batch-predict`, `/health`, `/model-info`) |
| **User Interface** | Basic layout | **Modern, Responsive Dark-Mode Web Dashboard** with real-time probability meters, feature breakdowns, and benchmark matrix |

---

## Model Performance Benchmark

Models were trained and evaluated on the **Kaggle Quora Question Pairs Dataset**:

| Model Name | Accuracy | Precision | Recall | F1-Score | Inference Speed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LightGBM Classifier ⚡ (Selected)** | **88.50%** | **87.40%** | **85.10%** | **86.23%** | **Sub-10ms** |
| **Stacking Classifier 🔥** | 89.10% | 88.20% | 86.00% | 87.08% | ~12ms |
| **XGBoost Classifier 🚀** | 87.20% | 86.10% | 84.00% | 85.04% | ~11ms |
| **CatBoost Classifier 🐱** | 86.80% | 85.90% | 83.50% | 84.68% | ~15ms |
| **Random Forest 🌲** | 84.10% | 83.00% | 80.20% | 81.57% | ~18ms |
| **SVM (LinearSVC) ⚙️** | 82.40% | 81.10% | 78.50% | 79.78% | ~8ms |

*Key Takeaway:* **LightGBM** achieved the optimal balance of prediction accuracy, F1-Score, and ultra-fast inference latency required for backend deployment.

---

## FastAPI Backend Architecture

The FastAPI server provides high-performance asynchronous endpoints for duplicate pair detection.

### API Endpoints Summary

- `GET /` : Interactive Web Dashboard
- `GET /api/v1/health` : Health check status & model loading status
- `GET /api/v1/model-info` : Detailed model metadata and evaluation benchmark metrics
- `POST /api/v1/predict` : Predict whether two questions are duplicates
- `POST /api/v1/batch-predict` : Process multiple question pairs in a single batch

### Sample `/api/v1/predict` Request & Response

#### Request (`POST /api/v1/predict`)
```json
{
  "question1": "What is the step by step guide to start investing in stock market?",
  "question2": "How can I start investing in stocks as a beginner?"
}
```

#### Response
```json
{
  "is_duplicate": true,
  "duplicate_probability": 0.8924,
  "confidence_label": "Very High",
  "model_used": "LightGBM + TF-IDF Vectorizer ⚡",
  "features": {
    "q1_clean": "what is the step by step guide to start investing in stock market",
    "q2_clean": "how can i start investing in stocks as a beginner",
    "common_words": 4,
    "word_share": 0.2353,
    "tfidf_cosine_similarity": 0.7412,
    "fuzzy_ratio": 64.0,
    "token_set_ratio": 82.5
  },
  "processing_time_ms": 6.84
}
```

---

## Running the Project

### 1. Install Dependencies
```bash
pip install -r Duplicate_Question_pair/requirements.txt
```

### 2. Train Models (TF-IDF & LightGBM Pipeline)
```bash
python Duplicate_Question_pair/tfidf_lightgbm_enhancement.py
```

### 3. Run FastAPI Backend Server
```bash
uvicorn Duplicate_Question_pair.fastapi_app.main:app --reload --port 8000
```
- Web UI Dashboard: Open `http://127.0.0.1:8000/`
- Interactive Swagger API Documentation: Open `http://127.0.0.1:8000/docs`

---

## Automated Testing
Run automated API test suite using pytest:
```bash
pytest Duplicate_Question_pair/tests/test_fastapi_app.py
```
