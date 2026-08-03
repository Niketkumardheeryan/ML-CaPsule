# Hyperparameter Optimization Notebooks
This repository contains a collection of Jupyter notebooks that demonstrate the application of different Sequential Model-Based Optimization (SMBO) models for hyperparameter tuning. The notebooks cover three popular Bayesian optimization algorithms: SMAC, TPE, and Gaussian Processes (GP).

Notebooks
1. SMAC with Scikit-Optimize

Description: This notebook demonstrates the use of SMAC (Sequential Model-based Algorithm Configuration) from the Scikit-Optimize library to optimize hyperparameters of a Convolutional Neural Network (CNN).

2. Tree-structured Parzen Estimator (TPE)

Description: This notebook provides a simple demonstration of the TPE algorithm using the Hyperopt library to perform hyperparameter optimization on a sample machine learning model.
- TPE with CNN
    - Description: Extending the TPE demonstration, this notebook applies the TPE algorithm to optimize the hyperparameters of a CNN.

4. Gaussian Processes (GP) with Scikit-Optimize

Description: This notebook utilizes the Gaussian Processes implementation from the Scikit-Optimize library for hyperparameter tuning of a machine learning model.
How to Use
Clone the repository:

- `git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git`
- `cd HyperParameter Tuning`
Install dependencies:
Ensure you have all necessary libraries installed. You can use the provided requirements.txt file:

- `pip install -r requirements.txt`

Run the notebooks:
Open any notebook in Jupyter and run the cells to see the optimization in action:

## Additional Information
SMAC: SMAC is a flexible tool for algorithm configuration and hyperparameter optimization. It models the performance of the hyperparameter configurations with a random forest.
TPE: The TPE algorithm models the objective function with a tree-structured Parzen estimator, which is useful for complex search spaces.
Gaussian Processes: GP is a probabilistic model where observations occur in a continuous domain, e.g., time or space. It is used for optimizing expensive black-box functions.
For further details, refer to the respective notebooks and the documentation of the libraries used.