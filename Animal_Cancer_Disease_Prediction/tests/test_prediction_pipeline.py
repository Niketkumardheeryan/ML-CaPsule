"""Tests for the end-to-end prediction pipeline."""

from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image

from Animal_Cancer_Disease_Prediction.src.model_utils import CLASS_LABELS
from Animal_Cancer_Disease_Prediction.src.predict import predict_image


def _create_test_image(path: Path) -> Path:
    generator = np.random.default_rng(1871)
    pixels = generator.integers(25, 225, size=(48, 48, 3), dtype=np.uint8)
    Image.fromarray(pixels, mode="RGB").save(path)
    return path


def test_prediction_returns_valid_label(tmp_path: Path) -> None:
    result = predict_image(_create_test_image(tmp_path / "cells.png"))

    assert result.success
    assert result.label in CLASS_LABELS


def test_confidence_is_between_zero_and_one(tmp_path: Path) -> None:
    result = predict_image(_create_test_image(tmp_path / "cells.jpg"))

    assert result.success
    assert result.confidence is not None
    assert 0.0 <= result.confidence <= 1.0


def test_uploaded_image_object_is_supported() -> None:
    buffer = BytesIO()
    buffer.name = "uploaded.png"
    Image.new("RGB", (24, 24), color=(130, 80, 90)).save(buffer, format="PNG")
    buffer.seek(0)

    result = predict_image(buffer)

    assert result.success
    assert result.label in CLASS_LABELS


def test_invalid_input_is_handled_safely() -> None:
    result = predict_image(None)

    assert not result.success
    assert result.label is None
    assert result.confidence is None
    assert result.error
