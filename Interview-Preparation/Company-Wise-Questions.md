# 🏢 Company-Wise & Case Study Interview Questions

This section covers real-world scenario-based (ML System Design) questions, frequently asked interview coding problems (implementing ML concepts from scratch), and actual questions asked in interviews at top tech companies.

---

## 🗺️ Section Directory
1. [ML System Design & Scenario-Based Questions](#1-ml-system-design--scenario-based-questions)
2. [Frequently Asked Coding Problems (From Scratch)](#2-frequently-asked-coding-problems-from-scratch)
3. [Company-Specific Interview Questions](#3-company-specific-interview-questions)

---

## 1. ML System Design & Scenario-Based Questions

### Q1: How would you design a recommendation engine for an e-commerce platform like Amazon? (Hard)
**Answer**:
A production-grade recommendation system is typically split into a multi-stage pipeline:
```text
All Items (Millions) ➔ Retrieval (Candidate Gen) ➔ Filtering (Rules) ➔ Ranking (Scoring) ➔ Re-ranking (Diversity)
```

1. **Candidate Generation (Retrieval)**:
   - *Goal*: Reduce millions of items to hundreds.
   - *Techniques*: Collaborative Filtering (Matrix Factorization), Two-Tower Neural Networks (User tower and Item tower generating embeddings), Vector similarity search (using Approximate Nearest Neighbors - ANN like Faiss).
2. **Filtering**:
   - *Goal*: Remove items that the user has already bought, out-of-stock items, or age-inappropriate content.
3. **Scoring & Ranking**:
   - *Goal*: Sort candidates by exact user preference.
   - *Techniques*: Train a binary classifier (e.g., Deep & Cross Networks - DCN, or Gradient Boosted Trees) predicting click-through rate (CTR) or conversion rate (CVR). Features include user profile, item features, user-item interactions, and context (time, device).
4. **Re-ranking & Diversity**:
   - *Goal*: Ensure recommendations aren't repetitive (e.g., showing 10 black shirts).
   - *Techniques*: Deduplication, popularity de-biasing, and epsilon-greedy exploration to introduce new items.

---

### Q2: You deploy an ML model and notice its accuracy degrades after a month. What is this phenomenon, and how do you address it? (Medium)
**Answer**:
This is called **Model Degradation**, usually caused by **Dataset Drift**:
- **Covariate Shift (Data Drift)**: The distribution of the input features $P(X)$ changes over time, but the conditional probability $P(Y|X)$ remains constant.
  - *Example*: An app gets a massive influx of users from a new demographic.
- **Concept Drift**: The statistical properties of the target variable $P(Y|X)$ change, meaning the same inputs map to different outputs.
  - *Example*: Consumer buying habits change radically during a global pandemic.

**How to address it**:
1. **Monitoring**: Track statistics (mean, variance) of input features using tests like the Kolmogorov-Smirnov test or Population Stability Index (PSI).
2. **Data Logging**: Set up feedback loops to log ground-truth predictions where possible.
3. **Continuous Retraining**: Set up pipelines to retrain the model on the latest data (e.g., using a sliding window of the last 30 days).
4. **Fallback mechanism**: If drift is severe, fall back to a rule-based baseline model while investigation is underway.

---

## 2. Frequently Asked Coding Problems (From Scratch)

### Q3: Write a Python function to compute the confusion matrix, precision, recall, and F1-score from scratch (without sklearn). (Medium)
**Answer**:
```python
def compute_metrics(y_true, y_pred):
    """
    Computes classification metrics for binary predictions.
    y_true: List of ground-truth labels (0 or 1)
    y_pred: List of predicted labels (0 or 1)
    """
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    
    for true, pred in zip(y_true, y_pred):
        if true == 1 and pred == 1:
            tp += 1
        elif true == 0 and pred == 1:
            fp += 1
        elif true == 0 and pred == 0:
            tn += 1
        elif true == 1 and pred == 0:
            fn += 1
            
    confusion_matrix = [[tn, fp], [fn, tp]]
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "confusion_matrix": confusion_matrix,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score
    }

# Example validation
y_t = [1, 0, 1, 1, 0, 1]
y_p = [1, 0, 0, 1, 1, 1]
print(compute_metrics(y_t, y_p))
```

---

### Q4: Write a Python function to calculate the Intersection over Union (IoU) of two bounding boxes. (Hard)
**Answer**:
Intersection over Union (IoU) is a common metric in object detection used to evaluate overlapping bounding boxes.
```python
def calculate_iou(boxA, boxB):
    """
    Computes IoU of two bounding boxes.
    Format: [x1, y1, x2, y2] representing coordinates of top-left and bottom-right corners.
    """
    # Determine the coordinates of the intersection rectangle
    x_left = max(boxA[0], boxB[0])
    y_top = max(boxA[1], boxB[1])
    x_right = min(boxA[2], boxB[2])
    y_bottom = min(boxA[3], boxB[3])

    # Calculate area of intersection rectangle
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Calculate area of individual boxes
    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # Calculate union area
    union_area = float(areaA + areaB - intersection_area)

    return intersection_area / union_area if union_area > 0 else 0.0
```

---

### Q5: Write a NumPy-based class to perform Linear Regression parameter updates via gradient descent. (Medium)
**Answer**:
```python
import numpy as np

class LinearRegressionGD:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        # X: shape (N, F), y: shape (N,)
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0.0

        for _ in range(self.epochs):
            # Forward pass (predictions)
            y_predicted = np.dot(X, self.weights) + self.bias
            
            # Compute gradients
            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)
            
            # Update weights and bias
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias
```

---

## 3. Company-Specific Interview Questions

### 🏢 Google

#### Q6: Explain active learning. When is it most beneficial? (Medium)
**Answer**:
Active Learning is a subfield of machine learning where the algorithm dynamically queries a user (often an oracle or human labeler) to label new data points that are most informative.
**When it is beneficial**:
It is used when unlabeled data is abundant but labeling data is extremely expensive, time-consuming, or requires domain experts (e.g., medical image labeling). Instead of labeling randomly, the model queries instances where it has the highest uncertainty (uncertainty sampling) or that would cause the largest gradient change (expected model change), training highly accurate models with fractionally fewer labeled samples.

#### Q7: What is the difference between L1 and L2 regularization in terms of their gradients? (Hard)
**Answer**:
The derivative of the regularization terms determines how updates occur during gradient descent:
- **L2 Regularization Penalty**: $R(w) = \frac{1}{2} \lambda ||w||_2^2$
  - Gradient: $\frac{\partial R}{\partial w_j} = \lambda w_j$
  - The gradient scales linearly with the weight value. As the weight $w_j$ approaches $0$, its gradient update also approaches $0$. Thus, weight updates slow down, meaning weights get close to $0$ but never reach exactly $0$.
- **L1 Regularization Penalty**: $R(w) = \lambda ||w||_1$
  - Gradient: $\frac{\partial R}{\partial w_j} = \lambda \cdot \text{sign}(w_j)$ (for $w_j \ne 0$)
  - The gradient magnitude is constant ($\lambda$ or $-\lambda$) regardless of the weight value. This means weights are constantly pushed towards $0$ at a constant rate, driving them to exactly $0$.

---

### 🏢 Amazon

#### Q8: How would you address the "Cold-Start" problem in a recommendation system? (Medium)
**Answer**:
The cold-start problem occurs when a new user joins (no interaction history) or a new item is added (no reviews/views).
**Solutions**:
1. **For New Users**:
   - Recommend popular or trending items (non-personalized).
   - Ask users for preferences upon sign-up (select topics, genres, or keywords).
   - Leverage demographic details (location, age, device).
2. **For New Items**:
   - Use **Content-Based Filtering**: Map item metadata (text description, category, tags) to existing item embeddings and place it near similar items.
   - Run active exploration campaigns (e.g., allocate $5\%$ of recommendation slots to show new items randomly to collect initial interaction data).

#### Q9: How do you handle model training on highly imbalanced datasets? (Medium)
**Answer**:
1. **Data-level methods**:
   - **Undersampling**: Down-sample the majority class (risks losing information).
   - **Oversampling**: Up-sample the minority class (risks overfitting).
   - **Synthetic Minority Over-sampling Technique (SMOTE)**: Creates synthetic minority samples along the lines joining neighbors of the minority class.
2. **Model-level methods**:
   - **Class Weighting**: Pass class weights to the loss function (e.g., cross-entropy) so misclassifying a minority instance incurs a much higher loss penalty.
   - **Use Alternative Loss Functions**: Use Focal Loss (commonly used in object detection) to down-weight easy-to-classify examples and focus on hard examples.
3. **Use Tree-based / Ensemble Models**: Algorithms like Random Forest or XGBoost are relatively robust to class imbalance if parameters like scale_pos_weight are adjusted.

---

### 🏢 Microsoft

#### Q10: How does the Transformer architecture solve the limitations of RNNs/LSTMs? (Hard)
**Answer**:
1. **Parallel Training**: RNNs must process tokens sequentially (token by token over time steps), which cannot be parallelized across GPUs. Transformers process the entire sequence at once, enabling massive parallel computing.
2. **Long-Range Dependencies**: RNNs struggle to retain information across long sequences due to vanishing gradients across time steps. Transformers use **Self-Attention**, where the distance between any two tokens in a sequence is $O(1)$, meaning long-range context is preserved perfectly without degradation.
3. **Self-Attention Mechanism**: Attention calculations allow tokens to dynamically focus on other relevant tokens in the sentence using Query ($Q$), Key ($K$), and Value ($V$) matrices:
   $$\text{Attention}(Q, K, V) = \text{softmax}\left( \frac{QK^T}{\sqrt{d_k}} \right) V$$

---

### 🏢 TCS & Infosys

#### Q11: What is the difference between correlation and covariance? Explain with formulas. (Easy)
**Answer**:
Both measure the relationship between two variables, but they differ in scale:
- **Covariance**: Measures the directional relationship between two variables. It is scale-dependent (dependent on the units of the variables).
  $$\text{Cov}(X, Y) = \frac{\sum (X_i - \bar{X})(Y_i - \bar{Y})}{N}$$
  Range: $(-\infty, \infty)$.
- **Correlation (Pearson's Correlation Coefficient)**: A standardized measure of the linear strength and direction between two variables. It is scale-invariant.
  $$\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$$
  Range: $[-1, 1]$.

#### Q12: What are the typical preprocessing steps performed before feeding data to a model? (Easy)
**Answer**:
1. **Data Cleaning**: Remove duplicate rows, handle garbage characters, and parse datetimes.
2. **Handling Missing Values**: Impute (mean, median, mode, or KNN) or drop rows/columns.
3. **Handling Outliers**: Detect using IQR or Z-score, and cap, transform, or remove.
4. **Feature Encoding**: Convert categorical variables using One-Hot encoding, Label encoding, or Target encoding.
5. **Feature Scaling**: Apply Standardization (Z-score) or Min-Max scaling to numerical features.
6. **Feature Transformation**: Apply Log-transform to highly skewed distributions to make them normal.

---

## ⚠️ Common Mistakes in Interviews

1. **Suggesting SMOTE without splitting**: Applying SMOTE on the *entire* dataset before splitting into train/test. This leaks synthesized information based on test points into the training fold, yielding artificially high test accuracy.
2. **Assuming Transformers are always better**: Suggesting Transformers for simple, structured tabular data. Traditional models like XGBoost/LightGBM routinely outperform deep learning models on small-to-medium tabular datasets.
3. **Not defining the coordinate system in IoU**: Calculating Intersection over Union (IoU) without clarifying whether coordinate layouts use top-left/bottom-right vs. center/width/height configurations.

---

## 📚 Additional Learning Resources

- **System Design Resources**:
  - *Designing Machine Learning Systems* by Chip Huyen.
  - [Google Machine Learning Systems Design Guide](https://developers.google.com/machine-learning/guides/rules-of-ml)
- **Coding Prep Platforms**:
  - [LeetCode (Machine Learning section / standard SQL/Python)](https://leetcode.com/)
