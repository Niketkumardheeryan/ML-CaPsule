"""Utility helpers for MediaPipe hand landmark extraction and preprocessing."""
from collections import deque
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands

def extract_keypoints(results):
    """Return flattened (x,y,z) array of 21 hand landmarks, normalized relative to wrist.

    If no hand detected, returns a zero array of length 63.
    """
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        coords = np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark])
        # Normalize: subtract wrist (landmark 0) and scale by max distance
        origin = coords[0].copy()
        coords = coords - origin
        max_val = np.max(np.abs(coords))
        if max_val > 0:
            coords = coords / max_val
        return coords.flatten()
    else:
        return np.zeros(21 * 3, dtype=float)

class SmoothPredictor:
    """Simple prediction smoothing using last-k majority vote.

    Usage:
        sp = SmoothPredictor(k=10)
        label = sp.update(pred_label)
    """
    def __init__(self, k=10):
        self.k = k
        self.q = deque(maxlen=k)

    def update(self, label):
        self.q.append(label)
        # majority vote
        vals, counts = np.unique(np.array(self.q), return_counts=True)
        return vals[np.argmax(counts)]
