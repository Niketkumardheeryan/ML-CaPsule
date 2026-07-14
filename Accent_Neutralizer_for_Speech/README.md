# Accent Neutralizer for Speech

A Deep Learning + Speech Processing project that transforms speech from
non-native accents toward a native-English reference accent, while aiming
to preserve the original sentence content.

## Overview

This v1 implementation focuses on **acoustic feature conversion** (MFCC-level)
as a baseline approach. Given a speech clip in a non-native accent (e.g.,
Hindi-accented or Chinese-accented English), the model learns to map its
MFCC features toward the corresponding features of native-accent speech,
using a BiLSTM-based sequence model trained on parallel accented/native
sentence pairs.

**Scope note:** true accent conversion is an open research problem — accent
and speaker identity are entangled in the same acoustic features (MFCCs,
formants), so a model attempting to change *only* accent while perfectly
preserving voice identity has to disentangle signals that overlap heavily.
This v1 targets a scoped baseline (2 accent pairs) rather than a
general-purpose, production-grade solution. "Neutral" here refers to a
specific reference accent (General American, via the CMU ARCTIC corpus),
not an absence of accent.

## Approach

1. **Data**: Parallel sentence pairs built from two public corpora:
   - [L2-ARCTIC](https://huggingface.co/datasets/KoelLabs/L2Arctic) — non-native
     English speech (Hindi and Chinese speakers used in this v1)
   - [CMU ARCTIC](https://huggingface.co/datasets/MikhailT/cmu-arctic) — native
     English reference speech, same underlying prompt sentences
   - Matched by normalized sentence text → **1,148 aligned pairs** (575 Hindi, 573 Chinese)

2. **Feature extraction** (`feature_extractor.py`): MFCC, pitch (via `pyin`),
   and formant estimation (via LPC) extracted per clip.

3. **Alignment**: Since accented and native recordings differ in speaking rate,
   pairs are time-aligned using **Dynamic Time Warping (DTW)** before training,
   so the model learns a frame-correspondent mapping rather than a naive
   position-wise one.

4. **Model** (`neutralizer_model.py`): A BiLSTM encoder-decoder with a residual
   connection, trained to predict native-accent MFCCs from accented MFCCs
   (~576K parameters, trains in minutes on CPU).

5. **Reconstruction**: Converted MFCCs are turned back into audio using
   Griffin-Lim phase estimation (`librosa.feature.inverse.mfcc_to_audio`).

## Results (v1)

- Training loss decreased consistently over 30 epochs (621 → 350 train,
  597 → 384 validation), with train/val loss tracking closely — indicating
  real learning without significant overfitting.
- Qualitatively, converted audio remains intelligible (sentence content is
  preserved) with an audible timbral shift from the source accent.

## Known Limitations

- **Audio quality**: Griffin-Lim reconstruction introduces a robotic/synthetic
  quality, since it estimates phase information that was discarded during
  MFCC extraction. This is a reconstruction-method limitation, not a failure
  of the conversion model itself.
- **Speaker identity preservation**: this v1 does not explicitly disentangle
  speaker identity from accent — some voice-identity drift is expected in
  the current approach.
- **Prosody**: pitch/rhythm patterns are extracted but not yet incorporated
  into the conversion model itself (MFCC-only conversion in this version).
- **Accent coverage**: limited to Hindi and Chinese non-native accents in v1.

## Future Work

- Replace Griffin-Lim with a neural vocoder (e.g., HiFi-GAN) for natural-sounding output
- Incorporate prosody (pitch/rhythm) into the conversion model
- Explicit speaker-identity preservation via separate content/speaker embeddings
- Extend to additional accent pairs (Spanish, Arabic, Korean, Vietnamese — already
  present in the source dataset)

## How to Run

```bash
pip install -r requirements.txt

# Train the model (uses cached/downloaded datasets automatically)
python prepare_training_data.py
python train.py

# Run inference on your own audio file
python main.py --input path/to/your_audio.wav --output result.wav

# Or run a quick demo (no input needed, uses a sample from L2-ARCTIC)
python main.py
```

## Project Structure

Accent_Neutralizer_for_Speech/
├── README.md
├── requirements.txt
├── feature_extractor.py       (MFCC, pitch, formant extraction)
├── neutralizer_model.py       (BiLSTM conversion model)
├── prepare_training_data.py   (DTW alignment + padding)
├── train.py                   (Training loop)
├── main.py                    (Entry point - inference)
└── best_model.pt              (Trained model checkpoint)

## Acknowledgements

- L2-ARCTIC corpus (Texas A&M University, Iowa State University) - https://psi.engr.tamu.edu/l2-arctic-corpus/
- CMU ARCTIC corpus (Carnegie Mellon University) - http://festvox.org/cmu_arctic/
