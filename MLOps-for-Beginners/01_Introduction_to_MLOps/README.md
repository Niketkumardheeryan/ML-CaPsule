# Introduction to MLOps

## What is MLOps?

MLOps stands for **Machine Learning Operations**.

It is a set of practices that combines Machine Learning, Software Engineering,
and DevOps to help teams build, deploy, and maintain ML systems reliably.

Think of it like this:

> Training a model is only 20% of the work.
> The other 80% is deploying it, keeping it running, and updating it over time.

## Why Does MLOps Exist?

Imagine you trained a model to predict house prices. It works great on your laptop.

But then:
- How do other people use it?
- What if the data changes next year?
- How do you know if it stops working correctly?
- How do you update it without breaking things?

MLOps answers all of these questions.

## Traditional ML vs MLOps

| Traditional ML | With MLOps |
|---------------|------------|
| Train model on laptop | Train in a reproducible pipeline |
| Share as a `.pkl` file | Deploy as an API |
| No monitoring | Monitor accuracy and data quality |
| Retrain manually | Automate retraining when needed |

## Key Roles

**Data Scientist** — Experiments with data, builds models.

**ML Engineer** — Deploys and optimises models for production.

**MLOps Engineer** — Manages the full pipeline: training, deployment,
monitoring, and automation.

## Real-World Example

You train a spam classifier. Without MLOps:
- You email the `.pkl` file to your team
- It breaks on Python 3.11 because you used 3.9
- Nobody knows when accuracy drops
- Retraining requires you personally each time

With MLOps:
- Model is served via an API anyone can call
- Versions are tracked automatically
- Accuracy is monitored daily
- Retraining runs automatically when drift is detected

## Summary

MLOps = making ML systems work reliably in the real world, not just on your laptop.

**Next:** [ML Lifecycle →](../02_ML_Lifecycle/README.md)
