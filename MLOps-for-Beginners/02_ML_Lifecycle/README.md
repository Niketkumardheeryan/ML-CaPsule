# ML Lifecycle

## What is the ML Lifecycle?

The ML lifecycle is the full journey of a machine learning project —
from raw data to a model running in production and being maintained over time.

Most beginners only know steps 4 and 5. This module covers all 8.

<img width="732" height="167" alt="image" src="https://github.com/user-attachments/assets/3300bfdc-efce-44e6-b476-83e1801d1231" />


## The 8 Stages

### 1. Data Collection
Gather data from sources like databases, APIs, sensors, or user logs.

Good data = good model. Garbage in, garbage out.

### 2. Data Cleaning
Real-world data is messy. This step handles:
- Missing values
- Duplicate rows
- Wrong data types
- Outliers

### 3. Feature Engineering
Transform raw data into useful inputs for the model.

Examples:
- Scale numbers between 0 and 1
- Convert text to numbers
- Create a "day of week" column from a date

### 4. Model Training
Feed data into a learning algorithm so it can find patterns.

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)
```

### 5. Evaluation
Test how well the model performs on unseen data.

Common metrics:
- **Accuracy** — what % of predictions are correct
- **Precision/Recall** — important for imbalanced datasets
- **RMSE** — for regression problems

### 6. Deployment
Make the model available for real-world use — usually via an API.
User sends request → API receives it → Model predicts → Response returned

### 7. Monitoring
Watch the model in production to catch problems early.

Things to monitor:
- Is accuracy dropping?
- Is the input data changing?
- Are there slow responses?

### 8. Retraining
Over time, real-world data changes. The model needs to be updated.

Example: A fraud detection model trained in 2022 may not catch
fraud patterns from 2025.

## The Cycle
Data → Clean → Features → Train → Evaluate → Deploy → Monitor → Retrain → (repeat)

This is not a one-time process. It is a continuous loop.

**Next:** [Model Deployment →](../03_Model_Deployment/README.md)
