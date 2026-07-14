"""
feature_extractor.py
Extracts acoustic features (MFCC, pitch, formants) from speech audio
for accent analysis and conversion.
"""

import numpy as np
import librosa


class FeatureExtractor:
    def __init__(self, sample_rate=16000, n_mfcc=13, n_fft=1024, hop_length=256):
        self.sr = sample_rate
        self.n_mfcc = n_mfcc
        self.n_fft = n_fft
        self.hop_length = hop_length

    def extract_mfcc(self, audio):
        """Extract MFCC features (timbre/phonetic content)."""
        mfcc = librosa.feature.mfcc(
            y=audio, sr=self.sr, n_mfcc=self.n_mfcc,
            n_fft=self.n_fft, hop_length=self.hop_length
        )
        return mfcc  # shape: (n_mfcc, time_frames)

    def extract_pitch(self, audio):
        """Extract fundamental frequency (F0) contour using pyin."""
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio, fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=self.sr, hop_length=self.hop_length
        )
        f0 = np.nan_to_num(f0)  # replace unvoiced NaNs with 0
        return f0

    def extract_formants(self, audio, n_formants=3, order=12):
        """
        Estimate formants (F1, F2, F3) using LPC analysis per frame.
        Formants carry most of the accent-distinguishing information.
        """
        frame_length = self.n_fft
        hop = self.hop_length
        formants_over_time = []

        for start in range(0, len(audio) - frame_length, hop):
            frame = audio[start:start + frame_length] * np.hamming(frame_length)
            try:
                lpc_coeffs = librosa.lpc(frame, order=order)
                roots = np.roots(lpc_coeffs)
                roots = roots[np.imag(roots) >= 0]
                angles = np.arctan2(np.imag(roots), np.real(roots))
                freqs = angles * (self.sr / (2 * np.pi))
                freqs = sorted(freqs[freqs > 90])  # discard near-zero/negative
                formants_over_time.append(freqs[:n_formants])
            except Exception:
                formants_over_time.append([0] * n_formants)

        return formants_over_time

    def extract_all(self, audio):
        """Convenience method: extract MFCC, pitch, and formants together."""
        return {
            'mfcc': self.extract_mfcc(audio),
            'pitch': self.extract_pitch(audio),
            'formants': self.extract_formants(audio),
        }


if __name__ == "__main__":
    # Quick smoke test with random noise (replace with real audio when integrating)
    dummy_audio = np.random.randn(16000 * 2).astype(np.float32)  # 2 sec of noise
    extractor = FeatureExtractor()
    features = extractor.extract_all(dummy_audio)
    print("MFCC shape:", features['mfcc'].shape)
    print("Pitch shape:", features['pitch'].shape)
    print("Number of formant frames:", len(features['formants']))
    print("Sample formants (first frame):", features['formants'][0])
