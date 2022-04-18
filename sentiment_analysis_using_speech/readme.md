# Sentiment_analysis_from_speech
We are going to analyse and detect emotion from speech.

# Dataset we are going to use
1. https://www.kaggle.com/datasets/ejlok1/surrey-audiovisual-expressed-emotion-savee
2. https://www.kaggle.com/datasets/uwrfkaggler/ravdess-emotional-speech-audio

# About Datasets

## Datasets are downloaded using Kaggle API, please Add your API key in first section 

## Surrey Audio-Visual Expressed Emotion (SAVEE)

### Context
I'm on a journey to create an emotion classifier from audio and the SAVEE dataset is one of the 4 key datasets that I was lucky to stumble upon. What's interesting is that this dataset is male only and is of very high quality audio. Because the male only speaker will bring about a slightly imbalance representation, it would be advisable to complement other datasets with more female speakers

### Content
The SAVEE database was recorded from four native English male speakers (identified as DC, JE, JK, KL), postgraduate students and researchers at the University of Surrey aged from 27 to 31 years. Emotion has been described psychologically in discrete categories: anger, disgust, fear, happiness, sadness and surprise. A neutral category is also added to provide recordings of 7 emotion categories.

The text material consisted of 15 TIMIT sentences per emotion: 3 common, 2 emotion-specific and 10 generic sentences that were different for each emotion and phonetically-balanced. The 3 common and 2 × 6 = 12 emotion-specific sentences were recorded as neutral to give 30 neutral sentences. This resulted in a total of 120 utterances per speaker

## Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS)
Speech audio-only files (16bit, 48kHz .wav) from the RAVDESS. Full dataset of speech and song, audio and video (24.8 GB) available from Zenodo. Construction and perceptual validation of the RAVDESS is described in our Open Access paper in PLoS ONE.

Check out our Kaggle Song emotion dataset.

### Files

This portion of the RAVDESS contains 1440 files: 60 trials per actor x 24 actors = 1440. The RAVDESS contains 24 professional actors (12 female, 12 male), vocalizing two lexically-matched statements in a neutral North American accent. Speech emotions includes calm, happy, sad, angry, fearful, surprise, and disgust expressions. Each expression is produced at two levels of emotional intensity (normal, strong), with an additional neutral expression.

### File naming convention

Each of the 1440 files has a unique filename. The filename consists of a 7-part numerical identifier (e.g., 03-01-06-01-02-01-12.wav). These identifiers define the stimulus characteristics:

Filename identifiers

1. Modality (01 = full-AV, 02 = video-only, 03 = audio-only).

2. Vocal channel (01 = speech, 02 = song).

3. Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).

4. Emotional intensity (01 = normal, 02 = strong). NOTE: There is no strong intensity for the 'neutral' emotion.

5. Statement (01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door").

6. Repetition (01 = 1st repetition, 02 = 2nd repetition).

7. Actor (01 to 24. Odd numbered actors are male, even numbered actors are female).

8. Filename example: 03-01-06-01-02-01-12.wav

Audio-only (03)
Speech (01)
Fearful (06)
Normal intensity (01)
Statement "dogs" (02)
1st Repetition (01)
12th Actor (12)
Female, as the actor ID number is even.

### Academic citation

If you use the RAVDESS in an academic publication, please use the following citation: Livingstone SR, Russo FA (2018) The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS): A dynamic, multimodal set of facial and vocal expressions in North American English. PLoS ONE 13(5): e0196391. https://doi.org/10.1371/journal.pone.0196391.

### All other attributions

If you use the RAVDESS in a form other than an academic publication, such as in a blog post, school project, or non-commercial product, please use the following attribution: "The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS)" by Livingstone & Russo is licensed under CC BY-NA-SC 4.0.

# Prerequisites

Experience with jupyter notebook or google colab.

Knowledge of following is recomended:

1. pandas

2. matplotlib

3. keras

4. tensorflow

5. CNN

6. Kaggle Api

7. python 

# Steps followed
1. Downloading datasets

2. Importing Libraries

3. Data Preparation
-  As we are working with two different datasets, so i will be creating a dataframe storing all emotions of the data in dataframe with their paths.
We will use this dataframe to extract features for our model training.

4. Data Visualisation and Exploration

5. Data Augmentation
- Data augmentation is the process by which we create new synthetic data samples by adding small perturbations on our initial training set.
To generate syntactic data for audio, we can apply noise injection, shifting time, changing pitch and speed.
The objective is to make our model invariant to those perturbations and enhace its ability to generalize.
In order to this to work adding the perturbations must conserve the same label as the original training sample.
In images data augmention can be performed by shifting the image, zooming, rotating ...
First, let's check which augmentation techniques works better for our dataset.


6. Feature Extraction
- Extraction of features is a very important part in analyzing and finding relations between different things. As we already know that the data provided of audio cannot be understood by the models directly so we need to convert them into an understandable format for which feature extraction is used.
The audio signal is a three-dimensional signal in which three axes represent time, amplitude and frequency.


In this project i am not going deep in feature selection process to check which features are good for our dataset rather i am only extracting 5 features:

1. Zero Crossing Rate
2. Chroma_stft
3. MFCC
4. RMS(root mean square) value
5. MelSpectogram to train our model.
- 

7. Data Preparation
- As of now we have extracted the data, now we need to normalize and split our data for training and testing.

8. Modelling - building a 5 layer CNN model.

# Conclusion

* Model gives the best accuray that is 61%.

## Author

[Paritosh Tripathi](https://github.com/paritoshtripathi935)