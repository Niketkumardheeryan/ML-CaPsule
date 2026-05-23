"""
preprocessing.py
----------------
Hand landmark extraction using MediaPipe and dataset preparation
for Sign Language to Speech translation.
"""

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
import json
from pathlib import Path
from tqdm import tqdm
from typing import Optional, Tuple, List, Dict


# ── MediaPipe setup ──────────────────────────────────────────────────────────

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

NUM_LANDMARKS = 21          # MediaPipe Hands produces 21 landmarks
LANDMARK_DIM  = 3           # x, y, z per landmark
FEATURE_DIM   = NUM_LANDMARKS * LANDMARK_DIM  # 63 features per frame


# ── Landmark extraction ───────────────────────────────────────────────────────

class HandLandmarkExtractor:
    """
    Extracts normalised hand landmarks from images or video frames
    using MediaPipe Hands.

    Args:
        static_image_mode:  True for images, False for video streams.
        max_num_hands:      Maximum number of hands to detect.
        min_detection_confidence: Minimum confidence for detection.
        min_tracking_confidence:  Minimum confidence for tracking.
    """

    def __init__(
        self,
        static_image_mode: bool = True,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.5,
    ):
        self.hands = mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def extract(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract and normalise landmarks from a single BGR frame.

        Returns:
            numpy array of shape (63,) if a hand is detected, else None.
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None

        landmarks = results.multi_hand_landmarks[0]

        # Flatten (x, y, z) for all 21 landmarks
        coords = np.array(
            [[lm.x, lm.y, lm.z] for lm in landmarks.landmark],
            dtype=np.float32,
        ).flatten()

        return self._normalize(coords)

    def _normalize(self, coords: np.ndarray) -> np.ndarray:
        """
        Translate landmarks so the wrist (landmark 0) is at the origin,
        then scale so the palm span == 1.
        """
        coords = coords.reshape(NUM_LANDMARKS, LANDMARK_DIM)

        # Centre on wrist
        wrist = coords[0].copy()
        coords -= wrist

        # Scale by distance between wrist and middle-finger MCP (landmark 9)
        scale = np.linalg.norm(coords[9])
        if scale > 1e-6:
            coords /= scale

        return coords.flatten()

    def draw_landmarks(self, frame: np.ndarray) -> np.ndarray:
        """Overlay landmark skeleton on a BGR frame and return annotated copy."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )
        return frame

    def close(self):
        self.hands.close()


# ── Dataset building ──────────────────────────────────────────────────────────

class DatasetBuilder:
    """
    Walks an image dataset organised as:
        dataset_root/
            <class_label>/
                img_001.jpg
                img_002.jpg
                ...

    and extracts landmark features for each image, saving a CSV
    suitable for training.
    """

    def __init__(self, dataset_root: str, output_path: str):
        self.dataset_root = Path(dataset_root)
        self.output_path  = Path(output_path)
        self.extractor    = HandLandmarkExtractor(static_image_mode=True)

    def build(self) -> pd.DataFrame:
        """
        Process every image in the dataset, extract landmarks, and
        return a DataFrame (also saved to output_path).
        """
        records: List[Dict] = []
        class_dirs = sorted(p for p in self.dataset_root.iterdir() if p.is_dir())

        for class_dir in tqdm(class_dirs, desc="Classes"):
            label = class_dir.name
            images = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png"))

            for img_path in images:
                frame = cv2.imread(str(img_path))
                if frame is None:
                    continue

                features = self.extractor.extract(frame)
                if features is None:
                    continue

                record = {f"f{i}": v for i, v in enumerate(features)}
                record["label"] = label
                records.append(record)

        df = pd.DataFrame(records)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_path, index=False)
        print(f"Saved {len(df)} samples → {self.output_path}")
        return df

    def close(self):
        self.extractor.close()


# ── Sequence builder for temporal data ───────────────────────────────────────

class SequenceBuilder:
    """
    Reads a video or webcam stream and assembles fixed-length sequences
    of landmark frames for sentence-level prediction.

    Args:
        sequence_length: Number of frames per sequence.
        extractor:       HandLandmarkExtractor instance.
    """

    def __init__(self, sequence_length: int = 30,
                 extractor: Optional[HandLandmarkExtractor] = None):
        self.sequence_length = sequence_length
        self.extractor = extractor or HandLandmarkExtractor(static_image_mode=False)
        self._buffer: List[np.ndarray] = []

    def push_frame(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Add one frame to the rolling buffer.

        Returns:
            Complete sequence array of shape (sequence_length, FEATURE_DIM)
            once the buffer is full, else None.
        """
        features = self.extractor.extract(frame)
        if features is not None:
            self._buffer.append(features)
            if len(self._buffer) > self.sequence_length:
                self._buffer.pop(0)

        if len(self._buffer) == self.sequence_length:
            return np.stack(self._buffer)
        return None

    def reset(self):
        self._buffer.clear()


# ── Label encoding helpers ────────────────────────────────────────────────────

def build_label_encoder(labels: List[str]) -> Tuple[Dict, Dict]:
    """
    Return (label→index, index→label) mappings for a list of class names.
    """
    unique = sorted(set(labels))
    l2i = {l: i for i, l in enumerate(unique)}
    i2l = {i: l for l, i in l2i.items()}
    return l2i, i2l


def save_label_encoder(l2i: Dict, path: str):
    with open(path, "w") as f:
        json.dump(l2i, f, indent=2)
    print(f"Label encoder saved → {path}")


def load_label_encoder(path: str) -> Tuple[Dict, Dict]:
    with open(path) as f:
        l2i = json.load(f)
    i2l = {int(i): l for l, i in l2i.items()}
    return l2i, i2l


# ── Data augmentation ─────────────────────────────────────────────────────────

def augment_landmarks(features: np.ndarray,
                      noise_std: float = 0.005,
                      rotation_deg: float = 15.0) -> np.ndarray:
    """
    Apply minor noise and 2-D rotation to landmark coordinates for
    data augmentation during training.

    Args:
        features:     Flat landmark array of length FEATURE_DIM.
        noise_std:    Standard deviation of Gaussian noise.
        rotation_deg: Maximum rotation in degrees.

    Returns:
        Augmented landmark array of the same shape.
    """
    pts = features.reshape(NUM_LANDMARKS, LANDMARK_DIM).copy()

    # Gaussian noise
    pts += np.random.normal(0, noise_std, pts.shape).astype(np.float32)

    # Random 2-D rotation around z-axis (in-plane)
    angle = np.radians(np.random.uniform(-rotation_deg, rotation_deg))
    c, s  = np.cos(angle), np.sin(angle)
    rot   = np.array([[c, -s], [s, c]], dtype=np.float32)
    pts[:, :2] = pts[:, :2] @ rot.T

    return pts.flatten()


# ── CLI entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Preprocess sign language dataset")
    parser.add_argument("--dataset_root", type=str, required=True,
                        help="Root directory containing class sub-directories")
    parser.add_argument("--output",       type=str, default="dataset/features.csv",
                        help="Output CSV path")
    args = parser.parse_args()

    builder = DatasetBuilder(args.dataset_root, args.output)
    df = builder.build()
    builder.close()
    print(df.head())
