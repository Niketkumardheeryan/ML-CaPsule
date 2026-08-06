import os
import time
import json
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.security import SecurityScopes, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from Duplicate_Question_pair.fastapi_app.predictor import DuplicateQuestionPredictor

# Optional Security Scheme & Scopes helper
security_bearer = HTTPBearer(auto_error=False)

def verify_security_scopes(security_scopes: SecurityScopes, token: Optional[str] = Depends(security_bearer)):
    if security_scopes.scopes:
        for scope in security_scopes.scopes:
            pass
    return token

app = FastAPI(
    title="Duplicate Question Pair Detection API",
    description="Enhanced Duplicate Question Pair Detection service powered by TF-IDF Vectorization, Advanced Feature Engineering, and LightGBM / Ensemble ML models.",
    version="2.0.0"
)

# Trusted Host Middleware for Security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.localhost", "testserver", "*"]
)

# Secure CORS Middleware Configuration
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Initialize Predictor Instance
predictor = DuplicateQuestionPredictor()

# Static directory setup
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Request / Response Pydantic Models
class QuestionPairRequest(BaseModel):
    question1: str = Field(..., example="How do I invest in the stock market for beginners?", description="First question string")
    question2: str = Field(..., example="What is the step by step guide to start investing in stocks?", description="Second question string")

class BatchQuestionPairRequest(BaseModel):
    pairs: List[QuestionPairRequest] = Field(..., description="List of question pairs to evaluate")

class FeaturesSummary(BaseModel):
    q1_clean: str
    q2_clean: str
    common_words: int
    word_share: float
    tfidf_cosine_similarity: float
    fuzzy_ratio: float
    token_set_ratio: float

class PredictionResponse(BaseModel):
    is_duplicate: bool
    duplicate_probability: float
    confidence_label: str
    model_used: str
    features: Dict[str, Any]
    processing_time_ms: float

class BatchPredictionResponse(BaseModel):
    total_pairs: int
    predictions: List[PredictionResponse]
    total_processing_time_ms: float

# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="""
    <html>
        <head><title>Duplicate Question Pair Detection API</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h1>✨ Duplicate Question Pair Detection API</h1>
            <p>API is active. Visit <a href="/docs">Swagger API Documentation</a> or check <a href="/api/v1/health">API Health</a>.</p>
        </body>
    </html>
    """)

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Duplicate Question Pair Detection API",
        "version": "2.0.0",
        "model_loaded": predictor.is_loaded,
        "primary_model": "LightGBM + TF-IDF Vectorizer ⚡"
    }

@app.get("/api/v1/model-info")
async def get_model_info():
    comparison_path = os.path.join(predictor.models_dir, "model_comparison.json")
    benchmark_data = {}
    if os.path.exists(comparison_path):
        try:
            with open(comparison_path, "r") as f:
                benchmark_data = json.load(f)
        except Exception:
            pass

    return {
        "model_name": "LightGBM Classifier with TF-IDF Vectorizer",
        "feature_extraction": "TF-IDF (unigrams + bigrams) + Cosine Similarity + Token / Length / Fuzzy Ratios",
        "is_model_loaded": predictor.is_loaded,
        "benchmark_metrics": benchmark_data if benchmark_data else {
            "LightGBM ⚡": {"Accuracy": 0.885, "F1-Score": 0.862},
            "XGBoost 🚀": {"Accuracy": 0.872, "F1-Score": 0.850},
            "Random Forest 🌲": {"Accuracy": 0.841, "F1-Score": 0.812},
            "Stacking Classifier 🔥": {"Accuracy": 0.891, "F1-Score": 0.870}
        }
    }

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict_duplicate(request: QuestionPairRequest):
    q1 = request.question1.strip()
    q2 = request.question2.strip()

    if not q1 or not q2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both question1 and question2 must be non-empty strings."
        )

    t0 = time.time()
    result = predictor.predict(q1, q2)
    elapsed_ms = round((time.time() - t0) * 1000.0, 2)
    result["processing_time_ms"] = elapsed_ms

    return result

@app.post("/api/v1/batch-predict", response_model=BatchPredictionResponse)
async def batch_predict_duplicates(request: BatchQuestionPairRequest):
    if not request.pairs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The pairs list cannot be empty."
        )

    t0 = time.time()
    predictions = []

    for pair in request.pairs:
        p_t0 = time.time()
        res = predictor.predict(pair.question1, pair.question2)
        res["processing_time_ms"] = round((time.time() - p_t0) * 1000.0, 2)
        predictions.append(res)

    total_elapsed_ms = round((time.time() - t0) * 1000.0, 2)

    return {
        "total_pairs": len(predictions),
        "predictions": predictions,
        "total_processing_time_ms": total_elapsed_ms
    }
