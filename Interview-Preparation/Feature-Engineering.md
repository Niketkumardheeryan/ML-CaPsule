# 🛠️ Feature Engineering Interview Questions

Feature Engineering is the process of using domain knowledge to extract features (characteristics, properties, attributes) from raw data via data mining techniques. These features are designed to improve the performance and generalizability of machine learning models.

---

## 🔍 Core Concept Overview

- **Key Focus Areas**: Feature Scaling, Categorical Encoding, Missing Value Imputation, Outlier Handling, Feature Selection, Data Leakage.
- **Key Algorithms/Methods**: Z-Score Standardization, Min-Max Normalization, Target Encoding, KNN Imputation, Filter/Wrapper/Embedded methods, Box-Cox Transformation.

---

## 🙋 Interview Questions & Answers

### Q1: What is the difference between Standardization and Normalization? When do you use which? (Easy)
**Answer**:
- **Standardization (Z-score normalization)**: Rescales data to have a mean ($\mu$) of $0$ and a standard deviation ($\sigma$) of $1$.
  $$x_{\text{std}} = \frac{x - \mu}{\sigma}$$
  - *Properties*: Does not bound values to a specific range. It is less sensitive to outliers because extreme values still exist but are measured in standard deviations.
- **Normalization (Min-Max Scaling)**: Rescales the data to a fixed range, usually $[0, 1]$ or $[-1, 1]$.
  $$x_{\text{norm}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$
  - *Properties*: Bounds the range. It is highly sensitive to outliers because a single extreme outlier will squash all other normal values into a very tight, narrow range.

**When to use**:
- Use **Standardization** for algorithms that assume normally distributed data (e.g., Linear Regression, Logistic Regression, LDA) and optimization methods like Gradient Descent (faster convergence).
- Use **Normalization** when you need a bounded range, such as in Neural Networks (where activations like Sigmoid operate in $[0, 1]$) or distance-based algorithms like KNN/SVM when you are sure there are no extreme outliers.

---

### Q2: What is the "Dummy Variable Trap" in One-Hot Encoding, and how do you avoid it? (Easy)
**Answer**:
The Dummy Variable Trap is a scenario in which independent variables are highly multicollinear—meaning two or more variables are highly correlated. This occurs when One-Hot encoding is applied to a categorical variable with $K$ categories, and all $K$ new binary features are included in the model.

Since the sum of all one-hot columns always equals $1$ (for every row), there is a perfect linear relationship between the dummy variables and the intercept term.
$$\sum_{j=1}^{K} D_j = 1$$

**How to avoid it**:
Drop one of the dummy variables. If you have $K$ categories, keep only $K-1$ dummy variables. The omitted class acts as the baseline reference, and its absence avoids perfect multicollinearity. (Most ML frameworks, like `pandas.get_dummies(drop_first=True)` or `OneHotEncoder(drop='first')`, do this automatically).

---

### Q3: Explain Target Encoding. What is its primary risk, and how is it mitigated? (Medium)
**Answer**:
Target Encoding (or Mean Encoding) replaces each categorical value with the average target value for that category.
$$\hat{x}_{i} = E[Y | X = x_i]$$
- *Example*: In a classification task predicting churn, if category "Zipcode 90210" has a churn rate of $0.35$, the value "90210" is replaced by $0.35$.

**Primary Risk: Severe Overfitting & Data Leakage**:
If a category has very few samples (e.g., a Zipcode with only 1 sample), the encoded value will perfectly match the target of that single sample. The model will memorize this association, failing to generalize to the test set.

**Mitigation**:
1. **Smoothing**: Blend the category mean with the global target mean ($\mu_{\text{global}}$):
   $$S_i = \lambda(n_i) \cdot \mu_i + (1 - \lambda(n_i)) \cdot \mu_{\text{global}}$$
   Where $n_i$ is the number of samples in category $i$, and $\lambda(n_i)$ is a weight function that approaches $1$ as $n_i$ grows.
2. **K-Fold Target Encoding (Cross-Fitting)**: Calculate the category mean using only the training folds, then apply it to the validation fold, preventing leakage.

---

### Q4: What is Data Leakage? Give a concrete example and explain how to prevent it. (Hard)
**Answer**:
Data Leakage occurs when information from outside the training dataset is used to train the model, leading to overly optimistic training/validation scores but poor performance on true unseen data.

**Concrete Example (Scaling Leakage)**:
If you calculate the mean ($\mu$) and standard deviation ($\sigma$) of the *entire* dataset (train + test) and use those values to standardize your features *before* splitting the data:
```python
# INCORRECT - LACKS BOUNDARY
scaler.fit(X_all)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```
Here, information about the scale (distribution) of the test set has leaked into the training set.

**How to prevent it**:
Always fit feature engineering transformers (scalers, encoders, imputers) **only on the training set**, and then use those fitted parameters to transform both the training and test sets.
```python
# CORRECT
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test) # Transform using training parameters
```
Using pipeline structures (like `sklearn.pipeline.Pipeline`) helps automate this and prevents accidental leakage.

---

### Q5: Compare Filter, Wrapper, and Embedded methods for feature selection. (Medium)
**Answer**:

1. **Filter Methods**:
   - Assess features individually based on statistical properties, independent of any machine learning model.
   - *Metrics*: Correlation coefficient, Chi-Square test, Mutual Information, ANOVA.
   - *Pros*: Extremely fast, model-agnostic, prevents overfitting.
   - *Cons*: Ignores feature interactions (a feature might be useless alone but highly predictive when combined with another).

2. **Wrapper Methods**:
   - Evaluate subsets of features by training a model on them and measuring performance.
   - *Methods*: Forward Selection, Backward Elimination, Recursive Feature Elimination (RFE).
   - *Pros*: Finds the optimal subset for a specific model, captures feature interactions.
   - *Cons*: Extremely computationally expensive, high risk of overfitting.

3. **Embedded Methods**:
   - Feature selection is built directly into the model training process.
   - *Methods*: Lasso (L1) regularization, Decision Tree-based feature importances.
   - *Pros*: Balances computational efficiency and model accuracy; captures feature interactions.

---

### Q6: How do you handle missing values in a dataset? (Medium)
**Answer**:
Handling missing values depends on the mechanism of missingness:

1. **Deletion**:
   - *Listwise deletion*: Remove the entire row. Use only if missing values are small in number ($< 5\%$) and occur completely at random (MCAR).
   - *Column deletion*: Drop the feature if it has $> 60\%$ missing values and is not critical.
2. **Imputation (Simple)**:
   - *Numerical*: Impute with Mean (if data is symmetric) or Median (robust to outliers).
   - *Categorical*: Impute with Mode (most frequent value) or a placeholder like "Unknown".
3. **Imputation (Advanced)**:
   - *KNN Imputation*: Impute missing values based on the values of the $k$ most similar rows.
   - *MICE (Multivariate Imputation by Chained Equations)*: Models each feature with missing values as a function of other features iteratively.
4. **Model-native support**: Use algorithms like XGBoost or LightGBM that handle missing values natively during split finding.

---

### Q7: Why do tree-based algorithms not require feature scaling, while distance-based algorithms do? (Medium)
**Answer**:
- **Tree-Based Algorithms (e.g., Decision Trees, Random Forests)**:
  - Trees make decisions by splitting nodes based on threshold rules ($X_j \le \text{threshold}$).
  - A threshold split on feature $X_j$ is determined purely by the rank/order of values, not their absolute scale. If you multiply all values of $X_j$ by $1000$, the tree will simply scale its threshold split by $1000$, and the resulting splits will remain identical.
- **Distance-Based Algorithms (e.g., KNN, SVM, K-Means)**:
  - These compute distances (like Euclidean distance) between data points:
    $$d = \sqrt{(x_1 - y_1)^2 + (x_2 - y_2)^2}$$
  - If feature $1$ ranges from $0$ to $1,000,000$ (e.g., income) and feature $2$ ranges from $0$ to $1$ (e.g., scale of $0-1$ for feedback), the income feature will dominate the distance calculation, making feature $2$ irrelevant. Scaling prevents this.

---

### Q8: What are the three types of missing data mechanisms (MCAR, MAR, MNAR)? (Hard)
**Answer**:
1. **Missing Completely at Random (MCAR)**:
   - The probability of data being missing is completely independent of any observed or unobserved variables.
   - *Example*: A test tube breaks in the lab by accident.
2. **Missing at Random (MAR)**:
   - The probability of data being missing is systematically related to some observed data, but not the missing values themselves.
   - *Example*: Men are less likely to disclose their weight, meaning weight is missing conditionally on the observed variable "Gender".
3. **Missing Not at Random (MNAR)**:
   - The probability of data being missing depends on the value of the missing variable itself.
   - *Example*: People with high incomes refuse to answer income survey questions. This is hard to handle because the missingness contains information.

---

### Q9: What is the Feature Hashing Trick, and when is it useful? (Hard)
**Answer**:
The Feature Hashing Trick (or Hashing Vectorizer) maps high-cardinality categorical features (like raw text words or user IDs) into a fixed-size numerical index using a hash function.

**How it works**:
- Choose a target number of features (bins) $B$ (e.g., $B = 2^{18}$).
- Apply a hash function $H(\text{category})$ and take the modulo $B$:
  $$\text{Index} = H(\text{category}) \pmod B$$
- Increment the value at that index in a sparse vector.

**Pros**:
1. **Saves Memory**: You don't need to maintain a vocabulary dictionary mapping categories to indices.
2. **Handles Out-of-Vocabulary (OOV)**: New categories in production are mapped to the same fixed-size space without rebuilding the model.
**Cons**:
1. **Hash Collisions**: Multiple distinct categories can map to the same index. Choosing a large enough $B$ minimizes the impact.

---

### Q10: How do you detect and handle outliers in a dataset? (Medium)
**Answer**:
**Detection**:
1. **Boxplots / IQR Method**: Points lying beyond $1.5 \times \text{IQR}$ from the 1st or 3rd quartile:
   $$\text{Lower Limit} = Q_1 - 1.5 \times \text{IQR}$$
   $$\text{Upper Limit} = Q_3 + 1.5 \times \text{IQR}$$
2. **Z-Score**: Points with a Z-score $|Z| > 3$ (assumes normal distribution).
3. **Isolation Forest**: An unsupervised algorithm that isolates anomalies instead of profiling normal points. Anomalies are easier to isolate (require fewer splits in a tree).

**Handling**:
- **Trimming (Removal)**: Delete outlier rows if they represent data entry errors.
- **Winsorization (Capping)**: Cap outliers at a specific percentile (e.g., replacing values above 99th percentile with the 99th percentile value).
- **Transformation**: Apply $\log$ or Box-Cox transformations to reduce the skewness caused by extreme values.
- **Use Robust Algorithms**: Choose models like Decision Trees or Huber Loss regression that are naturally robust to outliers.

---

## ⚠️ Common Mistakes in Interviews

1. **Incorrectly applying `fit_transform` on testing data**: Always call `.fit_transform()` on the training split, and only `.transform()` on the validation/test split.
2. **Over-imputing without flag columns**: Imputing missing values with the median but forgetting to add a binary indicator column (e.g., `is_missing_Age`) which informs the model that the original data was missing (especially critical in MAR/MNAR scenarios).
3. **Encoding Ordinal Features with One-Hot Encoding**: Categories like `[Low, Medium, High]` have a natural ordering. One-hot encoding destroys this structural information. Use Ordinal Encoding instead.

---

## 📚 Additional Learning Resources

- **Books**:
  - *Feature Engineering for Machine Learning* by Alice Zheng and Amanda Casari.
- **Documentation**:
  - [scikit-learn Preprocessing Guide](https://scikit-learn.org/stable/modules/preprocessing.html)
