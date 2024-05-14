# Parkinson's Disease Detection using Support Vector Machine Classifier

This repository contains code for detecting Parkinson's Disease using a Support Vector Machine (SVM) classifier. The dataset used in this project contains various acoustic measures from voice recordings of Parkinson's Disease patients and healthy individuals.

## Dataset

The dataset used for this project is stored in the file `Parkinson_data.csv`. It consists of 195 records and 24 attributes, including features such as fundamental frequency, jitter, shimmer, and various other acoustic measures.

## Dependencies

The following Python libraries are required to run the code:

- numpy
- pandas
- seaborn
- matplotlib
- scikit-learn
- imbalanced-learn (imblearn)

You can install these dependencies using pip:
```bash
pip install numpy pandas seaborn matplotlib scikit-learn imbalanced-learn
```
## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
    cd ML-CaPsule
    ```

2. Go the directory of the Parkinson's detection:

    ```bash
    cd 'Parkinsons Disease Prediction using SVM'
    ```

3. Run the Jupyter notebook `Parkinson_Disease_Detection.ipynb` to train the SVM model and evaluate its performance.

4. To use the trained model for prediction on new data, follow the steps outlined in the "Building a Predictive System" section of the notebook.

## Model Evaluation

The trained SVM model achieved an accuracy of approximately 90% on the test dataset. The classification report and confusion matrix are provided in the notebook to evaluate the model's performa

## Predictive System

A predictive system has been implemented to demonstrate how to use the trained SVM model to predict Parkinson's Disease status for new data points. Detailed instructions are provided in the notebook.

## Author

### [Soumyajit Roy](https://github.com/roysammy123)

## License

This project is licensed under the MIT License.