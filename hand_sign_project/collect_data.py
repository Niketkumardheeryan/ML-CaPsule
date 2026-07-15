"""Collect hand gesture data using MediaPipe and save sequences as .npy files.

Usage:
    python collect_data.py --output_dir data --gestures A B C ... --sequences 30 --sequence_length 30
"""
import argparse
import os
import time
import numpy as np
import cv2
import mediapipe as mp
from utils import extract_keypoints


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def collect(output_dir, gestures, sequences=30, sequence_length=30, camera=0):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                           min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    ensure_dir(output_dir)
    for gesture in gestures:
        gesture_dir = os.path.join(output_dir, gesture)
        ensure_dir(gesture_dir)

    cap = cv2.VideoCapture(camera)
    if not cap.isOpened():
        raise RuntimeError('Could not open webcam')

    try:
        for gesture in gestures:
            print(f'Collecting for gesture: {gesture}')
            for seq in range(sequences):
                print(f'  Sequence {seq+1}/{sequences}')
                sequence = []
                # countdown
                for i in range(3, 0, -1):
                    ret, frame = cap.read()
                    if not ret:
                        continue
                    cv2.putText(frame, f'Starting in {i}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                    cv2.imshow('Collect', frame)
                    cv2.waitKey(500)

                frames_captured = 0
                while frames_captured < sequence_length:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(image)
                    keypoints = extract_keypoints(results)
                    sequence.append(keypoints)

                    # UI overlay
                    display = frame.copy()
                    cv2.putText(display, f'Gesture: {gesture} Seq: {seq+1}/{sequences} Frame: {frames_captured+1}/{sequence_length}',
                                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                    cv2.imshow('Collect', display)
                    frames_captured += 1
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        raise KeyboardInterrupt

                sequence = np.array(sequence)
                file_path = os.path.join(output_dir, gesture, f'{gesture}_{seq}.npy')
                np.save(file_path, sequence)
                print(f'    Saved {file_path} shape={sequence.shape}')

    except KeyboardInterrupt:
        print('Interrupted by user')
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str, default='data')
    parser.add_argument('--gestures', nargs='+', required=True,
                        help='List of gesture labels')
    parser.add_argument('--sequences', type=int, default=30)
    parser.add_argument('--sequence_length', type=int, default=30)
    parser.add_argument('--camera', type=int, default=0)
    args = parser.parse_args()

    collect(args.output_dir, args.gestures, args.sequences, args.sequence_length, args.camera)
