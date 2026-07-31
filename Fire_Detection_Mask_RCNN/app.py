"""
Streamlit Web Application for Fire Detection & Segmentation using Mask R-CNN
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt
from model import SimpleMaskRCNN, detect_fire_rgb_heuristic

st.set_page_config(
    page_title="Fire Mask R-CNN Segmentation",
    page_icon="🔥",
    layout="wide"
)

@st.cache_resource
def load_model():
    model = SimpleMaskRCNN(input_shape=(128, 128, 3))
    # Dummy forward pass to initialize weights
    dummy_input = tf.zeros((1, 128, 128, 3))
    _ = model(dummy_input)
    return model

def main():
    st.title("🔥 Image Segmentation using Mask R-CNN with TensorFlow")
    st.markdown("""
    This interactive web application demonstrates **Fire Detection and Instance Segmentation** using a multi-task **Mask R-CNN** deep learning architecture and RGB chromatic analysis.
    """)
    
    st.sidebar.header("Settings & Options")
    conf_threshold = st.sidebar.slider("Mask Binarization Threshold", 0.1, 0.9, 0.5, 0.05)
    method = st.sidebar.radio("Segmentation Method", ["Mask R-CNN (Deep Learning)", "RGB Chromatic Heuristic", "Hybrid Ensemble"])
    
    model = load_model()
    
    uploaded_file = st.sidebar.file_uploader("Upload an Image containing Fire/Smoke", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image_pil = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image_pil)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(image_pil, use_column_width=True)
            
        # Preprocess for model
        orig_h, orig_w, _ = img_np.shape
        resized_img = cv2.resize(img_np, (128, 128))
        input_tensor = np.expand_dims(resized_img / 255.0, axis=0).astype(np.float32)
        
        # Inference
        predictions = model(input_tensor)
        pred_mask = predictions["mask"][0, :, :, 0].numpy()
        pred_bbox = predictions["bbox"][0].numpy() # [ymin, xmin, ymax, xmax]
        
        # RGB Heuristic fallback / hybrid computation
        rgb_mask = detect_fire_rgb_heuristic(resized_img)
        
        if method == "Mask R-CNN (Deep Learning)":
            final_mask = (pred_mask > conf_threshold).astype(np.uint8)
        elif method == "RGB Chromatic Heuristic":
            final_mask = rgb_mask
        else:
            final_mask = np.logical_or(pred_mask > conf_threshold, rgb_mask == 1).astype(np.uint8)
            
        # Resize mask back to original dimensions
        mask_orig = cv2.resize(final_mask, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST)
        
        # Overlay visualization
        overlay = img_np.copy()
        fire_pixels_count = np.sum(mask_orig == 1)
        total_pixels = orig_w * orig_h
        fire_percentage = (fire_pixels_count / total_pixels) * 100
        
        # Apply red-yellow mask overlay
        overlay[mask_orig == 1] = (overlay[mask_orig == 1] * 0.4 + np.array([255, 69, 0]) * 0.6).astype(np.uint8)
        
        # Draw bounding box
        ymin, xmin, ymax, xmax = int(pred_bbox[0] * orig_h), int(pred_bbox[1] * orig_w), int(pred_bbox[2] * orig_h), int(pred_bbox[3] * orig_w)
        cv2.rectangle(overlay, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(overlay, f"Fire Region ({fire_percentage:.1f}%)", (xmin, max(15, ymin - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        with col2:
            st.subheader("Segmentation & Localization Result")
            st.image(overlay, use_column_width=True)
            
        st.markdown("---")
        st.subheader("📊 Diagnostic Summary")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Fire Status Detected", "YES" if fire_pixels_count > 0 else "NO")
        m_col2.metric("Estimated Fire Area", f"{fire_percentage:.2f}%")
        m_col3.metric("Bounding Box Coordinates", f"[{xmin}, {ymin}, {xmax}, {ymax}]")
        
    else:
        st.info("💡 Please upload an image from the sidebar to test Fire Detection and Mask R-CNN Segmentation.")
        
        # Generate sample image button
        if st.button("Generate & Test with Synthetic Sample Image"):
            from model import create_synthetic_fire_image
            sample_img, sample_mask, sample_bbox = create_synthetic_fire_image((256, 256))
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Synthetic Sample Image")
                st.image(sample_img, use_column_width=True)
                
            resized_img = cv2.resize(sample_img, (128, 128))
            input_tensor = np.expand_dims(resized_img / 255.0, axis=0).astype(np.float32)
            predictions = model(input_tensor)
            pred_mask = predictions["mask"][0, :, :, 0].numpy()
            
            mask_orig = cv2.resize((pred_mask > conf_threshold).astype(np.uint8), (256, 256), interpolation=cv2.INTER_NEAREST)
            overlay = sample_img.copy()
            overlay[mask_orig == 1] = (overlay[mask_orig == 1] * 0.4 + np.array([255, 69, 0]) * 0.6).astype(np.uint8)
            
            with col2:
                st.subheader("Predicted Segmentation Mask")
                st.image(overlay, use_column_width=True)

if __name__ == "__main__":
    main()
