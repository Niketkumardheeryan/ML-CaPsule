# Experiment Tracking

## What is Experiment Tracking?

Experiment tracking is the practice of recording and organizing information about machine learning experiments to understand which models and parameters work best.

## The Problem Without Experiment Tracking

Imagine you train 50 different models:

```
model_final.pkl
model_final_v2.pkl
model_final_v3_REAL.pkl
model_final_v3_REAL_fixed.pkl
model_final_v3_REALLY_FINAL.pkl
...
```

**Questions you can't answer:**
- Which model had the best accuracy?
- What parameters did model_v3 use?
- When was model trained?
- What dataset was used?
- Did adding this feature help?

## Benefits of Experiment Tracking

✅ Organize and compare experiments
✅ Track parameters, metrics, and artifacts
✅ Reproduce results
✅ Collaborate with team members
✅ Make data-driven decisions
✅ Prevent duplicate work

## What to Track

### 1. Parameters (Inputs)
```
Algorithm: Random Forest
Number of trees: 100
Max depth: 15
Min samples split: 2
Random state: 42
```

### 2. Metrics (Outputs)
```
Accuracy: 0.96
Precision: 0.95
Recall: 0.94
F1-Score: 0.945
Training time: 45.2 seconds
```

### 3. Artifacts (Files)
```
- Trained model: model.pkl
- Feature importance plot: feature_importance.png
- Confusion matrix: confusion_matrix.png
- Training logs: training.log
```

### 4. Metadata (Context)
```
Dataset: spam_dataset_v2.csv
Dataset size: 100,000 emails
Train/Test split: 80/20
Date: 2024-05-18
Author: Aryan
Dataset version: v2
```

## Experiment Tracking Tools

| Tool | Ease | Features | Best For |
|------|------|----------|----------|
| MLflow | Easy | Tracking, Registry, Serving | General ML |
| Weights & Biases | Easy | Tracking, Visualization | Research |
| Neptune | Medium | Collaboration, Monitoring | Teams |
| Comet ML | Medium | Optimization, Monitoring | Production |
| TensorBoard | Easy | Deep Learning Visualization | TensorFlow/PyTorch |

## MLflow: Simple Example

### 1. Install MLflow

```bash
pip install mlflow
```

### 2. Track Experiment

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Start MLflow run
with mlflow.start_run():
    
    # Log parameters
    mlflow.log_param("algorithm", "Random Forest")
    mlflow.log_param("n_trees", 100)
    mlflow.log_param("max_depth", 15)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=15)
    model.fit(X_train, y_train)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    
    # Log model
    mlflow.sklearn.log_model(model, "spam_detector")
    
    # Log artifact
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot([1, 2, 3, 4])
    plt.savefig('plot.png')
    mlflow.log_artifact('plot.png')

print("Experiment tracked!")
```

### 3. View Experiments

```bash
mlflow ui
# Open http://localhost:5000
```

## Experiment Comparison Example

### Experiment 1: Random Forest
```
Parameters:
- Algorithm: Random Forest
- Trees: 50
- Depth: 10

Metrics:
- Accuracy: 0.94
- Precision: 0.92
- Recall: 0.91
```

### Experiment 2: Random Forest (Improved)
```
Parameters:
- Algorithm: Random Forest
- Trees: 100
- Depth: 15

Metrics:
- Accuracy: 0.96  ✅ Better
- Precision: 0.95  ✅ Better
- Recall: 0.94  ✅ Better
```

### Experiment 3: Gradient Boosting
```
Parameters:
- Algorithm: Gradient Boosting
- Learning rate: 0.1
- Trees: 100

Metrics:
- Accuracy: 0.97  ✅ Best
- Precision: 0.96  ✅ Best
- Recall: 0.95  ✅ Best
```

**Decision:** Use Gradient Boosting (best performance)

## Best Practices

### 1. Be Descriptive
```python
# BAD
mlflow.log_param("param1", 100)

