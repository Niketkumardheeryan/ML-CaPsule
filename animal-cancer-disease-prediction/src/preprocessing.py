"""Safe image validation and preprocessing utilities.

The functions in this module accept file paths, Pillow images, and file-like
objects such as Streamlit's ``UploadedFile``.
"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

ALLOWED_EXTENSIONS = frozenset(
    {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
)
DEFAULT_IMAGE_SIZE = (128, 128)

ImageSource = Union[str, Path, BinaryIO, Image.Image]


class ImageProcessingError(ValueError):
    """Raised when an image cannot be validated or decoded safely."""


def is_allowed_extension(filename: str | Path) -> bool:
    """Return whether *filename* has a supported image extension."""

    return Path(str(filename)).suffix.lower() in ALLOWED_EXTENSIONS


def validate_image_extension(filename: str | Path) -> None:
    """Raise ``ImageProcessingError`` if *filename* is not supported."""

    if not filename or not is_allowed_extension(filename):
        supported = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ImageProcessingError(
            f"Unsupported image extension. Choose one of: {supported}."
        )


def _validate_source_name(source: ImageSource) -> None:
    """Validate a path or an uploaded object's filename when available."""

    if isinstance(source, (str, Path)):
        validate_image_extension(source)
        return

    source_name = getattr(source, "name", None)
    if source_name:
        validate_image_extension(source_name)


def load_image(source: ImageSource) -> Image.Image:
    """Load *source* as an independent RGB Pillow image.

    The image data is read eagerly, so the returned object does not depend on
    an open file handle. Invalid paths, extensions, and corrupt image bytes are
    converted to the project-specific ``ImageProcessingError``.
    """

    if source is None:
        raise ImageProcessingError("No image was provided.")

    _validate_source_name(source)

    if isinstance(source, Image.Image):
        try:
            return ImageOps.exif_transpose(source).convert("RGB").copy()
        except (OSError, ValueError) as exc:
            raise ImageProcessingError("The provided image is invalid.") from exc

    if isinstance(source, (str, Path)) and not Path(source).is_file():
        raise ImageProcessingError(f"Image file not found: {source}")

    original_position = None
    if hasattr(source, "tell") and hasattr(source, "seek"):
        try:
            original_position = source.tell()
            source.seek(0)
        except (OSError, ValueError):
            original_position = None

    try:
        with Image.open(source) as opened_image:
            opened_image.load()
            image = ImageOps.exif_transpose(opened_image).convert("RGB").copy()
    except (
        FileNotFoundError,
        IsADirectoryError,
        OSError,
        TypeError,
        UnidentifiedImageError,
        ValueError,
    ) as exc:
        raise ImageProcessingError(
            "The file could not be read as a valid image."
        ) from exc
    finally:
        if original_position is not None:
            try:
                source.seek(original_position)
            except (OSError, ValueError):
                pass

    return image


def resize_image(
    image: Image.Image, target_size: tuple[int, int] = DEFAULT_IMAGE_SIZE
) -> Image.Image:
    """Resize an image to ``(width, height)`` using high-quality resampling."""

    if (
        len(target_size) != 2
        or target_size[0] <= 0
        or target_size[1] <= 0
    ):
        raise ImageProcessingError("Target size must contain two positive values.")

    return image.resize(target_size, Image.Resampling.LANCZOS)


def normalize_pixels(image: Image.Image) -> np.ndarray:
    """Convert an RGB Pillow image to a float32 array in the [0, 1] range."""

    pixels = np.asarray(image, dtype=np.float32) / 255.0
    return np.clip(pixels, 0.0, 1.0)


def preprocess_image(
    source: ImageSource, target_size: tuple[int, int] = DEFAULT_IMAGE_SIZE
) -> np.ndarray:
    """Validate, load, resize, and normalize an image.

    Returns:
        A float32 NumPy array shaped ``(height, width, 3)``.
    """

    image = load_image(source)
    resized = resize_image(image, target_size)
    return normalize_pixels(resized)
