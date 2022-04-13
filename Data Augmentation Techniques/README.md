# Data Augmentation Techniques

Data augmentation techniques generate different versions of a real dataset artificially to increase its size. Computer vision and natural language processing (NLP) models use data augmentation strategy to handle with data scarcity and insufficient data diversity.

Data augmentation algorithms can increase accuracy of machine learning models. For example, a deep learning model after image augmentation performs better in training loss (i.e. penalty for a bad prediction) & accuracy and validation loss & accuracy than a deep learning model without augmentation for image classification task.

## Image Data Augmentation Techniques

- Adding noise
- Cropping
- Flipping
- Rotation
- Scaling
- Translation
- Brightness
- Contrast
- Color Augmentation
- Saturation

The `Keras` deep learning neural network library provides the capability to fit models using image data augmentation via the `ImageDataGenerator` class.
[Click Here](./Image_Data_Augmentation/data-augmentation-cv.ipynb) to see the example of implementing Image Data Augmentation on [this](https://www.kaggle.com/datasets/iamsouravbanerjee/animal-image-dataset-90-different-animals) dataset using Keras.

## Text Data Augmentation Techniques

Data augmentation techniques are applied on character, word and text levels.

- **Easy Data Augmentation (EDA) Methods**:

  EDA methods include easy text transformations, for example a word is chosen randomly from the sentence and replaced with one of this word synonyms or two words are chosen and swapped in the sentence. EDA techniques examples in NLP processing are

  - Synonym replacement
  - Text Substitution (rule-based, ML-based, mask-based and etc.)
  - Random insertion
  - Random swap
  - Random deletion
  - Word & sentence shuffling

- **Back Translation**

  A sentence is translated in one language and then new sentence is translated again in the original language. So, different sentences are created.

- **Text Generation**

  A generative adversarial networks (GAN) is trained to generate text with a few words.

The `nlpaug` python library helps with augmenting nlp for our machine learning projects.It provides the capability to apply various text data augmentation techniques using the `Augmenter` class.
[Click here](./Text_Data_Augmentation/text_data_augmentation_eda.ipynb) to see the implementation of EDA using nlpaug.

## Audio Data Augmentation Techniques

Audio data augmentation methods include

- Cropping out a portion of data
- Noise Injection
- Shifting Time
- Speed tuning
- Changing pitch
- Mixing background noise
- Masking frequency.

[Click here](./Audio_Data_Augmentation/audio-data-augmentation.ipynb) to see implementation of Audio data augmentation techniques using `librosa` , `ipd` and `numpy` on [this](https://www.kaggle.com/competitions/tensorflow-speech-recognition-challenge/data) dataset

## References

Different data augmentation libraries discussed here have been referred from [this](https://towardsdatascience.com/data-augmentation-in-nlp-2801a34dfc28) medium article

#### CONTRIBUTED BY

[Shreya Ghosh](https://github.com/shreya024)
