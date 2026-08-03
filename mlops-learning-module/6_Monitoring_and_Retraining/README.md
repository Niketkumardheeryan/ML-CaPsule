# Monitoring and Retraining

## Why Monitor Models?

A model deployed today won't work perfectly tomorrow. Here's why:

```
Day 1: Spam detector accuracy = 97%
Day 30: Spam detector accuracy = 93% (degradation)
Day 90: Spam detector accuracy = 88% (severe drop)

Why?
- Spam techniques change
- User behavior changes
- Data patterns shift (data drift)
- Model loses relevance
```

## What is Data Drift?

Data drift occurs when the statistical properties of input data change over time.

### Example: Email Spam Patterns

**Before (Day 1):**
```
Common spam keywords: "Free", "Click", "Win", "Prize"
Email length: 200-500 characters
Sender: Unknown, suspicious domains
```

**After (Day 90):**
```
Common spam keywords: "Verify", "Confirm", "Urgent", "Action"
Email length: 50-150 characters (shorter phishing emails)
Sender: Looks legitimate
```

**Result:** Model trained on old patterns performs poorly on new data

## What to Monitor

### 1. Model Performance Metrics

```
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
```

### 2. Data Characteristics

```
- Input feature distributions
- Missing values
- Outliers
- Class distribution
- Data types
```

### 3. System Performance

```
- Prediction latency (how fast)
- Throughput (requests per second)
- Error rate
- Uptime
- Resource usage (CPU, memory)
```

### 4. User Impact

```
- Prediction feedback (user correction)
- Complaint rate
- False positive/negative impact
- Business metrics
```

## Monitoring Example: Spam Detector

```python
# Monitoring dashboard showing daily metrics

Date        | Accuracy | Precision | Recall | Data Drift | Action
2024-05-01  | 97%      | 96%       | 95%    | Normal     | ✓ Good
2024-05-08  | 96%      | 95%       | 94%    | Normal     | ✓ Good
2024-05-15  | 94%      | 93%       | 92%    | Low        | ⚠ Watch
2024-05-22  | 91%      | 89%       | 88%    | High       | 🔴 Alert!
2024-05-29  | 89%      | 87%       | 85%    | High       | 🔴 Action needed!
```

## Monitoring Tools

| Tool | Features | Best For |
|------|----------|----------|
| Prometheus | Metrics collection | Infrastructure |
| Grafana | Visualization | Dashboards |
| Datadog | APM & Monitoring | Full stack |
| CloudWatch | AWS native | AWS |
| Custom solution | Full control | ML-specific |

## Simple Monitoring Implementation

### Step 1: Collect Predictions

```python
import pandas as pd
from datetime import datetime

# Log predictions
prediction_log = {
    'timestamp': datetime.now(),
    'email_id': '12345',
    'prediction': 1,  # 1 = Spam, 0 = Ham
    'confidence': 0.95,
    'actual': 1,  # True label (when available)
    'features': ['length', 'keyword_count']
}

# Save to database or CSV
predictions_df = pd.DataFrame([prediction_log])
predictions_df.to_csv('predictions.csv', mode='a', header=False)
```

### Step 2: Calculate Metrics Daily

```python
def calculate_daily_metrics(predictions_df):
    """Calculate performance metrics"""
    
    # Get today's predictions
    today = predictions_df[predictions_df['timestamp'].dt.date == datetime.today().date()]
    
    if len(today) == 0:
        return None
    
    # Calculate metrics
    actual = today['actual']
    predicted = today['prediction']
    
    accuracy = (actual == predicted).sum() / len(actual)
    precision = ((predicted == 1) & (actual == 1)).sum() / (predicted == 1).sum()
    recall = ((predicted == 1) & (actual == 1)).sum() / (actual == 1).sum()
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'predictions_count': len(today)
    }
```

### Step 3: Check for Data Drift

```python
def detect_data_drift(current_data, historical_baseline):
    """Detect if input data distribution changed"""
    
    # Compare distributions
    for feature in current_data.columns:
        current_mean = current_data[feature].mean()
        baseline_mean = historical_baseline[feature].mean()
        
        # Calculate percentage change
        pct_change = abs(current_mean - baseline_mean) / baseline_mean
        
        if pct_change > 0.2:  # 20% change threshold
            print(f"Data drift detected in {feature}: {pct_change*100:.1f}% change")
            return True
    
    return False
```

### Step 4: Alert System

```python
def monitor_and_alert(metrics, drift_detected):
    """Alert if metrics drop or drift detected"""
    
    accuracy_threshold = 0.90  # 90% minimum
    
    if metrics['accuracy'] < accuracy_threshold:
        send_alert(f"Accuracy dropped to {metrics['accuracy']:.2%}")
        trigger_retraining()
    
    if drift_detected:
        send_alert("Data drift detected!")
        trigger_retraining()
    
    if metrics['predictions_count'] == 0:
        send_alert("No predictions today - model might be down!")

def send_alert(message):
    """Send alert to team"""
    print(f"ALERT: {message}")
    # Send email, Slack message, PagerDuty, etc.
```

