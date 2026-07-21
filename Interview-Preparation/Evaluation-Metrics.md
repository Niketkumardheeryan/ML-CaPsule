# 📊 Evaluation Metrics Interview Questions

Evaluation metrics are quantitative measures used to assess the quality, performance, and generalizability of machine learning models. Choosing the correct evaluation metric is crucial because it aligns the model's objective with real-world business goals.

---

## 🔍 Core Concept Overview

- **Classification Metrics**: Accuracy, Precision, Recall (Sensitivity), Specificity, F1-Score, Confusion Matrix, ROC-AUC, Precision-Recall AUC (PR-AUC), Log Loss.
- **Regression Metrics**: Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), Mean Absolute Percentage Error (MAPE), R-squared ($R^2$), Adjusted R-squared.

---

## 🙋 Interview Questions & Answers

### Q1: What is a Confusion Matrix? Define TP, FP, TN, FN. (Easy)
**Answer**:
A Confusion Matrix is a tabular summary of the prediction results on a classification problem. It compares the actual target values with the values predicted by the model.

| | Predicted Positive | Predicted Negative |
| :--- | :--- | :--- |
| **Actual Positive** | **True Positive (TP)** | **False Negative (FN)** (Type II Error) |
| **Actual Negative** | **False Positive (FP)** (Type I Error) | **True Negative (TN)** |

Definitions:
- **True Positive (TP)**: Model predicted positive, and the actual label is positive.
- **True Negative (TN)**: Model predicted negative, and the actual label is negative.
- **False Positive (FP)**: Model predicted positive, but the actual label is negative (Type I Error).
- **False Negative (FN)**: Model predicted negative, but the actual label is positive (Type II Error).

---

### Q2: Explain Accuracy, Precision, and Recall. Give examples of when to prioritize each. (Easy)
**Answer**:
- **Accuracy**: The ratio of correct predictions to the total number of input samples.
  $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
- **Precision**: The proportion of predicted positive cases that were actually correct.
  $$\text{Precision} = \frac{TP}{TP + FP}$$
- **Recall (Sensitivity)**: The proportion of actual positive cases that were correctly identified.
  $$\text{Recall} = \frac{TP}{TP + FN}$$

**When to prioritize**:
- **Prioritize Precision (Minimize False Positives)**: When a false positive is highly costly or damaging.
  - *Example*: **Spam email detection**. If an email is predicted as spam (positive) but is actually an important job offer (negative), it is lost in the spam folder. We want high precision so that only true spam is flagged.
- **Prioritize Recall (Minimize False Negatives)**: When missing a positive instance is dangerous or life-threatening.
  - *Example*: **Cancer detection**. If a patient has cancer (positive) but the model predicts them as healthy (negative), they won't receive treatment. We want high recall to catch every potential positive case, even if it leads to some false alarms.

---

### Q3: What is the F1-Score, and why is it preferred over Accuracy for imbalanced datasets? (Easy)
**Answer**:
The F1-Score is the **harmonic mean of Precision and Recall**.

$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + Recall} = \frac{2TP}{2TP + FP + FN}$$

**Why it is preferred over Accuracy**:
If you have a dataset with $99\%$ negative samples and $1\%$ positive samples (e.g., credit card fraud), a naive model that predicts "No Fraud" for every single transaction will achieve $99\%$ Accuracy. However, its Precision and Recall for the "Fraud" class will be $0$.

The F1-Score for this naive model will be $0$, exposing its uselessness. The harmonic mean punishes extreme values (if either Precision or Recall is close to $0$, the F1-Score drops precipitously), making it a much more robust indicator of model performance on imbalanced data.

---

### Q4: Explain the ROC Curve and ROC-AUC score. How is the curve plotted? (Medium)
**Answer**:
- **ROC Curve (Receiver Operating Characteristic)**: A graphical plot that illustrates the diagnostic ability of a binary classifier system as its discrimination threshold is varied.
- **Plotted Axes**:
  - **Y-axis**: True Positive Rate (TPR) / Recall / Sensitivity:
    $$\text{TPR} = \frac{TP}{TP + FN}$$
  - **X-axis**: False Positive Rate (FPR) / (1 - Specificity):
    $$\text{FPR} = \frac{FP}{FP + TN}$$
- **ROC-AUC (Area Under the Curve)**: Measures the entire two-dimensional area underneath the entire ROC curve from $(0,0)$ to $(1,1)$.
  - **Interpretation**: ROC-AUC represents the probability that the model will rank a randomly chosen positive instance higher than a randomly chosen negative instance.
  - A perfect classifier has an AUC of $1.0$. A random classifier has an AUC of $0.5$.

---

### Q5: Compare ROC-AUC and Precision-Recall AUC (PR-AUC). When is PR-AUC preferred? (Medium)
**Answer**:
- **ROC-AUC**: Evaluates both TPR and FPR. Because FPR includes True Negatives (TN) in its denominator ($\frac{FP}{FP + TN}$), if the negative class is extremely large, a large change in the number of false positives (FP) will have a negligible impact on the FPR. Thus, ROC-AUC remains optimistically high even if the model performs poorly on positive instances.
- **PR-AUC**: Plots Precision vs. Recall (TPR). Neither metric uses True Negatives (TN). It focuses almost entirely on the positive class.

