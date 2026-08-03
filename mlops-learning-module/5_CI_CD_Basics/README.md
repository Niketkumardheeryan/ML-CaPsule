# CI/CD Basics for Machine Learning

## What is CI/CD?

**CI/CD** stands for **Continuous Integration / Continuous Deployment**.

- **Continuous Integration (CI):** Automatically test code when changes are made
- **Continuous Deployment (CD):** Automatically deploy code to production if tests pass

## Without CI/CD

```
Developer writes code
    ↓
Manually tests locally
    ↓
Manually merges with other code
    ↓
Tests break (merged code conflict)
    ↓
Manually debug and fix
    ↓
Manually deploy to production
    ↓
Something breaks in production
    ↓
Manual rollback and fix
```

## With CI/CD

```
Developer writes code
    ↓
Push to GitHub
    ↓
Automated tests run
    ↓
Code quality checks
    ↓
If all pass → Automatically deploy
    ↓
If fail → Notify developer
    ↓
Production updated automatically
```

## Benefits of CI/CD

✅ Catch bugs early
✅ Faster deployment
✅ Fewer manual errors
✅ Team collaboration
✅ Continuous feedback
✅ Faster feedback loop
✅ Frequent, small updates (safer than big updates)

## CI/CD Pipeline Stages

```
Code Push
    ↓
Stage 1: Build & Lint
    - Check code syntax
    - Check code style (PEP8)
    - Build application
    ↓
Stage 2: Unit Tests
    - Test individual functions
    - Test model predictions
    ↓
Stage 3: Integration Tests
    - Test components together
    - Test API endpoints
    ↓
Stage 4: Model Tests
    - Test model accuracy
    - Check for data drift
    ↓
Stage 5: Deploy
    - Deploy to production
    - Update API
    ↓
Stage 6: Monitor
    - Monitor performance
    - Alert on failures
```

## CI/CD Tools

| Tool | Platform | Best For |
|------|----------|----------|
| GitHub Actions | GitHub | Free, integrated |
| GitLab CI | GitLab | Comprehensive |
| Jenkins | On-premise | Flexible, complex |
| CircleCI | Cloud | Simple, fast |
| Travis CI | Cloud | Legacy |

## GitHub Actions: Simple Example

### Step 1: Create Workflow File

Create `.github/workflows/ml_pipeline.yml`:

```yaml
name: ML Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Lint code
        run: |
          pip install pylint
          pylint *.py
      
      - name: Run tests
        run: |
          pytest tests/
      
      - name: Train and test model
        run: |
          python train_model.py
          python test_model.py
```

### Step 2: What Happens

When you push code:
1. Workflow automatically starts
2. Sets up Python environment
3. Installs dependencies
4. Checks code quality
5. Runs tests
6. Trains and tests model
7. Sends report back to GitHub

## CI Tests for ML Models

### Test 1: Input Validation

```python
import pytest
from model import preprocess

def test_preprocess_invalid_input():
    """Test that invalid input raises error"""
    with pytest.raises(ValueError):
        preprocess(None)
    
    with pytest.raises(ValueError):
        preprocess([])

def test_preprocess_valid_input():
    """Test that valid input works"""
    result = preprocess(["Hello world"])
    assert len(result) > 0
```

### Test 2: Model Predictions

```python
def test_model_output_shape():
    """Test model output shape is correct"""
    model = load_model()
    predictions = model.predict(X_test)
    
    assert predictions.shape == (len(X_test),)

def test_model_prediction_range():
    """Test predictions are in valid range"""
    model = load_model()
    predictions = model.predict(X_test)
    
    assert all(0 <= p <= 1 for p in predictions)

def test_model_accuracy_threshold():
    """Test model accuracy is above threshold"""
    model = load_model()
    accuracy = model.score(X_test, y_test)
    
    assert accuracy > 0.90, f"Accuracy {accuracy} below 90%"
```

### Test 3: Data Validation

