"""
prepare_training_data.py
Aligns accented/native MFCC pairs using DTW, then pads to a fixed
length so they can be batched for training.
"""

import pickle
import numpy as np
import librosa
from tqdm import tqdm

MAX_FRAMES = 300

def align_pair(acc_mfcc, nat_mfcc):
    D, wp = librosa.sequence.dtw(X=acc_mfcc, Y=nat_mfcc, metric='euclidean')
    wp = wp[::-1]

    aligned_acc = np.zeros_like(nat_mfcc)
    counts = np.zeros(nat_mfcc.shape[1])
    for acc_idx, nat_idx in wp:
        aligned_acc[:, nat_idx] += acc_mfcc[:, acc_idx]
        counts[nat_idx] += 1
    counts[counts == 0] = 1
    aligned_acc = aligned_acc / counts

    return aligned_acc

def pad_or_crop(mfcc, max_frames=MAX_FRAMES):
    n_frames = mfcc.shape[1]
    if n_frames >= max_frames:
        return mfcc[:, :max_frames]
    else:
        pad_width = max_frames - n_frames
        return np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')

print("Loading extracted features...")
with open('data/processed/features_final.pkl', 'rb') as f:
    data = pickle.load(f)

print(f"Total pairs: {len(data)}")
print("Aligning pairs with DTW and padding...")

X_list = []
Y_list = []

for item in tqdm(data):
    try:
        acc_mfcc = item['accented_mfcc']
        nat_mfcc = item['native_mfcc']

        aligned_acc = align_pair(acc_mfcc, nat_mfcc)

        acc_padded = pad_or_crop(aligned_acc)
        nat_padded = pad_or_crop(nat_mfcc)

        X_list.append(acc_padded.T)
        Y_list.append(nat_padded.T)
    except Exception as e:
        continue

X = np.stack(X_list)
Y = np.stack(Y_list)

print(f"\nFinal dataset shape: X={X.shape}, Y={Y.shape}")

np.save('data/processed/X_train.npy', X)
np.save('data/processed/Y_train.npy', Y)
print("Saved aligned training data to data/processed/X_train.npy and Y_train.npy")
