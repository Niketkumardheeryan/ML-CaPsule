# SkinGen — Synthetic Skin Cancer Image Generation using CGAN

## Problem Statement
Rare skin cancer subtypes are hard to diagnose because AI models have too few
images to learn from. SkinGen generates realistic synthetic images using a
Conditional GAN (CGAN) trained on HAM10000 to address this data-scarcity problem.

## Tech Stack
- Python, PyTorch, Torchvision
- NumPy, Pandas, Matplotlib
- scikit-learn
- Google Colab (for GPU training)

## Dataset
[HAM10000](https://www.kaggle.com/datasets/kmader/skin-lesion-analysis-toward-melanoma-detection)
— 10,000 dermoscopy images across 7 lesion categories. Not committed to this
repo; download link is above and instructions are in the notebook.

## How It Works
1. Load HAM10000 images and metadata, label-encode the 7 lesion classes
2. Train a class-conditional GAN (Generator + Discriminator, both conditioned
   on lesion label via embeddings)
3. Generate synthetic images per class to balance rare categories
4. (Future work) Train a downstream classifier on real + synthetic images and
   compare performance against a real-only baseline

## Project Structure
```
SkinGen_CGAN_Skin_Cancer/
├── README.md
├── requirements.txt
└── SkinGen_CGAN.ipynb
```

## Usage
Open `SkinGen_CGAN.ipynb` in Google Colab, enable a GPU runtime, download the
HAM10000 dataset from the link above, update `DATA_DIR` in the notebook to
point at it, and run all cells.
