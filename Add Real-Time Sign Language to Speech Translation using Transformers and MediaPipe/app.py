"""
app.py
------
Gradio web interface for Sign Language → Speech Translation.

Supports:
  - Live webcam stream inference
  - Single-image upload inference
  - Sentence accumulation + TTS playback
  - Attention visualisation heatmap
  - Performance metrics dashboard
"""

import os
import io
import json
import time
import tempfile
import threading
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import torch
import gradio as gr
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from gtts import gTTS

from preprocessing import HandLandmarkExtractor, load_label_encoder, FEATURE_DIM
from train import SignLanguageTransformer
from inference import SignLanguageInference


# ── Config ─────────────────────────────────────────────────────────────────

MODEL_PATH   = os.environ.get("MODEL_PATH",   "models/best_model.pt")
ENCODER_PATH = os.environ.get("ENCODER_PATH", "models/label_encoder.json")
THRESHOLD    = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.75"))


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_engine() -> Optional[SignLanguageInference]:
    """Try to load the inference engine; return None if model files are absent."""
    if not (Path(MODEL_PATH).exists() and Path(ENCODER_PATH).exists()):
        return None
    return SignLanguageInference(
        model_path=MODEL_PATH,
        label_encoder_path=ENCODER_PATH,
        confidence_thresh=THRESHOLD,
    )


def text_to_speech(text: str) -> str:
    """Convert text to an MP3 file via gTTS and return the file path."""
    tts = gTTS(text=text, lang="en", slow=False)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name


