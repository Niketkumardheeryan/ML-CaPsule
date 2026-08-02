# Chess Piece Classification using Machine learning

This project involves developing a machine learning application to classify chess pieces from images using a Convolutional Neural Network (CNN). The process begins with collecting and preprocessing a dataset of chess piece images, including various classes such as bishop, king, knight, pawn, queen, and rook. The images are resized, normalized, and split into training and validation sets to train the CNN model. The model's performance is evaluated based on accuracy, precision, recall, and F1 score.

For real-time predictions, a Streamlit application is created. Users can upload images of chess pieces, which are then processed and classified by the trained model. The application displays the prediction result in a styled success box with bold white text, and also provides additional information about the identified chess piece. The project integrates image preprocessing, model inference, and user interaction, showcasing how machine learning models can be deployed in web applications for practical use cases.


## Model Training and evaluation :
 
CNN model is trained over batch size = 128 ,with 100 epochs input image size =(128,128,3)  achieved average validation accuracy of 97.11 %

## Dataset :

https://www.kaggle.com/datasets/s4lman/chess-pieces-dataset-85x85


## Inference : 

Deployed the model with the help streamlit web application to classify the chess piece and provide info regarding its moves with the help of text and visuals.

## Libraries Used


1. **Scikit learn**: For machine learning processing  and operations
2. **Matplotlib**: For plotting and visualizing the detection results.
3. **Pandas**: For image manipulation.
4. **NumPy**: For efficient numerical operations.
5. **Seaborn** : for advanced data visualizations
6. **plotly** : for 3D data visualizations .
7. **Streamlit** : for creating gui of the web application.
8. **Tensorflow** : for image based manipulation operations.


## How to Use

1. **Clone the Repository**: 
    ```sh
    git clone url_to_this_repository
    ```

