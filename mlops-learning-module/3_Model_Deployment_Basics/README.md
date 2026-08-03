# Model Deployment Basics

## What is Model Deployment?

Model deployment is the process of taking a trained machine learning model and making it available in a production environment where it can make predictions on new data.

## Before Deployment vs After Deployment

### Before Deployment
```
Your Computer
    ↓
Jupyter Notebook
    ↓
Only you can use the model
    ↓
Only when your computer is on
```

### After Deployment
```
Your Computer → Save Model → Server/Cloud → Users Can Access
    ↓
    Many users can use it simultaneously
    ↓
    Always available
    ↓
    Makes real-world impact
```

## Deployment Process Overview

```
Step 1: Save the trained model
        ↓
Step 2: Create a web service/API
        ↓
Step 3: Deploy to server/cloud
        ↓
Step 4: Expose to users
        ↓
Step 5: Monitor performance
```

## Step 1: Save the Model

### Why Save Models?
- Reuse without retraining
- Deploy to production
- Version control
- Backup and recovery

### Common Model Formats

| Format | Extension | Advantage | Disadvantage |
|--------|-----------|-----------|---------------|
| Pickle | .pkl | Easy Python serialization | Python specific |
| Joblib | .joblib | Efficient for large models | Python specific |
| SavedModel | folder | TensorFlow/Keras standard | Large file size |
| ONNX | .onnx | Framework independent | Conversion needed |
| H5 | .h5 | Keras models | Older format |

### Example: Save Model Using Pickle

```python
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save using pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Or save using joblib (preferred for large models)
joblib.dump(model, 'model.joblib')

# Load model later
loaded_model = joblib.load('model.joblib')
prediction = loaded_model.predict([[1, 2, 3, 4]])
```

## Step 2: Create a Web Service (API)

### What is an API?
API (Application Programming Interface) is a way for programs to communicate with each other.

### How It Works
```
User's App → HTTP Request → Our API → Model → Prediction → HTTP Response → User's App
```

### Popular Frameworks

| Framework | Complexity | Speed | Best For |
|-----------|-----------|-------|----------|
| Flask | Easy | Good | Learning, small projects |
| FastAPI | Easy | Excellent | Modern, production use |
| Django | Complex | Good | Large applications |
| Streamlit | Very Easy | Good | Interactive dashboards |

### Example: Flask API for Spam Detector

```python
from flask import Flask, request, jsonify
import joblib
import numpy as np

# Load saved model
model = joblib.load('spam_model.joblib')

# Create Flask app
app = Flask(__name__)

# Define API endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from request
    data = request.json
    email_features = data['features']  # List of features
    
    # Make prediction
    prediction = model.predict([email_features])
    
    # Return prediction
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Using the API

```bash
# Send request to API
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1, 0, 1, 2, 5]}'

# Response
{"prediction": 1}  # 1 = Spam, 0 = Ham
```

## Step 3: Containerization with Docker

### What is Docker?
Docker packages your application and all dependencies into a container that runs the same everywhere.

### Why Use Docker?
- Works on any computer (local, cloud, Linux, Windows)
- Easy deployment
- Reproducible environment
- Version control for environment

### Dockerfile Example

```dockerfile
# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY app.py .
COPY spam_model.joblib .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

### requirements.txt

```
flask==2.0.1
scikit-learn==0.24.2
joblib==1.0.1
numpy==1.21.0
```

## Step 4: Deploy to Cloud

### Deployment Options

| Platform | Ease | Cost | Best For |
|----------|------|------|----------|
| AWS EC2 | Medium | Pay per hour | General purpose |
| Heroku | Easy | Pay per dyno | Simple apps |
| Google Cloud | Medium | Pay per use | Google ecosystem |
| Azure | Medium | Pay per use | Microsoft ecosystem |
| Local Server | Easy | One-time cost | Small scale |

### Simple Heroku Deployment (Steps)

1. Create Procfile
2. Create app.json
3. Connect to GitHub
4. Deploy with one click

## Step 5: Monitor Performance

### What to Monitor
- **Availability:** Is the service running?
- **Latency:** How fast are predictions?
- **Accuracy:** Do predictions remain accurate?
- **Throughput:** How many requests per second?
- **Error Rate:** What percentage fail?

### Simple Monitoring

```python
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    
    try:
        # Make prediction
        prediction = model.predict([features])
        
        # Log success
        latency = time.time() - start_time
        logger.info(f"Prediction successful. Latency: {latency:.2f}s")
        
        return jsonify({'prediction': int(prediction[0])})
    
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        return jsonify({'error': str(e)}), 500
```

## Complete Deployment Workflow

```
1. Train and save model
        ↓
2. Create Flask/FastAPI app
        ↓
3. Test locally
        ↓
4. Create Docker container
        ↓
5. Deploy to cloud
        ↓
6. Set up monitoring
        ↓
7. Monitor and maintain
```

## Common Deployment Challenges

| Challenge | Solution |
|-----------|----------|
| Model too large | Use model compression, quantization |
| Slow predictions | Optimize code, use faster libraries |
| High latency | Add caching, use GPU |
| High cost | Optimize infrastructure, use auto-scaling |
| Model updates | Use blue-green deployment, canary releases |

## Real-World Example: Spam Detector Deployment

```
Local Testing
    ↓
    Save model as spam_model.joblib
    ↓
    Create Flask API (app.py)
    ↓
    Test API locally (http://localhost:5000)
    ↓
    Create Docker container
    ↓
    Push to Docker Hub
    ↓
    Deploy to AWS/Heroku
    ↓
    Expose API endpoint: https://spam-detector-api.com/predict
    ↓
    Users can now use it!
    ↓
    Monitor predictions and accuracy
```

## Key Takeaways

1. **Model saving** is the first step
2. **APIs** make models accessible
3. **Docker** ensures consistency
4. **Cloud deployment** makes it scalable
5. **Monitoring** ensures reliability

## Best Practices

- Keep models small for faster predictions
- Version your models and APIs
- Use infrastructure-as-code
- Implement comprehensive logging
- Set up alerts for failures
- Plan for rollbacks

## Next Steps

Ready to track your experiments? Check Section 4: Experiment Tracking!

---

See the Jupyter notebook for practical Flask API examples!
