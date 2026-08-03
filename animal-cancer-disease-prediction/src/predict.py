"""End-to-end prediction pipeline for paths and uploaded images."""

from __future__ import annotations

from dataclasses import dataclass

from .model_utils import (
    DeterministicImageClassifier,
    load_model,
    predict_with_confidence,
)
from .preprocessing import ImageProcessingError, ImageSource, preprocess_image


@dataclass(frozen=True)
class PredictionResult:
    """Safe public result returned by ``predict_image``."""

    label: str | None = None
    confidence: float | None = None
    cancer_probability: float | None = None
    error: str | None = None

    @property
    def success(self) -> bool:
        """Whether prediction completed successfully."""

        return self.error is None and self.label is not None


def predict_image(
    source: ImageSource,
    model: DeterministicImageClassifier | None = None,
) -> PredictionResult:
    """Run the complete prediction pipeline without leaking input errors.

    Args:
        source: Image path, Pillow image, or uploaded file-like object.
        model: Optional compatible classifier. The default is deterministic.

    Returns:
        ``PredictionResult`` containing either prediction values or an error.
    """

    try:
        image_array = preprocess_image(source)
        prediction = predict_with_confidence(model or load_model(), image_array)
        return PredictionResult(
            label=prediction.label,
            confidence=prediction.confidence,
            cancer_probability=prediction.cancer_probability,
        )
    except (ImageProcessingError, OSError, TypeError, ValueError) as exc:
        return PredictionResult(error=str(exc))
    except Exception:
        # The app boundary should fail safely even if a custom model misbehaves.
        return PredictionResult(
            error="Prediction could not be completed. Please try another image."
        )
