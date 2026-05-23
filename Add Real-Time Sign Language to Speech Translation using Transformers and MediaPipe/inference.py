"""
inference.py
------------
Real-time sign language recognition from webcam.

Pipeline:
  webcam → MediaPipe landmarks → Transformer → predicted label → TTS
"""

import cv2
import time
import queue
import threading
import numpy as np
import torch
from pathlib import Path
from collections import deque
from typing import Optional, Dict, Tuple

import pyttsx3

from preprocessing import HandLandmarkExtractor, SequenceBuilder, load_label_encoder, FEATURE_DIM
from train import SignLanguageTransformer


# ── TTS engine (runs in background thread) ───────────────────────────────────

class TTSWorker:
    """
    Asynchronous text-to-speech worker using pyttsx3.
    Accepts strings via put() and speaks them without blocking inference.
    """

    def __init__(self, rate: int = 150, volume: float = 1.0):
        self._queue  = queue.Queue()
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate",   rate)
        self._engine.setProperty("volume", volume)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def put(self, text: str):
        self._queue.put(text)

    def _run(self):
        while True:
            text = self._queue.get()
            if text is None:
                break
            self._engine.say(text)
            self._engine.runAndWait()

    def stop(self):
        self._queue.put(None)


# ── Inference engine ──────────────────────────────────────────────────────────