**When to prefer PR-AUC**:
Use PR-AUC when you have a **highly imbalanced dataset** (where the positive class is rare, e.g., anomaly detection, search engine relevance, click-through-rate prediction). In these cases, PR-AUC provides a much more realistic and strict assessment of model performance.

---

### Q6: Compare MSE, RMSE, and MAE. How do they react to outliers? (Medium)
**Answer**:
- **Mean Squared Error (MSE)**: The average of the squared differences between predictions and actual values.
  $$\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$
- **Root Mean Squared Error (RMSE)**: The square root of MSE, which brings the error metric back to the original units of the target variable.
  $$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2}$$
- **Mean Absolute Error (MAE)**: The average of the absolute differences between predictions and actual values.
  $$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i|$$

**Reaction to Outliers**:
- **MSE and RMSE** penalize larger errors much more severely than smaller errors because the errors are squared. A single large outlier can significantly inflate MSE/RMSE.
- **MAE** treats all errors linearly. The penalty for an error of size 10 is exactly twice the penalty for an error of size 5. Thus, MAE is **robust to outliers**.

---

### Q7: What is R-squared ($R^2$), and what are its limitations? (Medium)
**Answer**:
R-squared ($R^2$), also called the **Coefficient of Determination**, measures the proportion of variance in the dependent variable that is predictable from the independent variables.

$$R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$

Where $\text{SS}_{\text{res}}$ is the sum of squared residuals and $\text{SS}_{\text{tot}}$ is the total sum of squares (variance of the baseline mean model).

**Limitations**:
1. **Always increases with more variables**: Even if you add completely irrelevant random features to your regression model, $R^2$ will always increase or remain constant, never decrease. This encourages overfitting.
2. **Does not indicate model bias**: A high $R^2$ model can still be biased or poorly specified.

---

### Q8: What is Adjusted R-squared, and how does it solve the limitation of $R^2$? (Hard)
**Answer**:
Adjusted R-squared penalizes the model for adding features that do not improve its predictive power.

$$\text{Adjusted } R^2 = 1 - \left[ \frac{(1 - R^2)(N - 1)}{N - p - 1} \right]$$

Where:
- $N$ is the number of samples.
- $p$ is the number of predictors (features).

**How it works**:
As $p$ (number of features) increases, the term $N - p - 1$ in the denominator decreases, which increases the subtracted fraction, thereby decreasing the Adjusted $R^2$. If the added features do not improve $R^2$ enough to offset this penalty, the Adjusted $R^2$ will decrease.

---

### Q9: Can $R^2$ be negative? If yes, under what circumstances? (Hard)
**Answer**:
Yes, $R^2$ can be negative.
According to the formula:
$$R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$$

If the model's predictions are worse than the simple baseline model that always predicts the mean value ($\bar{y}$), then the sum of squared residuals $\text{SS}_{\text{res}}$ will be greater than the total sum of squares $\text{SS}_{\text{tot}}$. The fraction will be greater than $1$, yielding a negative $R^2$.

**When this happens**:
1. When the model is forced to fit without an intercept term (no constant bias parameter).
2. When the model severely overfits on the training data and performs terribly on test data.
3. When using a completely inappropriate model for the dataset structure.

---

### Q10: Explain the differences between Micro, Macro, and Weighted F1-Scores for multi-class classification. (Hard)
**Answer**:
When calculating F1-score for $K$ classes ($K > 2$), we get an F1-score for each class. To aggregate them:

1. **Macro F1-Score**:
   - Calculates the F1-score for each class independently and takes the simple arithmetic average.
   - Treats all classes equally, regardless of their size/frequency.
   - Useful when you care about performance on minority classes.
2. **Micro F1-Score**:
   - Calculates global True Positives (TP), False Positives (FP), and False Negatives (FN) by summing them across all classes, and then computes F1.
   - Note: In multi-class classification where every instance gets exactly one class, Micro F1-score equals global Accuracy.
3. **Weighted F1-Score**:
   - Calculates the F1-score for each class, then takes the average weighted by the number of support samples (frequency) in each class.
   - Accounts for class imbalance, but can mask poor performance on small minority classes.

---

## ⚠️ Common Mistakes in Interviews

1. **Confusing Type I and Type II errors**: Type I is False Positive (FP) (finding something when it is not there); Type II is False Negative (FN) (missing something that is there).
2. **Recommending Accuracy for Imbalanced Data**: Giving a generic answer that "Accuracy is the best metric" without checking class distribution.
3. **Stating that ROC-AUC is threshold-dependent**: ROC-AUC is threshold-independent because it measures performance across *all possible* classification thresholds.

---

## 📚 Additional Learning Resources

- **Articles**:
  - [Understanding ROC-AUC (Towards Data Science)](https://towardsdatascience.com/understanding-auc-roc-curve-68b2303cc9c5)
- **Documentation**:
  - [scikit-learn Model Evaluation Guide](https://scikit-learn.org/stable/modules/model_evaluation.html)
