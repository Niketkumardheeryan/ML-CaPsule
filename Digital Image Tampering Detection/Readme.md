# Digital Image Tampering Detection: CASIA Dataset

## Overview
This project focuses on detecting digital image tampering using the CASIA dataset. The CASIA dataset is a comprehensive collection of images used for research in image forensics.

## Dataset Information
The CASIA dataset is divided into two main directories: CASIA1 and CASIA2. It contains a total of 14.3k files.

## Download
The dataset can be downloaded from [Kaggle](https://www.kaggle.com/datasets/sophatvathana/casia-dataset). The total size of the dataset is approximately 6 GB.

## Installation and Usage

### Prerequisites

Ensure you have the following installed:
- Python 3.6 or higher
- Git

### Clone the Repository

Clone the repository to your local machine using the following command:

```sh
git clone https://github.com/yourusername/Digital-Image-Tampering-Detection.git
cd Digital-Image-Tampering-Detection
```

### Install Dependencies

Install the required dependencies using the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

### Running the Jupyter Notebook

Launch Jupyter Notebook to run the provided notebook:

```sh
jupyter notebook
```

Open the `notebook.ipynb` notebook and run the cells to execute the code.

## Approach

1. **Import Libraries**: Import essential libraries like `numpy`, `matplotlib`, `sklearn`, `keras`, `PIL`, `os`, and `cv2`.

2. **Configuration**: Set paths and parameters (epochs, batch size, etc.) in a configuration class.

3. **ELA Conversion**: Create functions to convert images to Error Level Analysis (ELA) format.

4. **Prepare Data**: Load and convert images to ELA format, resize, and normalize them.

5. **Split Data**: Divide the dataset into training, validation, and test sets.

6. **Build and Compile Model**: Define and compile a CNN model using Keras.

7. **Data Augmentation**: Apply data augmentation techniques to improve model performance.

8. **Train and Evaluate**: Train the model, validate it, and evaluate its performance on the test set.


## Usability
- **Usability Score**: 3.13
- **License**: Unknown
- **Expected Update Frequency**: Not specified

## Summary
The CASIA dataset is a valuable resource for researchers working on digital image tampering detection. It provides a large number of images and scripts to facilitate the research process.