class SignLanguageInference:
    """
    Loads a trained model and runs real-time inference from a webcam.

    Args:
        model_path:        Path to best_model.pt checkpoint.
        label_encoder_path: Path to label_encoder.json.
        confidence_thresh: Minimum softmax probability to accept a prediction.
        sequence_length:   Frames per sequence (None = single-frame mode).
        smooth_window:     Number of consecutive matching predictions before accepting.
        camera_index:      OpenCV camera index.
    """

    def __init__(
        self,
        model_path: str = "models/best_model.pt",
        label_encoder_path: str = "models/label_encoder.json",
        confidence_thresh: float = 0.80,
        sequence_length: Optional[int] = None,
        smooth_window: int = 5,
        camera_index: int = 0,
    ):
        self.confidence_thresh = confidence_thresh
        self.smooth_window     = smooth_window
        self.sequence_length   = sequence_length

        # Label maps
        self.l2i, self.i2l = load_label_encoder(label_encoder_path)
        self.num_classes    = len(self.l2i)

        # Model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model  = self._load_model(model_path)

        # MediaPipe & sequence buffer
        self.extractor       = HandLandmarkExtractor(static_image_mode=False)
        self.sequence_builder = SequenceBuilder(
            sequence_length=sequence_length or 1,
            extractor=self.extractor
        ) if sequence_length else None

        # Smoothing buffer
        self._pred_buffer: deque = deque(maxlen=smooth_window)

        # TTS
        self.tts = TTSWorker()

        # Camera
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def _load_model(self, path: str) -> SignLanguageTransformer:
        ckpt = torch.load(path, map_location=self.device)
        model = SignLanguageTransformer(
            feature_dim=FEATURE_DIM,
            num_classes=self.num_classes,
        ).to(self.device)
        model.load_state_dict(ckpt["model_state"])
        model.eval()
        print(f"Model loaded from {path}  (epoch {ckpt.get('epoch', '?')})")
        return model

    @torch.no_grad()
    def predict_frame(self, frame: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Run inference on a single BGR frame.

        Returns:
            (predicted_label, confidence) or (None, 0.0) if no hand detected
            or confidence is below threshold.
        """
        if self.sequence_builder:
            seq = self.sequence_builder.push_frame(frame)
            if seq is None:
                return None, 0.0
            tensor = torch.tensor(seq, dtype=torch.float32).unsqueeze(0).to(self.device)
        else:
            features = self.extractor.extract(frame)
            if features is None:
                self._pred_buffer.clear()
                return None, 0.0
            tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(self.device)

        logits = self.model(tensor)
        probs  = torch.softmax(logits, dim=-1)[0]
        conf, idx = probs.max(0)
        conf = conf.item()

        if conf < self.confidence_thresh:
            return None, conf

        label = self.i2l[idx.item()]
        return label, conf

    def _smooth_prediction(self, label: Optional[str]) -> Optional[str]:
        """
        Accept a prediction only when the same label appears
        smooth_window times in a row.
        """
        self._pred_buffer.append(label)
        if len(self._pred_buffer) < self.smooth_window:
            return None
        unique = set(self._pred_buffer)
        if len(unique) == 1 and None not in unique:
            return self._pred_buffer[-1]
        return None

    def _draw_ui(self, frame: np.ndarray, label: Optional[str],
                 conf: float, sentence: str) -> np.ndarray:
        """Render landmark overlay + prediction HUD onto the frame."""
        frame = self.extractor.draw_landmarks(frame)
        h, w  = frame.shape[:2]

        # Prediction bar background
        cv2.rectangle(frame, (0, h - 80), (w, h), (0, 0, 0), -1)

        # Label
        if label:
            text = f"{label}  ({conf:.0%})"
            cv2.putText(frame, text, (20, h - 48),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 150), 2)

        # Sentence so far
        cv2.putText(frame, f"Sentence: {sentence}", (20, h - 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        # FPS (top-right)
        return frame

    def run(self):
        """Main loop: capture → predict → display → speak."""
        print("Starting real-time inference — press Q to quit, SPACE to speak sentence, C to clear")
        sentence: list = []
        last_spoken: Optional[str] = None
        prev_stable: Optional[str] = None
        t0 = time.time()

        while True:
            ok, frame = self.cap.read()
            if not ok:
                print("Camera read failed — exiting")
                break

            frame = cv2.flip(frame, 1)   # mirror for natural interaction
            label, conf = self.predict_frame(frame)
            stable = self._smooth_prediction(label)

            # Auto-append a newly stabilised sign
            if stable and stable != prev_stable:
                sentence.append(stable)
                prev_stable = stable
                # Speak individual letter/word
                self.tts.put(stable)

            sentence_str = " ".join(sentence)
            frame = self._draw_ui(frame, label, conf, sentence_str)

            # FPS
            fps = 1.0 / max(time.time() - t0, 1e-6)
            t0  = time.time()
            cv2.putText(frame, f"{fps:.0f} FPS", (frame.shape[1] - 90, 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 200, 255), 1)

            cv2.imshow("Sign Language → Speech", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            elif key == ord(" ") and sentence:
                full = " ".join(sentence)
                print(f"Speaking: {full}")
                self.tts.put(full)
            elif key == ord("c"):
                sentence.clear()
                prev_stable = None
                print("Sentence cleared")

        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.extractor.close()
        self.tts.stop()


# ── Static image inference ────────────────────────────────────────────────────

def predict_image(image_path: str, model_path: str, label_encoder_path: str) -> dict:
    """Run inference on a single image file and return results as a dict."""
    engine = SignLanguageInference(
        model_path=model_path,
        label_encoder_path=label_encoder_path,
    )
    frame = cv2.imread(image_path)
    if frame is None:
        return {"error": f"Could not load {image_path}"}

    label, conf = engine.predict_frame(frame)
    engine.cleanup()
    return {"label": label, "confidence": round(conf, 4)}


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Real-time sign language inference")
    parser.add_argument("--model",         default="models/best_model.pt")
    parser.add_argument("--label_encoder", default="models/label_encoder.json")
    parser.add_argument("--threshold",     type=float, default=0.80)
    parser.add_argument("--seq_len",       type=int,   default=None)
    parser.add_argument("--camera",        type=int,   default=0)
    parser.add_argument("--image",         type=str,   default=None,
                        help="Path to a single image for offline inference")
    args = parser.parse_args()

    if args.image:
        result = predict_image(args.image, args.model, args.label_encoder)
        print(result)
    else:
        engine = SignLanguageInference(
            model_path=args.model,
            label_encoder_path=args.label_encoder,
            confidence_thresh=args.threshold,
            sequence_length=args.seq_len,
            camera_index=args.camera,
        )
        engine.run()
