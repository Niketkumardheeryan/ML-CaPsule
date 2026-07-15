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

   **L2-ARCTIC** (non-native/accented speech) — https://huggingface.co/datasets/KoelLabs/L2Arctic
   - Compiled by researchers at Texas A&M University and Iowa State University
   - Contains English speech from 24 non-native speakers across 6 native-language backgrounds: Hindi, Chinese, Spanish, Arabic, Korean, and Vietnamese
   - This v1 uses the Hindi and Chinese speaker subsets
   - Includes phonemic annotations (IPA) alongside audio and transcripts
   - License: CC BY-NC 4.0 (non-commercial use, consistent with this educational project)
   - Approximately 220 minutes of speech, read from CMU ARCTIC prompt sentences

   **CMU ARCTIC** (native reference speech) — https://huggingface.co/datasets/MikhailT/cmu-arctic
   - Compiled by Carnegie Mellon University for speech synthesis research
   - Native English speakers reading the same standardized prompt sentences as L2-ARCTIC
   - This v1 uses two reference speakers: bdl (male) and slt (female)
   - Publicly available, no access restrictions

   **Pairing**: Since both corpora are built from the same underlying prompt sentence set, recordings are matched by normalized sentence text (lowercased, punctuation-stripped) to build parallel accented/native pairs, resulting in 1,148 aligned pairs (575 Hindi, 573 Chinese)

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

All code lives in a single Jupyter notebook: `Accent_Neutralizer_for_Speech.ipynb`

```bash
pip install -r requirements.txt
jupyter notebook Accent_Neutralizer_for_Speech.ipynb
```

Then run all cells in order (Kernel > Restart Kernel and Run All Cells). The notebook is organized into clearly labeled sections:

1. Setup - installs dependencies
2. Feature Extractor - MFCC, pitch, and formant extraction
3. Model Architecture - the BiLSTM conversion model
4. Data Preparation - downloads datasets, matches sentence pairs, aligns with DTW
5. Training - trains the model
6. Inference - runs the full pipeline on a sample sentence and saves before/after audio

Note: steps 4 and 5 automatically cache their results (extracted features, aligned tensors, and the trained model checkpoint). On first run these steps take time since they process the full dataset and train from scratch; on subsequent runs they load the cached results instantly.

## Project Structure

Accent_Neutralizer_for_Speech/
├── README.md
├── requirements.txt
├── Accent_Neutralizer_for_Speech.ipynb   (all code: feature extraction, model, training, inference)
├── best_model.pt                          (trained model checkpoint)
└── data/processed/                        (cached features and training tensors, generated on first run)

## Acknowledgements

- L2-ARCTIC corpus (Texas A&M University, Iowa State University) - https://psi.engr.tamu.edu/l2-arctic-corpus/
- CMU ARCTIC corpus (Carnegie Mellon University) - http://festvox.org/cmu_arctic/
