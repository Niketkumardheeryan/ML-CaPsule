import os
from pathlib import Path
from typing import List

import streamlit as st
import torch
from PIL import Image
from ultralytics import YOLO
import numpy as np

CLASS_NAMES: List[str] = [
    "pistol",
    "smartphone",
    "knife",
    "monedero",
    "billete",
    "tarjeta",
]

MODEL_PATHS = [
    Path("runs/detect/train-2/weights/best.pt"),
    Path("runs/detect/train-2/weights/last.pt"),
    Path("yolov8n.pt"),
    Path("yolo26n.pt"),
]


@st.cache_resource
def load_model(path: str) -> YOLO:
    return YOLO(path)


def format_detection_results(result) -> List[dict]:
    if result is None or len(result.boxes) == 0:
        return []

    boxes = result.boxes
    ids = boxes.cls.cpu().numpy().astype(int)
    scores = boxes.conf.cpu().numpy().astype(float)

    detections = []
    for idx, score in zip(ids, scores):
        class_name = CLASS_NAMES[idx] if 0 <= idx < len(CLASS_NAMES) else f"class_{idx}"
        detections.append({"class": class_name, "confidence": f"{score:.2f}"})

    return detections


def choose_model_path(available_paths: List[Path]) -> Path:
    for path in available_paths:
        if path.exists():
            return path
    raise FileNotFoundError(
        "No model weight file found. Add a YOLO model to one of these paths: "
        + ", ".join(str(p) for p in available_paths)
    )


def main() -> None:
    st.set_page_config(page_title="Object Detection Dashboard", layout="centered")
    st.title("Weapon / Object Detection Dashboard")
    st.write(
        "Upload an image and the dashboard will detect items and show the predicted object classes."
    )

    available_models = [str(path) for path in MODEL_PATHS if path.exists()]
    if not available_models:
        st.error(
            "No YOLO model weights were detected in the repository. "
            "Please add `runs/detect/train-2/weights/best.pt`, `runs/detect/train-2/weights/last.pt`, or `yolov8n.pt`."
        )
        return

    chosen_model = st.sidebar.selectbox("Select model", available_models)
    confidence_threshold = st.sidebar.slider("Confidence threshold", 0.05, 0.9, 0.25, step=0.05)
    iou_threshold = st.sidebar.slider("IOU threshold", 0.1, 0.9, 0.45, step=0.05)
    device_options = ["cpu"]
    if torch.cuda.is_available():
        device_options.append("cuda")
    selected_device = st.sidebar.selectbox("Device", device_options)

    try:
        model = load_model(chosen_model)
    except Exception as exc:
        st.error(f"Error loading model: {exc}")
        return

    uploaded_file = st.file_uploader(
        "Upload a JPG / PNG image for inference", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        st.info("Upload an image to see predictions.")
        return

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image", use_column_width=True)

    with st.spinner("Running inference..."):
        try:
            results = model.predict(
                source=np.asarray(image),
                imgsz=640,
                conf=confidence_threshold,
                iou=iou_threshold,
                device=selected_device,
                max_det=50,
            )
        except Exception as exc:
            st.error(f"Inference failed: {exc}")
            return

    if len(results) == 0 or len(results[0].boxes) == 0:
        st.warning("No objects detected with the selected confidence threshold.")
        return

    annotated_array = results[0].plot()
    try:
        annotated_image = Image.fromarray(annotated_array)
    except Exception:
        annotated_image = image

    st.subheader("Detection output")
    st.image(annotated_image, caption="Detected objects", use_column_width=True)

    detections = format_detection_results(results[0])
    if detections:
        st.subheader("Predicted classes")
        st.table(detections)
    else:
        st.warning("The model produced no detections.")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Supported classes:**")
    for class_name in CLASS_NAMES:
        st.sidebar.write(f"- {class_name}")


if __name__ == "__main__":
    main()
