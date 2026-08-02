"""
💳 Credit Card Fraud Detection — Streamlit App
================================================
Run:
    streamlit run fraud_detection_app.py

Requirements:
    pip install streamlit xgboost scikit-learn imbalanced-learn pandas numpy joblib plotly

Model file expected:  xgb_fraud_model.pkl  (saved via joblib after training)
Scaler file expected: robust_scaler.pkl     (saved via joblib after training)

If model files not found, app runs in DEMO MODE with random predictions.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import joblib
import os
import time
from pathlib import Path

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FraudSentinel — Credit Card Anomaly Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  CUSTOM CSS — Dark cyberpunk / fintech theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

:root {
    --bg-dark:    #0a0e1a;
    --bg-card:    #111827;
    --bg-border:  #1f2937;
    --accent:     #00d4ff;
    --accent2:    #7c3aed;
    --danger:     #ef4444;
    --success:    #10b981;
    --warning:    #f59e0b;
    --text-main:  #e2e8f0;
    --text-muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-main);
}

/* Header */
.fraud-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid var(--accent2);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.fraud-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(0,212,255,0.05) 0%, transparent 60%);
    pointer-events: none;
}
.fraud-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    color: var(--accent);
    margin: 0 0 6px 0;
    letter-spacing: -1px;
}
.fraud-header p {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin: 0;
}

/* Metric cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--bg-border);
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: var(--accent); }
.metric-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
}
.metric-lbl {
    font-size: 0.78rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* Result banner */
.result-fraud {
    background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05));
    border: 2px solid var(--danger);
    border-radius: 14px;
    padding: 24px 32px;
    text-align: center;
}
.result-safe {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.05));
    border: 2px solid var(--success);
    border-radius: 14px;
    padding: 24px 32px;
    text-align: center;
}
.result-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 8px;
}
.result-sub { font-size: 0.9rem; color: var(--text-muted); }

/* Section heading */
.section-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    border-bottom: 1px solid var(--bg-border);
    padding-bottom: 8px;
    margin-bottom: 16px;
}

/* Demo badge */
.demo-badge {
    background: rgba(245,158,11,0.15);
    border: 1px solid var(--warning);
    color: var(--warning);
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 0.8rem;
    font-family: 'Space Mono', monospace;
    display: inline-block;
    margin-bottom: 12px;
}

/* Streamlit overrides */
.stSlider > div > div { background: var(--bg-border) !important; }
div[data-testid="stSidebar"] { background: #0d1117 !important; }
.stButton > button {
    background: linear-gradient(135deg, var(--accent2), #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 12px 28px !important;
    transition: opacity 0.2s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LOAD MODEL (or run in demo mode)
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    """
    Tries to load saved XGBoost model + RobustScaler from disk.
    If not found, returns None (app runs in demo/random mode).

    To save model after training your notebook, add these lines:
        import joblib
        joblib.dump(xgb_clf,  'xgb_fraud_model.pkl')
        joblib.dump(scaler,   'robust_scaler.pkl')
    """
    model_path  = Path("xgb_fraud_model.pkl")
    scaler_path = Path("robust_scaler.pkl")
    if model_path.exists() and scaler_path.exists():
        model  = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    return None, None

model, scaler = load_model()
demo_mode = (model is None)

# Initialize session state for all inputs if not present
if "time_val" not in st.session_state:
    st.session_state["time_val"] = 50000.0
if "amount_val" not in st.session_state:
    st.session_state["amount_val"] = 120.50
for idx in range(1, 29):
    if f"v{idx}" not in st.session_state:
        st.session_state[f"v{idx}"] = 0.00



# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="fraud-header">
    <h1>🛡️ FraudSentinel</h1>
    <p>Credit Card Anomaly Detection · XGBoost + SMOTE · Real-time Inference</p>
</div>
""", unsafe_allow_html=True)