## When to Retrain

### Automatic Retraining Triggers

| Trigger | Example |
|---------|---------|
| Accuracy drop | Accuracy < 90% |
| Data drift | Feature distribution changed > 20% |
| Time-based | Retrain monthly |
| Performance metric | F1-score < 0.85 |
| New data volume | Retrain after 10,000 new examples |

### Retraining Decision Logic

```python
def should_retrain(metrics, drift_detected):
    """Determine if model should be retrained"""
    
    # Condition 1: Accuracy too low
    if metrics['accuracy'] < 0.90:
        return True, "Accuracy below 90%"
    
    # Condition 2: Data drift detected
    if drift_detected:
        return True, "Data drift detected"
    
    # Condition 3: No recent retraining
    last_retrain = get_last_retrain_date()
    days_since = (datetime.now() - last_retrain).days
    if days_since > 30:
        return True, "Monthly retraining due"
    
    return False, "Model performing well"
```

## Retraining Pipeline

```
Monitor Performance
    ↓
Detect Issue (drift/accuracy drop)
    ↓
Trigger Retraining
    ↓
Collect new data
    ↓
Preprocess & Engineer Features
    ↓
Train new model
    ↓
Evaluate performance
    ↓
If better than current:
    ↓
Deploy new model
    ↓
Retire old model (keep as backup)
    ↓
Continue monitoring
```

## Automated Retraining Example

```python
def automated_retraining_pipeline():
    """Automated retraining workflow"""
    
    # 1. Collect recent data
    recent_data = collect_recent_data(days=7)
    
    # 2. Preprocess
    X, y = preprocess_data(recent_data)
    
    # 3. Train new model
    new_model = RandomForestClassifier(n_estimators=100)
    new_model.fit(X, y)
    
    # 4. Evaluate
    new_accuracy = new_model.score(X_test, y_test)
    current_accuracy = evaluate_current_model()
    
    # 5. Compare and deploy
    if new_accuracy > current_accuracy:
        # Backup current model
        backup_current_model()
        
        # Deploy new model
        deploy_model(new_model)
        
        # Log success
        log_retraining_success(new_accuracy)
    else:
        log_retraining_failure("New model not better")
```

## Monitoring Dashboard Metrics

```
Real-time Model Health Dashboard
=====================================

Model: Spam Detector v2.1
Status: HEALTHY ✓

Last 24 Hours:
- Predictions: 50,234
- Accuracy: 96.2%
- Precision: 95.8%
- Recall: 95.1%
- Avg latency: 45ms
- Error rate: 0.2%

Data Drift Status: NORMAL ✓

Recent Changes:
- Last retraining: 15 days ago
- Model version: v2.1 (deployed 2024-05-15)
- Accuracy trend: ↑ Improving
- Data drift: None detected

Alerts: None

Next Actions:
- Next scheduled retraining: 2024-05-29
```

## Real-World Example: Spam Detector Monitoring

```
Day 1-30: Model runs smoothly
- Accuracy steady at 97%
- All metrics normal
- No data drift

Day 31-60: Minor degradation
- Accuracy drops to 95%
- Alert triggered
- Investigation shows new spam patterns
- Decide to retrain

Day 61: Retraining triggered
- Collect new spam examples from last 30 days
- Retrain model with new data
- New model accuracy: 96.5%
- Deploy new model
- Old model kept as backup

Day 61+: Continue monitoring
- Accuracy back to 96%
- Monitor for further degradation
```

## Best Practices

1. **Monitor continuously** - Don't wait for disasters
2. **Set clear thresholds** - Define what "bad" looks like
3. **Automate retraining** - Don't do it manually
4. **Keep model backups** - Quick rollback if needed
5. **Version models** - Track which version is running
6. **Log everything** - Predictions, retraining events
7. **Alert appropriately** - Don't over-alert or under-alert

## Common Monitoring Mistakes

❌ Only monitoring accuracy
❌ Not tracking data drift
❌ Manual retraining process
❌ No model versioning
❌ No rollback plan
❌ Not logging predictions
❌ Ignoring latency/performance

## Key Takeaways

1. **Monitoring is ongoing** - Deploy is not the end
2. **Data drift is real** - Patterns change over time
3. **Automated alerts** - Catch issues early
4. **Automated retraining** - Keep models fresh
5. **Versioning** - Always know what's running
6. **Rollback capability** - Revert quickly if needed

## Monitoring Stack Summary

```
Production Model
        ↓
Capture Predictions
        ↓
Calculate Metrics Daily
        ↓
Check for Data Drift
        ↓
Compare to Thresholds
        ↓
If Issue Detected
        ↓
Trigger Retraining
        ↓
Evaluate New Model
        ↓
Deploy if Better
        ↓
Continue Monitoring
```

## Congratulations!

You've completed the MLOps Learning Module! You now understand:

✓ What MLOps is
✓ The complete ML lifecycle
✓ How to deploy models
✓ How to track experiments
✓ How to automate with CI/CD
✓ How to monitor and retrain

You're ready to build production ML systems!

---

See the Jupyter notebook for monitoring implementation examples!
