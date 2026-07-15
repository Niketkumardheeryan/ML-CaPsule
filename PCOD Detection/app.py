import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
import lime
import lime.lime_tabular
import warnings
import re

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import VarianceThreshold
from xgboost import XGBClassifier
import xgboost as xgb

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PCOD Risk Detector",
    layout="wide"
)

# Clear stale cache on every startup so dirty-data models are never reused
if "cache_cleared" not in st.session_state:
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state["cache_cleared"] = True

# ==========================================
# CONSTANTS
# ==========================================

DATA_PATH = r"period - Copy.csv"

TARGET_COL = "pcod_status"

FEATURE_COLS = [
    'number_of_peak',
    'age',
    'length_of_cycle',
    'estimated_day_of_ovulution',
    'length_of_leutal_phase',
    'length_of_menses',
    'unusual_bleeding',
    'height',
    'weight',
    'income',
    'bmi',
    'mean_of_length_of_cycle',
    'menses_score'
]

# ==========================================
# NUMBER PARSER
# ==========================================

def parse_number(value):
    """Parse numbers that may be wrapped in brackets or use scientific notation like [5.15625E-1]"""
    try:
        if isinstance(value, (int, float)):
            if np.isnan(value):
                return 0.0
            return float(value)
        s = str(value).strip()
        # Strip ALL surrounding brackets, quotes, whitespace
        s = re.sub(r'^[\[\]\(\)\{\}\'\"\s]+|[\[\]\(\)\{\}\'\"\s]+$', '', s)
        # Also strip any internal brackets (e.g., '[val]' -> 'val')
        s = re.sub(r'[\[\]\(\)\{\}]', '', s)
        if s == '' or s.lower() in ('nan', 'none', 'null', 'na'):
            return 0.0
        return float(s)
    except:
        return 0.0

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_and_preprocess_data():
    df = pd.read_csv(DATA_PATH)
    
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.drop_duplicates()
    
    # Aggressively clean ALL columns that might have bracket-wrapped values
    for col in df.columns:
        if df[col].dtype == object:
            # Check if it's a numeric-looking column
            sample = df[col].dropna().astype(str).str.strip()
            # Strip brackets and try converting
            cleaned = sample.str.replace(r'[\[\]\(\)\{\}]', '', regex=True).str.strip()
            try:
                pd.to_numeric(cleaned, errors='raise')
                # It's numeric in disguise — clean it
                if col != 'unusual_bleeding':
                    df[col] = df[col].apply(parse_number)
            except:
                pass  # keep as-is for genuine string columns
    
    # Clean numeric feature columns explicitly
    for col in FEATURE_COLS:
        if col != 'unusual_bleeding' and col in df.columns:
            df[col] = df[col].apply(parse_number)
    
    # Clean target column too
    if TARGET_COL in df.columns:
        df[TARGET_COL] = df[TARGET_COL].apply(parse_number)
    
    df = df.ffill()
    
    for col in FEATURE_COLS:
        if col in df.columns and col != 'unusual_bleeding':
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            df[col] = df[col].fillna(df[col].median())
    
    # Create target if missing
    if TARGET_COL not in df.columns:
        df[TARGET_COL] = ((df['bmi'] > 25) | (df['menses_score'] > 3)).astype(int)
    
    # Clean height
    def clean_height(val):
        try:
            h = parse_number(val)
            if 2 < h < 10:
                return h * 30.48
            return h
        except:
            return 165.0
    
    if 'height' in df.columns:
        df['height'] = df['height'].apply(clean_height)
    
    # Encode categorical
    le = LabelEncoder()
    if 'unusual_bleeding' in df.columns:
        df['unusual_bleeding_encoded'] = le.fit_transform(df['unusual_bleeding'].astype(str))
    else:
        df['unusual_bleeding_encoded'] = 0
    
    # Features
    features = [
        f if f != 'unusual_bleeding' else 'unusual_bleeding_encoded'
        for f in FEATURE_COLS
    ]
    
    available_features = [f for f in features if f in df.columns]
    features = available_features
    
    X = df[features].copy()
    
    # Force to numeric — catches anything still slipping through
    for col in X.columns:
        X[col] = pd.to_numeric(X[col].apply(parse_number), errors='coerce').fillna(0.0)
    
    y = df[TARGET_COL].apply(parse_number).astype(int)
    
    # Remove zero variance
    selector = VarianceThreshold(threshold=0)
    X_filtered = selector.fit_transform(X)
    selected_features = X.columns[selector.get_support()]
    X = pd.DataFrame(X_filtered, columns=selected_features, dtype=np.float64)
    features = list(selected_features)
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X = pd.DataFrame(X_scaled, columns=features, dtype=np.float64)
    
    return X, y, scaler, features, df