2. **Install Dependencies**: 
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Model**: 
    (download the model final_chess.h5 from below link and put in same directoy :
      https://drive.google.com/file/d/1QK6a2yCJo3EvKvoEJA6QGkcFEmzm5IiG/view?usp=sharing)

    ```python
    streamlit run app.py
    ```

4. **View Results**: The script will allow you to classify the chess image and give information regrading tis moves with the help of text and visuals .

**DEMO** :


https://github.com/user-attachments/assets/c06554e5-81ff-4151-97a9-74fdfb4ff760




# ♟️ Chess Piece Detection and Classification using YOLOv8 and OpenCV

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8-orange?logo=pytorch)](https://docs.ultralytics.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green?logo=opencv)](https://opencv.org/)
[![Roboflow](https://img.shields.io/badge/Dataset-Roboflow-purple)](https://universe.roboflow.com/chess-pieces-nemtd/chess-pieces-detection)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](../LICENSE)

> A complete end-to-end Jupyter notebook for detecting and classifying chess pieces from board images using **YOLOv8** and **OpenCV**. Covers dataset download, model fine-tuning, inference, batch visualization, and evaluation metrics.

---

## 📌 Project Overview

This project trains a **YOLOv8** object detection model to recognize **12 chess piece classes** (white/black × king, queen, rook, bishop, knight, pawn) from board images in a single pass — combining detection and classification without requiring a separate cropping step.

### Why YOLO?

| Approach | Pros | Cons |
|---|---|---|
| **YOLOv8 (this project)** | Single-pass detection + classification, fast, accurate | Needs GPU for fast training |
| CNN on cropped pieces | Simple classifier | Needs separate detector; two-stage pipeline |
| Template matching / HOG | No training needed | Fails on varied angles and lighting |

---

## 🖼️ Results

> 📸 Run `chess_piece_detection_yolo.ipynb` end-to-end to generate result images.
> The notebook automatically saves the following to the `results/` folder:
>
> | Output file | Contents |
> |---|---|
> | `batch_inference.png` | 6-image grid with annotated bounding boxes |
> | `training_curves.png` | Loss and mAP curves over epochs |
> | `per_class_metrics.png` | Per-class AP@50 and AP@50-95 bar charts |
> | `confusion_matrix_display.png` | Validation confusion matrix |
> | `detection_statistics.png` | Piece count and confidence score distribution |

---

## 🗂️ Repository Structure

```
Chess_Piece_Detection_and_Classification_using_YOLO_and_OpenCV/
├── chess_piece_detection_yolo.ipynb   # Main Jupyter notebook (all steps)
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## 🧩 Classes Detected

| ID | Class | Color |
|----|-------|-------|
| 0–5 | king, queen, rook, bishop, knight, pawn | ⬜ White |
| 6–11 | king, queen, rook, bishop, knight, pawn | ⬛ Black |

*(Exact class IDs depend on the Roboflow dataset version.)*

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8+
- A GPU is **strongly recommended** for training (or use [Google Colab](https://colab.research.google.com/))
- A free [Roboflow API key](https://app.roboflow.com)

### 2. Installation

```bash
# Clone the repo (or your fork)
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd "ML-CaPsule/Chess_Piece_Detection_and_Classification_using_YOLO_and_OpenCV"

# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Get Your Roboflow API Key

1. Sign up for free at [app.roboflow.com](https://app.roboflow.com)
2. Go to **Settings → API Keys**
3. Copy your key

### 4. Run the Notebook

```bash
jupyter notebook chess_piece_detection_yolo.ipynb
```

Open the notebook and:
1. Paste your Roboflow API key into the `ROBOFLOW_API_KEY` variable in **Section 2**
2. Run all cells top to bottom (`Cell → Run All`)

---

## 📓 Notebook Walkthrough

| Section | Description |
|---------|-------------|
| **1. Dependencies** | Import libraries, check GPU availability |
| **2. Dataset Download** | Pull chess dataset from Roboflow in YOLOv8 format, show split sizes and sample annotations |
| **3. Model Training** | Fine-tune `yolov8n.pt` with configurable epochs, batch size, and early stopping; plot training curves |
| **4. Evaluation** | Compute mAP50, mAP50-95, precision, recall; display per-class bar charts and confusion matrix |
| **5. Inference & Visualization** | Run detection on single and batch test images with annotated bounding boxes; show confidence distribution |
| **6. Export** | Export trained model to ONNX for deployment |
| **7. Summary** | Results table, improvement ideas, references |

---

## ⚙️ Configuration

Key variables at the top of each training cell (easy to customize):

```python
MODEL_WEIGHTS = 'yolov8n.pt'   # 'yolov8s.pt' or 'yolov8m.pt' for better accuracy
EPOCHS        = 50             # Increase to 100 for best results
IMG_SIZE      = 640            # Standard YOLO input resolution
BATCH_SIZE    = 16             # Reduce to 8 if GPU runs out of memory
```

---

## 📦 Dataset

- **Source:** [Roboflow Universe — Chess Pieces Detection](https://universe.roboflow.com/chess-pieces-nemtd/chess-pieces-detection)
- **Format:** YOLOv8 (images + YOLO label `.txt` files + `data.yaml`)
- **License:** Public — free download via Roboflow API (no login required for public datasets)
- **Splits:** Train / Validation / Test

---

## 🔧 Requirements

| Package | Version |
|---------|---------|
| ultralytics | ≥ 8.0.0 |
| opencv-python | ≥ 4.8.0 |
| roboflow | ≥ 1.1.0 |
| matplotlib | ≥ 3.7.0 |
| seaborn | ≥ 0.12.0 |
| scikit-learn | ≥ 1.3.0 |
| pandas | ≥ 2.0.0 |
| numpy | ≥ 1.24.0 |

---

## 💡 Possible Extensions

- 🎥 **Real-time webcam detection** — stream a live board view through the model
- ♟️ **FEN string generation** — convert detected piece positions to chess notation
- 📱 **Mobile deployment** — export to TFLite or CoreML for on-device inference
- 🤖 **Game analysis** — feed detections into a chess engine (Stockfish) for move suggestions
- 🔁 **More epochs + larger model** — swap `yolov8n` for `yolov8m` for higher mAP

---

## 🤝 Contributing

Pull requests are welcome! Please read the repo's [CONTRIBUTING.md](../CONTRIBUTING.md) before submitting.

---

## 📄 License

This project follows the license of the parent [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) repository.

---

## 🔗 References

- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com)
- [Roboflow Chess Dataset](https://universe.roboflow.com/chess-pieces-nemtd/chess-pieces-detection)
- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- [GSSoC ML-CaPsule Issue #1501](https://github.com/Niketkumardheeryan/ML-CaPsule/issues/1501)
