# Impact Feature Scaling on Model's Performance

This project provides various techniques and tools for preprocessing your data to improve the performance of your machine learning models.

## Table of Contents

1. [What is Feature Scaling?](#what-is-feature-scaling)
2. [Why it Matters?](#why-it-matters)
3. [Feature Scaling Techniques](#feature-scaling-techniques)
   1. [Standardization](#standardization)
   2. [Normalization](#normalization)
   3. [Max-Abs Scaling](#max-abs-scaling)
   4. [Robust Scaling](#robust-scaling)
4. [Best Practices for Feature Scaling](#best-practices-for-feature-scaling)
5. [Summary](#summary)
6. [Author](#author)

## What is Feature Scaling?

### 1. What is Feature Scaling?
Feature scaling is a data preprocessing technique used in Machine Learning to standardize or normalize the range of independent variables or features of data. Feature scaling normalizes entire features in a similar range.

**↪** It is also known as **data normalization**.

## Why it Matters?
Feature Scaling brings all features in a similar range, to ensure each feature contributes equally to training and no feature dominates over the other.

Let's assume you have a dataset with three features: `Salary, Age, and IQ Level`. The Salary ranges from `30,000 to 80,000,` the Age ranges from `20 to 40,` while IQ Level ranges from `90 to 120.` If you use these features without scaling them, your machine learning algorithm might give importance to the Salary feature because it has a larger range and variance than the other two features. This could lead to a biased and inaccurate model. So, you have to scale these features for better results.

Upon analyzing this example, you now have a better understanding of feature scaling and why it is important.

![Feature Scaling Image](https://miro.medium.com/v2/resize:fit:640/format:webp/1*CWdxdIfma4O20wGIVVU7-g.png)

## Feature Scaling Techniques

### 1. Standardization:
Standardization, also known as **z-score Normalization.**

This technique transforms the features to have a `mean = 0` and a `standard deviation = 1`. It performs best when the distribution of data is not Gaussian(Normal).
$$
    Z = \frac{X - \bar{X}}{\sigma}
$$

```python
from sklearn.preprocessing import StandardScaler

# instance for scaler
scaler = StandardScaler()
X_transform = X.fit_transform(X)
```

### 2. Normalization:
Normalization re-scales values in the range of **`0-1`**,  while it doesn’t affect the original distribution and relationship of features. 

**↪** Normalization is also known as **`min-max normalizarion`** or **`min-max scaling`**. 

Min-Max Scaling is useful when data doesn't follow a normal distribution.

$$
    X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}
$$

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
x_scaled = scaler.fit_transform(x_train)
```

### 3. MaxAbs Scaling:

Max-Abs Scaler works very well in sparse data when most of the observations are 0. Max-Abs Scaler rescale each feature by its maximum absolute value. So, the maximum absolute value of each feature in the training set will be 1.0. 
$$
    X^{'} = \frac{X}{|X_{max}|}
$$

```python
from sklearn.preprocessing import MaxAbsScaler

scaler = MaxAbsScaler()
X_transformed = scaler.fit_transform(X)
```

### 4. Robust Scaling: 

Robust Scaler works well when there are outliers present in the data. Because it uses the **`median(x͂)`** and **`inter-quartile range(Q3 — Q1)`**, it absorbs the impact of outliers while scaling.

$$
    X^{'} = \frac{X - X_{median}}{I.Q.R}
$$
```python
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
X_transformed = scaler.fit_transform(X)
```
----------------------------------------------------------

## **Best Practices for Feature Scaling:**

# Few tips to Choose the Right Scaling Method for Improved Models

| Feature Scaling Technique | When to Use                                                                                     | Characteristics                                                                                         |
|---------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Standard Scaler**       | - When the distribution of data is normal<br>- Models assume to have Gaussian (Normal) Distribution<br>- Models that rely on Gradient Descent method (Linear Regression and Logistic Regression)<br>- Sensitive to Outliers | - Assumes data follows a normal distribution.<br>- Sensitive to outliers.                              |
| **Max-Abs Scaler**        | - Suitable for sparse data, when most of the values are 0<br>- Sensitive to outliers             | - Works well with sparse data.<br>- Sensitive to outliers.                                             |
| **Robust Scaler**         | - When data has outliers, robust scaler performs best<br>- When data has skewed distribution      | - Performs well with outliers.<br>- Suitable for skewed data.                                          |
| **Min-Max Scaler**        | - When the distribution of data is not Gaussian (Normal)<br>- Algorithms requiring features to specific Range [0,1]<br>- Not suitable for sparse data<br>- Sensitive to outliers<br>- Perform best with Neural Networks and KNN | - Scales features to a given range, usually [0, 1].<br>- Sensitive to outliers.<br>- Not suitable for sparse data.<br>- Best for Neural Networks and KNN. |

## **Summary**
> Machine Learning revolves around experimentation, the more you get hands-on, the better your understanding of this field becomes. It’s similar to the trial and error method.
Scaling the input data before feeding it to a machine learning model is always a good practice.


Scaling the input data before feeding it to a machine learning model is a best practice. Here are some key points to remember:

- **Scaling accelerates model convergence**: Properly scaled data can help models converge faster during training.
- **Normalization**: This technique scales data to a range between 0 and 1. It is particularly useful when the data does not follow a normal distribution.
- **Standardization**: This method scales data to have a mean of 0 and a standard deviation of 1. It is preferred for data with a normal or Gaussian distribution.
- **Robust Scaling**: This approach is beneficial when the data contains many outliers, as it uses statistics that are less sensitive to them.
- **Experimentation is key**: Often, the choice of scaling technique might not significantly affect the results, but it can in some cases. It’s good practice to try different scaling methods to see which works best for your specific dataset.
- **Only scale features, not labels**: Ensure that only the features (input variables) are scaled and not the target variable (labels).
- **Proper usage of scalers**: Do not fit the scaler on the test data. Fit the scaler only on the training data and then apply the transformation to the test data.
  - **Incorrect**: `scaler.fit_transform(X_test)`
  - **Correct**: `scaler.transform(X_test)`

Implementing these practices will help in building more efficient and reliable machine learning models.

## Author:
[Maryam Sikander](https://github.com/Maryam-Sikander)