import streamlit as st
import time
from model_utils import MentalHealthScorer

# Set page config for a premium dashboard look
st.set_page_config(
    page_title="Mental Health Risk Scorer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glassmorphism, gradients, and custom highlight styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* Header card */
    .header-box {
        background: rgba(30, 41, 59, 0.45);
        border-radius: 16px;
        padding: 2.5rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(12px);
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(to right, #818cf8, #c084fc, #fb7185);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 300;
    }
    
    /* Feature cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.35);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.15);
    }
    
    /* Custom Badge/Severity styles */
    .badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-low {
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .badge-moderate {
        background-color: rgba(249, 115, 22, 0.15);
        color: #fb923c;
        border: 1px solid rgba(249, 115, 22, 0.3);
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Highlighted text container */
    .explanation-container {
        line-height: 2.2;
        background: rgba(15, 23, 42, 0.6);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 1rem;
    }
    
    .explained-word {
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-weight: 500;
        margin: 0 0.1rem;
        display: inline-block;
        transition: background-color 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize scorer model
@st.cache_resource
def load_scorer():
    scorer = MentalHealthScorer()
    return scorer

scorer = load_scorer()

# Header Section
st.markdown("""
<div class="header-box">
    <div class="header-title">🧠 MindShield: NLP Mental Health Analyzer</div>
    <div class="header-subtitle">Analyze journal entries, thoughts, or social posts for multi-dimensional risk assessment using NLP transformers & explainable AI features.</div>
</div>
""", unsafe_allow_html=True)

# Main columns: Left for input, Right for results
col_input, col_results = st.columns([1.1, 0.9])

# Pre-defined templates for user ease of test
templates = {
    "Select a template...": "",
    "Academic Burnout": "I am so exhausted. I've been studying for 14 hours every day for exams and I feel like I'm not absorbing anything. I just want to sleep forever and never look at my desk again. It feels completely meaningless at this point.",
    "Panic & Anxiety": "My chest feels incredibly tight and my heart is racing. I can't shake this constant dread that something terrible is about to happen, even though everything is fine. My hands are shaking as I write this.",
    "Persistent Depression": "It's another day of feeling completely empty. I have no motivation to get out of bed or talk to anyone. I feel so lonely and worthless, like a heavy shadow is constantly hanging over me. Nothing brings me joy anymore.",
    "Balanced / Positive": "Today was a good day. I took a walk in the park, enjoyed a cup of coffee, and got some productive work done. Feeling calm and looking forward to the weekend."
}

with col_input:
    st.subheader("📝 Expressive Text Input")
    
    # Template dropdown helper
    selected_template = st.selectbox("💡 Choose a sample scenario to test:", list(templates.keys()))
    default_text = templates[selected_template] if selected_template else ""
    
    user_text = st.text_area(
        "Enter journal entry or text to analyze:",
        value=default_text,
        height=220,
        placeholder="Type how you are feeling, a diary entry, or social media text here..."
    )
    
    analyze_button = st.button("🚀 Analyze Mental State", use_container_width=True)

with col_results:
    st.subheader("📊 Diagnostic Risk Report")
    
    if analyze_button or user_text:
        if not user_text.strip():
            st.info("Please enter some text on the left to run the diagnostic tool.")
        else:
            with st.spinner("Analyzing mental health signals & projecting risk scores..."):
                time.sleep(0.6) # Sleek UX simulation
                scores = scorer.predict(user_text)
                
            # Render risk cards
            for cat in scorer.categories:
                val = scores[cat]
                severity, color = scorer.get_severity(val)
                
                badge_class = f"badge-{severity.lower()}"
                
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-weight: 600; font-size: 1.1rem; color: #e2e8f0;">{cat} Risk</span>
                        <span class="badge {badge_class}">{severity} Risk</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="flex-grow: 1; background-color: rgba(255,255,255,0.08); height: 10px; border-radius: 5px; overflow: hidden;">
                            <div style="background: linear-gradient(to right, #818cf8, #f87171); width: {val}%; height: 100%;"></div>
                        </div>
                        <span style="font-weight: bold; font-size: 1rem; min-width: 45px; text-align: right; color: #cbd5e1;">{val:.1f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Explainability selection
            st.write("---")
            st.subheader("🔍 Explainable AI Layer (Feature Attribution)")
            target_explain = st.selectbox("Select dimension to explain word attribution:", scorer.categories)
            
            explanations = scorer.explain_text(user_text, target_explain)
            
            html_words = []
            for item in explanations:
                word = item["word"]
                weight = item["weight"]
                
                # Highlight positive indicators (words contributing to the score) in soft red/orange
                if weight > 0.15:
                    alpha = min(0.65, weight * 0.7)
                    bg_color = f"rgba(239, 68, 68, {alpha})"
                    text_color = "#ffffff"
                    border = f"1px solid rgba(239, 68, 68, 0.4)"
                elif weight < -0.15:
                    alpha = min(0.65, abs(weight) * 0.7)
                    bg_color = f"rgba(34, 197, 94, {alpha})"
                    text_color = "#ffffff"
                    border = f"1px solid rgba(34, 197, 94, 0.4)"
                else:
                    bg_color = "transparent"
                    text_color = "#94a3b8"
                    border = "none"
                    
                html_words.append(
                    f'<span class="explained-word" style="background-color: {bg_color}; color: {text_color}; border: {border};" title="Weight: {weight:.2f}">{word}</span>'
                )
                
            st.markdown(f"""
            <div class="explanation-container">
                {" ".join(html_words)}
            </div>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem; text-align: right;">
                *Hover over words to see relative feature attribution weight. Red highlights indicate increased risk contribution.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👈 Enter a journal entry or click one of the quick templates and hit 'Analyze' to generate reports.")
