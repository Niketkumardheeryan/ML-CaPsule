"""Run real-time hand sign recognition using MediaPipe and a trained LSTM model.

Usage:
    python realtime_detection.py --model_dir models
"""
import time
import json
from collections import deque
import numpy as np
import cv2
import mediapipe as mp
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False

from utils import extract_keypoints, SmoothPredictor


def load_labels(model_dir='models'):
    with open(f'{model_dir}/labels.json', 'r') as f:
        labels = json.load(f)
    return labels


def main(model_dir='models', camera=0, sequence_length=30):
    labels = load_labels(model_dir)
    if TF_AVAILABLE:
        model = tf.keras.models.load_model(f'{model_dir}/best_model.h5')
    else:
        model = None

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                           min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(camera)
    if not cap.isOpened():
        raise RuntimeError('Could not open webcam')

    seq = deque(maxlen=sequence_length)
    sp = SmoothPredictor(k=10)

    prev_time = time.time()
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            keypoints = extract_keypoints(results)
            seq.append(keypoints)

            if len(seq) == sequence_length and model is not None:
                X = np.expand_dims(np.array(seq), axis=0)
                preds = model.predict(X)
                pred_idx = int(np.argmax(preds))
                conf = float(np.max(preds))
                label = labels[pred_idx]
                label_smoothed = sp.update(label)
            else:
                if not TF_AVAILABLE:
                    label_smoothed = 'TF not installed'
                else:
                    label_smoothed = '...'
                conf = 0.0

            # overlay
            h, w, _ = frame.shape
            cv2.rectangle(frame, (0,0), (w,40), (0,0,0), -1)
            cv2.putText(frame, f'Pred: {label_smoothed} ({conf:.2f})', (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

            # FPS
            curr_time = time.time()
            fps = 1/(curr_time - prev_time) if curr_time!=prev_time else 0.0
            prev_time = curr_time
            cv2.putText(frame, f'FPS: {int(fps)}', (w-120,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

            cv2.imshow('Real-Time Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str, default='models')
    parser.add_argument('--camera', type=int, default=0)
    parser.add_argument('--sequence_length', type=int, default=30)
    args = parser.parse_args()
    main(args.model_dir, args.camera, args.sequence_length)
