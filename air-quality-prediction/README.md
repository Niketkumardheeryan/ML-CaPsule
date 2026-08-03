# 🌫️ Delhi NCR Hybrid AQI Predictor

A real-time Air Quality Index (AQI) prediction dashboard built with Streamlit. This project utilizes a **Hybrid AI Architecture** combining a Deep Neural Network (PyTorch) for base predictions and a LightGBM model for residual refinement, specifically tuned for the geographic and meteorological nuances of the Delhi NCR region.

## 🚀 Features
- **Hybrid Inference Engine**: Fuses Deep Learning (PyTorch) with Gradient Boosting (LightGBM) to capture both complex non-linear patterns and granular decision boundaries.
- **Physics & Geo-Informed Features**: 
  - Cyclical time encoding (sine/cosine transformations for hours and months).
  - Domain-specific features like `is_monsoon` (rain washout effect) and `is_winter_saturation` (winter inversion layers).
  - Spatial interactions combining latitude and longitude coordinates.
- **Interactive Dashboard**: Built with Streamlit for a clean, user-friendly web interface.
- **Dynamic Artifact Loading**: Automatically pulls exact feature ordering and classes directly from the saved training `StandardScaler` and `LabelEncoders` to prevent inference shape errors.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Machine Learning**: PyTorch, LightGBM, scikit-learn
- **Data Processing**: Pandas, NumPy
- **Model Serialization**: Joblib

## 📁 Project Structure
```text
├── app.py               # Main Streamlit application script
├── weights.pkl          # Serialized dictionary containing the PyTorch model, LightGBM model, scaler, and encoders
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
# ⚙️ Installation & Setup
- Install dependencies:
```bash
pip install scikit-learn pandas numpy torch streamlit lightgbm joblib
```

- 💻 Usage
Run the Streamlit application locally:
```bash
streamlit run app.py
```
The dashboard will open in your default web browser (usually at http://localhost:8501). Enter the temporal, geographic, and weather details to generate an instant AQI prediction.

## 🧠 Model Architecture Details

The prediction pipeline follows a Two-Stage Hybrid Approach:

- Stage 1 (Deep Neural Network): Processes continuous and categorical inputs through entity embeddings and dense layers to output a base AQI prediction.
- Stage 2 (LightGBM Residuals): Takes the same inputs to predict the error (residual) of the Neural Network.
- Final Output: Final AQI = NN_Prediction + LightGBM_Prediction. The result is safely clipped between the standard AQI limits (25.0 to 500.0).
