# 📉 Regression Interview Questions

Regression is a supervised learning task focused on predicting a continuous numerical value (label) given a set of input features. It is one of the most fundamental areas of statistical machine learning.

---

## 🔍 Core Concept Overview

- **Algorithms Covered**: Simple and Multiple Linear Regression, Polynomial Regression, Ridge Regression (L1), Lasso Regression (L2), ElasticNet.
- **Core Concepts**: Assumptions of Linear Regression (L.I.N.E.), Multicollinearity, Variance Inflation Factor (VIF), Ordinary Least Squares (OLS), Gradient Descent, L1/L2 Regularization.

---

## 🙋 Interview Questions & Answers

### Q1: What is the optimization objective of Ordinary Least Squares (OLS) Linear Regression? (Easy)
**Answer**:
The objective of Ordinary Least Squares (OLS) is to find the coefficients (weights) that minimize the sum of squared differences (residuals) between the observed target values and the values predicted by the linear approximation.

Mathematically, given predictions $\hat{y}_i = \theta^T x_i$, we minimize the **Residual Sum of Squares (RSS)**:

$$\text{RSS}(\theta) = \sum_{i=1}^{N} (y_i - \hat{y}_i)^2 = \sum_{i=1}^{N} (y_i - \theta^T x_i)^2$$

In vector notation:
$$\text{RSS}(\theta) = (y - X\theta)^T (y - X\theta)$$

---

### Q2: What are the fundamental assumptions of Linear Regression? (Easy)
**Answer**:
A useful acronym to remember these assumptions is **L.I.N.E.**:
1. **L - Linearity**: The relationship between the independent variables and the dependent variable is linear.
2. **I - Independence of residuals**: The residuals (errors) are independent of each other (no autocorrelation, which is common in time-series data).
3. **N - Normality of residuals**: The residuals are normally distributed (important for hypothesis testing and calculating confidence intervals).
4. **E - Equal variance (Homoscedasticity)**: The variance of the residuals is constant across all levels of the independent variables.

*Additional Assumption*: **No Multicollinearity**—independent variables should not be highly correlated with each other.

---

### Q3: Explain the difference between Regression and Classification. (Easy)
**Answer**:
Both are types of supervised learning, but their targets differ:

| Feature | Regression | Classification |
| :--- | :--- | :--- |
| **Output Type** | Continuous numerical values (e.g., price, temperature) | Discrete categorical class labels (e.g., spam/not spam, dog/cat) |
| **Evaluation Metrics** | MSE, RMSE, MAE, $R^2$ | Accuracy, Precision, Recall, F1-Score, ROC-AUC |
| **Algorithms** | Linear Regression, Ridge, Lasso, SVR | Logistic Regression, Decision Trees, SVM, Naive Bayes |
| **Decision Boundary** | Not applicable (predicts coordinates on a hyperplane) | Separates classes in feature space |

---

### Q4: What is Multicollinearity, how does it affect Linear Regression, and how do you handle it? (Medium)
**Answer**:
Multicollinearity occurs when two or more independent variables in a multiple regression model are highly correlated with each other.

**Impact**:
- It doesn't reduce the model's overall predictive power, but it makes the coefficient estimates unstable and highly sensitive to small changes in the model.
- It becomes difficult to estimate the individual relationship between each independent variable and the dependent variable (p-values become unreliable).

**Detection**:
- **Correlation Matrix**: Look for high correlation coefficients ($> 0.8$).
- **Variance Inflation Factor (VIF)**: Measures how much the variance of an estimated regression coefficient is increased because of collinearity.
  $$\text{VIF}_i = \frac{1}{1 - R_i^2}$$
  A VIF $> 5$ or $10$ indicates significant multicollinearity.

**Handling**:
- Drop one of the highly correlated variables.
- Combine the correlated variables (e.g., averaging them).
- Use dimensionality reduction (like PCA) to create orthogonal features.
- Use **Ridge Regression**, which naturally handles multicollinearity by penalizing large weights.

---

### Q5: Compare Ridge (L2) and Lasso (L1) regularization. Why does Lasso lead to sparse weights? (Medium)
**Answer**:
Both add a penalty term to the OLS cost function to prevent overfitting:

- **Ridge Regression (L2)**: Adds a penalty proportional to the sum of squared weights.
  $$J(\theta) = \text{MSE}(\theta) + \lambda \sum_{j=1}^{F} \theta_j^2$$
- **Lasso Regression (L1)**: Adds a penalty proportional to the sum of absolute values of weights.
  $$J(\theta) = \text{MSE}(\theta) + \lambda \sum_{j=1}^{F} |\theta_j|$$

**Why Lasso leads to sparsity (feature selection)**:
Mathematically, the L1 penalty constraint boundary is a diamond shape (in 2D space) with sharp corners on the coordinate axes, while the L2 constraint boundary is a circle. The contours of the loss function are highly likely to hit the L1 constraint boundary at one of its corners where one of the coefficients is exactly $0$.
Thus, Lasso drives less important features' coefficients to exactly $0$, performing automatic feature selection, whereas Ridge shrinks coefficients close to $0$ but never exactly to $0$.

