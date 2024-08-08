# Flood Prediction Machine Learning Model

This Python project focuses on predicting floods using machine learning algorithms. The dataset used in this project contains various meteorological features, and different classification algorithms are employed to predict flood occurrences.

## Dataset

Due to the size, you should download the dataset from the provided link and place it in the specified directory.

[Dataset](dataset/India.csv)

## Installation

### Step 1: Install Anaconda

1.1 Download and install Anaconda from the following links:

- [Windows](https://www.anaconda.com/download/#windows)
- [macOS](https://www.anaconda.com/download/#macos)
- [Linux](https://www.anaconda.com/download/#linux)

1.2 Create a Python 3.6 environment:

```sh
conda create -n flood-prediction python=3.6
```

### Step 2: Install Required Packages

2.1 Install Jupyter Notebook & JupyterLab if you plan to use them.

2.2 Install the following packages using Anaconda Navigator or via Anaconda Prompt:

**Or**

Using Anaconda Prompt:

```sh
conda install matplotlib seaborn pandas numpy scikit-learn
```

2.3 Install additional packages:

```sh
conda install pydot python-graphviz pillow
```

### Step 3: Start JupyterLab

Launch JupyterLab:

```sh
jupyter lab
```

## Running the Code

**Download the dataset**

Ensure you download the dataset using the provided link and place it in the specified directory.

**Flood Prediction Model**

Open and run the Jupyter Notebook `flood_prediction.ipynb`:

```sh
flood_prediction.ipynb
```

Use `Shift + Enter` to execute code cells step by step. Each cell will provide the output of different processes, including data exploration, model training, and evaluation.

## Conclusion

- The project utilizes several machine learning algorithms to predict flood occurrences.
- Models compared include K-Nearest Neighbors (KNN), Logistic Regression, Support Vector Classification (SVC), Decision Tree, and Random Forest.
- The final results include accuracy, recall, ROC score, and confusion matrix for each model.

## Notice

Make sure to download the dataset and place it in the correct folder before running the code.