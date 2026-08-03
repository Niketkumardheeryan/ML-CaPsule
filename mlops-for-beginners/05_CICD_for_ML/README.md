# CI/CD for Machine Learning

## What is CI/CD?

**CI — Continuous Integration**
Every time you change your code, it is automatically tested.

**CD — Continuous Deployment**
If tests pass, the code (or model) is automatically deployed.

Together, they prevent broken code from reaching users.

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/fbd7e74f-5464-4507-8ef0-5ae9cf785d8b" />


## Why ML Needs CI/CD

Without CI/CD:
1. You train a model
2. You manually test it
3. You manually copy files to the server
4. Something breaks — you are not sure what

With CI/CD:
1. You push code to GitHub
2. Tests run automatically
3. If tests pass, model deploys automatically
4. If something breaks, it stops before reaching users

## Basic CI/CD Flow for ML

You push code to GitHub
│
▼
GitHub Actions runs automatically
│
▼
Run your tests
(does the model load? does the API respond?)
│
Pass?  Fail?
│        │
▼        ▼
Deploy   Stop here
(fix the bug first)

## Example: GitHub Actions

Create this file in your repo: `.github/workflows/ml-tests.yml`

```yaml
name: ML Model Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest tests/
```

Now every `git push` runs your tests automatically.

## What Should You Test?

```python
# tests/test_model.py
import pickle

def test_model_loads():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    assert model is not None

def test_model_predicts():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    result = model.predict([[5.1, 3.5, 1.4, 0.2]])
    assert len(result) == 1
```

These are basic checks. In production teams add many more.

## Summary

CI/CD for ML means your model pipeline runs automatically
with every code change — no manual steps, no surprises.

**Next:** [Monitoring & Retraining →](../06_Monitoring_and_Retraining/README.md)
