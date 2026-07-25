import streamlit as st
import pandas as pd
import numpy as np
import joblib
import torch
import torch.nn as nn

class AstraeaNet(nn.Module):
    def __init__(self, cat_dims, num_dim):
        super().__init__()
        self.embs = nn.ModuleList([nn.Embedding(d, 16) for d in cat_dims])
        self.input_layer = nn.Linear(16 * len(cat_dims) + num_dim, 512)
        
        self.res_block = nn.Sequential(
            nn.Linear(512, 512),
            nn.SiLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.2),
            nn.Linear(512, 512),
            nn.SiLU()
        )
        
        self.head = nn.Sequential(
            nn.Linear(512, 256),
            nn.SiLU(),
            nn.Linear(256, 1)
        )

    def forward(self, c, n):
        embeddings = [self.embs[i](c[:, i]) for i in range(len(self.embs))]
        x = torch.cat(embeddings + [n], dim=1)
        x = self.input_layer(x)
        x = x + self.res_block(x)
        return self.head(x)

# --- 2. SETUP & LOAD ARTIFACTS ---
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@st.cache_resource
def load_artifacts():
    return joblib.load("weights.pkl")

data = load_artifacts()

nn_model = data["model"].to(DEVICE)
nn_model.eval()
lgb_model = data["res_model"]
scaler = data["scaler"]
encoders = data["label_encoders"]

# THE FIX: Dynamically pull the EXACT column names and EXACT order from the saved scaler
num_cols = list(scaler.feature_names_in_)
cat_cols = ['day_of_week', 'season', 'city', 'station']

# --- 3. UI FRONTEND ---
st.title("🌫️ Delhi NCR AQI Predictor")
st.markdown("Enter the temporal, geographic, and meteorological details to get a hybrid AI prediction of the Air Quality Index.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Time & Date")
    month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=1)
    hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
    day_of_week = st.selectbox("Day of Week", options=encoders['day_of_week'].classes_)
    season = st.selectbox("Season", options=encoders['season'].classes_)

with col2:
    st.subheader("Location")
    city = st.selectbox("City", options=encoders['city'].classes_)
    station = st.selectbox("Station", options=encoders['station'].classes_)
    latitude = st.number_input("Latitude", value=28.6139, format="%.4f")
    longitude = st.number_input("Longitude", value=77.2090, format="%.4f")

with col3:
    st.subheader("Weather")
    temperature = st.number_input("Temperature (°C)", value=25.0)
    humidity = st.number_input("Humidity (%)", value=50.0)
    wind_speed = st.number_input("Wind Speed (km/h)", value=10.0)
    visibility = st.number_input("Visibility (km)", value=3.0)

# --- 4. PREDICTION LOGIC ---
if st.button("Predict AQI", type="primary", use_container_width=True):
    # 1. Construct raw dataframe
    input_data = pd.DataFrame({
        'month': [month], 'hour': [hour], 'day_of_week': [day_of_week], 
        'season': [season], 'city': [city], 'station': [station],
        'latitude': [latitude], 'longitude': [longitude], 'temperature': [temperature],
        'humidity': [humidity], 'wind_speed': [wind_speed], 'visibility': [visibility]
    })
    
    # 2. Build engineered features
    input_data['h_sin'] = np.sin(2 * np.pi * input_data['hour'] / 24)
    input_data['h_cos'] = np.cos(2 * np.pi * input_data['hour'] / 24)
    input_data['m_sin'] = np.sin(2 * np.pi * input_data['month'] / 12)
    input_data['m_cos'] = np.cos(2 * np.pi * input_data['month'] / 12)
    input_data['is_monsoon'] = (input_data['season'] == 'monsoon').astype(int)
    input_data['is_winter_saturation'] = ((input_data['season'] == 'winter') & (input_data['humidity'] > 85)).astype(int)
    input_data['geo_interaction'] = input_data['latitude'] * input_data['longitude']
    
    # 3. Label Encode Categoricals
    try:
        for col in cat_cols:
            input_data[col] = encoders[col].transform(input_data[col].astype(str))
    except ValueError as e:
        st.error(f"Unseen categorical value selected: {e}")
        st.stop()
        
    # 4. Scale Numericals (Guaranteed to work now because we use scaler.feature_names_in_)
    # We re-order the dataframe slice to perfectly match the scaler's training memory
    input_data[num_cols] = scaler.transform(input_data[num_cols])
    
    # 5. Extract Tensors
    c_tensor = torch.tensor(input_data[cat_cols].values).to(DEVICE).long()
    n_tensor = torch.tensor(input_data[num_cols].values).to(DEVICE).float()
    
    # 6. Hybrid Inference
    with torch.no_grad():
        nn_pred = nn_model(c_tensor, n_tensor).cpu().numpy().flatten()[0]
        
    # Get exact column order LightGBM expects
    try:
        lgb_expected_cols = lgb_model.feature_name()
    except AttributeError:
        # Fallback if it's a scikit-learn API LightGBM
        lgb_expected_cols = getattr(lgb_model, 'feature_name_', cat_cols + num_cols)
        
    lgb_pred = lgb_model.predict(input_data[lgb_expected_cols])[0]
    
    final_aqi = nn_pred + lgb_pred
    
    # 7. Post-Processing
    if final_aqi > 498.5:
        final_aqi = 500.0
    final_aqi = np.clip(final_aqi, 25.0, 500.0)
    
    # --- 5. UI RESULTS ---
    st.markdown("---")
    
    if final_aqi <= 50:
        color, status = "green", "Good"
    elif final_aqi <= 100:
        color, status = "green", "Satisfactory"
    elif final_aqi <= 200:
        color, status = "orange", "Moderate"
    elif final_aqi <= 300:
        color, status = "red", "Poor"
    elif final_aqi <= 400:
        color, status = "red", "Very Poor"
    else:
        color, status = "darkred", "Severe"

    st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f2f6;">
        <h2 style="margin:0; color: #31333F;">Predicted AQI</h2>
        <h1 style="margin:0; font-size: 4rem; color: {color};">{final_aqi:.1f}</h1>
        <h3 style="margin:0; color: {color};">{status}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("ℹ️ Breakdown: Deep Neural Net Base + LightGBM Residual Refinement")