def get_attention_heatmap(model: SignLanguageTransformer,
                          features: np.ndarray,
                          device: torch.device) -> np.ndarray:
    """
    Extract attention weights from the first transformer layer and
    return a heatmap image (H×W×3 uint8).
    """
    hooks, attention_maps = [], []

    def hook(module, input, output):
        # output[1] is the attention weight tensor when need_weights=True
        if isinstance(output, tuple) and len(output) > 1 and output[1] is not None:
            attention_maps.append(output[1].detach().cpu())

    for layer in model.transformer.layers:
        hooks.append(layer.self_attn.register_forward_hook(hook))

    model.eval()
    with torch.no_grad():
        tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(device)
        _ = model(tensor)

    for h in hooks:
        h.remove()

    if not attention_maps:
        return np.zeros((100, 100, 3), dtype=np.uint8)

    # Average over heads; take CLS row
    attn = attention_maps[0].squeeze(0)          # (heads, T+1, T+1)
    attn = attn.mean(0)[0, 1:].numpy()           # (T,)

    fig, ax = plt.subplots(figsize=(6, 1.5))
    ax.imshow(attn[np.newaxis, :], aspect="auto",
              cmap="YlOrRd", vmin=0, vmax=attn.max())
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Attention weights (CLS → input landmarks)", fontsize=9, pad=4)
    plt.tight_layout(pad=0.5)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=120)
    plt.close()
    buf.seek(0)
    arr = np.frombuffer(buf.read(), dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


# ── Gradio handlers ───────────────────────────────────────────────────────────

engine = load_engine()
sentence_state: list = []


def process_image(image: np.ndarray):
    """Handle an uploaded image: extract landmarks, predict, optionally speak."""
    if engine is None:
        return (
            image,
            "⚠️ Model not loaded. Run training first.",
            0.0,
            None,
            None,
        )

    frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw landmarks
    annotated = engine.extractor.draw_landmarks(frame.copy())
    annotated  = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    label, conf = engine.predict_frame(frame)
    result_text = f"Predicted: **{label}**  ({conf:.0%} confidence)" if label else "No hand detected"

    # Add to sentence
    if label:
        sentence_state.append(label)

    sentence_text = " ".join(sentence_state) if sentence_state else ""

    # Attention heatmap
    features = engine.extractor.extract(frame)
    heatmap  = None
    if features is not None:
        hm = get_attention_heatmap(engine.model, features, engine.device)
        heatmap = cv2.cvtColor(hm, cv2.COLOR_BGR2RGB)

    return annotated, result_text, conf, sentence_text, heatmap


def speak_sentence(sentence: str):
    """Convert current sentence to audio."""
    if not sentence.strip():
        return None
    return text_to_speech(sentence)


def clear_sentence():
    sentence_state.clear()
    return ""


def process_webcam_frame(frame: np.ndarray):
    """Used by the Gradio live stream component."""
    if frame is None or engine is None:
        return frame, "No input", ""

    bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    label, conf = engine.predict_frame(bgr)

    annotated = engine.extractor.draw_landmarks(bgr.copy())
    annotated  = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    label_str = f"{label}  ({conf:.0%})" if label else "Waiting for sign…"
    sentence  = " ".join(sentence_state)
    return annotated, label_str, sentence


# ── Gradio UI ─────────────────────────────────────────────────────────────────

THEME = gr.themes.Soft(
    primary_hue="teal",
    secondary_hue="blue",
    neutral_hue="slate",
)

with gr.Blocks(theme=THEME, title="Sign Language → Speech") as demo:
    gr.Markdown(
        """
        # 🤟 Real-Time Sign Language to Speech Translation
        Upload an image of a hand sign **or** use your webcam to translate
        ASL alphabet gestures into text and synthesised speech.
        > Built with MediaPipe · PyTorch Transformers · Gradio
        """
    )

    with gr.Tabs():

        # ── Tab 1: Image upload ────────────────────────────────────────────
        with gr.Tab("📷 Image Upload"):
            with gr.Row():
                with gr.Column():
                    img_input = gr.Image(
                        label="Upload hand-sign image",
                        type="numpy", height=360,
                    )
                    run_btn = gr.Button("Predict", variant="primary")

                with gr.Column():
                    img_output   = gr.Image(label="Landmarks overlay", height=360)
                    label_output = gr.Markdown("Prediction will appear here")
                    conf_bar     = gr.Slider(label="Confidence", minimum=0,
                                            maximum=1, interactive=False)

            with gr.Row():
                sentence_box = gr.Textbox(label="Accumulated sentence",
                                          placeholder="Signs will be appended here…",
                                          interactive=False)
                speak_btn = gr.Button("🔊 Speak sentence")
                clear_btn = gr.Button("🗑 Clear")
                audio_out = gr.Audio(label="Speech output", type="filepath")

            attn_img = gr.Image(label="Attention heatmap")

            run_btn.click(
                process_image,
                inputs=[img_input],
                outputs=[img_output, label_output, conf_bar, sentence_box, attn_img],
            )
            speak_btn.click(speak_sentence, inputs=[sentence_box], outputs=[audio_out])
            clear_btn.click(clear_sentence, outputs=[sentence_box])

        # ── Tab 2: Live webcam ─────────────────────────────────────────────
        with gr.Tab("🎥 Live Webcam"):
            gr.Markdown("Grant camera access then click **Start**.")
            with gr.Row():
                webcam_in  = gr.Image(label="Webcam", sources=["webcam"],
                                      streaming=True, height=360)
                webcam_out = gr.Image(label="Landmark overlay",  height=360)

            with gr.Row():
                live_label    = gr.Textbox(label="Current sign", interactive=False)
                live_sentence = gr.Textbox(label="Sentence",     interactive=False)

            webcam_in.stream(
                process_webcam_frame,
                inputs=[webcam_in],
                outputs=[webcam_out, live_label, live_sentence],
                stream_every=0.1,
            )

        # ── Tab 3: Metrics dashboard ───────────────────────────────────────
        with gr.Tab("📊 Model Metrics"):
            history_path = "models/history.json"
            if Path(history_path).exists():
                with open(history_path) as f:
                    hist = json.load(f)
                epochs = list(range(1, len(hist["train_loss"]) + 1))

                fig, axes = plt.subplots(1, 2, figsize=(10, 4))
                axes[0].plot(epochs, hist["train_loss"], label="train")
                axes[0].plot(epochs, hist["val_loss"],   label="val")
                axes[0].set_title("Loss"); axes[0].legend()
                axes[1].plot(epochs, hist["train_acc"], label="train")
                axes[1].plot(epochs, hist["val_acc"],   label="val")
                axes[1].set_title("Accuracy"); axes[1].legend()
                plt.tight_layout()
                gr.Plot(fig)
            else:
                gr.Markdown("_Run training first to see metrics here._")

        # ── Tab 4: About ───────────────────────────────────────────────────
        with gr.Tab("ℹ️ About"):
            gr.Markdown(
                """
                ## How it works
                1. **MediaPipe Hands** extracts 21 3-D landmarks per frame (63 features).
                2. Landmarks are normalised relative to the wrist for scale/rotation invariance.
                3. A **Transformer encoder** with a CLS token classifies the landmark sequence.
                4. Predictions are smoothed over a rolling window to reduce flicker.
                5. Stable signs are appended to a sentence buffer and spoken via **gTTS**.

                ## Supported signs
                - ASL alphabet A–Z
                - Common words (space, delete, nothing) depending on the dataset used

                ## Training your own model
                ```bash
                python src/preprocessing.py --dataset_root dataset/asl_alphabet_train --output dataset/features.csv
                python src/train.py --data dataset/features.csv --model_dir models/ --epochs 80
                ```
                """
            )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )
