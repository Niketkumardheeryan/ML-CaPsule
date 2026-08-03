# Experiment Tracking

## The Problem

When you try different models, you probably do something like:

```python
# Try 1
model = RandomForestClassifier(n_estimators=100)
# accuracy: 0.87

# Try 2
model = RandomForestClassifier(n_estimators=200)
# accuracy: 0.89  <-- which one was this again?
```

After 20 experiments you cannot remember what worked and why.

## What is Experiment Tracking?

Experiment tracking automatically records:
- Which parameters you used
- What metrics you got
- Which model file was saved
- When the experiment ran

So you can compare, reproduce, and share your results.

## MLflow — Beginner Example

MLflow is the most popular tool for experiment tracking.

### Install

```bash
pip install mlflow
```

### Track an experiment

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2
)

with mlflow.start_run():
    n = 100
    model = RandomForestClassifier(n_estimators=n)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))

    mlflow.log_param("n_estimators", n)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")

    print(f"Accuracy: {acc}")
```

### View the dashboard

```bash
mlflow ui
```

Open `http://localhost:5000` to see all your experiments in a table.

## Key Concepts

**Parameters** — inputs to your model (learning rate, tree depth, etc.)

**Metrics** — outputs you measure (accuracy, loss, RMSE)

**Run** — one experiment attempt

**Reproducibility** — being able to re-run an experiment and get the same result

## Why This Matters in MLOps

In production, you need to know exactly which model version is running
and how to recreate it. Experiment tracking makes that possible.

**Next:** [CI/CD for ML →](../05_CICD_for_ML/README.md)
