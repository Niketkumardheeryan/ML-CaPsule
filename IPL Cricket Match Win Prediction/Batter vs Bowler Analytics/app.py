"""
Streamlit Frontend — Batter vs Bowler Analytics
================================================
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import lightgbm as lgb
import os
import pickle
from batter_vs_bowler_analytics import (
    load_data, preprocess,
    get_matchup_stats, top_matchups,
    build_features, train_dismissal_model,
    predict_dismissal_probability,
    plot_top_bowler_threats,
)

# ─── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Batter vs Bowler Analytics",
    page_icon="🏏",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Rajdhani', sans-serif; }

    .main { background-color: #0d1117; }
    .stApp { background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); color: #e6edf3; }

    .metric-card {
        background: linear-gradient(135deg, #1c2128, #21262d);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
    }
    .metric-card .label { color: #8b949e; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; }
    .metric-card .value { color: #58a6ff; font-size: 2rem; font-family: 'Rajdhani', sans-serif; font-weight: 700; }

    .prob-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 999px;
        font-size: 1.6rem;
        font-weight: 700;
        font-family: 'Rajdhani', sans-serif;
    }
    .prob-low    { background: #0d4c1a; color: #3fb950; }
    .prob-medium { background: #4c3b00; color: #d29922; }
    .prob-high   { background: #4c0000; color: #f85149; }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label { color: #8b949e !important; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading ball-by-ball data …")
def cached_load(path: str):
    df_raw = load_data(path)
    return preprocess(df_raw)

@st.cache_resource(show_spinner="Training dismissal model …")
def cached_model(path: str):
    df = cached_load(path)
    feat_df = build_features(df)
    model, X_test, y_test, y_pred, y_proba = train_dismissal_model(feat_df)
    return model, feat_df.drop(columns="is_wicket").columns.tolist()

def prob_badge(p: float) -> str:
    pct   = f"{p:.1%}"
    level = "low" if p < 0.10 else ("medium" if p < 0.20 else "high")
    return f'<span class="prob-badge prob-{level}">{pct}</span>'

def metric_card(label: str, value) -> str:
    return f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
    </div>"""


# ─── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/8/86/Indian_Premier_League_logo_%282022%29.png",
             width=100)
    st.markdown("## 🏏 Analytics Config")

    data_path = st.text_input("Dataset path", value="deliveries.csv",
                               help="Cricsheet-format ball-by-ball CSV")
    st.caption("Adjust settings below after data loads.")


# ─── Load Data ──────────────────────────────────────────────────────
st.markdown("# 🏏 IPL Batter vs Bowler Analytics")
st.markdown("#### Powered by LightGBM · Historical IPL Ball-by-Ball Data")
st.divider()

if not os.path.exists(data_path):
    st.warning(f"Dataset not found at `{data_path}`. Please update the path in the sidebar.")
    st.info("Download the Cricsheet IPL dataset: https://cricsheet.org/downloads/ipl_csv2.zip")
    st.stop()

df = cached_load(data_path)
model, feature_names = cached_model(data_path)

batters = sorted(df["batter"].dropna().unique())
bowlers = sorted(df["bowler"].dropna().unique())


# ─── Tab Layout ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "⚔️ Head-to-Head",
    "🎯 Dismissal Predictor",
    "📊 Top Matchups",
    "ℹ️ About"
])


