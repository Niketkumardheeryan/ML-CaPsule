import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split

from model_evaluation import (
    build_preprocessor,
    build_model_pipelines,
    evaluate_models,
    plot_confusion_matrix,
    plot_comparison
)

# Set page config
st.set_page_config(
    page_title="ASD Classifier Evaluator",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Title & Styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 16px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 5px;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 24px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🧩 Autism Spectrum Disorder (ASD) Model Evaluator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">An interactive machine learning workbench to train, evaluate, and compare classifiers on clinical screening questionnaire responses.</div>', unsafe_allow_html=True)

# ----------------- SIDEBAR CONFIGURATION -----------------
st.sidebar.image("https://img.icons8.com/color/96/autism.png", width=90)
st.sidebar.header("Configuration Panel")

# 1. Dataset Selection
st.sidebar.subheader("1. Data Selection")
data_source = st.sidebar.radio("Source", ["Default Dataset", "Upload Custom CSV"])

uploaded_file = None
if data_source == "Upload Custom CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# 2. Select Classifiers to Include
st.sidebar.subheader("2. Models to Compare")
include_lr = st.sidebar.checkbox("Logistic Regression", value=True)
include_svc = st.sidebar.checkbox("Support Vector Classifier (SVC)", value=True)
include_rf = st.sidebar.checkbox("Random Forest", value=True)
include_dummy = st.sidebar.checkbox("Baseline Dummy Classifier", value=True)

# 3. Train-Test Split Configurations
st.sidebar.subheader("3. Validation Settings")
test_size = st.sidebar.slider("Test Size Split (%)", min_value=10, max_value=50, value=20, step=5) / 100.0
random_state_val = st.sidebar.number_input("Random Seed (for reproducibility)", value=42, min_value=0)

# 4. Hyperparameters Tuning
st.sidebar.subheader("4. Classifier Hyperparameters")

param_grid = {}

if include_lr:
    with st.sidebar.expander("Logistic Regression Parameters"):
        lr_c = st.number_input("Regularization C (LR)", value=1.0, min_value=0.01, max_value=100.0, step=0.1)
        lr_solver = st.selectbox("Solver", ["lbfgs", "liblinear", "saga"])
        param_grid['LogisticRegression'] = {'C': lr_c, 'solver': lr_solver}

if include_svc:
    with st.sidebar.expander("SVC Parameters"):
        svc_c = st.number_input("Regularization C (SVC)", value=1.0, min_value=0.01, max_value=100.0, step=0.1)
        svc_kernel = st.selectbox("Kernel Function", ["rbf", "linear", "poly", "sigmoid"])
        param_grid['SVC'] = {'C': svc_c, 'kernel': svc_kernel}

if include_rf:
    with st.sidebar.expander("Random Forest Parameters"):
        rf_estimators = st.slider("Number of Estimators", min_value=10, max_value=500, value=100, step=10)
        rf_max_depth = st.slider("Max Depth", min_value=1, max_value=50, value=10)
        param_grid['RandomForestClassifier'] = {'n_estimators': rf_estimators, 'max_depth': rf_max_depth}

# ----------------- DATA LOADING -----------------
@st.cache_data
def load_data(uploaded_file, data_source):
    if data_source == "Upload Custom CSV" and uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error loading custom CSV file: {e}")
            return None
    else:
        # Load local Default dataset
        local_paths = ["Data.csv", "Autism Identification System/Data.csv"]
        for path in local_paths:
            if os.path.exists(path):
                try:
                    return pd.read_csv(path)
                except Exception as e:
                    st.error(f"Error loading default dataset: {e}")
                    return None
        st.error("Default dataset 'Data.csv' could not be found.")
        return None

df_raw = load_data(uploaded_file, data_source)

if df_raw is not None:
    # Handle cleaning rules for default dataset columns automatically
    df_clean = df_raw.copy()
    if 'relation' in df_clean.columns:
        # replace '?' with mode
        relation_mode = df_clean['relation'].mode()[0] if not df_clean['relation'].mode().empty else 'Self'
        df_clean['relation'] = df_clean['relation'].replace('?', relation_mode)
    if 'ethnicity' in df_clean.columns:
        df_clean['ethnicity'] = df_clean['ethnicity'].replace('?', 'Others')
        df_clean['ethnicity'] = df_clean['ethnicity'].replace('others', 'Others')

    # Prepare features and target
    # Automatically drop uninformative features if they exist
    cols_to_drop = []
    target_col = None
    
    # Try finding the target column case-insensitively
    for col in df_clean.columns:
        if col.lower() in ['class/asd', 'class', 'label', 'target', 'asd']:
            target_col = col
            break
            
    if target_col is None:
        st.error("No target class column found (e.g. 'Class/ASD'). Please specify labels.")
        st.stop()

    for col in ['age_desc', 'used_app_before']:
        if col in df_clean.columns:
            cols_to_drop.append(col)
            
    X = df_clean.drop(columns=[target_col] + cols_to_drop)
    y = df_clean[target_col]

    # Display dataset preview
    st.markdown('<div class="section-title">📊 Dataset Explorer</div>', unsafe_allow_html=True)
    col_preview1, col_preview2 = st.columns([3, 1])
    with col_preview1:
        st.write(f"Preview of Features (`X` shape: {X.shape}):")
        st.dataframe(X.head(5), use_container_width=True)
    with col_preview2:
        st.write("Target Distribution:")
        st.dataframe(y.value_counts().to_frame("Counts"), use_container_width=True)

    # ----------------- TRAINING & EVALUATION -----------------
    # Auto-train default models in state so predictor is ready right away
    if 'pipelines' not in st.session_state or st.session_state.get('last_source') != data_source:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        preprocessor = build_preprocessor(X)
        default_pipelines = build_model_pipelines(preprocessor)
        metrics_df, reports, cms, roc_data = evaluate_models(default_pipelines, X_train, X_test, y_train, y_test)
        
        st.session_state['pipelines'] = default_pipelines
        st.session_state['metrics_df'] = metrics_df
        st.session_state['reports'] = reports
        st.session_state['cms'] = cms
        st.session_state['roc_data'] = roc_data
        st.session_state['last_source'] = data_source
        st.session_state['features_cols'] = X.columns.tolist()

    # If the user clicks "Run Evaluation", we recalculate with their custom hyperparams
    if st.sidebar.button("Run Evaluation", use_container_width=True):
        selected_pipelines = {}
        preprocessor = build_preprocessor(X)
        all_pipelines = build_model_pipelines(preprocessor, param_grid)
        
        if include_lr:
            selected_pipelines['LogisticRegression'] = all_pipelines['LogisticRegression']
        if include_svc:
            selected_pipelines['SVC'] = all_pipelines['SVC']
        if include_rf:
            selected_pipelines['RandomForestClassifier'] = all_pipelines['RandomForestClassifier']
        if include_dummy:
            selected_pipelines['DummyClassifier'] = all_pipelines['DummyClassifier']

        if not selected_pipelines:
            st.sidebar.error("Please select at least one model to compare!")
        else:
            with st.spinner("Training models and computing performance metrics..."):
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state_val)
                metrics_df, reports, cms, roc_data = evaluate_models(selected_pipelines, X_train, X_test, y_train, y_test)
                
                # Save to session state
                st.session_state['pipelines'] = selected_pipelines
                st.session_state['metrics_df'] = metrics_df
                st.session_state['reports'] = reports
                st.session_state['cms'] = cms
                st.session_state['roc_data'] = roc_data

    # Load session variables
    pipelines = st.session_state['pipelines']
    metrics_df = st.session_state['metrics_df']
    reports = st.session_state['reports']
    cms = st.session_state['cms']
    roc_data = st.session_state['roc_data']

    # ----------------- DISPLAY EVALUATION RESULTS -----------------
    st.markdown('<div class="section-title">🏆 Model Performance Comparison</div>', unsafe_allow_html=True)
    
    col_res1, col_res2 = st.columns([1, 1])
    
    with col_res1:
        st.subheader("Performance Scores Table")
        # Style metrics table
        styled_metrics = metrics_df.style.background_gradient(cmap='Blues', subset=['Accuracy', 'Precision', 'Recall', 'F1-Score'])
        st.dataframe(styled_metrics, use_container_width=True)
        
    with col_res2:
        st.subheader("Metrics Visual Comparison")
        fig_comp = plot_comparison(metrics_df)
        st.pyplot(fig_comp)

    # Tabs for more advanced stats
    tab1, tab2, tab3 = st.tabs(["Confusion Matrices", "ROC Curves", "Classification Reports"])
    
    with tab1:
        st.subheader("Confusion Matrices (Normalized and Absolute)")
        model_to_matrix = st.selectbox("Select Model for Confusion Matrix:", options=list(cms.keys()))
        if model_to_matrix:
            col_cm1, col_cm2 = st.columns(2)
            with col_cm1:
                fig_cm_abs = plot_confusion_matrix(cms[model_to_matrix], labels=['No ASD', 'ASD'], normalize=False)
                st.pyplot(fig_cm_abs)
            with col_cm2:
                fig_cm_norm = plot_confusion_matrix(cms[model_to_matrix], labels=['No ASD', 'ASD'], normalize=True)
                st.pyplot(fig_cm_norm)

    with tab2:
        st.subheader("Receiver Operating Characteristic (ROC) Curves")
        if roc_data:
            fig, ax = plt.subplots(figsize=(8, 6))
            for name, data in roc_data.items():
                ax.plot(data['fpr'], data['tpr'], lw=2, label=f"{name} (AUC = {data['auc']:.2f})")
            ax.plot([0, 1], [0, 1], color='navy', lw=1.5, linestyle='--', label='Chance (AUC = 0.50)')
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('False Positive Rate', fontsize=10, fontweight='bold')
            ax.set_ylabel('True Positive Rate', fontsize=10, fontweight='bold')
            ax.set_title('ROC Curves comparison', fontsize=11, fontweight='bold')
            ax.legend(loc="lower right")
            ax.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No ROC-AUC data available. Make sure the models predict probabilities.")

    with tab3:
        st.subheader("Detailed Classification Reports")
        model_to_report = st.selectbox("Select Model for Report Details:", options=list(reports.keys()))
        if model_to_report:
            st.text(reports[model_to_report])

    # ----------------- INTERACTIVE PREDICTION PANEL -----------------
    st.markdown('<div class="section-title">🎯 Single-Sample Prediction Panel</div>', unsafe_allow_html=True)
    st.write("Input patient features dynamically to classify the risk of Autism Spectrum Disorder (ASD) and inspect the model confidence.")

    input_data = {}
    
    # Render input widgets dynamically
    widget_cols = st.columns(3)
    
    for idx, col_name in enumerate(X.columns):
        col_type = X[col_name].dtype
        unique_vals = X[col_name].dropna().unique()
        
        with widget_cols[idx % 3]:
            # Binary score columns (A1_Score through A10_Score)
            if col_name.startswith('A') and col_name.endswith('_Score') and set(unique_vals).issubset({0, 1}):
                val = st.radio(
                    f"{col_name}: Questionnaire Score", 
                    options=[0, 1], 
                    index=0, 
                    horizontal=True,
                    help=f"Response score for clinical question {col_name.split('_')[0]}"
                )
                input_data[col_name] = val
                
            elif col_name == 'result':
                # Skip direct rendering of result; it will be dynamically derived below to avoid leakage
                pass
                
            elif col_name == 'age':
                min_val = int(X[col_name].min()) if not pd.isna(X[col_name].min()) else 1
                max_val = int(X[col_name].max()) if not pd.isna(X[col_name].max()) else 100
                val = st.slider(
                    "Age (Years)", 
                    min_value=min_val, 
                    max_value=max_val, 
                    value=int(np.clip(25, min_val, max_val)),
                    help="Age of the screening candidate in years."
                )
                input_data[col_name] = float(val)
                
            elif col_type in ['object', 'category']:
                # Dropdown selectbox for categorical properties
                val = st.selectbox(
                    f"{col_name.replace('_', ' ').capitalize()}", 
                    options=sorted(unique_vals),
                    help=f"Select values corresponding to {col_name}."
                )
                input_data[col_name] = val
                
            else:
                # Fallback slider for numeric properties
                min_val = float(X[col_name].min()) if not pd.isna(X[col_name].min()) else 0.0
                max_val = float(X[col_name].max()) if not pd.isna(X[col_name].max()) else 100.0
                val = st.slider(
                    f"{col_name.capitalize()}", 
                    min_value=min_val, 
                    max_value=max_val, 
                    value=(min_val + max_val) / 2.0
                )
                input_data[col_name] = val

    # Dynamic calculation of total score ("result") to ensure exact clinical logic match
    if 'result' in X.columns:
        score_cols = [c for c in X.columns if c.startswith('A') and c.endswith('_Score')]
        calculated_result = sum(input_data[c] for c in score_cols) if score_cols else 0
        st.markdown(f"Auto-calculated AQ screening score (Result): **{calculated_result}**")
        input_data['result'] = calculated_result

    # Select trained classifier to make prediction
    pred_col1, pred_col2 = st.columns([1, 2])
    with pred_col1:
        selected_pred_model = st.selectbox("Select Classifier for Inference:", options=list(pipelines.keys()))

    with pred_col2:
        if selected_pred_model:
            # Create a 1-row DataFrame representing the input
            input_df = pd.DataFrame([input_data])
            
            # Reorder columns to match original training columns X exactly
            input_df = input_df[X.columns]
            
            active_pipeline = pipelines[selected_pred_model]
            
            # Predict
            try:
                prediction_class = active_pipeline.predict(input_df)[0]
                
                # Check target class mappings from training logic
                # Clean y_test mappings to YES/NO
                prediction_str = "ASD Detected (YES)" if prediction_class in [1, 'YES', '1', '1.0'] else "No ASD (NO)"
                bg_color = "#FEE2E2" if prediction_class in [1, 'YES', '1', '1.0'] else "#D1FAE5"
                text_color = "#991B1B" if prediction_class in [1, 'YES', '1', '1.0'] else "#065F46"
                
                # Display output block
                st.markdown(
                    f"""
                    <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; border: 1px solid {text_color}; margin-top: 15px;">
                        <h4 style="margin: 0; color: {text_color}; font-weight: bold;">Prediction: {prediction_str}</h4>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Predict Probabilities
                if hasattr(active_pipeline.named_steps['classifier'], "predict_proba"):
                    probabilities = active_pipeline.predict_proba(input_df)[0]
                    asd_prob = probabilities[1]
                    no_asd_prob = probabilities[0]
                    
                    st.write("")
                    st.write(f"Model Confidence metrics:")
                    st.progress(float(asd_prob))
                    st.write(f"Probability of ASD: **{asd_prob:.2%}** | Probability of No ASD: **{no_asd_prob:.2%}**")
            except Exception as e:
                st.error(f"Prediction failed: {e}")
else:
    st.info("Upload a CSV file or check dataset folder to begin evaluation.")
