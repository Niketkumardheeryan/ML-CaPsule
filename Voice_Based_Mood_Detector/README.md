# Audio Emotion Recognition using 2D CNN

An end-to-end PyTorch implementation for classifying human emotions from speech audio files using 2D Convolutional Neural Networks (CNNs). This project integrates data from two major datasets—**TESS (Toronto Emotional Speech Set)** and **RAVDESS (Ryerson Audio-Visual Database of Emotional Speech and Song)**—capturing both female and male speech samples for a balanced representation.

---

##  System Architecture & Workflow

The pipeline treats audio features (**MFCCs**) exactly like single-channel grayscale images. 

1. **Audio Standardization:** Audio signals are loaded and forced to a sampling rate of 16kHz to maintain temporal consistency.(The second dimension of the mfcc matrix(128 columns) =Number of samples/Hop length .Here the Number of samples depends on the sampling rate.If the sampling rate was different the CNN would throw an error.)
2. **Feature Extraction:** 20 Mel-Frequency Cepstral Coefficients (MFCCs) are extracted.
3. **Temporal Alignment:** Features are systematically truncated or zero-padded to a static width of 128 frames, outputting a fixed matrix size of `(20, 128)`.
4. **Custom PyTorch Dataset:** The 2D feature matrix is unsqueezed into shape `(1, 20, 128)` to append the explicit channel dimension required by `nn.Conv2d`.
5. **Stratified Sampling:** Implements a balanced collection to prevent the model from biasing toward a specific dataset, speaker gender, or target label.We have taken total 192(96 tess+96 ravdess) samples per emotion.

---

##  Installation & Setup

### Prerequisites
Make sure you have Python 3.8+ installed. 

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/audio-emotion-cnn.git](https://github.com/yourusername/audio-emotion-cnn.git)
cd audio-emotion-cnn
```

### 2. Install Dependencies
```bash
pip install torch torchvision librosa numpy 
```
 -----


### MODEL SPECIFICATIONS:
The network relies on a 2D CNN architecture tailored for spectrograms/MFCC spatial features:

1.Convolutional Block 1: Conv2d(1 -> 16 channels, kernel=3,dilation=(1,2)) + ReLU + MaxPool2d(kernel=2, stride=2)

2.Convolutional Block 2: Conv2d(16 -> 32 channels, kernel=3,dilation=(1,2)) + ReLU + MaxPool2d(kernel=2, stride=2)

3.Dimensional Safety Layer: AdaptiveAvgPool2d((4, 4)) .This is done to make the spatial features of the input feature map into linear layer consistent.We could have used original 5*32 but we converted to 4 *4 to reduce computational cost.

4.Torch.flatten(x,1) :flattens the tensor(32,32,4,4) into a 2d matrix of shape (32,32x4x4) as expected by nn.Linear.

5.Fully Connected Head: Linear(32 * 4 * 4 -> 4 classes) maps features to categorical probabilities via Cross-Entropy Loss.

----
### I have also made a raw_&_mfcc_demonstration.py file which can be used to visualize the raw waveform and mfcc spectrogram of a test audio.Clone the repo and load any audio file in wav format and run the python file to see the waveforms for better understanding.
---

