# 🚗 Simulating Self-Driving Cars
### Deep Learning + Computer Vision | GSSoC 2026 | Issue [#383](https://github.com/Niketkumardheeryan/ML-CaPsule/issues/383)

---

## 📌 Overview

This project implements a **self-driving car simulation** with a full perception pipeline:

| Module | Method | Output |
|---|---|---|
| 🛣️ Lane Detection | Hough Transform + weighted lane averaging | Lane overlay + steering angle |
| 🚦 Traffic Detection | YOLOv8 Nano (pre-trained COCO) | Bounding boxes + class labels |
| 🎯 Steering Control | Geometric lane-center offset → angle | Degrees left / right / straight |
| 🎮 2D Simulation | Matplotlib animation | Real-time top-down car navigation |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **OpenCV** — Image processing, edge detection, Hough lines
- **YOLOv8 (Ultralytics)** — Real-time object & traffic sign detection
- **NumPy** — Numerical computation
- **Matplotlib** — Visualization & animated simulation

---

## 📁 Project Structure

```
Simulating Self Driving Cars/
├── simulating_self_driving_cars.ipynb   # Main notebook
├── README.md                            # This file
├── sample_road.png                      # Generated synthetic road image
├── lane_pipeline_steps.png              # Step-by-step lane detection result
├── object_detection.png                 # YOLOv8 detection result
├── full_pipeline_result.png             # Combined pipeline output
├── steering_visualization.png           # Steering angle visualization
├── simulation.gif                       # 2D simulation animation
└── results_summary.png                  # Summary of all results
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd "ML-CaPsule/Simulating Self Driving Cars"
```

### 2. Install dependencies
```bash
pip install opencv-python-headless ultralytics matplotlib numpy Pillow
```

### 3. Run the notebook
Open `simulating_self_driving_cars.ipynb` in **Jupyter Notebook** or **Google Colab** and run cells top to bottom.

> 💡 **Google Colab** recommended — no local setup required, GPU available for faster YOLOv8 inference.

---

## 📸 Results

### Lane Detection Pipeline
![Lane Detection Steps](lane_pipeline_steps.png)

### Object Detection (YOLOv8)
![Object Detection](object_detection.png)

### Full Pipeline Output
![Full Pipeline](full_pipeline_result.png)

### 2D Self-Driving Simulation
![Simulation](simulation.gif)

---

## 🔍 How It Works

### Lane Detection
```
Image → Grayscale → Gaussian Blur → Canny Edges
     → ROI Mask → Hough Lines → Weighted Average → Lane Overlay
```
- **ROI Masking** focuses only on the road area (trapezoidal region)
- **Hough Transform** detects line segments in edge image
- **Weighted averaging** by line length produces stable, smooth lanes

### Steering Angle
```
steering_angle = arctan( (image_center_x - lane_center_x) / look_ahead_distance )
```
- Positive angle → steer left
- Negative angle → steer right
- Near-zero → go straight

### Object Detection
- **YOLOv8 Nano** runs on every frame (CPU ~15 FPS, GPU ~60 FPS)
- Detects: cars, trucks, buses, motorcycles, pedestrians, traffic lights, stop signs
- Bounding boxes color-coded by class

### 2D Simulation
- Sinusoidal road path with perspective scrolling
- Car follows lane center using proportional steering controller
- Real-time steering chart plotted alongside simulation

---

## 🔮 Future Improvements

- Replace Hough lanes with **U-Net semantic segmentation**
- Add **PID controller** for smoother steering
- Train custom YOLOv8 on **GTSRB traffic sign dataset**
- Integrate with **CARLA 3D simulator**
- Add **speed control** based on detected obstacles

---

## 📄 License

This project is part of [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) — open source under MIT License.

---

*Contributed as part of **GSSoC 2026** — Open Source Track + AI/Agents Track*
