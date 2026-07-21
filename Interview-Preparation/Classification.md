# 🏷️ Classification Interview Questions

Classification is a supervised learning task where the objective is to predict a discrete categorical class label (target) for a given input. It is used in applications like spam detection, medical diagnosis, and sentiment analysis.

---

## 🔍 Core Concept Overview

- **Algorithms Covered**: Logistic Regression, Support Vector Classifier (SVC), Naive Bayes, Decision Trees/Random Forest, K-Nearest Neighbors.
- **Core Concepts**: Sigmoid/Softmax Functions, Log-Odds, Binary Cross-Entropy (Log Loss), Generative vs. Discriminative Models, One-vs-Rest (OvR), One-vs-One (OvO), Multi-class vs. Multi-label.

---

## 🙋 Interview Questions & Answers

### Q1: Why is Logistic Regression called "Regression" if it is used for classification? (Easy)
**Answer**:
Logistic Regression is called "Regression" because its underlying mechanism is very similar to Linear Regression. It estimates the relationship between a dependent variable and one or more independent variables.

Specifically, it fits a linear regression model to the **log-odds** (logit) of the probability of the target class:

$$\log\left(\frac{p}{1-p}\right) = \theta_0 + \theta_1 x_1 + \dots + \theta_n x_n = \theta^T x$$

It is a classification algorithm because it maps this continuous log-odds value to a probability between $0$ and $1$ using the Sigmoid function, and then applies a threshold (e.g., $0.5$) to classify the output into discrete categories.

---

### Q2: What is the Sigmoid function, and why is it used? (Easy)
**Answer**:
The Sigmoid function (or logistic function) is an S-shaped curve that maps any real-valued number into a probability range between $0$ and $1$.

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

**Why it is used**:
1. It squashes the infinite range of a linear model $(-\infty, \infty)$ to the interval $[0, 1]$, which can be interpreted as a probability $P(Y=1 | X)$.
2. It is differentiable everywhere, which makes it suitable for gradient-based optimization algorithms.

---

### Q3: What is the cost function of Logistic Regression, and why is Mean Squared Error (MSE) not used? (Medium)
**Answer**:
The cost function of Logistic Regression is **Binary Cross-Entropy Loss** (also called **Log Loss**):

$$J(\theta) = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$

Where $y_i$ is the actual label ($0$ or $1$) and $\hat{y}_i = \sigma(\theta^T x_i)$ is the predicted probability.

**Why MSE is not used**:
1. If we plug the non-linear Sigmoid function $\sigma(z)$ into the MSE cost function $\frac{1}{2}(y - \sigma(z))^2$, the resulting cost function becomes **non-convex**. This means gradient descent can get trapped in local minima. Using Log Loss ensures a **convex** optimization landscape with a single global minimum.
2. Log Loss penalizes confident wrong predictions extremely heavily (approaching infinity as $\hat{y}_i \to 0$ when $y_i=1$).

---

### Q4: Explain the difference between Multi-class and Multi-label classification. (Easy)
**Answer**:
- **Multi-class classification**: A classification task where each instance belongs to **exactly one** class out of $K$ total classes ($K > 2$).
  - *Example*: Classifying an image of a hand-written digit as $0, 1, 2, \dots, \text{or } 9$.
  - *Activation function*: **Softmax** is used at the output layer to get a probability distribution summing to $1$.
- **Multi-label classification**: A classification task where each instance can belong to **multiple** classes simultaneously (classes are not mutually exclusive).
  - *Example*: Tagging a news article with tags like "Finance", "Technology", and "Global News".
  - *Activation function*: Multiple independent **Sigmoid** activations are used to output independent probabilities for each class label.

---

### Q5: Compare Generative and Discriminative classifiers. (Medium)
**Answer**:
- **Discriminative Models**: Learn the decision boundary directly by modeling the conditional probability $P(Y | X)$. They focus on finding the boundary that separates the classes.
  - *Examples*: Logistic Regression, SVM, Decision Trees, Neural Networks.
  - *Pros*: Generally achieve higher accuracy on large datasets.
- **Generative Models**: Learn the joint probability distribution $P(X, Y)$ (i.e., how the data of each class is generated). They use Bayes' Theorem to compute $P(Y | X)$:
  $$P(Y | X) = \frac{P(X | Y)P(Y)}{P(X)}$$
  - *Examples*: Naive Bayes, Linear Discriminant Analysis (LDA), Gaussian Mixture Models (GMM).
  - *Pros*: Can work well with smaller datasets and can generate new samples.

---

### Q6: How do we extend binary classifiers to handle multi-class problems? (Medium)
**Answer**:
Two common strategies are:

