"""Utilities for extracting raw text from uploaded resumes."""

from __future__ import annotations

import logging
import os
from io import BytesIO
from pathlib import Path
from typing import Any
import re

logger = logging.getLogger(__name__)


def _clean_text(text: str) -> str:
    """Normalize extracted text without applying NLP-style cleaning."""
    if not text:
        return ""
    cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(cleaned_lines)


def _read_file_bytes(file: Any) -> bytes:
    """Read bytes from a file-like object or a filesystem path."""
    if isinstance(file, (str, os.PathLike)):
        path = Path(file)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return path.read_bytes()

    if hasattr(file, "read"):
        try:
            if hasattr(file, "seek"):
                file.seek(0)
            data = file.read()
            if hasattr(file, "seek"):
                file.seek(0)
            return data if isinstance(data, (bytes, bytearray)) else data.encode("utf-8")
        except Exception as exc:  # pragma: no cover - defensive path
            raise ValueError(f"Unable to read the uploaded file: {exc}") from exc

    raise TypeError("Expected a file-like object or a filesystem path.")


def extract_text_from_pdf(file: Any) -> str:
    """Extract raw text from a PDF file object or path.

    The implementation prefers PyPDF2 and falls back to pdfplumber when needed.
    """
    logger.info("Attempting to extract text from PDF")
    data = _read_file_bytes(file)
    if not data.strip():
        raise ValueError("The PDF file is empty.")

    try:
        from PyPDF2 import PdfReader
    except ImportError:  # pragma: no cover - dependency handling
        PdfReader = None

    try:
        from pdfplumber import open as pdfplumber_open
    except ImportError:  # pragma: no cover - dependency handling
        pdfplumber_open = None

    text_parts: list[str] = []

    if PdfReader is not None:
        try:
            reader = PdfReader(BytesIO(data))
            text_parts = [page.extract_text() or "" for page in reader.pages]
        except Exception as exc:
            logger.warning("PyPDF2 extraction failed: %s", exc)
            text_parts = []

    if not "".join(text_parts).strip() and pdfplumber_open is not None:
        try:
            with pdfplumber_open(BytesIO(data)) as pdf:
                text_parts = [page.extract_text() or "" for page in pdf.pages]
        except Exception as exc:
            logger.warning("pdfplumber fallback failed: %s", exc)
            raise ValueError(f"Could not extract text from the PDF file: {exc}") from exc

    if not "".join(text_parts).strip():
        raise ValueError(
            "No readable text was found in the PDF file. "
            "Direct text extraction works best with text-based PDFs."
        )

    return _clean_text("\n".join(part for part in text_parts if part))


def extract_text_from_docx(file: Any) -> str:
    """Extract paragraph text from a DOCX file object or path."""
    logger.info("Attempting to extract text from DOCX")
    data = _read_file_bytes(file)
    if not data.strip():
        raise ValueError("The DOCX file is empty.")

    try:
        from docx import Document
    except ImportError as exc:  # pragma: no cover - dependency handling
        raise ValueError("python-docx is required to read DOCX files.") from exc

    try:
        document = Document(BytesIO(data))
        paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text and paragraph.text.strip()]
    except Exception as exc:
        raise ValueError(f"Could not read the DOCX file: {exc}") from exc

    text = "\n".join(paragraphs)
    if not text.strip():
        raise ValueError("No readable text was found in the DOCX file.")

    return _clean_text(text)


def parse_resume(uploaded_file: Any) -> str:
    """Parse a resume upload into plain text.

    The function accepts a Streamlit UploadedFile-like object, validates the
    extension, routes to the correct extractor, and returns cleaned text.
    Unsupported file types raise ValueError. Empty or corrupted files return
    an informative message instead of crashing the application.
    """
    if uploaded_file is None:
        raise ValueError("No file was provided.")

    filename = getattr(uploaded_file, "name", None) or getattr(uploaded_file, "filename", None) or ""
    extension = Path(filename).suffix.lower() if filename else ""

    if extension == ".pdf":
        try:
            return extract_text_from_pdf(uploaded_file)
        except Exception as exc:
            logger.exception("Failed to parse PDF resume from %s", filename)
            raise ValueError(f"Could not read the uploaded file: {exc}") from exc

    if extension == ".docx":
        try:
            return extract_text_from_docx(uploaded_file)
        except Exception as exc:
            logger.exception("Failed to parse DOCX resume from %s", filename)
            raise ValueError(f"Could not read the uploaded file: {exc}") from exc

    raise ValueError(f"Unsupported file type: {extension or 'unknown'}. Please upload a .pdf or .docx file.")


if __name__ == "__main__":
    import argparse

    class UploadedFileShim:
        def __init__(self, path: str) -> None:
            self._handle = open(path, "rb")
            self.name = Path(path).name

        def read(self, *args: Any, **kwargs: Any) -> bytes:
            return self._handle.read(*args, **kwargs)

        def seek(self, *args: Any, **kwargs: Any) -> int:
            return self._handle.seek(*args, **kwargs)

        def close(self) -> None:
            self._handle.close()

    parser = argparse.ArgumentParser(description="Test the resume parser against a file path")
    parser.add_argument("file_path", help="Path to a .pdf or .docx file")
    args = parser.parse_args()

    try:
        with open(args.file_path, "rb") as handle:
            shim = UploadedFileShim(args.file_path)
            try:
                text = parse_resume(shim)
            finally:
                shim.close()
        print(text[:3000])
    except Exception as exc:  # pragma: no cover - CLI helper
        print(f"Error: {exc}")
