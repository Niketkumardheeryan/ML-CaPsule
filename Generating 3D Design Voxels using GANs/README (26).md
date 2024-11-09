# 3D Voxel Data Generation using GANs:
--------------------------------------


This project implements a Generative Adversarial Networks framework (GAN) to generate 3D voxel data. The goal is to train a GAN to produce synthetic 3D voxel-based structures that resemble real-world data, allowing for data augmentation and analysis of generated samples.

## Project Overview

This repository contains code for:

- **Generator**: A neural network model that takes a latent vector (noise) as input and generates 3D voxel data.
- **Discriminator**: A neural network model that distinguishes between real voxel data and generated voxel data.
- **GAN Model**: A combination of the generator and discriminator models, trained together in an adversarial setup.

The model is trained on 3D voxel datasets and can generate new voxel structures by learning the underlying data distribution.


## Requirements

To run this project, you need the following dependencies installed:

- Python 3.x
- TensorFlow 2.x
- NumPy
- Matplotlib (for visualization)

## Install the dependencies using the following command:

pip install -r requirements.txt

## How to Run the Project
1. Clone the repository

git clone https://github.com/Panchadip-128/Generating-3D-Designs-with-AI.git


2. Prepare Your Dataset
Place your 3D voxel data in a data/ directory or use the random voxel data generator as shown in the sample code.

3. Train the GAN
To start training the GAN on your 3D voxel dataset, run:

python train.py
You can adjust the number of epochs, batch size, and other hyperparameters in the train.py file to improvise parameters like accuracy,precision of the model with advanced GPUs.

4. Visualize Generated Voxels
After training, you can visualize the generated 3D voxel data using:

python visualize.py
This will generate and display synthetic voxel samples from the generator model.

## Model Architecture
Generator: Takes a 150-dimensional latent space vector and transforms it through a series of Conv3DTranspose layers to generate a 32x32x32 voxel volume.
Discriminator: A 3D convolutional neural network that classifies input voxel volumes as real or fake.
Results
The GAN is trained over several epochs, and during training, both the generator loss and discriminator loss are monitored to ensure balanced training. At regular intervals, generated voxel samples are visualized to assess the quality of the outputs.

Sample generated voxel at epoch 100:

![smp1](https://github.com/user-attachments/assets/915a48cd-9065-47b0-b411-b2ddaecfb761)
![smp2](https://github.com/user-attachments/assets/70a5e97b-6386-4442-939b-8dd292bca64d)

![smp3](https://github.com/user-attachments/assets/19e8c32f-0964-4aba-9137-04a659e087fb)
![smp4](https://github.com/user-attachments/assets/ae853ddd-06a0-487c-83bc-2c331d33e123)

![smp5](https://github.com/user-attachments/assets/bc5d88e3-72f0-48ae-9031-eacedfa9b183)



## Future Improvements
Implement Conditional GANs to generate voxel data conditioned on labels or classes.
Use Progressive Growing to generate higher resolution voxel structures.
Add more advanced loss functions like Wasserstein loss to stabilize training.
Experiment with Transfer Learning to apply the GAN model to different 3D voxel datasets.

## Contributing:
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are welcome!