1. **One-vs-Rest (OvR) or One-vs-All**:
   - Train $K$ independent binary classifiers (where $K$ is the number of classes).
   - For classifier $i$, class $i$ is treated as positive and all other classes are grouped as negative.
   - For prediction, feed the input to all $K$ classifiers and select the class with the highest probability.
   - *Complexity*: $K$ models.

2. **One-vs-One (OvO)**:
   - Train a binary classifier for every possible pair of classes.
   - *Complexity*: $\frac{K(K-1)}{2}$ models.
   - For prediction, pass the input through all classifiers. Each classifier votes for a class, and the class with the most votes is predicted.
   - Preferred for algorithms that do not scale well with dataset size (like SVM), since each binary classifier is trained on a smaller subset of data.

---

### Q7: Derive the derivative of the Sigmoid function. (Hard)
**Answer**:
Let $\sigma(z) = \frac{1}{1 + e^{-z}} = (1 + e^{-z})^{-1}$.

Using the chain rule:
$$\frac{d}{dz} \sigma(z) = -1(1 + e^{-z})^{-2} \cdot (-e^{-z})$$
$$\frac{d}{dz} \sigma(z) = \frac{e^{-z}}{(1 + e^{-z})^2}$$

We can rewrite the numerator as $(1 + e^{-z}) - 1$:
$$\frac{d}{dz} \sigma(z) = \frac{(1 + e^{-z}) - 1}{(1 + e^{-z})^2}$$
$$\frac{d}{dz} \sigma(z) = \frac{1 + e^{-z}}{(1 + e^{-z})^2} - \frac{1}{(1 + e^{-z})^2}$$
$$\frac{d}{dz} \sigma(z) = \frac{1}{1 + e^{-z}} - \left(\frac{1}{1 + e^{-z}}\right)^2$$
$$\frac{d}{dz} \sigma(z) = \sigma(z) - \sigma(z)^2$$
$$\frac{d}{dz} \sigma(z) = \sigma(z)(1 - \sigma(z))$$

This simple derivative is extremely useful in neural network gradient computations.

---

### Q8: What is the concept of soft-margin SVM, and what is the role of the hyperparameter $C$? (Hard)
**Answer**:
In real-world data, classes are rarely perfectly separable. A **soft-margin SVM** allows some training points to violate the margin or even be misclassified to achieve better generalization.
The optimization objective introduces slack variables $\xi_i \ge 0$:

$$\min_{w, b, \xi} \frac{1}{2} ||w||^2 + C \sum_{i=1}^{N} \xi_i$$
Subject to: $y_i (w^T x_i + b) \ge 1 - \xi_i$

**Role of the hyperparameter $C$**:
- **Large $C$**: Heavy penalty for misclassification. The model tries to fit the training data as perfectly as possible.
  - *Result*: Narrow margin, **Low Bias, High Variance** (risks overfitting).
- **Small $C$**: Low penalty for misclassification. The model prioritizes a wider margin, even if it means misclassifying some points.
  - *Result*: Wide margin, **High Bias, Low Variance** (risks underfitting).

---

### Q9: How does Naive Bayes handle continuous numerical features? (Medium)
**Answer**:
If a feature $x_i$ is continuous, we cannot calculate frequency counts to estimate $P(x_i | y)$.
Instead, we use **Gaussian Naive Bayes**:
1. We assume that the continuous values associated with each class are distributed according to a normal (Gaussian) distribution.
2. During training, we calculate the mean ($\mu_y$) and variance ($\sigma^2_y$) of feature $x_i$ for each class $y$.
3. During inference, we calculate the probability using the Gaussian Probability Density Function (PDF):

$$P(x_i | y) = \frac{1}{\sqrt{2\pi\sigma^2_y}} \exp\left( -\frac{(x_i - \mu_y)^2}{2\sigma^2_y} \right)$$

---

## ⚠️ Common Mistakes in Interviews

1. **Saying SVM natively outputs probabilities**: SVM is a geometric classifier; it computes distances to a decision boundary, not probabilities. To get probabilities from SVM, one must apply Platt scaling (which trains an auxiliary logistic regression model on the SVM outputs), which is computationally expensive.
2. **Confusing Sigmoid and Softmax**: Sigmoid is for binary classification (independent outputs), whereas Softmax is for multi-class classification (outputs sum to $1$).
3. **Threshold Blindness**: Assuming classification predictions always use a threshold of $0.5$. In imbalanced classification, this threshold must often be tuned to optimize precision or recall.

---

## 📚 Additional Learning Resources

- **Interactive Demos**:
  - [SVM Decision Boundaries Visualizer](https://cs.stanford.edu/people/karpathy/svmjs/demo/)
- **Documentation**:
  - [scikit-learn Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
  - [scikit-learn Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html)
