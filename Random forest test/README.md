# Random Forest Test

## Introduction
Random Forest is a supervised ensemble learning algorithm used for both classification and regression.
It combines multiple decision trees and improves performance by reducing overfitting through bagging.

## How It Works
1. Select random samples from the dataset using bootstrap sampling
2. Build a decision tree for each sample
3. Collect predictions from all trees
4. Use majority vote for classification or the mean for regression

## Key Points
- Random Forest Classifier returns the majority vote
- Random Forest Regressor returns the average prediction
- The model is built from multiple decision trees

## Notes
- Random Forest is useful when you want a strong baseline model with good generalization.
- It works well for both structured classification and regression tasks.
