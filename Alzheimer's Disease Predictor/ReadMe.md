# Alzheimer's Disease Predictor – Data Leakage & Model Optimization Fix

## Overview

This contribution fixes a major train-test data leakage issue in the Alzheimer’s Disease Predictor pipeline and improves the CNN architecture for better generalization and faster training.

The original implementation trained the model using unsplit dataset variables before evaluation, resulting in unrealistic performance and overfitting.

This fix introduces:
- Proper dataset splitting
- Safer validation workflow
- Reduced model complexity
- Better reproducibility
- Improved training efficiency

---

## Problem Identified

The notebook previously used:

```python
model.fit(train_feature, train_target)
```

before ensuring proper separation between training and testing data.

This caused:
- Data leakage
- Inflated accuracy
- Poor real-world generalization
- Overfitting
- Unreliable validation results

---

## Fixes Implemented

### 1. Proper Train-Test Split

Implemented:

```python
train_test_split()
```

with:
- random_state
- stratified splitting
- isolated validation data

---

### 2. Leakage-Free Training

Model now trains only on:

```python
X_train, y_train
```

and validates using:

```python
X_test, y_test
```

---

### 3. CNN Optimization

Reduced model complexity by:
- lowering convolution filter sizes
- reducing dense layer size
- simplifying architecture
- improving training speed

---

### 4. Improved Reproducibility

Added:
- fixed random state
- structured preprocessing
- cleaner workflow

---

## Updated Model Architecture

- Conv2D
- MaxPooling2D
- Conv2D
- MaxPooling2D
- Flatten
- Dense
- Dropout
- Softmax Output

---

## Technologies Used

- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Matplotlib
- Scikit-learn

---

## Results

### Improvements Achieved

- Eliminated train-test leakage
- Reduced overfitting
- Faster model training
- Cleaner evaluation workflow
- Better maintainability

---

## Project Structure

```text
Alzheimer's Disease Predictor/
│
├── Alzheimer_Disease_predictor.ipynb
├── ReadMe.md
├── Images/
├── Alzheimers-ADNI/
```

---

## Future Improvements

- Data augmentation
- Early stopping
- Transfer learning
- Model checkpointing
- Hyperparameter tuning

---

## Contributor

Shreya Mahajan  
GitHub: https://github.com/shreya975