# GOOD
mlflow.log_param("n_estimators", 100)
mlflow.log_param("algorithm_name", "Random Forest")
```

### 2. Log Everything
```python
# Log all relevant info
mlflow.log_param("dataset", "spam_emails_v2")
mlflow.log_param("preprocessing", "text_cleaned_stemmed")
mlflow.log_param("feature_engineering", "tfidf_bigrams")
mlflow.log_param("train_test_split", 0.8)
```

### 3. Use Tags for Organization
```python
mlflow.set_tag("project", "spam_detection")
mlflow.set_tag("team", "data_science")
mlflow.set_tag("environment", "development")
```

### 4. Log Visualizations
```python
# Confusion matrix
plt.figure()
sns.heatmap(confusion_matrix(y_test, predictions))
plt.savefig('confusion_matrix.png')
mlflow.log_artifact('confusion_matrix.png')

# Feature importance
plt.figure()
plt.barh(feature_names, model.feature_importances_)
plt.savefig('feature_importance.png')
mlflow.log_artifact('feature_importance.png')
```

## Experiment Tracking Workflow

```
Train Model 1
    ↓
Log parameters, metrics, artifacts
    ↓
Train Model 2
    ↓
Log parameters, metrics, artifacts
    ↓
Train Model 3
    ↓
Log parameters, metrics, artifacts
    ↓
Compare all experiments
    ↓
Choose best model
    ↓
Deploy best model
```

## Real-World Example: Spam Detection Experiments

```
Experiment 1: Baseline
- Algorithm: Logistic Regression
- Features: Email length, keyword count
- Accuracy: 0.92

Experiment 2: Better Features
- Algorithm: Logistic Regression
- Features: TF-IDF vectors
- Accuracy: 0.94

Experiment 3: Better Algorithm
- Algorithm: Random Forest
- Features: TF-IDF vectors
- Accuracy: 0.96

Experiment 4: Ensemble
- Algorithm: Gradient Boosting
- Features: TF-IDF vectors
- Accuracy: 0.97

Experiment 5: Hyperparameter Tuning
- Algorithm: Gradient Boosting
- Features: TF-IDF vectors
- Learning rate: 0.05
- Accuracy: 0.975 ✅ Best
```

## Common Experiment Tracking Patterns

### Pattern 1: Grid Search Tracking
```python
for n_trees in [50, 100, 150, 200]:
    for max_depth in [10, 15, 20]:
        with mlflow.start_run():
            mlflow.log_param("n_trees", n_trees)
            mlflow.log_param("max_depth", max_depth)
            
            model = RandomForestClassifier(
                n_estimators=n_trees,
                max_depth=max_depth
            )
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)
            
            mlflow.log_metric("accuracy", accuracy)
```

### Pattern 2: Feature Engineering Tracking
```python
features_list = [
    ["email_length"],
    ["email_length", "keyword_count"],
    ["email_length", "keyword_count", "sender_reputation"],
]

for features in features_list:
    with mlflow.start_run():
        mlflow.log_param("features", ",".join(features))
        
        X_subset = X[features]
        model.fit(X_subset, y)
        
        mlflow.log_metric("accuracy", model.score(X_test[features], y_test))
```

## Key Takeaways

1. **Experiment tracking** prevents chaos
2. **MLflow** is a great free tool
3. **Compare experiments** to find best model
4. **Log everything** - parameters, metrics, artifacts
5. **Organize with tags** - easier to find experiments
6. **Reproducibility** - track exactly what worked

## Common Mistakes

❌ Not logging parameters
❌ Not versioning datasets
❌ Unclear experiment names
❌ Not saving artifacts
❌ Comparing experiments without full context
❌ Not tracking data preprocessing steps

## Next Steps

Ready to automate ML workflows? Check Section 5: CI/CD Basics!

---

See the Jupyter notebook for MLflow practical examples!