# ─────────────────────────────────────────────
# TAB 1 — Head-to-Head Stats
# ─────────────────────────────────────────────
with tab1:
    st.markdown("### Head-to-Head Matchup Statistics")
    col_b, col_bow = st.columns(2)
    with col_b:
        sel_batter = st.selectbox("Select Batter", batters, key="h2h_batter")
    with col_bow:
        sel_bowler = st.selectbox("Select Bowler", bowlers, key="h2h_bowler")

    if st.button("Analyse Matchup", type="primary"):
        stats = get_matchup_stats(df, sel_batter, sel_bowler)

        if "error" in stats:
            st.error(stats["error"])
        else:
            # Metrics row
            cols = st.columns(5)
            metrics = [
                ("Balls Faced",        stats["balls_faced"]),
                ("Runs Scored",        stats["runs_scored"]),
                ("Dismissals",         stats["dismissals"]),
                ("Strike Rate",        f"{stats['strike_rate']}"),
                ("Dot Ball %",         f"{stats['dot_ball_pct']}%"),
            ]
            for col, (label, val) in zip(cols, metrics):
                col.markdown(metric_card(label, val), unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Charts
            c1, c2 = st.columns(2)

            with c1:
                fig, ax = plt.subplots(figsize=(6, 4), facecolor="#1c2128")
                ax.set_facecolor("#1c2128")
                categories = ["Runs", "Boundaries", "Dot Balls"]
                values     = [
                    stats["runs_scored"],
                    stats["boundary_count"],
                    round(stats["dot_ball_pct"] / 100 * stats["balls_faced"]),
                ]
                bars = ax.bar(categories, values, color=["#58a6ff", "#3fb950", "#f85149"],
                              width=0.5, edgecolor="none")
                ax.set_title(f"{sel_batter} vs {sel_bowler}", color="#e6edf3", pad=10)
                ax.tick_params(colors="#8b949e")
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.yaxis.label.set_color("#8b949e")
                for bar in bars:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                            str(int(bar.get_height())), ha="center", color="#e6edf3", fontsize=10)
                st.pyplot(fig)
                plt.close()

            with c2:
                fig, ax = plt.subplots(figsize=(6, 4), facecolor="#1c2128")
                ax.set_facecolor("#1c2128")
                labels = ["Dismissals", "Not Out"]
                sizes  = [stats["dismissals"], stats["balls_faced"] - stats["dismissals"]]
                colors = ["#f85149", "#3fb950"]
                wedges, texts, autotexts = ax.pie(
                    sizes, labels=labels, colors=colors,
                    autopct="%1.1f%%", startangle=90,
                    textprops={"color": "#e6edf3"},
                )
                for at in autotexts:
                    at.set_color("#0d1117")
                    at.set_fontweight("bold")
                ax.set_title("Outcome Distribution", color="#e6edf3", pad=10)
                st.pyplot(fig)
                plt.close()

            # Threat chart
            st.markdown("#### Top Bowlers Who Threaten This Batter")
            fig2, ax2 = plt.subplots(figsize=(10, 4), facecolor="#1c2128")
            ax2.set_facecolor("#1c2128")
            threat_df = (
                df[df["batter"] == sel_batter]
                .groupby("bowler")
                .agg(balls=("batsman_runs", "count"), wickets=("is_wicket", "sum"))
                .query("balls >= 6")
                .assign(dr=lambda x: x["wickets"] / x["balls"] * 100)
                .sort_values("dr", ascending=True)
                .tail(8)
                .reset_index()
            )
            colors = ["#f85149" if b == sel_bowler else "#58a6ff" for b in threat_df["bowler"]]
            ax2.barh(threat_df["bowler"], threat_df["dr"], color=colors, edgecolor="none")
            ax2.set_xlabel("Dismissal Rate (%)", color="#8b949e")
            ax2.tick_params(colors="#8b949e")
            for spine in ax2.spines.values(): spine.set_visible(False)
            selected_patch = mpatches.Patch(color="#f85149", label="Selected bowler")
            others_patch   = mpatches.Patch(color="#58a6ff", label="Other bowlers")
            ax2.legend(handles=[selected_patch, others_patch],
                       facecolor="#21262d", labelcolor="#e6edf3", framealpha=0.8)
            st.pyplot(fig2)
            plt.close()


