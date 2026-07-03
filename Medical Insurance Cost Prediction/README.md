# Medical Insurance Cost Prediction

## Overview
This project aims to predict the cost of medical insurance for individuals based on various factors such as age, gender, BMI, number of children, smoking habits, and region. Using machine learning algorithms, the model is trained on a dataset to understand how these factors influence the insurance cost and provide accurate predictions for new data.

## Features
* Data Preprocessing: Cleaning and preparing the data for analysis and model training.
* Exploratory Data Analysis (EDA): Understanding the relationships between different variables and the insurance cost.
* Model Training: Using machine learning algorithms like Linear Regression to predict insurance costs.
* Model Evaluation: Assessing the model's performance using metrics like Mean Squared Error (MSE) and R-squared.
* Prediction: Providing a tool to predict insurance costs for new data inputs.

## Dataset
The dataset used for this project includes the following features:

* age: Age of the individual.
* sex: Gender of the individual (male/female).
* bmi: Body Mass Index, a measure of body fat based on height and weight.
* children: Number of children/dependents covered by the insurance.
* smoker: Smoking status of the individual (yes/no).
* region: Region where the individual resides (northeast, northwest, southeast, southwest).
* charges: Medical insurance cost (target variable).

## Requirements
To run this project, you need to have the following libraries installed:

* Python 3.x
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Scikit-learn
* Jupyter Notebook (for running the notebook file)

You can install these dependencies using pip:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn jupyter
```

## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/yourusername/Medical-Insurance-Cost-Prediction.git
cd Medical-Insurance-Cost-Prediction
```

### Run the Jupyter Notebook

Open the terminal and run the following command to start Jupyter Notebook:

```bash
jupyter notebook
```
Then open `Project_11_Medical_Insurance_Cost_Prediction.ipynb` in Jupyter Notebook.

## Usage

- Data preprocessing: handle missing values, encode categorical variables, and normalize numerical features.
- Exploratory Data Analysis (EDA): visualize the relationships between the features and the insurance cost using plots.
- Model training and evaluation: train the model using algorithms like Linear Regression and evaluate it with MSE and R-squared.
- Prediction: use the trained model to predict insurance costs for new data inputs.

## Results
The final model is evaluated against actual insurance costs and then used to make predictions on new data.
