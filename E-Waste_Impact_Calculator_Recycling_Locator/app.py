import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

# Set page config with high-end style
st.set_page_config(
    page_title="E-Waste Carbon & Toxic Impact Tracker",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "e_waste_model.pkl")

@st.cache_resource
def load_assets():
    if not os.path.exists(model_path):
        return None
    with open(model_path, "rb") as f:
        return pickle.load(f)

assets = load_assets()

# Design Custom CSS for premium Glassmorphism & Modern aesthetics
st.markdown("""
<style>
    .reportview-container {
        background: #0f172a;
    }
    .main {
        background: #0f172a;
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #10b981 !important;
        font-family: 'Outfit', sans-serif;
    }
    .stButton>button {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #059669;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #34d399;
        margin-bottom: 5px;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
    }
    .fact-card {
        background: rgba(16, 185, 129, 0.1);
        border-left: 5px solid #10b981;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title & Hero Header
st.title("🌱 E-Waste Environmental Impact Calculator & Recycler Locator")
st.markdown("Assess the carbon footprint, toxic hazard, and recyclability of your electronics, then find nearby disposal facilities.")

if assets is None:
    st.error("⚠️ Model assets not found! Please run the training script `python train_model.py` first to generate the models.")
    st.stop()

# Sidebar Setup
st.sidebar.image("https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?auto=format&fit=crop&w=400&q=80", caption="Responsible Disposal Matters", use_column_width=True)
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to:", ["Impact Calculator", "Recycling Locator", "Educational Dashboard"])

# Load metadata from assets
models = assets["models"]
encoders = assets["encoders"]
categories = sorted(assets["categories"])
brands = sorted(assets["brands"])
conditions = assets["conditions"]

# Helper to calculate haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# ----------------- Tab 1: Impact Calculator -----------------
if app_mode == "Impact Calculator":
    st.header("🔌 Calculate Environmental Impact")
    st.write("Enter your electronic device specifications to estimate its lifecycle carbon footprint and recycling parameters.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Device Specifications")
        category = st.selectbox("Gadget Category", categories)
        brand = st.selectbox("Brand/Manufacturer", brands)
        age = st.slider("Age of Device (Years)", min_value=0.0, max_value=15.0, value=2.0, step=0.5)
        condition = st.selectbox("Current Condition", conditions)
        
        submit = st.button("Calculate Impact")
        
    with col2:
        if submit or 'predicted' in st.session_state:
            st.session_state['predicted'] = True
            
            # Encode inputs
            cat_enc = encoders["category"].transform([category])[0]
            brand_enc = encoders["brand"].transform([brand])[0]
            cond_enc = encoders["condition"].transform([condition])[0]
            
            # Predict
            features = pd.DataFrame([[cat_enc, brand_enc, age, cond_enc]], 
                                    columns=["category", "brand", "age_years", "condition"])
            
            co2_pred = models["co2_footprint"].predict(features)[0]
            toxic_pred = models["toxic_score"].predict(features)[0]
            recy_pred = models["recyclability"].predict(features)[0]
            
            st.subheader("📊 Estimated footprint results")
            
            # Metrics display
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{co2_pred:.1f} kg</div>
                    <div class="metric-label">CO₂ Footprint (CO₂ eq)</div>
                </div>
                """, unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{toxic_pred:.1f}/100</div>
                    <div class="metric-label">Toxic Material Score</div>
                </div>
                """, unsafe_allow_html=True)
            with m_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{recy_pred:.1f}%</div>
                    <div class="metric-label">Recyclability Potential</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.write("---")
            
            # Equivalencies
            st.subheader("💡 Environmental Equivalency")
            car_miles = co2_pred * 2.5 # ~2.5 miles per kg CO2
            smartphone_charges = co2_pred * 120 # ~120 charges per kg CO2
            trees_needed = co2_pred / 22 # ~22 kg CO2 absorbed by one tree per year
            
            eq_col1, eq_col2, eq_col3 = st.columns(3)
            with eq_col1:
                st.info(f"🚗 Equivalent to driving a standard petrol car **{car_miles:.1f} miles**.")
            with eq_col2:
                st.info(f"📱 Equivalent to charging a smartphone **{int(smartphone_charges):,} times**.")
            with eq_col3:
                st.info(f"🌳 Requires **{trees_needed:.2f} mature trees** one full year to absorb this carbon footprint.")
                
            # Warnings based on toxic score
            if toxic_pred > 75:
                st.warning("⚠️ **High Toxic Hazard:** This device contains significant levels of heavy metals (like Lead, Cadmium, or Mercury). It MUST NOT be disposed of in standard household trash.")
            elif toxic_pred > 50:
                st.info("ℹ️ **Medium Toxic Hazard:** Contains moderate amounts of toxic chemicals. Secure professional e-waste recycling is strongly recommended.")
            else:
                st.success("✅ **Low Toxic Hazard:** Lower toxicity level, but recycling remains highly recommended to recover precious metals.")

# ----------------- Tab 2: Recycling Locator -----------------
elif app_mode == "Recycling Locator":
    st.header("📍 Find Authorized Recycling Centers")
    st.write("Locate nearby authorized e-waste recycling facilities based on your location.")
    
    # Pre-defined list of recycling centers across major cities
    recyclers_data = [
        # New York
        {"name": "NYC Safe Disposal Site", "city": "New York", "lat": 40.7250, "lon": -73.9960, "address": "74 Spring St, New York, NY", "phone": "+1 212-555-0199"},
        {"name": "Green E-Waste Solutions NY", "city": "New York", "lat": 40.7128, "lon": -74.0060, "address": "250 Broadway, New York, NY", "phone": "+1 212-555-0145"},
        # San Francisco
        {"name": "Recology San Francisco", "city": "San Francisco", "lat": 37.7344, "lon": -122.3908, "address": "501 Tunnel Ave, San Francisco, CA", "phone": "+1 415-555-0188"},
        {"name": "Bay Area Green E-Waste", "city": "San Francisco", "lat": 37.7749, "lon": -122.4194, "address": "100 Pine St, San Francisco, CA", "phone": "+1 415-555-0122"},
        # London
        {"name": "London Eco-Recycling Hub", "city": "London", "lat": 51.5074, "lon": -0.1278, "address": "12 Whitehall, London, UK", "phone": "+44 20 7946 0192"},
        {"name": "GreenTech E-Cycle London", "city": "London", "lat": 51.5200, "lon": -0.1100, "address": "88 Kingsway, London, UK", "phone": "+44 20 7946 0144"},
        # Mumbai
        {"name": "Eco-Recyclers Mumbai", "city": "Mumbai", "lat": 19.1130, "lon": 72.8633, "address": "Andheri East, Mumbai, MH", "phone": "+91 22 5550 1782"},
        {"name": "Maharashtra E-Waste Depot", "city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "address": "Bandra Kurla Complex, Mumbai, MH", "phone": "+91 22 5550 1234"},
        # Bengaluru
        {"name": "E-Ward Bengaluru", "city": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "address": "MG Road, Bengaluru, KA", "phone": "+91 80 5550 9988"},
        {"name": "Karnataka Green Recyclers", "city": "Bengaluru", "lat": 12.9250, "lon": 77.6100, "address": "HSR Layout, Bengaluru, KA", "phone": "+91 80 5550 4422"},
        # Delhi
        {"name": "Delhi Pollution Control E-Waste Hub", "city": "Delhi", "lat": 28.6139, "lon": 77.2090, "address": "Connaught Place, New Delhi, DL", "phone": "+91 11 5550 3344"},
        {"name": "Capital E-Waste Recyclers", "city": "Delhi", "lat": 28.6300, "lon": 77.2200, "address": "Karol Bagh, New Delhi, DL", "phone": "+91 11 5550 8899"}
    ]
    
    df_recyclers = pd.DataFrame(recyclers_data)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Your Location")
        location_type = st.radio("Choose search method:", ["Select City", "Enter Coordinates"])
        
        user_lat, user_lon = 0.0, 0.0
        
        if location_type == "Select City":
            cities = sorted(list(df_recyclers["city"].unique()))
            selected_city = st.selectbox("Select your nearest city:", cities)
            # Center coordinates of the selected city based on first center entry
            city_center = df_recyclers[df_recyclers["city"] == selected_city].iloc[0]
            user_lat = city_center["lat"]
            user_lon = city_center["lon"]
        else:
            user_lat = st.number_input("Your Latitude:", value=40.7128, format="%.5f")
            user_lon = st.number_input("Your Longitude:", value=-74.0060, format="%.5f")
            
        # Calculate distances
        df_recyclers["distance_km"] = df_recyclers.apply(
            lambda row: round(haversine(user_lat, user_lon, row["lat"], row["lon"]), 2),
            axis=1
        )
        
        # Sort by distance
        df_sorted = df_recyclers.sort_values(by="distance_km").reset_index(drop=True)
        
        st.subheader("Nearest Centers")
        for i in range(min(3, len(df_sorted))):
            center = df_sorted.iloc[i]
            st.markdown(f"""
            <div style="background: rgba(30,41,59,0.5); padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.05);">
                <strong>📍 {center['name']}</strong><br/>
                🚗 {center['distance_km']} km away<br/>
                🏢 {center['address']}<br/>
                📞 {center['phone']}
            </div>
            """, unsafe_allow_html=True)
            
    with col2:
        st.subheader("Interactive Recycler Map")
        # Prepare data for st.map (must contain columns 'latitude' & 'longitude')
        map_df = df_sorted.copy()
        map_df = map_df.rename(columns={"lat": "latitude", "lon": "longitude"})
        
        # Highlight recycler locations
        st.map(map_df[["latitude", "longitude"]])
        st.info("💡 Map pins indicate authorized e-waste collection and recycling hubs.")

# ----------------- Tab 3: Educational Dashboard -----------------
else:
    st.header("📚 E-Waste Educational Hub")
    st.write("Why responsible disposal matters and how you can make a difference.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚠️ The Growing E-Waste Problem")
        st.markdown("""
        <div class="fact-card">
            <strong>Global Scale:</strong> Over 53.6 million metric tons of e-waste are generated globally every year, and this figure is rising by 3-5% annually.
        </div>
        <div class="fact-card">
            <strong>Recycling Rates:</strong> Currently, only about 17.4% of global e-waste is officially documented as collected and properly recycled.
        </div>
        <div class="fact-card">
            <strong>Landfill Impact:</strong> E-waste constitutes only 2% of solid waste in landfills but accounts for nearly 70% of all toxic heavy metal hazardous waste!
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🧪 Toxic Elements inside your Devices")
        toxic_data = {
            "Chemical/Metal": ["Lead", "Mercury", "Cadmium", "Beryllium", "Brominated Flame Retardants"],
            "Found in": ["CRT screens, soldering", "LCD screens, switches", "Chip resistors, old batteries", "Motherboards, connectors", "Plastic casings, circuit boards"],
            "Environmental/Health Hazard": ["Cognitive damage, kidney dysfunction", "Neurological impairment, bioaccumulation", "Kidney damage, carcinogen", "Lung diseases (berylliosis)", "Hormonal disruptions, persistence"]
        }
        st.table(pd.DataFrame(toxic_data))
        
    with col2:
        st.subheader("✅ Actionable Guidelines for Users")
        st.markdown("""
        Before you recycle or donate your device, make sure to follow these best practices:
        1. 💾 **Back Up Your Data:** Ensure all your personal photos, files, and settings are backed up.
        2. 🔒 **Factory Reset:** Perform a complete factory reset to remove all personal data and accounts.
        3. 🔋 **Remove Batteries:** If the battery is removable and bloated/damaged, package it separately in a fireproof container.
        4. 🏷️ **Labels & Cables:** Bundle matching charging bricks and cables together with the device; recyclers can reuse them!
        """)
        
        st.subheader("💡 Simple Tips to Reduce E-Waste")
        st.markdown("""
        * **Repair over Replace:** Consider upgrading RAM/storage or replacing a degraded battery before buying a completely new machine.
        * **Buy Certified Refurbished:** When acquiring new electronics, look for certified refurbished options to extend existing lifecycles.
        * **Donate Working Tech:** If your device still works but no longer fits your needs, donate it to local community organizations or schools.
        """)
