# Animal Cancer Disease Prediction

## Dataset

- This project uses a synthetic/demo image-classification workflow.
- No clinical animal cancer dataset or diagnostic model is included in this repository.
- The notebook demonstrates preprocessing, feature extraction, evaluation metrics, and sample prediction flow using generated demo patterns.

Animal cancer detection normally requires veterinary expertise, validated microscopy data, and laboratory confirmation. This project is an educational machine learning demo that shows how an animal cell or tissue image can be safely uploaded, preprocessed, classified, and displayed through a simple Streamlit interface.

> **Medical disclaimer:** This project is for educational purposes only and should not be used as a medical or veterinary diagnosis tool.

## Key Features

1. Safe image validation for BMP, JPEG, PNG, TIFF, and WebP files
2. RGB conversion, EXIF orientation correction, resizing, and normalization
3. Reusable prediction pipeline for image paths, Pillow images, and uploaded files
4. Lightweight deterministic classifier with interpretable visual features
5. Streamlit app for image upload, preview, prediction result, and confidence score
6. Friendly error handling for unsupported or invalid images
7. Automated tests for preprocessing and prediction pipeline behavior
8. Reproducible notebook with accuracy, precision, recall, F1-score, and confusion matrix

## Tech Stack

- Python
- NumPy
- Pillow
- Streamlit
- scikit-learn
- Matplotlib
- pytest

## Usage

1. Install dependencies from the repository root:

```bash
python -m pip install -r Animal_Cancer_Disease_Prediction/requirements.txt
```

2. Run the Streamlit app:

```bash
streamlit run Animal_Cancer_Disease_Prediction/app.py
```

3. Upload a supported animal cell or tissue image.

4. Click **Predict sample class** to view the predicted class and confidence score.

5. Run tests:

```bash
python -m pytest Animal_Cancer_Disease_Prediction/tests
```

## Notebook

The `animal_cancer_prediction.ipynb` notebook contains the executed model workflow. It demonstrates synthetic/demo data generation, preprocessing, feature extraction, prediction logic, evaluation metrics, and confusion matrix output.

Run the notebook cells from top to bottom to reproduce the model evaluation flow.


## Project Files

- `app.py`: Streamlit user interface
- `animal_cancer_prediction.ipynb`: Educational notebook with demo workflow and metrics
- `src/preprocessing.py`: Image validation and preprocessing utilities
- `src/model_utils.py`: Lightweight deterministic classifier
- `src/predict.py`: End-to-end prediction pipeline
- `tests/`: Automated tests for preprocessing and prediction behavior

## Limitations

- The classifier is heuristic-based and not trained on real veterinary pathology data.
- Synthetic evaluation images do not represent biological diversity.
- Predictions may change with lighting, staining, magnification, or compression.
- Confidence is algorithmic certainty, not diagnostic certainty.
- Real deployment would require expert-labelled data, clinical validation, bias analysis, security review, and veterinary oversight.