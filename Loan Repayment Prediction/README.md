# Loan Repayment Prediction

This project aims to predict loan repayment using machine learning techniques. The dataset contains various features related to the borrowers' financial status and loan details, and the target variable indicates whether the loan was fully repaid or not.

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Overview

The goal of this project is to build a model that can predict whether a loan will be fully repaid based on the given features. The project involves data preprocessing, exploratory data analysis, feature engineering, model training, and evaluation.

## Dataset

The dataset used in this project contains various attributes related to loan details and borrowers' financial status. It includes features such as `fico` score, loan purpose, credit policy, and more. The target variable is `not.fully.paid`.

## Installation

To run this project locally, please ensure you have Python installed. Then, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/loan-repayment-prediction.git
    ```
2. Navigate to the project directory:
    ```bash
    cd loan-repayment-prediction
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Launch Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
2. Open the `Loan_Repayment_Prediction.ipynb` notebook.
3. Follow the steps in the notebook to preprocess the data, visualize it, and build predictive models.

### Importing Libraries

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
```

### Data Preprocessing

Reading the dataset:

```python
df = pd.read_csv("/content/loan_data.csv")
df.head()
```

Handling categorical variables and encoding:

```python
df['purpose'] = LabelEncoder().fit_transform(df['purpose'])
df.head()
```

### Data Visualization

Visualizing the FICO scores:

```python
sns.set_style('darkgrid')
plt.hist(df['fico'].loc[df['credit.policy']==1], bins=30, label='Credit.Policy=1')
plt.hist(df['fico'].loc[df['credit.policy']==0], bins=30, label='Credit.Policy=0')
plt.legend()
plt.xlabel('FICO')
```

## Results

The performance of the model is evaluated using various metrics such as accuracy, precision, recall, and confusion matrix. The results are displayed in the notebook.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

