"""Streamlit interface for the animal cancer prediction demo."""

from __future__ import annotations

import streamlit as st

from src.predict import predict_image
from src.preprocessing import ImageProcessingError, load_image

DISCLAIMER = (
    "This project is for educational purposes only and should not be used as "
    "a medical diagnosis tool."
)


def main() -> None:
    """Render the Streamlit application."""

    st.set_page_config(
        page_title="Animal Cancer Disease Prediction",
        page_icon="🔬",
        layout="centered",
    )

    st.title("Animal Cancer Disease Prediction")
    st.write(
        "Upload an animal cell or tissue image to explore a lightweight, "
        "deterministic image-classification pipeline."
    )
    st.info(DISCLAIMER)

    uploaded_file = st.file_uploader(
        "Upload an animal cell or tissue image",
        type=["bmp", "jpeg", "jpg", "png", "tif", "tiff", "webp"],
        help="Supported formats: BMP, JPEG, PNG, TIFF, and WebP.",
    )

    preview_image = None
    if uploaded_file is not None:
        try:
            preview_image = load_image(uploaded_file)
            st.image(
                preview_image,
                caption="Uploaded image preview",
                use_column_width=True,
            )
        except ImageProcessingError as exc:
            st.error(f"Unable to preview this image: {exc}")

    if st.button(
        "Predict sample class",
        type="primary",
        use_container_width=True,
    ):
        if preview_image is None:
            st.warning("Please upload a valid image before requesting a prediction.")
        else:
            with st.spinner("Analysing image features..."):
                result = predict_image(preview_image)

            if not result.success:
                st.error(result.error or "Prediction failed.")
            elif result.label == "cancerous":
                st.error("Predicted class: Cancerous")
                st.metric("Model confidence", f"{result.confidence:.1%}")
            else:
                st.success("Predicted class: Non-cancerous")
                st.metric("Model confidence", f"{result.confidence:.1%}")

            st.caption(
                "Confidence describes this demo classifier's output, not "
                "clinical certainty."
            )

    st.divider()
    st.warning(DISCLAIMER)


if __name__ == "__main__":
    main()
