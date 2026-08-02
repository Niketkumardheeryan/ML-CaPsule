import pytest
from fastapi.testclient import TestClient
from Duplicate_Question_pair.fastapi_app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "primary_model" in data

def test_model_info_endpoint():
    response = client.get("/api/v1/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "benchmark_metrics" in data

def test_predict_duplicate_endpoint():
    payload = {
        "question1": "What is the step by step guide to start investing in stock market?",
        "question2": "How can I start investing in stocks as a beginner?"
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "is_duplicate" in data
    assert "duplicate_probability" in data
    assert "features" in data
    assert isinstance(data["is_duplicate"], bool)

def test_predict_non_duplicate_endpoint():
    payload = {
        "question1": "What is the capital city of France?",
        "question2": "How do I bake a chocolate cake at home?"
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "is_duplicate" in data
    assert data["is_duplicate"] is False

def test_batch_predict_endpoint():
    payload = {
        "pairs": [
            {
                "question1": "How do I learn Python programming quickly?",
                "question2": "What is the best way to master Python for beginners?"
            },
            {
                "question1": "Where is Mount Everest located?",
                "question2": "What is the highest mountain in the world?"
            }
        ]
    }
    response = client.post("/api/v1/batch-predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_pairs"] == 2
    assert len(data["predictions"]) == 2
