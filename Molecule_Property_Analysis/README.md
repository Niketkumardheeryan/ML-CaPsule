# Molecule Property Analysis using GNN

## Overview
This project aims to develop and evaluate a custom Graph Neural Network (GNN) architecture for classifying molecular data. The primary goal is to accurately predict molecular properties by leveraging the structural information of molecules represented as graphs.

## Dataset
The dataset that has been used in this project is a collection of molecular data provided by the **NIH's Tox21 Data Challenge**. It contains SMILES (Simplified Molecular Input Line Entry System) strings representing molecular structures and corresponding activity labels indicating whether a molecule is active or inactive in a specific biological assay.

Link to the dataset: (<https://tripod.nih.gov/tox21/challenge/data.jsp>)

## Prerequisites
- Python 3.6+
- PyTorch
- PyTorch Geometric
- RDKit
- Scikit-learn
- Matplotlib
- Pandas
- Numpy
- NetworkX

## Models Used
1. Random Forest with ECFP4:

- Baseline model using ECFP4 fingerprints.
- Trained using scikit-learn's RandomForestClassifier.
- Evaluated with accuracy, balanced accuracy, and ROC AUC score.

2. AttentiveFP:
- Includes attention mechanisms to focus on important parts of the graph.
- Trained with cross-entropy loss and evaluated on classification tasks.

3. Custom GNN with GINEConv and GATv2Conv:

- Combines GIN and GATv2 convolution layers to capture node and edge features.
- Uses embedding layers for atom and bond features.
- Includes a classification head with batch normalization, dropout, and linear layers.
- Trained with AdamW optimizer and OneCycleLR scheduler.

## Use Case
This project is designed to classify molecular data using GNNs. It can be used for:

- Predicting molecular properties.
- Drug discovery and design.
- Chemical informatics and bioinformatics research.

## Evaluation Results

#### Validation Set:

```
Accuracy Score: 0.979
Balanced Accuracy Score: 0.770
ROC AUC Score: 0.770
```
#### Test Set:

```
Accuracy Score: 0.965
Balanced Accuracy Score: 0.728
ROC AUC Score: 0.728
```
## Contribution
Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to improve the system.
