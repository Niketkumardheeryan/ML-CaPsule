# ──────> Clean, modern CSS
import streamlit as st

def get_css() -> str:
    """Return the CSS stylesheet for the Cat vs Dog Classifier app."""
    return """
<style>
    /* Root variables for consistent theming */
    :root {
        --bg: #fafafa;
        --card: #ffffff;
        --text: #1a1a2e;
        --muted: #6b7280;
        --border: #e5e7eb;
        --cat: #f97316;
        --dog: #3b82f6;
        --cat-bg: #fff7ed;
        --dog-bg: #eff6ff;
        --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
        --shadow-lg: 0 10px 25px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
        --radius: 12px;
        --radius-sm: 8px;
        --transition: 200ms ease;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --text: #f1f5f9;
            --muted: #94a3b8;
            --border: #334155;
            --cat: #fb923c;
            --dog: #60a5fa;
            --cat-bg: #7c2d12;
            --dog-bg: #1e3a5f;
            --shadow: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.4);
        }
    }

    /* Page container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 640px;
    }

    /* Typography */
    h1 {
        text-align: center;
        font-weight: 700;
        font-size: 2.25rem;
        color: var(--text);
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .subtitle {
        text-align: center;
        color: var(--muted);
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }

    /* File uploader */
    .stFileUploader > div:first-child {
        border: 2px dashed var(--border);
        border-radius: var(--radius);
        padding: 2.5rem 2rem;
        background: var(--card);
        transition: all var(--transition);
    }

    .stFileUploader > div:first-child:hover {
        border-color: var(--dog);
        background: var(--dog-bg);
    }

    .stFileUploader label {
        font-weight: 500;
        color: var(--text) !important;
    }

    .stFileUploader small {
        color: var(--muted) !important;
    }

    /* Result card */
    .result-card {
        background: var(--card);
        border-radius: var(--radius);
        padding: 2rem;
        margin-top: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        text-align: center;
    }

    .result-card.cat {
        border-color: var(--cat);
        background: linear-gradient(180deg, var(--cat-bg) 0%, var(--card) 100%);
    }

    .result-card.dog {
        border-color: var(--dog);
        background: linear-gradient(180deg, var(--dog-bg) 0%, var(--card) 100%);
    }

    .result-emoji {
        font-size: 3.5rem;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .result-label {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.25rem;
    }

    .result-confidence {
        font-size: 1.1rem;
        color: var(--muted);
        font-weight: 500;
    }

    /* Confidence bar */
    .confidence-bar {
        margin-top: 1.25rem;
        height: 6px;
        border-radius: 3px;
        background: var(--border);
        overflow: hidden;
    }

    .confidence-fill {
        height: 100%;
        border-radius: 3px;
        transition: width 600ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    .confidence-fill.cat { background: var(--cat); }
    .confidence-fill.dog { background: var(--dog); }

    /* Probability bars */
    .prob-section {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }

    .prob-section h3 {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }

    .prob-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }

    .prob-label {
        width: 70px;
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text);
    }

    .prob-bar {
        flex: 1;
        height: 8px;
        border-radius: 4px;
        background: var(--border);
        overflow: hidden;
    }

    .prob-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 600ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    .prob-fill.cat { background: var(--cat); }
    .prob-fill.dog { background: var(--dog); }

    .prob-value {
        width: 55px;
        text-align: right;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--muted);
        font-variant-numeric: tabular-nums;
    }

    /* Info card */
    .info-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.25rem;
        margin-top: 2.5rem;
        box-shadow: var(--shadow);
    }

    .info-card h4 {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }

    .info-card ul {
        margin: 0;
        padding-left: 1.25rem;
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.7;
    }

    .info-card li { margin-bottom: 0.25rem; }
    .info-card strong { color: var(--text); }

    /* Sample images */
    .samples-section {
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }

    .samples-section h3 {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }

    .sample-btn {
        width: 100%;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 0.75rem 1rem;
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text);
        cursor: pointer;
        transition: all var(--transition);
    }

    .sample-btn:hover:not(:disabled) {
        border-color: var(--dog);
        background: var(--dog-bg);
    }

    .sample-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    /* Sample image display */
    .sample-result {
        margin-top: 1.5rem;
        padding: 1.5rem;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
    }

    .sample-result img {
        border-radius: var(--radius-sm);
        margin-bottom: 1rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
        color: var(--muted);
        font-size: 0.8rem;
    }

    .footer a { color: var(--muted); text-decoration: none; }
    .footer a:hover { color: var(--dog); }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Button styling */
    .stButton > button {
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
        transition: all var(--transition) !important;
    }

    /* Spinner */
    .stSpinner > div { border-color: var(--dog) transparent !important; }

    /* Image caption */
    .stImage caption {
        font-size: 0.85rem !important;
        color: var(--muted) !important;
    }
</style>
"""

def page_css():
    """Apply the CSS to the Streamlit app."""
    st.markdown(get_css(), unsafe_allow_html=True)