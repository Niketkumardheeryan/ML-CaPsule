"""Tests for safe image preprocessing."""

from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from Animal_Cancer_Disease_Prediction.src.preprocessing import (
    ImageProcessingError,
    load_image,
    preprocess_image,
    validate_image_extension,
)


def _save_test_image(path: Path, size: tuple[int, int] = (40, 24)) -> Path:
    pixels = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    pixels[..., 0] = 180
    pixels[..., 1] = 90
    Image.fromarray(pixels, mode="RGB").save(path)
    return path


def test_valid_image_preprocessing(tmp_path: Path) -> None:
    image_path = _save_test_image(tmp_path / "sample.png")

    loaded = load_image(image_path)

    assert loaded.mode == "RGB"
    assert loaded.size == (40, 24)


def test_invalid_extension_is_rejected() -> None:
    with pytest.raises(ImageProcessingError, match="Unsupported"):
        validate_image_extension("sample.txt")


def test_resized_normalized_output_shape(tmp_path: Path) -> None:
    image_path = _save_test_image(tmp_path / "sample.jpg")

    result = preprocess_image(image_path, target_size=(64, 48))

    assert result.shape == (48, 64, 3)
    assert result.dtype == np.float32
    assert 0.0 <= float(result.min()) <= float(result.max()) <= 1.0


def test_corrupt_image_is_handled(tmp_path: Path) -> None:
    corrupt_path = tmp_path / "corrupt.png"
    corrupt_path.write_bytes(b"this is not an image")

    with pytest.raises(ImageProcessingError, match="valid image"):
        preprocess_image(corrupt_path)