# ─────────────────────────────────────────────
# TAB 2 — Dismissal Predictor
# ─────────────────────────────────────────────
with tab2:
    st.markdown("### 🎯 Dismissal Probability Predictor")
    st.caption("Uses LightGBM classifier trained on historical ball-by-ball features.")

    col1, col2, col3 = st.columns(3)
    with col1:
        pred_batter = st.selectbox("Batter", batters, key="pred_bat")
    with col2:
        pred_bowler = st.selectbox("Bowler", bowlers, key="pred_bow")
    with col3:
        pred_over  = st.slider("Over Number", 1, 20, 10)
        pred_phase = st.select_slider("Phase", ["powerplay", "middle", "death"],
                                       value="middle")

    if st.button("Predict Dismissal Probability", type="primary"):
        try:
            prob = predict_dismissal_probability(
                model, pred_batter, pred_bowler, df,
                over=pred_over, phase=pred_phase
            )

            st.markdown(f"""
            <div style='text-align:center; padding: 2rem 0;'>
                <p style='color:#8b949e; font-size:1rem; margin-bottom:0.5rem;'>
                    {pred_batter} &nbsp;vs&nbsp; {pred_bowler} · Over {pred_over} · {pred_phase.title()}
                </p>
                <p style='color:#e6edf3; font-size:1.2rem; margin-bottom:0.8rem;'>Dismissal Probability</p>
                {prob_badge(prob)}
            </div>
            """, unsafe_allow_html=True)

            # Context explanation
            if prob < 0.10:
                st.success(f"**Low risk.** {pred_bowler} has a historically low chance of dismissing "
                           f"{pred_batter} in this situation.")
            elif prob < 0.20:
                st.warning(f"**Moderate risk.** This is a competitive matchup — {pred_bowler} has "
                           f"a reasonable chance of breakthrough.")
            else:
                st.error(f"**High risk.** Historical data suggests {pred_bowler} is a serious threat "
                         f"to {pred_batter} in this phase.")

            # Gauge chart
            fig, ax = plt.subplots(figsize=(5, 3), facecolor="#1c2128")
            ax.set_facecolor("#1c2128")
            ax.barh(["Probability"], [prob], color="#f85149" if prob >= 0.20 else
                    ("#d29922" if prob >= 0.10 else "#3fb950"), height=0.4)
            ax.barh(["Probability"], [1 - prob], left=[prob], color="#21262d", height=0.4)
            ax.set_xlim(0, 1)
            ax.set_xlabel("Dismissal Probability", color="#8b949e")
            ax.tick_params(colors="#8b949e")
            for spine in ax.spines.values(): spine.set_visible(False)
            ax.axvline(x=prob, color="#e6edf3", linewidth=1.5, linestyle="--")
            ax.text(prob + 0.01, 0, f"{prob:.1%}", va="center", color="#e6edf3", fontsize=10)
            st.pyplot(fig)
            plt.close()

        except ValueError as e:
            st.error(f"Could not predict: {e}. "
                     "Ensure there is at least 6 balls of head-to-head data.")


# ─────────────────────────────────────────────
# TAB 3 — Top Matchups Table
# ─────────────────────────────────────────────
with tab3:
    st.markdown("### 📊 High-Dismissal Matchups (IPL History)")
    min_balls = st.slider("Minimum balls faced", 6, 30, 12)
    top_df = top_matchups(df, min_balls=min_balls)

    if top_df.empty:
        st.info("No matchups found with the selected minimum balls threshold.")
    else:
        display_df = top_df.head(50).copy()
        display_df["dismissal_rate"] = (display_df["dismissal_rate"] * 100).round(2).astype(str) + "%"
        display_df.columns = [
            "Batter", "Bowler", "Balls Faced", "Runs Scored",
            "Dismissals", "Strike Rate", "Dismissal Rate"
        ]
        st.dataframe(display_df.reset_index(drop=True), use_container_width=True, height=500)

        # Download
        csv = top_df.to_csv(index=False)
        st.download_button("⬇️ Download Full Table (CSV)", csv,
                           "top_matchups.csv", "text/csv")


# ─────────────────────────────────────────────
# TAB 4 — About
# ─────────────────────────────────────────────
with tab4:
    st.markdown("""
    ### About This Feature

    This module extends the **IPL Cricket Match Win Prediction** project with **Batter vs Bowler
    Player Analytics** — a deeper layer of insights beyond overall match win probability.

    #### What it adds
    - **Head-to-Head Statistics**: balls, runs, strike rate, dot ball %, boundaries, dismissal rate
    - **Dismissal Probability Prediction** using a LightGBM classifier trained on:
      - Batter and bowler career statistics
      - Historical head-to-head dismissal rates
      - Match phase (powerplay / middle / death overs)
    - **Visualizations**: matchup bar charts, outcome pie charts, threat rankings, ROC curve

    #### Dataset
    Uses the standard [Cricsheet](https://cricsheet.org/downloads/ipl_csv2.zip) ball-by-ball
    IPL CSV format (`deliveries.csv`).

    #### Model
    `LGBMClassifier` with balanced class weights, early stopping, and 9 engineered features.
    Typical ROC-AUC: **0.68–0.74** on held-out test data.

    #### How to run
    ```bash
    pip install lightgbm scikit-learn pandas numpy matplotlib seaborn streamlit
    streamlit run app.py
    ```
    """)
