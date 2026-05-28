import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 1. Define the path to your audio file
audio_path ='test.wav'
# 2. Load the audio file
# sr=None tells librosa to preserve the native sampling rate of your recording
signal, sr = librosa.load(audio_path, sr=None)

print("Audio data properites---")
#here the data type would be np.ndarray as the signal is converted to np.ndarray by librosa.load

print(f"data type of the signal :,{type(signal)}")
print(f"Shape of the Signal Array: {signal.shape}")

print(f"Sampling Rate (sr): {sr} Hz")
#the number of "snapshots" in which the sample is divided per sec
print(f"Duration of Audio: {len(signal) / sr:.2f} seconds")
# 4. Plot the raw waveform
plt.figure(figsize=(10, 4))
librosa.display.waveshow(signal, sr=sr, color="blue")
plt.title("Raw Audio Waveform (Time Domain)")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.show()

#plotting the mfccs and mel spectrogram
mel_spectro=librosa.feature.melspectrogram(y=signal,sr=sr,n_mels=128)
#taking 128 is the sweet spot..any higher noise detection..any lower "blurred" frequency values
#for mood detection we would use padding and slanely normalization

mel_spectro_db=librosa.power_to_db(mel_spectro,ref=np.max)
#human ears percieve both high freqencies and hifh loudness in a much more" lineant" way\

mfccs=librosa.feature.mfcc(y=signal,sr=sr,n_mfcc=20)
# we would use liftering padding and dct normalization for mood detection(liftering and dct norm are alr applied by librosa)
plt.figure(figsize=(12, 8))

# Plot the Mel-Spectrogram
plt.subplot(2, 1, 1)
librosa.display.specshow(mel_spectro_db, sr=sr, x_axis='time', y_axis='mel', cmap='viridis')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel-Spectrogram (Voice Frequencies over Time)')

# Plot the MFCCs
plt.subplot(2, 1, 2)
librosa.display.specshow(mfccs, sr=sr, x_axis='time', cmap='coolwarm')
plt.colorbar()
plt.title('MFCCs (Compressed Vocal Features)')

plt.tight_layout()
plt.show()

# Print matrix dimensions to understand the structural change
print("--- Matrix Dimensionality Check ---")
print(f"Mel-Spectrogram Matrix Shape: {mel_spectro_db.shape}")
print(f"MFCC Matrix Shape: {mfccs.shape}")


