# 😷 Face Mask Detection using EfficientNetB0

A Deep Learning based Face Mask Detection system capable of classifying whether a person is:

- ✅ Wearing a Mask Correctly
- ⚠️ Wearing a Mask Incorrectly
- ❌ Not Wearing a Mask

The project uses **EfficientNetB0** with **Transfer Learning** for mask classification and **MTCNN** for face detection. A **Streamlit** web application is included for image upload and real-time webcam detection.

---

## Features

- Multi-class mask detection
- EfficientNetB0 Transfer Learning
- Face detection using MTCNN
- Image upload prediction
- Real-time webcam detection
- Streamlit web application
- Early stopping and learning rate scheduling
- Model checkpointing
- TensorFlow/Keras implementation

---

## Classes

| Label | Class |
|-------|-------|
| 0 | No Mask |
| 1 | Incorrect Mask |
| 2 | Mask Worn Correctly |

---

## Dataset

Dataset used:

**Face Mask Dataset**

https://www.kaggle.com/datasets/shiekhburhan/face-mask-dataset

Dataset Structure

```
FMD_DATASET/
│
├── with_mask/
│   └── simple/
│
├── without_mask/
│   └── simple/
│
└── incorrect_mask/
    ├── mc/
    └── mmc/
```

Total images:

- With Mask
- Without Mask
- Incorrect Mask (MC)
- Incorrect Mask (MMC)

Total ≈ **13,000 images**

---

## Project Structure

```
FaceMaskDetect/
│
├── app.py
├── FaceMaskDetection.ipynb
├── best_facemask_effnet.keras
├── requirements.txt
├── README.md
│
├── images/
│
└── screenshots/
```

---

## Model Architecture

### Face Detection

- MTCNN

### Classification Model

- EfficientNetB0
- ImageNet Pretrained Weights
- GlobalAveragePooling
- Dense (128)
- Dropout (0.4)
- Dense (Softmax)

Input Size

```
128 × 128 × 3
```

Output

```
3 Classes
```

---

## Training

### Optimizer

Adam

Learning Rate

```
1e-4
```

Loss Function

```
Sparse Categorical Crossentropy
```

Callbacks

- EarlyStopping
- ReduceLROnPlateau
- ModelCheckpoint

---

## Installation


Install dependencies

```bash
pip install -r requirements.txt
```

---

## Download Dataset

Using KaggleHub

```python
import kagglehub

path = kagglehub.dataset_download(
    "shiekhburhan/face-mask-dataset"
)
```

---

## Train the Model

Run

```
FaceMaskDetection.ipynb
```

The trained model will be saved as

```
best_facemask_effnet.keras
```

---

## Run Streamlit App

```bash
streamlit run app.py
```

---

## Webcam Detection

The application supports

- Live webcam detection
- Multiple faces
- Confidence score
- Bounding boxes
- Color coded predictions

Green

```
Mask Worn Correctly
```

Orange

```
Incorrect Mask
```

Red

```
No Mask
```

---

## Technologies Used

- Python
- TensorFlow
- Keras
- EfficientNetB0
- MTCNN
- OpenCV
- Streamlit
- streamlit-webrtc
- NumPy
- Matplotlib
- Pillow
- KaggleHub

---

## Results

The model successfully classifies:

- Correct Mask
- Incorrect Mask
- No Mask

using transfer learning with EfficientNetB0 and performs real-time inference on webcam streams.

---

## Future Improvements

- MobileNetV3 implementation
- TensorRT optimization
- YOLOv11 integration
- Quantized TensorFlow Lite model
- ONNX deployment
- Docker support
- Hugging Face Spaces deployment
- Multi-camera support

---

## License

This project is intended for educational and research purposes.