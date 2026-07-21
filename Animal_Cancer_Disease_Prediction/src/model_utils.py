"""A lightweight, deterministic image classifier for the educational demo.

No trained clinical model is bundled with this repository. Instead, the
classifier combines simple colour, contrast, and edge features. This makes the
pipeline reproducible and fast while demonstrating the same API shape that a
trained CNN could later implement.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Mapping

import numpy as np

CLASS_LABELS = ("non-cancerous", "cancerous")
DEFAULT_WEIGHTS = {
    "bias": -1.35,
    "contrast": 3.0,
    "edge_density": 2.4,
    "saturation": 1.1,
    "red_excess": 1.0,
}


@dataclass(frozen=True)
class Prediction:
    """A model prediction with a normalized confidence score."""

    label: str
    confidence: float
    cancer_probability: float


class DeterministicImageClassifier:
    """Classify images using documented, deterministic visual heuristics."""

    def __init__(self, weights: Mapping[str, float] | None = None) -> None:
        configured_weights = dict(DEFAULT_WEIGHTS)
        if weights:
            unknown = set(weights) - set(DEFAULT_WEIGHTS)
            if unknown:
                raise ValueError(f"Unknown model weight(s): {sorted(unknown)}")
            configured_weights.update(
                {name: float(value) for name, value in weights.items()}
            )
        self.weights = configured_weights

    @staticmethod
    def _validate_array(image_array: np.ndarray) -> np.ndarray:
        pixels = np.asarray(image_array, dtype=np.float32)
        if pixels.ndim != 3 or pixels.shape[-1] != 3:
            raise ValueError("Expected an image array shaped (height, width, 3).")
        if pixels.size == 0 or not np.isfinite(pixels).all():
            raise ValueError("Image array must contain finite pixel values.")
        if pixels.min() < 0.0 or pixels.max() > 1.0:
            raise ValueError("Image pixels must be normalized to the [0, 1] range.")
        return pixels

    def extract_features(self, image_array: np.ndarray) -> dict[str, float]:
        """Extract interpretable colour and texture features."""

        pixels = self._validate_array(image_array)
        gray = (
            0.299 * pixels[..., 0]
            + 0.587 * pixels[..., 1]
            + 0.114 * pixels[..., 2]
        )
        horizontal_edges = (
            float(np.abs(np.diff(gray, axis=1)).mean())
            if gray.shape[1] > 1
            else 0.0
        )
        vertical_edges = (
            float(np.abs(np.diff(gray, axis=0)).mean())
            if gray.shape[0] > 1
            else 0.0
        )
        channel_range = pixels.max(axis=2) - pixels.min(axis=2)
        red_excess = np.maximum(
            pixels[..., 0]
            - (pixels[..., 1] + pixels[..., 2]) / 2.0,
            0.0,
        )

        return {
            "contrast": float(gray.std()),
            "edge_density": (horizontal_edges + vertical_edges) / 2.0,
            "saturation": float(channel_range.mean()),
            "red_excess": float(red_excess.mean()),
        }

    def predict_cancer_probability(self, image_array: np.ndarray) -> float:
        """Return a deterministic cancer-like pattern score from 0 to 1."""

        features = self.extract_features(image_array)
        logit = self.weights["bias"] + sum(
            self.weights[name] * features[name] for name in features
        )
        probability = 1.0 / (1.0 + np.exp(-np.clip(logit, -30.0, 30.0)))
        return float(probability)


def create_demo_model(
    weights: Mapping[str, float] | None = None,
) -> DeterministicImageClassifier:
    """Create a fresh deterministic classifier."""

    return DeterministicImageClassifier(weights=weights)


def load_model(config_path: str | Path | None = None) -> DeterministicImageClassifier:
    """Load optional JSON weights, or return the default demo classifier.

    A configuration file should be a JSON object containing any subset of the
    keys in ``DEFAULT_WEIGHTS``.
    """

    if config_path is None:
        return create_demo_model()

    path = Path(config_path)
    try:
        with path.open("r", encoding="utf-8") as config_file:
            weights = json.load(config_file)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not load model configuration: {path}") from exc

    if not isinstance(weights, dict):
        raise ValueError("Model configuration must be a JSON object.")
    return create_demo_model(weights)


def predict_with_confidence(
    model: DeterministicImageClassifier, image_array: np.ndarray
) -> Prediction:
    """Return the most likely class and confidence for a preprocessed image."""

    cancer_probability = model.predict_cancer_probability(image_array)
    if cancer_probability >= 0.5:
        label = CLASS_LABELS[1]
        confidence = cancer_probability
    else:
        label = CLASS_LABELS[0]
        confidence = 1.0 - cancer_probability

    return Prediction(
        label=label,
        confidence=float(np.clip(confidence, 0.0, 1.0)),
        cancer_probability=float(np.clip(cancer_probability, 0.0, 1.0)),
    )