# ==========================================
# TRAIN MODEL
# ==========================================

@st.cache_resource
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = XGBClassifier(
        eval_metric='logloss',
        random_state=42,
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05
    )
    
    model.fit(X_train, y_train)
    
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    
    st.sidebar.info(f"Model: Train {train_acc:.2%} | Test {test_acc:.2%}")
    
    return model, X_train, X_test

# ==========================================
# CUSTOM SHAP FUNCTION - FIXED
# ==========================================

def show_shap_plot(model, input_data, X_background, features):
    """
    Computes SHAP values using XGBoost's native C++ implementation via
    xgb.DMatrix + pred_contribs=True.  This completely bypasses Python-level
    string/float conversion and is immune to '[5.15625E-1]'-style errors.
    """
    try:
        # --- build a guaranteed-clean float32 numpy array ---
        raw = input_data.copy()
        for c in raw.columns:
            raw[c] = pd.to_numeric(raw[c].apply(
                lambda v: re.sub(r'[\[\]\(\)\{\}]', '', str(v)).strip()
            ), errors='coerce').fillna(0.0)
        input_array = raw.values.astype(np.float32)

        # --- native XGBoost DMatrix (C++ side, no Python string coercion) ---
        dmat = xgb.DMatrix(input_array, feature_names=features)

        # pred_contribs returns shape (n_samples, n_features + 1)
        # last column is the bias term — drop it
        contribs = model.get_booster().predict(dmat, pred_contribs=True)
        vals = contribs[0, :-1].astype(np.float64)  # 1-D: one value per feature

        # Sort by absolute impact for readability
        abs_vals = np.abs(vals)
        sorted_idx = np.argsort(abs_vals)
        sorted_features = [features[i] for i in sorted_idx]
        sorted_vals     = abs_vals[sorted_idx]
        colors = ['#E74C3C' if vals[i] > 0 else '#3498DB' for i in sorted_idx]

        fig, ax = plt.subplots(figsize=(10, max(4, len(features) * 0.45)))
        ax.barh(sorted_features, sorted_vals, color=colors)
        ax.set_xlabel('|SHAP Value| — Feature Impact on PCOD Prediction')
        ax.set_title('SHAP Feature Importance  (🔴 increases risk  |  🔵 decreases risk)')
        plt.tight_layout()
        return fig

    except Exception as e:
        st.error(f"SHAP Error: {str(e)}")
        return None

# ==========================================
# MAIN UI
# ==========================================

st.title("🩺 PCOD Risk Detection & Explainable AI")

st.markdown("""
This system predicts **PCOD Risk** using Machine Learning and provides:

- SHAP Explainability
- LIME Interpretability
- Real-time Risk Prediction
""")

