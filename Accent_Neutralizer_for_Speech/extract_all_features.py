from datasets import load_dataset, Audio
import io
import soundfile as sf
import numpy as np
import pickle
import os
import re
from feature_extractor import FeatureExtractor
from tqdm import tqdm

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("Loading datasets...")
l2 = load_dataset("KoelLabs/L2Arctic")
l2 = l2.cast_column("audio", Audio(decode=False))
cmu = load_dataset("MikhailT/cmu-arctic")
cmu = cmu.cast_column("audio", Audio(decode=False))

TARGET_LANGUAGES = ['Hindi', 'Chinese']
NATIVE_SPEAKERS = ['bdl', 'slt']

print("Building native sentence lookup...")
native_lookup = {}
for spk in NATIVE_SPEAKERS:
    for row in cmu[spk]:
        text_key = normalize_text(row['text'])
        if text_key not in native_lookup:
            native_lookup[text_key] = row

print("Matching pairs...")
pairs = []
for row in l2['scripted']:
    if row['speaker_native_language'] not in TARGET_LANGUAGES:
        continue
    text_key = normalize_text(row['text'])
    if text_key in native_lookup:
        pairs.append({'accented': row, 'native': native_lookup[text_key], 'language': row['speaker_native_language']})

print(f"Total pairs: {len(pairs)}")

extractor = FeatureExtractor()
processed_data = []

os.makedirs('data/processed', exist_ok=True)

print("Extracting features for all pairs (this will take a while)...")
for i, pair in enumerate(tqdm(pairs)):
    try:
        acc_bytes = pair['accented']['audio']['bytes']
        acc_audio, acc_sr = sf.read(io.BytesIO(acc_bytes))
        acc_audio = acc_audio.astype(np.float32)

        nat_bytes = pair['native']['audio']['bytes']
        nat_audio, nat_sr = sf.read(io.BytesIO(nat_bytes))
        nat_audio = nat_audio.astype(np.float32)

        acc_features = extractor.extract_all(acc_audio)
        nat_features = extractor.extract_all(nat_audio)

        processed_data.append({
            'text': pair['accented']['text'],
            'language': pair['language'],
            'accented_speaker': pair['accented']['speaker_code'],
            'native_speaker': pair['native']['speaker'],
            'accented_mfcc': acc_features['mfcc'],
            'accented_pitch': acc_features['pitch'],
            'native_mfcc': nat_features['mfcc'],
            'native_pitch': nat_features['pitch'],
        })
    except Exception as e:
        print(f"Skipping pair {i} due to error: {e}")
        continue

    if (i + 1) % 200 == 0:
        with open('data/processed/features_checkpoint.pkl', 'wb') as f:
            pickle.dump(processed_data, f)
        print(f"Checkpoint saved at {i+1} pairs")

with open('data/processed/features_final.pkl', 'wb') as f:
    pickle.dump(processed_data, f)

print(f"\nDone! Successfully processed {len(processed_data)} out of {len(pairs)} pairs")
print("Saved to data/processed/features_final.pkl")
