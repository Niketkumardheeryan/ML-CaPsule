# Fake Currency Detection System

A custom-built Machine Learning application that detects counterfeit currency using a **Logistic Regression** model developed from scratch. The system extracts statistical features from banknote images and predicts their authenticity.

## Project Structure

```text
├── app.py             # Streamlit dashboard for image upload and real-time inference
├── model.py           # Core Logistic Regression implementation (from scratch)
├── banknote_data.py   # Downloads/caches the UCI banknote dataset, split and scaling
├── pipeline.ipynb     # Data processing, training, and model saving notebook
├── tests/             # Offline unit tests for the model and data pipeline
├── requirements.txt
├── README.md          # Project documentation
```

## Features
- Custom Logistic Regression: Implemented from scratch using NumPy (no reliance on sklearn.linear_model for training).

- Image Feature Extraction: Processes uploaded images to calculate statistical features (Variance, Skewness, Kurtosis, Entropy) required for classification.

- Kagglehub Integration: Automatically manages dataset and model weight downloads.

- Streamlit Dashboard: Interactive UI for real-time banknote authentication.

## Prerequisites
Before running the project, ensure you have the following installed:
```bash
pip install numpy pandas scikit-learn streamlit kagglehub joblib pillow scipy matplotlib seaborn
```
## How it Works
- Data Acquisition: The project utilizes kagglehub to download the necessary datasets and pre-trained configurations.

- Model Training: Training is conducted in pipeline.ipynb, where data is pre-processed, scaled, and the custom LogisticRegression model is fitted.

- Persistence: Trained models are exported using joblib for efficient loading.

- Inference: app.py loads the saved model, accepts an image upload, extracts the necessary statistical features, and performs a prediction.

## Quick start — train and evaluate on the real dataset

`model.py` trains the hand-written model on the **UCI banknote authentication** dataset
(1,372 notes, 4 wavelet features). The data is downloaded and cached on first run, so no
Kaggle account or API token is needed:

```bash
pip install -r requirements.txt
python model.py
```

Measured on a stratified 80/20 split, scaled with training statistics only:

```text
Dataset: 1372 banknotes, 4 features (762 genuine / 610 forged)
Features: variance, skewness, kurtosis, entropy

Epoch : 1000 Loss : 0.080568
Test accuracy : 97.45%  (274 held-out notes)
Genuine : 146 correct, 6 flagged as forged
Forged  : 121 caught,  1 missed
```

Only **one forged note out of 122 was missed**, which is the error that matters most here —
a false negative means a counterfeit passes as genuine.

### Tests

```bash
python -m unittest discover -s tests -v
```

15 tests run fully offline, with no download. They cover the maths of the from-scratch
model — the sigmoid stays in `[0, 1]`, the analytic gradient is checked against a
finite-difference estimate, the loss decreases and never goes negative — plus the stratified
split and the scaler.

## Usage
- Train the model: Run the cells in pipeline.ipynb to generate and save your model weights.

- Launch the dashboard:
```bash
streamlit run app.py
```
- Predict: Upload a banknote image via the browser interface to receive an authenticity prediction.

## Technical Details
- Logic: The custom LogisticRegression class uses Gradient Descent for weight optimization.

- Preprocessing: StandardScaler is used to normalize statistical features before model inference to ensure high accuracy.