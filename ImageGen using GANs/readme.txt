# DCGAN: Deep Convolutional Generative Adversarial Network

Welcome to the Image generation using GANs, a deep convolutional generative adversarial network implemented in PyTorch! This project is designed to generate realistic images from random noise using the power of deep learning.

![DCGAN Image](https://github.com/chiragHimself/dcgan_random/raw/main/results/fake_samples_epoch_024.png)

## Overview
- **Project Name**: ImageGen using GANs
- **Description**: A deep convolutional generative adversarial network to generate realistic images.
- **Framework**: PyTorch 2.2.1
- **Training Device**: RTX 3050 Ti with CUDA 11.2
- **IDE**: Spyder (can be run on other IDEs and Google Colab)

## Dependencies
- `torch`
- `torch.nn`
- `torch.optim`
- `torch.utils.data`
- `torchvision.datasets`
- `torchvision.transforms`
- `torchvision.utils`

## Training Data
The training data for this project is obtained from the CIFAR-10 open dataset. It is downloaded to a local directory named `data`, where the training is conducted.

## Training Details
- **Epochs**: 25
- **Training Time**: Approximately 4 hours
- **Result**: various batch png's are included in the repository, showcasing the generated images after each epoch. Please note that this file will be overwritten if you run the code in your IDE.

## Generated Images
Here are some samples of the generated images produced by the DCGAN model:

![Generated Image 1](https://github.com/chiragHimself/dcgan_random/blob/main/results/fake_samples_epoch_000.png)
![Generated Image 2](https://github.com/chiragHimself/dcgan_random/blob/main/results/fake_samples_epoch_006.png)
![Generated Image 3](https://github.com/chiragHimself/dcgan_random/blob/main/results/fake_samples_epoch_024.png)
