# Model Deployment

## What is Deployment?

Deployment means making your trained model available so that
other people or systems can use it — not just you on your laptop.

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/a44a8233-dc18-4e88-b8a5-8f348b89f5ec" />


## Why APIs?

An API (Application Programming Interface) lets any program
send data to your model and receive a prediction back.

Mobile App ──► API ──► Your Model ──► Prediction ──► Mobile App

This way, your model works on any device, in any language.

## Batch vs Real-Time Inference

| Batch | Real-Time |
|-------|-----------|
| Process many inputs at once | Process one input immediately |
| Run overnight | Run within milliseconds |
| Example: daily email spam scan | Example: fraud detection on card swipe |

## Simple Deployment with FastAPI

FastAPI is a Python library that makes it easy to create an API.

### Step 1 — Train and save the model

```python
import pickle
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

data = load_iris()
model = RandomForestClassifier()
model.fit(data.data, data.target)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
```

### Step 2 — Create the API

```python
# app.py
from fastapi import FastAPI
import pickle
import numpy as np

app = FastAPI()

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
def predict(features: list):
    prediction = model.predict([features])
    return {"prediction": int(prediction[0])}
```

### Step 3 — Run it

```bash
pip install fastapi uvicorn
uvicorn app:app --reload
```

### Step 4 — Call it

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Response:
```json
{"prediction": 0}
```

That is a deployed ML model — live and callable by anyone.

## What About Docker?

Docker packages your app and all its dependencies into a container,
so it runs the same way on any computer or cloud server.

Beginner summary: think of Docker as a shipping container for your code.

**Next:** [Experiment Tracking →](../04_Experiment_Tracking/README.md)

## Practical Example

This repository also includes beginner-friendly MLOps project examples and deployment workflows.

Reference Project:
- Post Mortem Intelligence
- https://github.com/Sampada-23-00/Post-Mortem-Intelligence