---

### Q6: What is ElasticNet Regression, and when should it be used? (Medium)
**Answer**:
ElasticNet is a regularized regression method that linearly combines both L1 (Lasso) and L2 (Ridge) penalties.

$$J(\theta) = \text{MSE}(\theta) + r \cdot \lambda \sum_{j=1}^{F} |\theta_j| + \frac{1 - r}{2} \cdot \lambda \sum_{j=1}^{F} \theta_j^2$$

Where $r$ is the mixing parameter ($0 \le r \le 1$).

**When to use it**:
1. When there are multiple correlated features. Lasso tends to select only one feature randomly from a group of correlated features, whereas ElasticNet tends to select them together (group effect).
2. When the number of features is much larger than the number of samples ($F > N$), Lasso can select at most $N$ features, whereas ElasticNet can select more than $N$ features.

---

### Q7: Explain the closed-form solution of Ordinary Least Squares (The Normal Equation). (Hard)
**Answer**:
The coefficients $\theta$ that minimize the RSS can be found analytically by taking the gradient of RSS with respect to $\theta$, setting it to $0$, and solving.

Let the cost function be:
$$J(\theta) = (y - X\theta)^T (y - X\theta)$$

Expanding the terms:
$$J(\theta) = y^T y - 2 \theta^T X^T y + \theta^T X^T X \theta$$

Taking the derivative with respect to $\theta$:
$$\frac{\partial J}{\partial \theta} = -2 X^T y + 2 X^T X \theta = 0$$
$$X^T X \theta = X^T y$$

Solving for $\theta$:
$$\theta = (X^T X)^{-1} X^T y$$

This is the **Normal Equation**.

---

### Q8: Under what conditions does the Normal Equation fail or become impractical? (Hard)
**Answer**:
1. **Non-Invertible Matrix ($X^T X$ is singular)**:
   - This occurs if features are linearly dependent (perfect multicollinearity).
   - It also occurs if the number of features is larger than the number of samples ($F > N$).
   - *Solution*: Use regularization (Ridge adds $\lambda I$ to $X^T X$, making it invertible) or pseudo-inverse (SVD).
2. **Computational Inefficiency**:
   - Computing $(X^T X)^{-1}$ requires $O(F^3)$ time complexity.
   - If you have $100,000$ features, inverting the matrix is computationally prohibitive.
   - *Solution*: Use **Gradient Descent** instead, which scales linearly with the number of features ($O(N \cdot F)$ per iteration).

---

### Q9: What is Homoscedasticity vs Heteroscedasticity, and how does Heteroscedasticity impact OLS? (Hard)
**Answer**:
- **Homoscedasticity**: The spread of residuals remains constant across all values of the independent variables.
- **Heteroscedasticity**: The spread of residuals varies (e.g., residuals get larger as predictions get larger).

**Impact on OLS**:
- OLS estimators remain **unbiased**, but they are no longer **efficient** (they are no longer BLUE - Best Linear Unbiased Estimator).
- The standard errors of the coefficients will be underestimated or overestimated, making confidence intervals and hypothesis tests (p-values, t-tests) unreliable.
- *Solution*: Transform the target variable (e.g., using $\log(y)$ or Box-Cox transformation) or use Weighted Least Squares (WLS).

---

### Q10: Why is Polynomial Regression considered a form of Linear Regression? (Medium)
**Answer**:
In statistics, a model is considered **linear** if it is linear in its **parameters ($\theta$)**, not necessarily in its features ($x$).

For example, a 2nd-degree polynomial regression:
$$y = \theta_0 + \theta_1 x + \theta_2 x^2 + \epsilon$$

Although $x^2$ is a non-linear function of $x$, the parameters $\theta_1$ and $\theta_2$ enter the equation linearly (they are raised only to the power of 1, and not inside non-linear functions like $\sin(\theta_2)$ or $e^{\theta_2}$). Thus, we can treat $x^2$ as a new feature $z = x^2$ and solve it using standard linear OLS methods.

---

## ⚠️ Common Mistakes in Interviews

1. **Forgetting to scale features before L1/L2 Regularization**: If features are on different scales, the regularization penalty will unfairly punish features with smaller values (since their coefficients need to be larger to compensate).
2. **Confusing L1 and L2 penalty effects**: Stating that Ridge Regression performs feature selection by driving weights to absolute zero. (Only Lasso does this).
3. **Assuming Correlation implies Causation**: Interpreting a highly positive coefficient in linear regression as a direct causal link. Regression only measures association.

---

## 📚 Additional Learning Resources

- **Interactive Simulations**:
  - [Ordinary Least Squares regression visualizer (Explained Visually)](https://explained.ai/regularization/index.html)
- **Documentation**:
  - [scikit-learn Generalized Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)