if demo_mode:
    st.markdown("""
    <div class="demo-badge">⚠ DEMO MODE — Place xgb_fraud_model.pkl + robust_scaler.pkl in app directory to activate real model</div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background: rgba(16,185,129,0.1); border: 1px solid #10b981; color: #10b981; 
                border-radius: 6px; padding: 6px 14px; font-size: 0.8rem; font-family: 'Space Mono', monospace; 
                display: inline-block; margin-bottom: 12px;">
        Active Model: XGBoost + SMOTE (Supervised) | PR-AUC: 0.8340 | ROC-AUC: 0.9776 | Recall (Fraud): 0.90
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR — ALL INPUT FEATURES
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 Transaction Inputs")
    st.caption("Fill in all 30 features to run prediction")

    # PRESET TEST CASES
    st.markdown('<div class="section-head">Presets & Test Cases</div>', unsafe_allow_html=True)
    st.caption("Click a preset to quickly load realistic values:")
    
    col_preset_1, col_preset_2 = st.columns(2)
    with col_preset_1:
        if st.button("🟢 Normal Txn", help="Load typical legitimate transaction values", use_container_width=True):
            st.session_state["time_val"] = 0.0
            st.session_state["amount_val"] = 149.62
            normal_v = {
                1: -1.3598, 2: -0.0728, 3: 2.5363, 4: 1.3782, 5: -0.3383, 6: 0.4624, 7: 0.2396,
                8: 0.0987, 9: 0.3638, 10: 0.0908, 11: -0.5516, 12: -0.6178, 13: -0.9914, 14: -0.3112,
                15: 1.4682, 16: -0.4704, 17: 0.2080, 18: 0.0258, 19: 0.4040, 20: 0.2514, 21: -0.0183,
                22: 0.2778, 23: -0.1105, 24: 0.0669, 25: 0.1285, 26: -0.1891, 27: 0.1336, 28: -0.0211
            }
            for k, v in normal_v.items():
                st.session_state[f"v{k}"] = v
            st.rerun()
            
    with col_preset_2:
        if st.button("🔴 Fraud Txn", help="Load verified fraudulent transaction values", use_container_width=True):
            st.session_state["time_val"] = 406.0
            st.session_state["amount_val"] = 0.0
            fraud_v = {
                1: -2.3122, 2: 1.9520, 3: -1.6099, 4: 3.9979, 5: -0.5222, 6: -1.4265, 7: -2.5374,
                8: 1.3917, 9: -2.7701, 10: -2.7723, 11: 3.2020, 12: -2.8999, 13: -0.5952, 14: -4.2893,
                15: 0.3897, 16: -1.1407, 17: -2.8301, 18: -0.0168, 19: 0.4170, 20: 0.1269, 21: 0.5172,
                22: -0.0350, 23: -0.4652, 24: 0.3202, 25: 0.0445, 26: 0.1778, 27: 0.2611, 28: -0.1433
            }
            for k, v in fraud_v.items():
                st.session_state[f"v{k}"] = v
            st.rerun()

    st.markdown('<div class="section-head">Core Features</div>', unsafe_allow_html=True)

    # Time & Amount — the two non-PCA features
    time_val   = st.number_input(
        "⏱ Time (seconds since first txn)",
        min_value=0.0, max_value=200000.0,
        value=st.session_state["time_val"], step=100.0,
        key="time_val",
        help="Seconds elapsed from the very first transaction in the dataset"
    )
    amount_val = st.number_input(
        "💰 Amount ($)",
        min_value=0.0, max_value=30000.0,
        value=st.session_state["amount_val"], step=0.01,
        key="amount_val",
        help="Transaction amount in USD"
    )

    st.markdown('<div class="section-head" style="margin-top:20px">PCA Features (V1–V14)</div>',
                unsafe_allow_html=True)
    st.caption("V1–V28 are anonymized PCA components from original card data")

    # V1 – V14
    v_vals = {}
    cols = st.columns(2)
    for i in range(1, 15):
        with cols[(i - 1) % 2]:
            v_vals[f"V{i}"] = st.number_input(
                f"V{i}", format="%.4f",
                step=0.01, key=f"v{i}",
                help=f"PCA component {i}"
            )

    st.markdown('<div class="section-head" style="margin-top:20px">PCA Features (V15–V28)</div>',
                unsafe_allow_html=True)
    cols2 = st.columns(2)
    for i in range(15, 29):
        with cols2[(i - 15) % 2]:
            v_vals[f"V{i}"] = st.number_input(
                f"V{i}", format="%.4f",
                step=0.01, key=f"v{i}",
                help=f"PCA component {i}"
            )

    st.markdown("---")
    predict_btn = st.button("🔍 Run Fraud Analysis", use_container_width=True)


# ─────────────────────────────────────────────
#  BUILD FEATURE VECTOR
# ─────────────────────────────────────────────
def build_feature_vector(time_val, amount_val, v_vals, scaler):
    """
    Assembles all 30 features into a single row DataFrame.
    Applies RobustScaler to Time and Amount (same as training pipeline).
    Returns numpy array ready for model.predict_proba()
    """
    feature_dict = {"Time": time_val, "Amount": amount_val}
    feature_dict.update(v_vals)  # V1 … V28

    # Column order must match training data exactly
    col_order = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
    df_input = pd.DataFrame([feature_dict])[col_order]

    if scaler is not None:
        df_input[["Time", "Amount"]] = scaler.transform(df_input[["Time", "Amount"]])

    return df_input.values


# ─────────────────────────────────────────────
#  MAIN PANEL
# ─────────────────────────────────────────────
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown('<div class="section-head">Transaction Summary</div>', unsafe_allow_html=True)

    # Show summary table of entered values
    summary_data = {"Feature": ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)],
                    "Value": [time_val, amount_val] + [v_vals[f"V{i}"] for i in range(1, 29)]}
    df_summary = pd.DataFrame(summary_data)

    # Radar-style bar chart for V1–V28 values
    v_names = [f"V{i}" for i in range(1, 29)]
    v_values = [v_vals[k] for k in v_names]

    fig_bar = go.Figure()
    colors = ["#ef4444" if v < 0 else "#00d4ff" for v in v_values]
    fig_bar.add_trace(go.Bar(
        x=v_names,
        y=v_values,
        marker_color=colors,
        marker_line_width=0,
    ))
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="DM Sans"),
        height=260,
        margin=dict(l=10, r=10, t=30, b=10),
        title=dict(text="PCA Feature Values (V1–V28)", font=dict(size=13, color="#e2e8f0")),
        xaxis=dict(tickfont=dict(size=9), gridcolor="#1f2937"),
        yaxis=dict(gridcolor="#1f2937", zerolinecolor="#334155"),
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Time & Amount display
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">${amount_val:,.2f}</div>
            <div class="metric-lbl">Transaction Amount</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{int(time_val):,}s</div>
            <div class="metric-lbl">Time Since Start</div>
        </div>""", unsafe_allow_html=True)


