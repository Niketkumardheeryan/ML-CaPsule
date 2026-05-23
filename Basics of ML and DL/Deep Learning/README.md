# CIFAR-10 Image Classification with PyTorch

A baseline CNN built with PyTorch to classify the CIFAR-10 dataset. Downloads data, normalizes it, trains, and evaluates accuracy.

## Code Structure

* **Data Prep**: Standard CIFAR-10 channel normalization. `num_workers=0` to avoid multiprocessing crashes on Windows.
* **Model**: 2-conv + maxpool -> dropout (0.3) -> 2 FC layers.
* **Optimization**: Cross-Entropy Loss, Adam, StepLR scheduler — halves lr every 5 epochs.

## Parameters

| Parameter | Value |
|---|---|
| Batch Size | 64 |
| Learning Rate | 0.001 |
| Dropout | 0.3 |
| Epochs | 2 (use 10+ for real training) |

## How to Run

```bash
pip install torch torchvision
python cnn_cifar10.py