```python
def test_data_quality():
    """Test data has no missing values"""
    data = load_data()
    assert data.isnull().sum() == 0

def test_feature_existence():
    """Test all required features exist"""
    data = load_data()
    required_features = ['feature1', 'feature2', 'feature3']
    
    for feature in required_features:
        assert feature in data.columns

def test_class_distribution():
    """Test class distribution is reasonable"""
    data = load_data()
    class_ratio = data['label'].value_counts()
    
    # Ensure no extreme imbalance
    assert (class_ratio.max() / class_ratio.min()) < 10
```

## Complete CI/CD Workflow Example

### Repository Structure
```
project/
├── .github/
│   └── workflows/
│       └── ml_pipeline.yml
├── src/
│   ├── model.py
│   ├── preprocessing.py
│   └── train.py
├── tests/
│   ├── test_model.py
│   ├── test_preprocessing.py
│   └── test_accuracy.py
├── requirements.txt
└── README.md
```

### requirements.txt
```
scikit-learn==0.24.2
pandas==1.3.0
numpy==1.21.0
pytest==6.2.4
pylint==2.8.2
```

### GitHub Actions Workflow
```yaml
name: ML CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Lint with pylint
        run: |
          pylint src/ --fail-under=8.0
      
      - name: Run unit tests
        run: |
          pytest tests/test_preprocessing.py -v
      
      - name: Run model tests
        run: |
          pytest tests/test_model.py -v
      
      - name: Test accuracy threshold
        run: |
          pytest tests/test_accuracy.py -v
      
      - name: Train model
        run: |
          python src/train.py
      
      - name: Generate report
        run: |
          echo "All tests passed! Ready for deployment."
```

## Deployment in CI/CD

### Option 1: Deploy to Cloud

```yaml
deploy:
  runs-on: ubuntu-latest
  needs: build-and-test
  
  steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to AWS
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      run: |
        aws s3 cp model.pkl s3://my-bucket/models/
```

### Option 2: Deploy to Docker Hub

```yaml
- name: Build and push Docker image
  run: |
    docker build -t myrepo/ml-model:latest .
    docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }}
    docker push myrepo/ml-model:latest
```

## Real-World Example: Spam Detector CI/CD

```yaml
name: Spam Detector CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - run: pip install -r requirements.txt
      
      - name: Test input validation
        run: pytest tests/test_input.py
      
      - name: Test email preprocessing
        run: pytest tests/test_preprocessing.py
      
      - name: Test model predictions
        run: pytest tests/test_predictions.py
      
      - name: Verify accuracy > 95%
        run: pytest tests/test_accuracy.py
      
      - name: Train new model
        run: python train.py
      
      - name: Deploy if all pass
        run: python deploy.py
```

## Best Practices

1. **Run tests on every push** - Catch bugs immediately
2. **Keep tests fast** - Developers don't want to wait
3. **Test at multiple levels** - Unit, integration, model tests
4. **Version your models** - Track which model is in production
5. **Monitor after deployment** - Catch production issues early
6. **Use secrets for credentials** - Never hardcode API keys
7. **Document your pipeline** - Make it understandable

## Common CI/CD Failures

| Failure | Solution |
|---------|----------|
| Tests timeout | Optimize code, use parallel tests |
| Flaky tests | Fix non-deterministic tests |
| Missing dependencies | Update requirements.txt |
| Model accuracy drops | Investigate data changes |
| Deployment fails | Check cloud credentials |

## Key Takeaways

1. **CI/CD automates** testing and deployment
2. **GitHub Actions** is free for public repos
3. **Automated tests** catch bugs early
4. **Model tests** are essential
5. **Deployment is fast** with CI/CD
6. **Feedback is immediate** - developers know issues right away

## Next Steps

Ready to monitor your models in production? Check Section 6: Monitoring and Retraining!

---

See the Jupyter notebook for GitHub Actions examples!
