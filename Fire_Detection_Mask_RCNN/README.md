# Fire Detection and Image Segmentation using Mask R-CNN with TensorFlow

## 📌 Project Overview
Fire is an abnormal event that can quickly cause significant injury and property damage in a very concise time frame. The best possible way to reduce the wreckage caused by fire is to detect the fire source as early as possible before it spreads.

This project implements an **Image Segmentation and Object Detection** system for **Fire Detection** using:
1. **Mask R-CNN Architecture** (CNN Backbone + Multi-task Bounding Box & Mask Decoder Heads) in TensorFlow / Keras.
2. **RGB Chromatic & Disorder Measurement** (Rule-based color space feature extraction).
3. **Interactive Streamlit Web Dashboard** for real-time visualization, mask overlay, and fire pixel percentage quantification.

---

## 🛠️ Tech Stack & Dependencies
- **Python 3.8+**
- **TensorFlow / Keras**
- **OpenCV (`cv2`)**
- **NumPy & Matplotlib**
- **Streamlit**

---

## 📁 Repository Structure
```
Fire_Detection_Mask_RCNN/
│
├── mask_rcnn_fire_segmentation.ipynb   # Jupyter Notebook pipeline (Data, Architecture, Training, Evaluation)
├── model.py                            # Modular Python script for Mask R-CNN & RGB Heuristic
├── app.py                              # Streamlit Web App for interactive inference
├── requirements.txt                    # Python Dependencies
└── README.md                           # Project Documentation
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Jupyter Notebook
```bash
jupyter notebook mask_rcnn_fire_segmentation.ipynb
```

### 3. Launch Streamlit Web Application
```bash
streamlit run app.py
```

---

## 📊 Key Features
- **Instance Segmentation**: Pixel-level binary mask prediction for fire boundaries.
- **Bounding Box Bounding**: Bounding box localization of fire source coordinates (`[ymin, xmin, ymax, xmax]`).
- **Chromatic Analysis**: RGB color thresholding fallback ($R > G > B \text{ and } R > 150$).
- **IoU Evaluation**: Quantitative segmentation quality assessment.
