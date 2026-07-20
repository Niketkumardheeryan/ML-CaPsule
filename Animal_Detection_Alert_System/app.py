import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
import tempfile
import os

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="Animal Detection & Alert System",
    page_icon="🐾",
    layout="wide",
)

# ── DANGER SETTINGS ─────────────────────────────────────────
DANGER_MAP = {
    "dog": "LOW",      "cat": "LOW",    "sheep": "LOW",
    "bird": "LOW",     "giraffe": "LOW",
    "cow": "MEDIUM",   "horse": "MEDIUM", "zebra": "MEDIUM",
    "elephant": "HIGH","bear": "HIGH",
    "lion": "HIGH",    "tiger": "HIGH",
}
EMOJI = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "NONE": "⚫"}

# ── MODEL LOAD ──────────────────────────────────────────────
@st.cache_resource(show_spinner="⏳ Loading YOLOv8 model...")
def load_model(variant):
    from ultralytics import YOLO
    return YOLO(variant)

# ── DETECTION ───────────────────────────────────────────────
def run_detection(model, pil_image, conf):
    img_np = np.array(pil_image.convert("RGB"))

    results    = model(img_np, conf=conf, verbose=False)
    annotated  = Image.fromarray(results[0].plot()[..., ::-1])  # BGR→RGB via PIL

    detections = []
    for r in results:
        for box in r.boxes:
            label  = model.names[int(box.cls[0])]
            danger = DANGER_MAP.get(label, "LOW")
            detections.append({
                "label":      label,
                "confidence": round(float(box.conf[0]), 3),
                "danger":     danger,
            })

    priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    highest  = max(detections, key=lambda d: priority[d["danger"]])["danger"] \
               if detections else "NONE"

    return annotated, detections, highest

# ── HEADER ───────────────────────────────────────────────────
st.title("🐾 Animal Detection & Alert System")
st.caption("YOLOv8 · Real-time danger classification · HIGH / MEDIUM / LOW alerts")
st.divider()

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    variant = st.selectbox("Model", ["yolov8n.pt", "yolov8s.pt"])
    conf    = st.slider("Confidence", 0.1, 1.0, 0.50, 0.05)
    st.divider()
    st.subheader("Danger Levels")
    for animal, level in sorted(DANGER_MAP.items(), key=lambda x: x[1]):
        st.write(f"{EMOJI[level]} **{animal.title()}** — {level}")
    st.divider()
    st.caption("ML-CaPsule · GSSoC 2026 · @Yugal0708")

model = load_model(variant)

# ── TABS ─────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📷 Image Detection", "🎬 Video Detection"])

# ── TAB 1 — IMAGE ────────────────────────────────────────────
with tab1:
    st.subheader("Upload an Image")
    uploaded = st.file_uploader("Choose image", type=["jpg","jpeg","png"])

    if uploaded:
        pil_img = Image.open(uploaded)
        with st.spinner("Detecting..."):
            result_img, dets, highest = run_detection(model, pil_img, conf)

        c1, c2 = st.columns([2, 1])
        with c1:
            st.image(result_img, caption="Detection Result", use_column_width=True)
        with c2:
            st.subheader("🚨 Alert")
            if   highest == "HIGH":   st.error("🔴 DANGER!\nHigh-risk animal!")
            elif highest == "MEDIUM": st.warning("🟡 CAUTION\nMedium-risk animal")
            elif highest == "LOW":    st.success("🟢 SAFE\nLow-risk animal")
            else:                     st.info("⚫ No animals detected")

            st.subheader("📋 Detected")
            if dets:
                for d in dets:
                    st.write(f"{EMOJI[d['danger']]} **{d['label'].title()}** "
                             f"`{d['danger']}` | `{d['confidence']}`")
            else:
                st.write("None found")
    else:
        st.info("⬆️ Upload an image to begin")

# ── TAB 2 — VIDEO ────────────────────────────────────────────
with tab2:
    st.subheader("Upload a Video")
    st.info("📹 Video detection requires OpenCV. "
            "Please run locally with: `streamlit run app.py`")
    st.code("pip install -r requirements.txt\nstreamlit run app.py")