with col_right:
    st.markdown('<div class="section-head">Prediction Result</div>', unsafe_allow_html=True)

    if predict_btn:
        with st.spinner("Analyzing transaction..."):
            time.sleep(0.6)  # small UX delay for realism

        # ── Inference ──────────────────────────────────────────────────────
        input_vec = build_feature_vector(time_val, amount_val, v_vals, scaler)

        if demo_mode:
            # Smart heuristic for demo mode based on important PCA components
            # Fraud usually has highly negative V17, V14, V12, V10 and highly positive V4, V11
            anomaly_score = (
                - v_vals.get("V17", 0.0)
                - v_vals.get("V14", 0.0)
                - v_vals.get("V12", 0.0)
                - v_vals.get("V10", 0.0)
                + v_vals.get("V4", 0.0)
                + v_vals.get("V11", 0.0)
            )
            # Normalize anomaly score to a probability [0.01, 0.99]
            fraud_prob = float(np.clip(1 / (1 + np.exp(-anomaly_score + 4.0)), 0.01, 0.99))
            is_fraud = fraud_prob > 0.5
        else:
            fraud_prob  = float(model.predict_proba(input_vec)[0][1])
            is_fraud    = fraud_prob > 0.5

        safe_prob = 1 - fraud_prob

        # ── Result Banner ──────────────────────────────────────────────────
        if is_fraud:
            st.markdown(f"""
            <div class="result-fraud">
                <div class="result-title" style="color:#ef4444">⚠️ FRAUD DETECTED</div>
                <div class="result-sub">This transaction has been flagged as potentially fraudulent.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
                <div class="result-title" style="color:#10b981">✅ TRANSACTION SAFE</div>
                <div class="result-sub">No anomaly detected. Transaction appears legitimate.</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Gauge Chart — Fraud Probability ───────────────────────────────
        gauge_color = "#ef4444" if fraud_prob > 0.5 else "#10b981"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(fraud_prob * 100, 2),
            number={"suffix": "%", "font": {"size": 36, "color": gauge_color,
                                             "family": "Space Mono"}},
            delta={"reference": 50, "increasing": {"color": "#ef4444"},
                   "decreasing": {"color": "#10b981"}},
            title={"text": "Fraud Probability", "font": {"color": "#94a3b8", "size": 14}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#334155",
                         "tickfont": {"color": "#64748b"}},
                "bar":  {"color": gauge_color, "thickness": 0.28},
                "bgcolor": "#111827",
                "borderwidth": 0,
                "steps": [
                    {"range": [0,  40], "color": "rgba(16,185,129,0.1)"},
                    {"range": [40, 60], "color": "rgba(245,158,11,0.1)"},
                    {"range": [60, 100],"color": "rgba(239,68,68,0.1)"},
                ],
                "threshold": {
                    "line": {"color": "#f59e0b", "width": 3},
                    "thickness": 0.8,
                    "value": 50
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=260,
            margin=dict(l=20, r=20, t=40, b=10),
            font=dict(color="#e2e8f0")
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        # ── Score breakdown ────────────────────────────────────────────────
        s1, s2, s3 = st.columns(3)
        risk_label = "HIGH" if fraud_prob > 0.6 else "MEDIUM" if fraud_prob > 0.3 else "LOW"
        risk_color = "#ef4444" if fraud_prob > 0.6 else "#f59e0b" if fraud_prob > 0.3 else "#10b981"

        s1.markdown(f"""
        <div class="metric-card">
            <div class="metric-val" style="color:#ef4444">{fraud_prob*100:.1f}%</div>
            <div class="metric-lbl">Fraud Score</div>
        </div>""", unsafe_allow_html=True)

        s2.markdown(f"""
        <div class="metric-card">
            <div class="metric-val" style="color:#10b981">{safe_prob*100:.1f}%</div>
            <div class="metric-lbl">Safe Score</div>
        </div>""", unsafe_allow_html=True)

        s3.markdown(f"""
        <div class="metric-card">
            <div class="metric-val" style="color:{risk_color}">{risk_label}</div>
            <div class="metric-lbl">Risk Level</div>
        </div>""", unsafe_allow_html=True)

    else:
        # Placeholder state
        st.markdown("""
        <div style="background:#111827; border:1px dashed #1f2937; border-radius:12px;
                    padding:48px 32px; text-align:center; color:#475569;">
            <div style="font-size:3rem; margin-bottom:12px">🔍</div>
            <div style="font-family:'Space Mono',monospace; font-size:1rem;">
                Fill in the features<br>and click Run Fraud Analysis
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BOTTOM — Batch CSV Upload
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-head">📂 Batch Analysis — Upload CSV</div>', unsafe_allow_html=True)
st.caption("Upload a CSV with columns: Time, Amount, V1…V28  (no Class column needed)")

uploaded = st.file_uploader("Drop your CSV here", type=["csv"])

if uploaded is not None:
    df_batch = pd.read_csv(uploaded)
    required_cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
    missing = [c for c in required_cols if c not in df_batch.columns]

    if missing:
        st.error(f"❌ Missing columns: {missing}")
    else:
        df_batch = df_batch[required_cols]

        if scaler is not None:
            df_batch[["Time", "Amount"]] = scaler.transform(df_batch[["Time", "Amount"]])

        if demo_mode:
            # Demo: random predictions
            probs = np.random.beta(0.3, 3, size=len(df_batch))
        else:
            probs = model.predict_proba(df_batch.values)[:, 1]
        # Fix: pointer reset karo before reading
        uploaded.seek(0)
        df_result = pd.read_csv(uploaded)
        df_result["Fraud_Probability"] = probs
        df_result["Prediction"]        = np.where(probs > 0.5, "⚠️ Fraud", "✅ Normal")
        df_result["Risk_Level"]        = pd.cut(probs, bins=[0, 0.3, 0.6, 1.0],
                                                  labels=["🟢 Low", "🟡 Medium", "🔴 High"])

        # Summary stats
        total = len(df_result)
        fraud_count = (probs > 0.5).sum()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Transactions", f"{total:,}")
        c2.metric("Fraud Detected",     f"{fraud_count:,}", delta=f"{fraud_count/total*100:.2f}%")
        c3.metric("Normal",             f"{total-fraud_count:,}")
        c4.metric("Avg Fraud Score",    f"{probs.mean()*100:.2f}%")

        # Distribution plot
        fig_hist = px.histogram(
            x=probs * 100,
            nbins=50,
            labels={"x": "Fraud Probability (%)"},
            title="Fraud Score Distribution Across Batch",
            color_discrete_sequence=["#00d4ff"]
        )
        fig_hist.add_vline(x=50, line_dash="dash", line_color="#ef4444",
                           annotation_text="Decision Threshold (50%)")
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            height=300,
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis=dict(gridcolor="#1f2937"),
            yaxis=dict(gridcolor="#1f2937"),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        # Results table
        st.dataframe(
            df_result[["Time", "Amount", "Fraud_Probability", "Prediction", "Risk_Level"]]
            .head(200)
            .style.background_gradient(subset=["Fraud_Probability"], cmap="RdYlGn_r"),
            use_container_width=True,
            height=320
        )

        # Download button
        csv_out = df_result.to_csv(index=False).encode()
        st.download_button(
            label="⬇️ Download Full Results CSV",
            data=csv_out,
            file_name="fraud_predictions.csv",
            mime="text/csv"
        )


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.78rem;
            font-family:'Space Mono',monospace; padding:24px 0 12px;">
    FraudSentinel · XGBoost + SMOTE · PR-AUC 0.8340 · Recall 0.90 · Built with Streamlit
</div>
""", unsafe_allow_html=True)
