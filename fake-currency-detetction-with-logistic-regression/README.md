# Fake Currency Detection System

A custom-built Machine Learning application that detects counterfeit currency using a **Logistic Regression** model developed from scratch. The system extracts statistical features from banknote images and predicts their authenticity.

## Project Structure

```text
├── app.py           # Streamlit dashboard for image upload and real-time inference
├── model.py         # Core Logistic Regression implementation (from scratch)
├── pipeline.ipynb   # Data processing, training, and model saving notebook
├── README.md        # Project documentation
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