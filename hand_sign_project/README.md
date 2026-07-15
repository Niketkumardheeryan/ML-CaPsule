# Real-Time Hand Sign Language Detection (MediaPipe + LSTM)

Project to collect hand landmark sequences with MediaPipe, train a 3-layer LSTM model, and perform real-time gesture recognition.

**Features**
- Real-time webcam capture
- MediaPipe Hands to extract 21 landmarks
- Sequence dataset collection (NumPy arrays)
- 3-layer LSTM for classification of 10 gestures
- Real-time prediction with smoothing and overlay
- Training reports: accuracy/loss plots, confusion matrix, classification report

**Project Structure**
```
hand_sign_project/
├── data/            # collected .npy sequences per gesture
├── models/          # saved models and labels
├── outputs/         # training plots and reports
├── notebooks/       # optional analysis notebooks
├── README.md
├── requirements.txt
├── train.py
├── collect_data.py
├── realtime_detection.py
├── utils.py
```

Installation
1. Create a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Usage
1. Collect data (example):

```bash
python collect_data.py --output_dir data --gestures A B C D E Hello Thanks Yes No I_Love_You --sequences 30 --sequence_length 30
```

2. Train model:

```bash
python train.py --data_dir data --model_dir models --outputs_dir outputs
```

3. Run realtime detection (after training):

```bash
python realtime_detection.py --model_dir models
```

Model Architecture
- 3 LSTM layers (64 -> 128 -> 64) with Dropout
- Dense(64, relu) -> Dense(num_classes, softmax)

Results
- Model summary, accuracy/loss plots, confusion matrix and classification report are saved in `outputs/`.

Future Improvements
- Add data augmentation and more participants
- Support multi-hand gestures
- Improve normalization and temporal augmentation
- Export a TensorFlow Lite model for mobile/web

Screenshots
- Place screenshots in `outputs/screenshots/` for demonstration.