try:
    # Load data
    X, y, scaler, features, raw_df = load_and_preprocess_data()
    
    # Train model
    model, X_train, X_test = train_model(X, y)
    
    # ==========================================
    # SIDEBAR INPUTS
    # ==========================================
    
    st.sidebar.header("Patient Information")
    
    input_dict = {}
    
    for col in FEATURE_COLS:
        encoded_col = col if col != 'unusual_bleeding' else 'unusual_bleeding_encoded'
        
        if encoded_col not in features:
            continue
        
        if col == 'unusual_bleeding':
            val = st.sidebar.selectbox("Unusual Bleeding", options=['no', 'yes'])
            input_dict['unusual_bleeding_encoded'] = 1 if val == 'yes' else 0
        else:
            if encoded_col in raw_df.columns:
                original_values = raw_df[encoded_col].apply(parse_number).dropna()
                if len(original_values) > 0:
                    min_val = float(original_values.quantile(0.05))
                    max_val = float(original_values.quantile(0.95))
                    default_val = float(original_values.median())
                else:
                    min_val, max_val, default_val = -3.0, 3.0, 0.0
            else:
                idx = features.index(encoded_col)
                mean_val = float(scaler.mean_[idx])
                std_val = float(np.sqrt(scaler.var_[idx]))
                min_val = mean_val - (2 * std_val)
                max_val = mean_val + (2 * std_val)
                default_val = mean_val
            
            if min_val >= max_val:
                min_val = default_val - 1
                max_val = default_val + 1
            
            input_dict[encoded_col] = st.sidebar.slider(
                f"{col.replace('_', ' ').title()}",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(default_val),
                format="%.2f"
            )
    
    # ==========================================
    # PREPARE INPUT
    # ==========================================
    
    input_df = pd.DataFrame([input_dict])
    input_df = input_df[features]
    input_df = input_df.astype(float)
    
    input_scaled = scaler.transform(input_df)
    input_scaled_df = pd.DataFrame(input_scaled, columns=features, dtype=float)
    
    # ==========================================
    # PREDICTION
    # ==========================================
    
    probability = model.predict_proba(input_scaled_df)[0][1]
    prediction = "⚠️ High Risk (PCOD Positive)" if probability > 0.5 else "✅ Low Risk (PCOD Negative)"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Prediction")
        st.metric("PCOD Risk Probability", f"{probability * 100:.2f}%")
        st.write(f"### {prediction}")
    
    with col2:
        st.subheader("Clinical Recommendation")
        if probability > 0.5:
            st.warning("⚠️ High risk detected.\n\n**Recommended:**\n- Hormonal profiling\n- Ultrasound examination\n- Gynecologist consultation")
        else:
            st.success("✅ Low risk detected.\n\n**Recommended:**\n- Healthy lifestyle\n- Regular monitoring")
    
    # ==========================================
    # EXPLAINABLE AI
    # ==========================================
    
    with st.expander("🔍 Explainable AI Analysis", expanded=True):
        
        # ==========================================
        # SHAP - USING CUSTOM FUNCTION
        # ==========================================
        
        st.subheader("SHAP Feature Importance")
        
        with st.spinner("Generating SHAP explanation..."):
            shap_fig = show_shap_plot(model, input_scaled_df, X_train, features)
            if shap_fig:
                st.pyplot(shap_fig)
                plt.close(shap_fig)
        
        # ==========================================
        # LIME
        # ==========================================
        
        st.divider()
        st.subheader("LIME Local Explanation")
        
        try:
            # Ensure training data is float
            X_train_float = X_train.astype(float)
            
            lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=X_train_float.values,
                feature_names=features,
                class_names=['No PCOD', 'PCOD'],
                mode='classification',
                random_state=42
            )
            
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                exp = lime_explainer.explain_instance(
                    input_scaled_df.iloc[0].values.astype(float),
                    model.predict_proba,
                    num_features=min(len(features), 10)
                )
            
            # Display LIME
            fig_lime = exp.as_pyplot_figure()
            st.pyplot(fig_lime)
            plt.close(fig_lime)
            
        except Exception as e:
            st.warning(f"LIME Error: {str(e)}")

except Exception as e:
    st.error(f"Application Error: {str(e)}")
    
    with st.expander("Debug Info"):
        st.exception(e)
