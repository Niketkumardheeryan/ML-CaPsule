"""
main.py
Accent Neutralizer for Speech - main entry point.

Usage:
    python main.py --input path/to/accented_audio.wav --output path/to/output.wav

If no --input is given, runs a demo using a sample from the L2-ARCTIC dataset.
"""

import argparse
import torch
import numpy as np
import librosa
import soundfile as sf
from neutralizer_model import AccentNeutralizer
from feature_extractor import FeatureExtractor

SR = 16000
MAX_FRAMES = 300


def load_model(checkpoint_path='best_model.pt'):
    device = torch.device('cpu')
    model = AccentNeutralizer().to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    return model


def neutralize_accent(audio, model, extractor):
    """Takes a raw audio waveform, returns accent-neutralized audio."""
    mfcc = extractor.extract_mfcc(audio)
    T = mfcc.shape[1]

    if T >= MAX_FRAMES:
        mfcc_input = mfcc[:, :MAX_FRAMES]
    else:
        mfcc_input = np.pad(mfcc, ((0, 0), (0, MAX_FRAMES - T)), mode='constant')

    x = torch.tensor(mfcc_input.T, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        output = model(x)
    predicted_mfcc = output.squeeze(0).numpy().T
    predicted_mfcc = predicted_mfcc[:, :T]

    converted_audio = librosa.feature.inverse.mfcc_to_audio(
        predicted_mfcc, sr=SR, n_fft=1024, hop_length=256
    )
    return converted_audio


def run_demo():
    """Runs a demo using a sample from L2-ARCTIC (Hindi speaker) since no input file was given."""
    from datasets import load_dataset, Audio
    import io

    print("No --input provided. Running demo on a sample L2-ARCTIC (Hindi) sentence...")
    l2 = load_dataset("KoelLabs/L2Arctic")
    l2 = l2.cast_column("audio", Audio(decode=False))

    sample = None
    for row in l2['scripted']:
        if row['speaker_native_language'] == 'Hindi':
            sample = row
            break

    print(f"Demo sentence: {sample['text']}")
    audio_bytes = sample['audio']['bytes']
    audio, sr = sf.read(io.BytesIO(audio_bytes))
    return audio.astype(np.float32)


def main():
    parser = argparse.ArgumentParser(description="Accent Neutralizer for Speech")
    parser.add_argument('--input', type=str, default=None, help='Path to input accented .wav file')
    parser.add_argument('--output', type=str, default='output_neutralized.wav', help='Path to save output audio')
    parser.add_argument('--checkpoint', type=str, default='best_model.pt', help='Path to trained model checkpoint')
    args = parser.parse_args()

    print("Loading model...")
    model = load_model(args.checkpoint)
    extractor = FeatureExtractor()

    if args.input:
        print(f"Loading input audio: {args.input}")
        audio, sr = sf.read(args.input)
        audio = audio.astype(np.float32)
    else:
        audio = run_demo()

    print("Running accent neutralization...")
    converted_audio = neutralize_accent(audio, model, extractor)

    sf.write(args.output, converted_audio, SR)
    print(f"Done! Saved neutralized audio to {args.output}")


if __name__ == "__main__":
    main()
