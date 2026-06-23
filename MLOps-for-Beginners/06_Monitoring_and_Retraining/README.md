# Monitoring and Retraining

## Why Monitor?

A model that works well today may fail silently next month.

Real-world data changes over time. Your model was trained on old data.
If nobody checks, users get wrong predictions without knowing it.

## What is Data Drift?

**Data drift** happens when the distribution of incoming data
changes compared to what the model was trained on.

Example:
- You trained a price prediction model on 2022 data
- In 2025, inflation changed all the prices
- The model's inputs look very different from what it learned

The model is not broken — the world changed.

## What is Concept Drift?

**Concept drift** happens when the relationship between
input and output changes over time.

Example:
- A spam filter learned that "free money" = spam in 2020
- Spammers now write differently to avoid detection
- Same words, different meaning for spam detection

## What to Monitor

| What | Why |
|------|-----|
| Prediction accuracy | Is the model still correct? |
| Input data distribution | Has the data changed? |
| Response latency | Is the API still fast? |
| Error rate | Are requests failing? |
| Feature statistics | Are averages/ranges shifting? |

## Simple Monitoring with Python

```python
import numpy as np

def check_drift(reference_data, new_data, threshold=0.1):
    ref_mean = np.mean(reference_data)
    new_mean = np.mean(new_data)

    shift = abs(ref_mean - new_mean) / (ref_mean + 1e-9)

    if shift > threshold:
        print(f"Warning: data drift detected! Shift = {shift:.2%}")
        return True
    return False

# Example
reference = [5.1, 4.9, 5.3, 5.0]   # training data average
production = [7.2, 7.8, 6.9, 7.5]  # current incoming data

check_drift(reference, production)
# Warning: data drift detected! Shift = 44.12%
```

## When to Retrain

Retrain your model when:
- Accuracy drops below a set threshold (e.g. below 85%)
- Drift is detected in input features
- New labelled data is available
- A scheduled time has passed (e.g. monthly)

## Retraining Loop

Monitor model in production
│
Drift detected?
Accuracy dropped?
│
▼
Collect new data
│
▼
Retrain model
│
▼
Evaluate new model
│
▼
Deploy if better
│
▼
Monitor again  ◄──── (loop continues)

## Popular Monitoring Tools

- **Evidently AI** — open source drift detection
- **Prometheus + Grafana** — infrastructure monitoring
- **WhyLogs** — lightweight data logging

You do not need all of these to start. Even a simple script
that checks accuracy daily is better than no monitoring at all.

## Summary

Monitoring is not optional in production ML. Models degrade.
Data changes. Retraining keeps your system useful over time.

---

**You have completed the MLOps for Beginners module.**

[← Back to overview](../README.md)
