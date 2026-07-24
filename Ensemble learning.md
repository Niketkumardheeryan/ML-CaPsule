# Ensemble Learning

Ensemble Learning is a machine learning technique that combines the predictions of multiple models to produce better performance than a single model. It helps improve accuracy, reduce overfitting, and build more robust predictive systems.

## Types of Ensemble Learning

### 1. Bagging (Bootstrap Aggregation)

Bagging, short for **Bootstrap Aggregation**, is a powerful ensemble technique that reduces the variance of high-variance models such as Decision Trees.

It works by:
- Creating multiple bootstrap samples (random samples with replacement) from the training dataset.
- Training a separate model on each sample.
- Combining the predictions of all models through voting (classification) or averaging (regression).

#### Advantages

- Reduces overfitting
- Improves model stability
- Works well with high-variance algorithms

#### Common Algorithm

- Random Forest

## 2. Boosting

Boosting is an ensemble technique that builds models sequentially. Each new model attempts to correct the errors made by the previous models, resulting in a stronger overall predictor.

Unlike Bagging, Boosting focuses more on difficult-to-predict samples.

#### Popular Boosting Algorithms

- AdaBoost (Adaptive Boosting)
- Gradient Boosting
- XGBoost (Extreme Gradient Boosting)

## Additional Learning Resources

### AdaBoost & Gradient Boosting

Learn more about AdaBoost and Gradient Boosting:

https://www.analyticsvidhya.com/blog/2015/11/quick-introduction-boosting-algorithms-machine-learning/

### XGBoost

Learn more about XGBoost and the mathematics behind it:

https://www.analyticsvidhya.com/blog/2018/09/an-end-to-end-guide-to-understand-the-math-behind-xgboost/

## Summary

| Technique | Strategy | Example Algorithms |
|-----------|----------|--------------------|
| Bagging | Train multiple models independently and combine predictions | Random Forest |
| Boosting | Train models sequentially, correcting previous errors | AdaBoost, Gradient Boosting, XGBoost |

Ensemble Learning is widely used in real-world machine learning applications because it often delivers higher accuracy and better generalization than individual models.
