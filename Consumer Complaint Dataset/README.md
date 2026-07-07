# Consumer Complaints Text Classification

## Overview
This project is a Natural Language Processing (NLP) task focused on classifying consumer complaints into specific financial categories. The goal is to streamline the complaint resolution process by routing complaints to the appropriate teams using an automated classification model. The project uses a dataset from the Consumer Financial Protection Bureau (CFPB) and applies a Random Forest Classifier to achieve this task.

## Dataset

### Context
The Consumer Financial Protection Bureau (CFPB) is a federal U.S. agency that helps mediate disputes between consumers and financial institutions. Consumers submit complaints through a web form, and these complaints are then tagged to assist in routing and resolving issues. An NLP model can automate the classification and routing of these complaints, improving efficiency over manual tagging.

### Content
The dataset consists of complaint submissions from March 2020 to March 2021. Each submission has been labeled with one of nine financial product classes, which we consolidated into five main categories for this project:
- **Credit Reporting**
- **Debt Collection**
- **Mortgages and Loans** (including car, payday, and student loans)
- **Credit Cards**
- **Retail Banking** (covering checking/savings accounts, money transfers, etc.)

After data cleaning, the dataset contained approximately 162,400 complaints, with a significant class imbalance (56% in the credit reporting class and the remaining classes distributed between 8% and 14%).

### Acknowledgements
The dataset was organized by CFPB and cleaned by [halpert3](https://github.com/halpert3).

## Project Structure
- **notebooks/** - Contains Jupyter notebooks for data processing, training, and evaluation of the model.
- **data/** - Directory to store the dataset (`complaints_processed.csv`).
- **src/** - Source code for data preprocessing, model training, and evaluation.
- **README.md** - Project overview and instructions.

## Model
We use a Random Forest Classifier to categorize each complaint into one of the five financial classes. The text data undergoes preprocessing, and we create a TF-IDF matrix for feature extraction. The model is then trained and evaluated on this matrix.

### Performance
The Random Forest model achieves approximately 79.6% accuracy, with a weighted F1-score of 0.80. Performance metrics are slightly varied due to class imbalance, with the model performing best on the majority class (Credit Reporting).


## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/consumer-complaints-classification.git
   ```
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Download and place `complaints_processed.csv` in the `ML-CaPsule/Consumer Complaint Dataset/complaints_processed.zip` directory.

## Usage
1. Open the `ML-CaPsule/Consumer Complaint Dataset/Complaint_Classification.ipynb` notebook to view the data processing and model training steps.
2. Run the cells in the notebook to reproduce the results.


