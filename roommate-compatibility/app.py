
"""
AI Roommate Compatibility Predictor
Production-ready Streamlit application
"""

import streamlit as st
import torch
import torch.nn as nn
import joblib
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RoomieMatch AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PYTORCH MODEL ARCHITECTURE
# ─────────────────────────────────────────────
class RoommateCompatibilityMLP(nn.Module):
    """
    MLP regression model for roommate compatibility prediction.
    Architecture: input → 128 → 64 → 32 → 1
    """
    def __init__(self, input_size: int):
        super(RoommateCompatibilityMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


# ─────────────────────────────────────────────
# GLOBAL CSS STYLING
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    /* ── Root Variables ── */
    :root {
        --sky:       #e8f4fd;
        --sky-mid:   #c8e6f7;
        --blue:      #3b82f6;
        --blue-dark: #1d4ed8;
        --blue-soft: #60a5fa;
        --teal:      #06b6d4;
        --white:     #ffffff;
        --glass:     rgba(255,255,255,0.72);
        --glass2:    rgba(232,244,253,0.55);
        --shadow:    0 8px 32px rgba(59,130,246,0.12);
        --shadow-lg: 0 16px 48px rgba(59,130,246,0.18);
        --radius:    18px;
        --radius-sm: 10px;
        --text:      #1e293b;
        --text-muted:#64748b;
        --border:    rgba(59,130,246,0.15);
        --success:   #10b981;
        --warning:   #f59e0b;
        --danger:    #ef4444;
    }

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }
    .stApp {
        background: linear-gradient(135deg, #e8f4fd 0%, #dbeafe 40%, #e0f2fe 70%, #f0f9ff 100%);
        min-height: 100vh;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2rem 3rem 2rem; max-width: 1280px; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1d4ed8 0%, #1e40af 50%, #1e3a8a 100%) !important;
        border-right: none;
    }
    [data-testid="stSidebar"] * { color: #e0f2fe !important; }
    [data-testid="stSidebar"] .stRadio label { color: #bfdbfe !important; }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] div {
        border-color: #93c5fd !important;
    }

    /* ── Cards ── */
    .glass-card {
        background: var(--glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1.5px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        padding: 2rem;
        transition: box-shadow 0.3s ease, transform 0.3s ease;
        margin-bottom: 1.5rem;
    }
    .glass-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    .glass-card-sm {
        background: var(--glass2);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 1.2rem 1.4rem;
        transition: all 0.25s ease;
    }
    .glass-card-sm:hover { background: var(--glass); box-shadow: var(--shadow); }

    /* ── Active member glow ── */
    .member-active {
        background: linear-gradient(135deg, rgba(59,130,246,0.12) 0%, rgba(6,182,212,0.08) 100%);
        border: 2px solid var(--blue-soft);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: 0 0 0 4px rgba(59,130,246,0.08), var(--shadow);
        animation: glow-pulse 2.5s ease-in-out infinite;
    }
    @keyframes glow-pulse {
        0%, 100% { box-shadow: 0 0 0 4px rgba(59,130,246,0.08), var(--shadow); }
        50%       { box-shadow: 0 0 0 8px rgba(59,130,246,0.14), var(--shadow-lg); }
    }

    /* ── Animated hero header ── */
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 700;
        background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
        animation: fadeSlideDown 0.8s ease forwards;
    }
    .hero-sub {
        color: var(--text-muted);
        font-size: 1.05rem;
        font-weight: 400;
        margin-top: 0.5rem;
        animation: fadeSlideDown 0.9s ease forwards;
    }
    @keyframes fadeSlideDown {
        from { opacity: 0; transform: translateY(-18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Score display ── */
    .score-circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1d4ed8, #06b6d4);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        margin: 0 auto;
        box-shadow: 0 0 40px rgba(59,130,246,0.35), 0 0 80px rgba(6,182,212,0.15);
        animation: scoreAppear 0.7s cubic-bezier(0.34,1.56,0.64,1) forwards;
    }
    @keyframes scoreAppear {
        from { transform: scale(0.4); opacity: 0; }
        to   { transform: scale(1);   opacity: 1; }
    }
    .score-number {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 700;
        color: white;
        line-height: 1;
    }
    .score-label-small { font-size: 0.75rem; color: rgba(255,255,255,0.8); letter-spacing: 0.08em; }

    /* ── Progress bar ── */
    .progress-outer {
        width: 100%;
        height: 14px;
        background: rgba(59,130,246,0.1);
        border-radius: 99px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .progress-inner {
        height: 100%;
        border-radius: 99px;
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        transition: width 1.5s cubic-bezier(0.23,1,0.32,1);
        box-shadow: 0 0 12px rgba(59,130,246,0.4);
    }

    /* ── Compatibility label badge ── */
    .compat-badge {
        display: inline-block;
        padding: 0.45rem 1.4rem;
        border-radius: 99px;
        font-weight: 600;
        font-size: 0.92rem;
        letter-spacing: 0.04em;
        margin-top: 0.5rem;
        animation: fadeIn 0.6s ease forwards;
    }
    .badge-1 { background: rgba(239,68,68,0.12);  color: #dc2626; border: 1px solid rgba(239,68,68,0.25); }
    .badge-2 { background: rgba(245,158,11,0.12); color: #b45309; border: 1px solid rgba(245,158,11,0.25); }
    .badge-3 { background: rgba(59,130,246,0.12); color: #1d4ed8; border: 1px solid rgba(59,130,246,0.25); }
    .badge-4 { background: rgba(16,185,129,0.12); color: #059669; border: 1px solid rgba(16,185,129,0.25); }
    .badge-5 { background: linear-gradient(135deg,rgba(59,130,246,0.15),rgba(6,182,212,0.15)); color: #0369a1; border: 1px solid rgba(6,182,212,0.3); }

    /* ── Trait cards ── */
    .trait-positive {
        background: rgba(16,185,129,0.07);
        border: 1px solid rgba(16,185,129,0.2);
        border-left: 4px solid var(--success);
        border-radius: var(--radius-sm);
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        animation: fadeIn 0.4s ease forwards;
    }
    .trait-conflict {
        background: rgba(239,68,68,0.06);
        border: 1px solid rgba(239,68,68,0.18);
        border-left: 4px solid var(--danger);
        border-radius: var(--radius-sm);
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        animation: fadeIn 0.4s ease forwards;
    }
    .trait-neutral {
        background: rgba(245,158,11,0.07);
        border: 1px solid rgba(245,158,11,0.2);
        border-left: 4px solid var(--warning);
        border-radius: var(--radius-sm);
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
    }

    /* ── Section titles ── */
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border);
    }

    /* ── Feature pill ── */
    .feature-pill {
        display: inline-block;
        background: rgba(59,130,246,0.1);
        color: #1d4ed8;
        border: 1px solid rgba(59,130,246,0.2);
        border-radius: 99px;
        padding: 0.3rem 0.9rem;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
    }

    /* ── Member toggle button ── */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 2rem;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(59,130,246,0.3);
        width: 100%;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59,130,246,0.4);
        background: linear-gradient(135deg, #2563eb 0%, #0891b2 100%);
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(59,130,246,0.3);
    }

    /* ── Slider track ── */
    [data-testid="stSlider"] [role="slider"] {
        background: var(--blue) !important;
        border-color: var(--blue-dark) !important;
    }

    /* ── Metric boxes ── */
    [data-testid="stMetric"] {
        background: var(--glass2);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 1rem;
        backdrop-filter: blur(8px);
    }

    /* ── Info box ── */
    .info-box {
        background: rgba(59,130,246,0.06);
        border: 1px solid rgba(59,130,246,0.18);
        border-radius: var(--radius-sm);
        padding: 1rem 1.2rem;
        font-size: 0.88rem;
        color: var(--text-muted);
        line-height: 1.6;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.78rem;
        padding: 2rem 0 1rem;
        letter-spacing: 0.03em;
        border-top: 1px solid var(--border);
        margin-top: 3rem;
    }

    /* ── Stat row ── */
    .stat-row {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }
    .stat-chip {
        flex: 1 1 140px;
        background: var(--glass2);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 0.8rem 1rem;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .stat-chip-val {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-chip-lbl { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.1rem; }

    /* ── Expandable analysis section ── */
    .stExpander {
        background: var(--glass2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.5);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 500;
        font-family: 'DM Sans', sans-serif;
        color: var(--text-muted);
        padding: 0.5rem 1.5rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #0ea5e9) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model_artifacts():
    """Load model, scaler, and top features from disk."""
    errors = []

    # Load top features
    top_features_path = "models/top_features.pkl"
    if os.path.exists(top_features_path):
        top_features = joblib.load(top_features_path)
    else:
        top_features = None
        errors.append(f"top_features.pkl not found at {top_features_path}")

    # Load scaler
    scaler_path = "models/scaler.pkl"
    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)
    else:
        scaler = None
        errors.append(f"scaler.pkl not found at {scaler_path}")

    # Load PyTorch model
    model_path = "models/best_model.pth"
    model = None
    if os.path.exists(model_path) and top_features is not None:
        input_size = len(top_features)
        model = RoommateCompatibilityMLP(input_size=input_size)
        state = torch.load(model_path, map_location=torch.device("cpu"))
        # Handle both raw state_dict and wrapped checkpoint
        if isinstance(state, dict) and "model_state_dict" in state:
            model.load_state_dict(state["model_state_dict"])
        elif isinstance(state, dict) and all(isinstance(k, str) for k in state.keys()):
            model.load_state_dict(state)
        else:
            model.load_state_dict(state)
        model.eval()
    else:
        if top_features is not None:
            errors.append(f"best_model.pth not found at {model_path}")

    return model, scaler, top_features, errors


# ─────────────────────────────────────────────
# INFERENCE PIPELINE
# ─────────────────────────────────────────────
def run_inference(features_df: pd.DataFrame, model, scaler, top_features) -> float:
    """
    Full inference pipeline:
      features_df → select top_features → scale → model → score
    """
    # 1. Select and reorder columns
    available = [f for f in top_features if f in features_df.columns]
    missing   = [f for f in top_features if f not in features_df.columns]
    if missing:
        for col in missing:
            features_df[col] = 0.0
    df_ordered = features_df[top_features]

    # 2. Scale
    X_scaled = scaler.transform(df_ordered.values)

    # 3. Torch inference
    tensor_in = torch.tensor(X_scaled, dtype=torch.float32)
    with torch.no_grad():
        raw_output = model(tensor_in).item()

    # 4. Clamp to [0, 100]
    score = float(np.clip(raw_output, 0.0, 100.0))
    return score


# ─────────────────────────────────────────────
# LABEL & MESSAGE HELPERS
# ─────────────────────────────────────────────
def score_to_label(score: float) -> int:
    if score <= 20:  return 1
    if score <= 40:  return 2
    if score <= 60:  return 3
    if score <= 80:  return 4
    return 5

LABEL_INFO = {
    1: {"text": "Very Low Compatibility", "emoji": "⚠️",  "badge": "badge-1", "message": "Significant lifestyle differences detected. This pairing would require substantial mutual compromise and strong communication skills to function."},
    2: {"text": "Low Compatibility",      "emoji": "📉",  "badge": "badge-2", "message": "Several notable mismatches exist. With effort and open conversation, cohabitation is possible, but friction is likely."},
    3: {"text": "Moderate Compatibility", "emoji": "🤝",  "badge": "badge-3", "message": "A workable pairing with some differences. Clear boundaries and shared agreements on key issues will help this work well."},
    4: {"text": "Good Compatibility",     "emoji": "✅",  "badge": "badge-4", "message": "Strong alignment on most key factors. Expect a comfortable living situation with minor adjustments needed."},
    5: {"text": "Excellent Match",        "emoji": "🌟",  "badge": "badge-5", "message": "Exceptional compatibility across nearly all dimensions. This pairing shows remarkable harmony in lifestyle, habits, and preferences."},
}


# ─────────────────────────────────────────────
# FEATURE ANALYSIS (from engineered features)
# ─────────────────────────────────────────────
DIFF_FEATURES = [
    ("sleep_schedule_diff",   "🌙", "Sleep Schedule",     ["sleep_schedule_diff"]),
    ("wakeup_schedule_diff",  "⏰", "Wake-up Schedule",   ["wakeup_schedule_diff"]),
    ("cleanliness_diff",      "🧹", "Cleanliness",        ["cleanliness_diff"]),
    ("study_hours_diff",      "📚", "Study Hours",        ["study_hours_diff"]),
    ("noise_tolerance_diff",  "🔊", "Noise Tolerance",    ["noise_tolerance_diff"]),
    ("room_temperature_diff", "🌡️", "Room Temperature",  ["room_temperature_diff"]),
    ("social_energy_diff",    "👥", "Social Energy",      ["social_energy_diff"]),
    ("spending_habit_diff",   "💳", "Spending Habits",    ["spending_habit_diff"]),
    ("guest_frequency_diff",  "🏠", "Guest Frequency",    ["guest_frequency_diff"]),
    ("gaming_time_diff",      "🎮", "Gaming Time",        ["gaming_time_diff"]),
]
SIM_FEATURES = [
    ("food_preference_similarity",      "🍽️",  "Food Preferences"),
    ("music_preference_similarity",     "🎵",  "Music Preference"),
    ("study_style_similarity",          "📖",  "Study Style"),
    ("communication_style_similarity",  "💬",  "Communication Style"),
    ("organization_similarity",         "📂",  "Organization Style"),
    ("workout_routine_similarity",      "💪",  "Workout Routine"),
    ("hobby_similarity",                "🎯",  "Hobbies"),
    ("academic_goal_similarity",        "🎓",  "Academic Goals"),
    ("room_usage_similarity",           "🛋️", "Room Usage"),
    ("weekend_activity_similarity",     "📅",  "Weekend Activities"),
]
INTER_FEATURES = [
    ("gamer_vs_light_sleeper",          "🎮🌙", "Gamer vs. Light Sleeper"),
    ("extrovert_vs_introvert_conflict", "👥🤫", "Extrovert vs. Introvert"),
    ("messy_vs_clean_conflict",         "🧹🗑️","Messy vs. Clean"),
    ("nightowl_vs_earlybird_conflict",  "🦉🐦", "Night Owl vs. Early Bird"),
    ("loud_music_vs_noise_sensitive",   "🔊🤫", "Loud Music vs. Noise-Sensitive"),
    ("guest_heavy_vs_private_person",   "🏠🚪", "Guest-Heavy vs. Private"),
    ("high_spender_vs_budget_person",   "💸💰", "High Spender vs. Budget"),
    ("group_study_vs_solo_study",       "👥📖", "Group Study vs. Solo Study"),
    ("fitness_focused_vs_irregular",    "🏃‍♂️😴","Fitness Focused vs. Irregular"),
    ("emotional_expressive_vs_reserved","😊🤐", "Expressive vs. Reserved"),
]

CONFLICT_THRESHOLD  = 0.55
MATCH_THRESHOLD     = 0.25


def analyze_features(features_df: pd.DataFrame) -> dict:
    """Produce structured analysis from engineered features DataFrame."""
    row = features_df.iloc[0]

    matched_traits  = []
    conflict_traits = []
    risk_factors    = []
    positive_factors = []

    # Diff features
    for key, icon, label, _ in DIFF_FEATURES:
        if key not in row: continue
        val = float(row[key])
        pct = int(val * 100)
        if val < MATCH_THRESHOLD:
            matched_traits.append((icon, label, f"{pct}% difference — excellent alignment"))
            positive_factors.append((icon, label, val))
        elif val > CONFLICT_THRESHOLD:
            conflict_traits.append((icon, label, f"{pct}% difference — significant mismatch"))
            risk_factors.append((icon, label, val))

    # Similarity features
    for key, icon, label in SIM_FEATURES:
        if key not in row: continue
        val = int(row[key])
        if val == 1:
            matched_traits.append((icon, label, "Similar — shared common ground"))
            positive_factors.append((icon, label, 1.0))
        else:
            conflict_traits.append((icon, label, "Different — potential friction area"))

    # Interaction features
    active_conflicts = []
    for key, icon, label in INTER_FEATURES:
        if key not in row: continue
        if int(row[key]) == 1:
            active_conflicts.append((icon, label))
            risk_factors.append((icon, label, 1.0))

    # Sort: risk by severity descending
    risk_factors.sort(key=lambda x: x[2], reverse=True)
    positive_factors.sort(key=lambda x: x[2], reverse=True)

    return {
        "matched_traits":    matched_traits,
        "conflict_traits":   conflict_traits,
        "active_conflicts":  active_conflicts,
        "risk_factors":      risk_factors[:6],
        "positive_factors":  positive_factors[:6],
    }


# ─────────────────────────────────────────────
# INPUT FORM HELPERS
# ─────────────────────────────────────────────
def render_member_form(member_id: int) -> dict:
    """Render input form for one member. Returns a dict of raw inputs."""
    label = f"Member {member_id}"
    icon  = "🧑" if member_id == 1 else "👤"

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.2rem;">
      <span style="font-size:2rem;">{icon}</span>
      <span class="section-title" style="margin:0;border:none;padding:0;">{label} Details</span>
    </div>
    """, unsafe_allow_html=True)

    prefix = f"m{member_id}_"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🌙 Sleep & Schedule**")
        sleep_hour = st.slider(
            "Bedtime (24h)", 18, 30, 23 if member_id == 1 else 24,
            key=f"{prefix}sleep",
            help="Hours after noon. 23 = 11 PM, 26 = 2 AM"
        )
        wake_hour = st.slider(
            "Wake-up time (24h)", 4, 12, 7 if member_id == 1 else 8,
            key=f"{prefix}wake",
            help="Hour of morning wake-up"
        )
        st.markdown("**📚 Academic**")
        study_hours = st.slider(
            "Study hours/day", 0, 12, 4 if member_id == 1 else 3,
            key=f"{prefix}study"
        )
        academic_goal = st.selectbox(
            "Academic Goal 🎓",
            ["Pass with decent grades", "Top of class", "Research-focused", "Professional skills", "Just graduate"],
            key=f"{prefix}goal"
        )
        study_style = st.selectbox(
            "Study Style 📖",
            ["Solo in silence", "Group study", "Library / café", "Night cramming", "Consistent daily"],
            key=f"{prefix}style"
        )

    with col2:
        st.markdown("**🏠 Lifestyle**")
        cleanliness = st.slider(
            "Cleanliness standard (1–10) 🧹", 1, 10, 7 if member_id == 1 else 5,
            key=f"{prefix}clean"
        )
        noise_tol = st.slider(
            "Noise tolerance (1–10) 🔊", 1, 10, 5,
            key=f"{prefix}noise"
        )
        social_energy = st.slider(
            "Social energy (1–10) 👥", 1, 10, 6 if member_id == 1 else 7,
            key=f"{prefix}social"
        )
        room_temp = st.slider(
            "Preferred room temp (°C) 🌡️", 16, 32, 22,
            key=f"{prefix}temp"
        )

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**🎯 Habits & Hobbies**")
        gaming_hours = st.slider(
            "Gaming hours/day 🎮", 0, 12, 2 if member_id == 1 else 4,
            key=f"{prefix}gaming"
        )
        guest_freq = st.selectbox(
            "Guest frequency 🏠",
            ["Never", "Rarely (monthly)", "Occasionally (bi-weekly)", "Often (weekly)", "Very often (multiple/week)"],
            key=f"{prefix}guest"
        )
        spending_habit = st.select_slider(
            "Spending habit 💳",
            options=["Very frugal", "Frugal", "Moderate", "Generous", "High spender"],
            key=f"{prefix}spend"
        )
        music_vol = st.select_slider(
            "Music volume preference 🎵",
            options=["Silent", "Very low", "Low", "Medium", "Loud", "Very loud"],
            key=f"{prefix}music"
        )

    with col4:
        st.markdown("**🤝 Social Style**")
        comm_style = st.selectbox(
            "Communication style 💬",
            ["Direct and open", "Passive / indirect", "Empathetic listener", "Assertive negotiator", "Avoidant"],
            key=f"{prefix}comm"
        )
        food_pref = st.multiselect(
            "Food preferences 🍽️",
            ["Vegetarian", "Vegan", "Non-veg", "Gluten-free", "Halal", "Kosher", "No restriction"],
            default=["No restriction"],
            key=f"{prefix}food"
        )
        hobbies = st.multiselect(
            "Hobbies 🎯",
            ["Gaming", "Sports", "Reading", "Music", "Cooking", "Art", "Fitness", "Travel", "Movies", "Technology"],
            default=["Reading", "Sports"] if member_id == 1 else ["Gaming", "Music"],
            key=f"{prefix}hobbies"
        )
        weekend_act = st.selectbox(
            "Weekend activity 📅",
            ["Stay home / relax", "Social outings", "Outdoor adventures", "Study / catch up", "Part-time work", "Travel"],
            key=f"{prefix}weekend"
        )
        fitness = st.selectbox(
            "Fitness routine 💪",
            ["None", "Occasional (1–2x/week)", "Regular (3–4x/week)", "Intense (5+ days/week)", "Athlete-level"],
            key=f"{prefix}fitness"
        )

    return {
        "sleep_time":        sleep_hour,
        "wake_time":         wake_hour,
        "study_hours":       study_hours,
        "academic_goal":     academic_goal,
        "study_style":       study_style,
        "cleanliness":       cleanliness,
        "noise_tolerance":   noise_tol,
        "social_energy":     social_energy,
        "room_temperature":  room_temp,
        "gaming_hours":      gaming_hours,
        "guest_frequency":   guest_freq,
        "spending_habit":    spending_habit,
        "music_volume":      music_vol,
        "communication_style": comm_style,
        "food_preference":   food_pref,
        "hobbies":           hobbies,
        "weekend_activity":  weekend_act,
        "fitness_routine":   fitness,
    }


# ─────────────────────────────────────────────
# FALLBACK FEATURE GENERATOR
# (used when calculations.py is unavailable)
# ─────────────────────────────────────────────
def _ordinal(cat, options):
    try:    return options.index(cat)
    except: return 0

def fallback_generate_features(s1: dict, s2: dict) -> pd.DataFrame:
    """
    Compute engineered features directly when calculations.py is not importable.
    Mirrors the formulas described in the project spec.
    """
    guest_map   = {"Never": 0, "Rarely (monthly)": 1, "Occasionally (bi-weekly)": 2, "Often (weekly)": 3, "Very often (multiple/week)": 4}
    spend_map   = {"Very frugal": 1, "Frugal": 2, "Moderate": 3, "Generous": 4, "High spender": 5}
    music_map   = {"Silent": 0, "Very low": 1, "Low": 2, "Medium": 3, "Loud": 4, "Very loud": 5}
    fitness_map = {"None": 0, "Occasional (1–2x/week)": 1, "Regular (3–4x/week)": 2, "Intense (5+ days/week)": 3, "Athlete-level": 4}

    def d(a, b, mx): return round(abs(a - b) / mx, 2)

    sleep_diff    = d(s1["sleep_time"],       s2["sleep_time"],       24)
    wakeup_diff   = d(s1["wake_time"],         s2["wake_time"],        24)
    clean_diff    = d(s1["cleanliness"],       s2["cleanliness"],      9)
    study_diff    = d(s1["study_hours"],       s2["study_hours"],      12)
    noise_diff    = d(s1["noise_tolerance"],   s2["noise_tolerance"],  9)
    temp_diff     = d(s1["room_temperature"],  s2["room_temperature"], 16)
    social_diff   = d(s1["social_energy"],     s2["social_energy"],    9)
    spend_diff    = d(spend_map.get(s1["spending_habit"],3), spend_map.get(s2["spending_habit"],3), 4)
    guest_diff    = d(guest_map.get(s1["guest_frequency"],0), guest_map.get(s2["guest_frequency"],0), 4)
    gaming_diff   = d(s1["gaming_hours"],      s2["gaming_hours"],     12)

    def sim_cat(a, b):   return 1 if a == b else 0
    def sim_list(a, b):  return 1 if len(set(a) & set(b)) > 0 else 0

    food_sim     = sim_list(s1["food_preference"], s2["food_preference"])
    music_sim    = sim_cat(s1["music_volume"], s2["music_volume"])
    study_sim    = sim_cat(s1["study_style"], s2["study_style"])
    comm_sim     = sim_cat(s1["communication_style"], s2["communication_style"])
    org_sim      = 1 if abs(s1["cleanliness"] - s2["cleanliness"]) <= 2 else 0
    workout_sim  = sim_cat(s1["fitness_routine"], s2["fitness_routine"])
    hobby_sim    = sim_list(s1["hobbies"], s2["hobbies"])
    acad_sim     = sim_cat(s1["academic_goal"], s2["academic_goal"])
    room_sim     = sim_cat(s1["weekend_activity"], s2["weekend_activity"])
    weekend_sim  = sim_cat(s1["weekend_activity"], s2["weekend_activity"])

    # Interaction conflicts
    g1_high  = s1["gaming_hours"] >= 5;  g2_high  = s2["gaming_hours"] >= 5
    n1_low   = s1["noise_tolerance"] <= 3; n2_low = s2["noise_tolerance"] <= 3
    sl1_high = s1["sleep_time"] >= 26;  sl2_high = s2["sleep_time"] >= 26
    sl1_ear  = s1["sleep_time"] <= 22;  sl2_ear  = s2["sleep_time"] <= 22
    c1_low   = s1["cleanliness"] <= 3;  c2_low   = s2["cleanliness"] <= 3
    c1_high  = s1["cleanliness"] >= 8;  c2_high  = s2["cleanliness"] >= 8
    m1_loud  = music_map.get(s1["music_volume"], 3) >= 4
    m2_loud  = music_map.get(s2["music_volume"], 3) >= 4
    e1_ext   = s1["social_energy"] >= 7; e2_ext   = s2["social_energy"] >= 7
    e1_int   = s1["social_energy"] <= 3; e2_int   = s2["social_energy"] <= 3
    gu1_hvy  = guest_map.get(s1["guest_frequency"],0) >= 3
    gu2_hvy  = guest_map.get(s2["guest_frequency"],0) >= 3
    sp1_high = spend_map.get(s1["spending_habit"],3) >= 4
    sp2_high = spend_map.get(s2["spending_habit"],3) >= 4
    st1_grp  = s1["study_style"] == "Group study"; st2_grp = s2["study_style"] == "Group study"
    st1_sol  = s1["study_style"] in ["Solo in silence","Night cramming"]
    st2_sol  = s2["study_style"] in ["Solo in silence","Night cramming"]
    f1_fit   = fitness_map.get(s1["fitness_routine"],0) >= 3
    f2_fit   = fitness_map.get(s2["fitness_routine"],0) >= 3
    f1_irr   = fitness_map.get(s1["fitness_routine"],0) <= 1
    f2_irr   = fitness_map.get(s2["fitness_routine"],0) <= 1
    em1_expr = s1["communication_style"] in ["Direct and open","Assertive negotiator"]
    em2_expr = s2["communication_style"] in ["Direct and open","Assertive negotiator"]
    em1_res  = s1["communication_style"] in ["Passive / indirect","Avoidant"]
    em2_res  = s2["communication_style"] in ["Passive / indirect","Avoidant"]

    gamer_sleeper   = int((g1_high and n2_low) or (g2_high and n1_low))
    extro_intro     = int((e1_ext and e2_int) or (e2_ext and e1_int))
    messy_clean     = int((c1_low and c2_high) or (c2_low and c1_high))
    night_early     = int((sl1_high and sl2_ear) or (sl2_high and sl1_ear))
    loud_noise      = int((m1_loud and n2_low) or (m2_loud and n1_low))
    guest_private   = int((gu1_hvy and e2_int) or (gu2_hvy and e1_int))
    spender_budget  = int((sp1_high and not sp2_high) or (sp2_high and not sp1_high))
    grp_solo        = int((st1_grp and st2_sol) or (st2_grp and st1_sol))
    fit_irreg       = int((f1_fit and f2_irr) or (f2_fit and f1_irr))
    emot_reserv     = int((em1_expr and em2_res) or (em2_expr and em1_res))

    data = {
        "sleep_schedule_diff":   [sleep_diff],
        "wakeup_schedule_diff":  [wakeup_diff],
        "cleanliness_diff":      [clean_diff],
        "study_hours_diff":      [study_diff],
        "noise_tolerance_diff":  [noise_diff],
        "room_temperature_diff": [temp_diff],
        "social_energy_diff":    [social_diff],
        "spending_habit_diff":   [spend_diff],
        "guest_frequency_diff":  [guest_diff],
        "gaming_time_diff":      [gaming_diff],
        "food_preference_similarity":      [food_sim],
        "music_preference_similarity":     [music_sim],
        "study_style_similarity":          [study_sim],
        "communication_style_similarity":  [comm_sim],
        "organization_similarity":         [org_sim],
        "workout_routine_similarity":      [workout_sim],
        "hobby_similarity":                [hobby_sim],
        "academic_goal_similarity":        [acad_sim],
        "room_usage_similarity":           [room_sim],
        "weekend_activity_similarity":     [weekend_sim],
        "gamer_vs_light_sleeper":          [gamer_sleeper],
        "extrovert_vs_introvert_conflict": [extro_intro],
        "messy_vs_clean_conflict":         [messy_clean],
        "nightowl_vs_earlybird_conflict":  [night_early],
        "loud_music_vs_noise_sensitive":   [loud_noise],
        "guest_heavy_vs_private_person":   [guest_private],
        "high_spender_vs_budget_person":   [spender_budget],
        "group_study_vs_solo_study":       [grp_solo],
        "fitness_focused_vs_irregular":    [fit_irreg],
        "emotional_expressive_vs_reserved":[emot_reserv],
    }
    return pd.DataFrame(data)


def generate_features_safe(s1: dict, s2: dict) -> pd.DataFrame:
    """Try calculations.py first; fall back to local implementation."""
    try:
        from calculations import generate_features
        return generate_features(s1, s2)
    except Exception:
        return fallback_generate_features(s1, s2)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 1.5rem 0 0.5rem;">
            <div style="font-size:3rem;">🏠</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;
                        color:white;margin-top:0.3rem;">RoomieMatch</div>
            <div style="font-size:0.78rem;color:#93c5fd;letter-spacing:0.08em;margin-top:0.2rem;">
                AI COMPATIBILITY ENGINE
            </div>
        </div>
        <hr style="border-color:rgba(147,197,253,0.2);margin:1rem 0;">
        """, unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            ["🔮 Predictor", "📊 Compatibility Analysis"],
            label_visibility="collapsed"
        )

        st.markdown("""
        <hr style="border-color:rgba(147,197,253,0.2);margin:1.5rem 0 1rem;">
        <div style="font-size:0.78rem;color:#93c5fd;padding:0 0.5rem;">
            <div style="font-weight:600;margin-bottom:0.6rem;color:#bfdbfe;">How it works</div>
            <div style="margin-bottom:0.5rem;">① Fill in Member 1 details</div>
            <div style="margin-bottom:0.5rem;">② Switch to Member 2</div>
            <div style="margin-bottom:0.5rem;">③ Run compatibility check</div>
            <div>④ View detailed report</div>
        </div>
        <hr style="border-color:rgba(147,197,253,0.2);margin:1.5rem 0 1rem;">
        <div style="font-size:0.73rem;color:#7dd3fc;padding:0 0.5rem;line-height:1.6;">
            Powered by a PyTorch MLP model trained on 30,000 synthetic roommate profiles with 30 engineered behavioral features.
        </div>
        """, unsafe_allow_html=True)

        # Model status indicator
        _, _, top_features, errors = load_model_artifacts()
        if errors:
            st.markdown("""
            <div style="background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.3);
                        border-radius:8px;padding:0.7rem;margin-top:1rem;font-size:0.78rem;color:#fca5a5;">
                ⚠️ Model files not loaded. Running in demo mode.
            </div>
            """, unsafe_allow_html=True)
        else:
            n_features = len(top_features) if top_features else "?"
            st.markdown(f"""
            <div style="background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.25);
                        border-radius:8px;padding:0.7rem;margin-top:1rem;font-size:0.78rem;color:#6ee7b7;">
                ✅ Model loaded · {n_features} features
            </div>
            """, unsafe_allow_html=True)

    return page


# ─────────────────────────────────────────────
# PAGE 1 — PREDICTOR
# ─────────────────────────────────────────────
def page_predictor():
    # Hero section
    st.markdown("""
    <div style="padding: 1.5rem 0 1rem;">
        <div class="hero-title">AI Roommate Compatibility Predictor</div>
        <div class="hero-sub">
            Enter details for both potential roommates and let our AI evaluate lifestyle alignment,
            conflict risks, and long-term cohabitation compatibility.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature highlight cards
    fc1, fc2, fc3, fc4 = st.columns(4)
    for col, icon, title, desc in [
        (fc1, "🧠", "AI-Powered", "PyTorch MLP model"),
        (fc2, "📊", "30 Features", "Behavioral signals"),
        (fc3, "⚡", "Instant", "Real-time inference"),
        (fc4, "📋", "Full Report", "Detailed analysis"),
    ]:
        with col:
            st.markdown(f"""
            <div class="glass-card-sm" style="text-align:center;padding:1rem;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-weight:600;font-size:0.9rem;margin-top:0.3rem;">{title}</div>
                <div style="font-size:0.77rem;color:var(--text-muted);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # ── Session state init ──
    if "active_member" not in st.session_state:
        st.session_state.active_member = 1
    if "member1_data" not in st.session_state:
        st.session_state.member1_data = None
    if "member2_data" not in st.session_state:
        st.session_state.member2_data = None
    if "prediction_done" not in st.session_state:
        st.session_state.prediction_done = False
    if "score" not in st.session_state:
        st.session_state.score = None
    if "features_df" not in st.session_state:
        st.session_state.features_df = None

    # ── Member toggle header ──
    active = st.session_state.active_member
    m1_status = "🟢 Active" if active == 1 else ("✅ Saved" if st.session_state.member1_data else "⬜ Pending")
    m2_status = "🟢 Active" if active == 2 else ("✅ Saved" if st.session_state.member2_data else "⬜ Pending")

    header_col1, header_col2 = st.columns(2)
    with header_col1:
        st.markdown(f"""
        <div style="padding:0.75rem 1.2rem;border-radius:10px;
                    background:{'linear-gradient(135deg,rgba(59,130,246,0.15),rgba(6,182,212,0.1))' if active==1 else 'rgba(100,116,139,0.07)'};
                    border:{'2px solid rgba(59,130,246,0.4)' if active==1 else '1px solid rgba(100,116,139,0.15)'};
                    transition:all 0.3s ease;">
            <span style="font-weight:600;font-size:0.95rem;">🧑 Member 1</span>
            <span style="float:right;font-size:0.8rem;color:var(--text-muted);">{m1_status}</span>
        </div>
        """, unsafe_allow_html=True)
    with header_col2:
        st.markdown(f"""
        <div style="padding:0.75rem 1.2rem;border-radius:10px;
                    background:{'linear-gradient(135deg,rgba(59,130,246,0.15),rgba(6,182,212,0.1))' if active==2 else 'rgba(100,116,139,0.07)'};
                    border:{'2px solid rgba(59,130,246,0.4)' if active==2 else '1px solid rgba(100,116,139,0.15)'};
                    transition:all 0.3s ease;">
            <span style="font-weight:600;font-size:0.95rem;">👤 Member 2</span>
            <span style="float:right;font-size:0.8rem;color:var(--text-muted);">{m2_status}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # ── Main input card ──
    active_class = "member-active"
    st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)
    member_data = render_member_form(active)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # ── Action buttons ──
    btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])

    with btn_col1:
        if active == 1:
            if st.button("💾 Save Member 1 & Switch to Member 2 →", use_container_width=True):
                st.session_state.member1_data = member_data
                st.session_state.active_member = 2
                st.session_state.prediction_done = False
                st.rerun()
        else:
            if st.button("← Switch back to Member 1", use_container_width=True):
                st.session_state.member2_data = member_data
                st.session_state.active_member = 1
                st.rerun()

    with btn_col2:
        both_ready = st.session_state.member1_data is not None
        if not both_ready:
            st.markdown("""
            <div class="info-box" style="text-align:center;">
                💡 Save Member 1 first to enable prediction
            </div>
            """, unsafe_allow_html=True)
        else:
            if active == 2:
                predict_data_2 = member_data
            else:
                predict_data_2 = st.session_state.member2_data

            if st.button("🔮 Run Compatibility Check", use_container_width=True):
                if predict_data_2 is None:
                    st.warning("Please fill in Member 2 details first.")
                else:
                    st.session_state.member2_data = predict_data_2

                    with st.spinner("Analyzing compatibility..."):
                        time.sleep(0.4)  # brief UX pause

                        # Generate features
                        features_df = generate_features_safe(
                            st.session_state.member1_data,
                            predict_data_2
                        )
                        st.session_state.features_df = features_df

                        # Run model inference
                        model, scaler, top_features, errors = load_model_artifacts()

                        if model is not None and scaler is not None and top_features is not None:
                            score = run_inference(features_df, model, scaler, top_features)
                        else:
                            # Demo scoring using feature weights
                            score = _demo_score(features_df)

                        st.session_state.score = score
                        st.session_state.prediction_done = True

                    st.rerun()

    # ── Results display ──
    if st.session_state.prediction_done and st.session_state.score is not None:
        score = st.session_state.score
        label = score_to_label(score)
        info  = LABEL_INFO[label]

        st.markdown("<hr style='border-color:var(--border);margin:2rem 0;'>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔮 Compatibility Result</div>', unsafe_allow_html=True)

        r_col1, r_col2 = st.columns([1, 2])

        with r_col1:
            st.markdown(f"""
            <div style="text-align:center;padding:1rem 0;">
                <div class="score-circle">
                    <div class="score-number">{score:.0f}</div>
                    <div class="score-label-small">OUT OF 100</div>
                </div>
                <div style="margin-top:1rem;">
                    <span class="compat-badge {info['badge']}">{info['emoji']} {info['text']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with r_col2:
            st.markdown(f"""
            <div style="padding:0.5rem 0 0.5rem 1rem;animation:fadeIn 0.6s ease forwards;">
                <div style="font-size:1.1rem;font-weight:600;color:var(--text);margin-bottom:0.8rem;">
                    Compatibility Score: {score:.1f}/100
                </div>
                <div class="progress-outer">
                    <div class="progress-inner" style="width:{score}%;"></div>
                </div>
                <div style="font-size:0.88rem;color:var(--text-muted);margin-top:0.5rem;">
                    Label {label} of 5 · {info['text']}
                </div>
                <div style="margin-top:1.2rem;font-size:0.92rem;color:var(--text);
                            line-height:1.7;padding:1rem;background:var(--glass2);
                            border-radius:var(--radius-sm);border-left:3px solid var(--blue);">
                    {info['message']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Quick stats
            if st.session_state.features_df is not None:
                fdf = st.session_state.features_df
                row = fdf.iloc[0]
                diff_cols = [c for c in fdf.columns if c.endswith("_diff")]
                sim_cols  = [c for c in fdf.columns if c.endswith("_similarity")]
                inter_cols = [c for c in fdf.columns if any(k in c for k in ["_vs_", "_conflict", "_person"])]
                avg_diff  = float(row[diff_cols].mean()) if diff_cols else 0
                n_sim     = int(row[sim_cols].sum()) if sim_cols else 0
                n_conf    = int(row[inter_cols].sum()) if inter_cols else 0

                st.markdown(f"""
                <div class="stat-row" style="margin-top:1.2rem;">
                    <div class="stat-chip">
                        <div class="stat-chip-val">{avg_diff*100:.0f}%</div>
                        <div class="stat-chip-lbl">Avg Difference</div>
                    </div>
                    <div class="stat-chip">
                        <div class="stat-chip-val">{n_sim}/{len(sim_cols)}</div>
                        <div class="stat-chip-lbl">Similarities</div>
                    </div>
                    <div class="stat-chip">
                        <div class="stat-chip-val">{n_conf}</div>
                        <div class="stat-chip-lbl">Conflicts</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # close glass-card

        st.markdown("""
        <div class="info-box" style="margin-top:0.5rem;">
            📊 Navigate to <strong>Compatibility Analysis</strong> in the sidebar for the full breakdown of matched traits,
            conflicts, and key risk factors.
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE 2 — COMPATIBILITY ANALYSIS
# ─────────────────────────────────────────────
def page_analysis():
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem;">
        <div class="hero-title" style="font-size:clamp(1.6rem,3vw,2.4rem);">
            📊 Compatibility Analysis Report
        </div>
        <div class="hero-sub">
            Detailed breakdown of matched traits, conflict zones, and behavioral risk factors.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("prediction_done") or st.session_state.get("features_df") is None:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">🔍</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.3rem;color:#1e3a8a;margin-bottom:0.8rem;">
                No Analysis Available Yet
            </div>
            <div style="color:var(--text-muted);font-size:0.92rem;max-width:400px;margin:0 auto;">
                Run a compatibility prediction on the Predictor page first to see the detailed analysis report here.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    score     = st.session_state.score
    label     = score_to_label(score)
    info      = LABEL_INFO[label]
    fdf       = st.session_state.features_df
    analysis  = analyze_features(fdf)

    # ── Score summary banner ──
    banner_color = {1:"#fee2e2",2:"#fef3c7",3:"#dbeafe",4:"#d1fae5",5:"#e0f2fe"}[label]
    banner_text  = {1:"#991b1b", 2:"#92400e", 3:"#1e40af", 4:"#065f46", 5:"#0c4a6e"}[label]
    st.markdown(f"""
    <div style="background:{banner_color};border-radius:var(--radius);padding:1.5rem 2rem;
                margin-bottom:1.5rem;display:flex;align-items:center;gap:1.5rem;">
        <div style="font-size:2.8rem;">{info['emoji']}</div>
        <div>
            <div style="font-family:'Playfair Display',serif;font-size:1.5rem;
                        font-weight:700;color:{banner_text};">{info['text']}</div>
            <div style="font-size:0.9rem;color:{banner_text};opacity:0.8;margin-top:0.2rem;">
                Compatibility Score: {score:.1f}/100 · Label {label}
            </div>
        </div>
        <div style="margin-left:auto;text-align:right;">
            <div style="font-family:'Playfair Display',serif;font-size:3rem;
                        font-weight:700;color:{banner_text};">{score:.0f}</div>
            <div style="font-size:0.78rem;color:{banner_text};opacity:0.7;">out of 100</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS ──
    tab1, tab2, tab3, tab4 = st.tabs([
        "✅ Matched Traits",
        "⚠️ Conflict Zones",
        "📈 Breakdown",
        "🔑 Key Factors"
    ])

    # ── Tab 1: Matched Traits ──
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✅ Matched Traits</div>', unsafe_allow_html=True)

        matched = analysis["matched_traits"]
        if not matched:
            st.markdown('<div class="info-box">No strong trait matches detected between these roommates.</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f"**{len(matched)} compatible traits found**")
            for icon, label_txt, desc in matched:
                st.markdown(f"""
                <div class="trait-positive">
                    <strong>{icon} {label_txt}</strong>
                    <span style="float:right;color:var(--success);font-size:0.82rem;">✓ Match</span>
                    <div style="color:var(--text-muted);font-size:0.82rem;margin-top:0.2rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 2: Conflict Zones ──
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚠️ Conflict Zones</div>', unsafe_allow_html=True)

        conflicts = analysis["conflict_traits"]
        active_c  = analysis["active_conflicts"]

        if active_c:
            st.markdown("**🔴 Active Behavioral Conflicts**")
            for icon, label_txt in active_c:
                st.markdown(f"""
                <div class="trait-conflict" style="background:rgba(239,68,68,0.1);border-left-color:#dc2626;">
                    <strong>{icon} {label_txt}</strong>
                    <span style="float:right;color:var(--danger);font-size:0.82rem;">⚡ Active conflict</span>
                    <div style="color:var(--text-muted);font-size:0.82rem;margin-top:0.2rem;">
                        Direct behavioral conflict detected — requires explicit agreement to manage.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

        if conflicts:
            st.markdown("**🟠 Lifestyle Mismatches**")
            for icon, label_txt, desc in conflicts:
                st.markdown(f"""
                <div class="trait-conflict">
                    <strong>{icon} {label_txt}</strong>
                    <span style="float:right;color:var(--danger);font-size:0.82rem;">✗ Mismatch</span>
                    <div style="color:var(--text-muted);font-size:0.82rem;margin-top:0.2rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        if not conflicts and not active_c:
            st.markdown('<div class="info-box">🎉 No significant conflicts detected. This is a strong pairing.</div>',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 3: Breakdown ──
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Compatibility Breakdown</div>', unsafe_allow_html=True)

        row = fdf.iloc[0]

        # Difference features bar chart
        st.markdown("**Difference Features** *(lower = more compatible)*")
        diff_data = {}
        for key, icon, label_txt, _ in DIFF_FEATURES:
            if key in row:
                diff_data[f"{icon} {label_txt}"] = float(row[key])

        if diff_data:
            diff_df = pd.DataFrame.from_dict(diff_data, orient="index", columns=["Difference"])
            diff_df = diff_df.sort_values("Difference", ascending=True)
            st.bar_chart(diff_df, height=300)

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        # Similarity overview
        st.markdown("**Similarity Features** *(binary: 1 = similar)*")
        sim_pairs = []
        for key, icon, label_txt in SIM_FEATURES:
            if key in row:
                sim_pairs.append({"Feature": f"{icon} {label_txt}", "Similar": "Yes ✓" if int(row[key]) == 1 else "No ✗"})
        if sim_pairs:
            sim_df = pd.DataFrame(sim_pairs)
            st.dataframe(sim_df, use_container_width=True, hide_index=True)

        # Interaction features
        st.markdown("**Interaction Conflicts** *(1 = conflict active)*")
        inter_pairs = []
        for key, icon, label_txt in INTER_FEATURES:
            if key in row:
                inter_pairs.append({
                    "Conflict Type": f"{icon} {label_txt}",
                    "Status": "⚡ Active" if int(row[key]) == 1 else "✅ None"
                })
        if inter_pairs:
            int_df = pd.DataFrame(inter_pairs)
            st.dataframe(int_df, use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 4: Key Factors ──
    with tab4:
        kf_col1, kf_col2 = st.columns(2)

        with kf_col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🔴 Key Risk Factors</div>', unsafe_allow_html=True)

            risks = analysis["risk_factors"]
            if not risks:
                st.markdown('<div class="info-box">No major risk factors detected.</div>', unsafe_allow_html=True)
            else:
                for i, (icon, label_txt, val) in enumerate(risks, 1):
                    severity = "High" if val > 0.7 else ("Medium" if val > 0.45 else "Low")
                    sev_color = {"High":"#dc2626","Medium":"#d97706","Low":"#2563eb"}[severity]
                    st.markdown(f"""
                    <div class="trait-conflict" style="margin-bottom:0.5rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong>{icon} {label_txt}</strong>
                            <span style="background:{sev_color}20;color:{sev_color};
                                         border:1px solid {sev_color}40;border-radius:99px;
                                         padding:0.15rem 0.6rem;font-size:0.75rem;font-weight:600;">
                                {severity}
                            </span>
                        </div>
                        <div style="margin-top:0.4rem;height:4px;background:rgba(239,68,68,0.1);border-radius:99px;overflow:hidden;">
                            <div style="width:{int(val*100)}%;height:100%;background:{sev_color};border-radius:99px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with kf_col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🟢 Positive Factors</div>', unsafe_allow_html=True)

            positives = analysis["positive_factors"]
            if not positives:
                st.markdown('<div class="info-box">No strong positive compatibility factors found.</div>',
                            unsafe_allow_html=True)
            else:
                for icon, label_txt, val in positives:
                    strength = "Strong" if val >= 0.8 else ("Good" if val >= 0.4 else "Moderate")
                    st.markdown(f"""
                    <div class="trait-positive" style="margin-bottom:0.5rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong>{icon} {label_txt}</strong>
                            <span style="background:rgba(16,185,129,0.12);color:#059669;
                                         border:1px solid rgba(16,185,129,0.25);border-radius:99px;
                                         padding:0.15rem 0.6rem;font-size:0.75rem;font-weight:600;">
                                {strength}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # AI recommendation
        n_risks = len(analysis["risk_factors"])
        n_pos   = len(analysis["positive_factors"])
        n_actc  = len(analysis["active_conflicts"])

        if n_actc >= 3 or score < 25:
            rec_level, rec_icon, rec_msg = "danger", "⚠️", "This pairing faces significant compatibility challenges. It is advisable to have detailed conversations about expectations and boundaries before committing. Consider whether the lifestyle differences are manageable."
        elif n_risks >= 4 or score < 45:
            rec_level, rec_icon, rec_msg = "warning", "📋", "Moderate compatibility with notable friction points. A structured roommate agreement covering noise, cleanliness, guests, and shared spaces is strongly recommended."
        elif score >= 75:
            rec_level, rec_icon, rec_msg = "success", "🌟", "This is a strong pairing. The roommates share many compatible traits. A brief initial conversation to align on a few minor differences should be sufficient."
        else:
            rec_level, rec_icon, rec_msg = "info", "🤝", "Decent compatibility with a few areas to navigate. Open communication early on about the identified conflict zones will set a positive foundation."

        rec_styles = {
            "danger":  ("rgba(239,68,68,0.08)", "rgba(239,68,68,0.2)", "#dc2626"),
            "warning": ("rgba(245,158,11,0.08)", "rgba(245,158,11,0.2)", "#b45309"),
            "success": ("rgba(16,185,129,0.08)", "rgba(16,185,129,0.2)", "#059669"),
            "info":    ("rgba(59,130,246,0.08)", "rgba(59,130,246,0.2)", "#1d4ed8"),
        }
        bg, border, color = rec_styles[rec_level]
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {border};border-left:4px solid {color};
                    border-radius:var(--radius-sm);padding:1.2rem 1.4rem;margin-top:0.5rem;">
            <div style="font-weight:600;color:{color};margin-bottom:0.5rem;">{rec_icon} AI Recommendation</div>
            <div style="font-size:0.9rem;color:var(--text);line-height:1.7;">{rec_msg}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DEMO SCORING (when model files absent)
# ─────────────────────────────────────────────
def _demo_score(features_df: pd.DataFrame) -> float:
    """Compute a plausible demo score using the original weight formula."""
    Wd = np.array([9, 7, 10, 6, 9, 4, 7, 5, 6, 4], dtype=float)
    Ws = np.array([4, 3, 7, 5, 4, 3, 4, 8, 3, 4], dtype=float)
    Wi = np.array([15, 11, 18, 16, 14, 12, 10, 9, 7, 8], dtype=float)

    row = features_df.iloc[0]
    diff_keys  = [k for k, *_ in DIFF_FEATURES]
    sim_keys   = [k for k, *_ in SIM_FEATURES]
    inter_keys = [k for k, *_ in INTER_FEATURES]

    diffs  = np.array([float(row.get(k, 0.3)) for k in diff_keys])
    sims   = np.array([float(row.get(k, 0))   for k in sim_keys])
    inters = np.array([float(row.get(k, 0))   for k in inter_keys])

    # Nonlinear for high-impact diffs
    pen_sleep = (diffs[0] ** 1.7) * Wd[0]
    pen_clean = (diffs[2] ** 1.8) * Wd[2]
    pen_noise = (diffs[4] ** 1.7) * Wd[4]
    pen_lin   = sum(diffs[i] * Wd[i] for i in [1, 3, 5, 6, 7, 8, 9])
    diff_pen  = pen_sleep + pen_clean + pen_noise + pen_lin
    sim_bon   = float(sims @ Ws) * 0.65
    inter_pen = float(inters @ Wi) * 0.58

    raw = 100 - diff_pen + sim_bon - inter_pen + np.random.uniform(-4, 4)
    return float(np.clip(raw, 0, 100))


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
def render_footer():
    st.markdown(f"""
    <div class="footer">
        RoomieMatch AI · Built with PyTorch &amp; Streamlit
        · {datetime.now().year} · For demonstration and research purposes
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    inject_css()

    # Initialise persistent session keys
    for key in ["active_member", "member1_data", "member2_data",
                "prediction_done", "score", "features_df"]:
        if key not in st.session_state:
            st.session_state[key] = None if key not in ("active_member",) else 1
            if key == "prediction_done":
                st.session_state[key] = False

    page = render_sidebar()

    if page == "🔮 Predictor":
        page_predictor()
    elif page == "📊 Compatibility Analysis":
        page_analysis()

    render_footer()


if __name__ == "__main__":
    main()
