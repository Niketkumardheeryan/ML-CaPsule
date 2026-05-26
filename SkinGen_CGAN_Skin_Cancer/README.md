\# SkinGen — Synthetic Skin Cancer Image Generation with CGAN



\## Goal

Skin cancers are hard to detect because AI models have very few rare case images to learn from.

SkinGen generates realistic synthetic images using a Conditional GAN (CGAN) trained on the

HAM10000 dataset to fix this problem.



\## Dataset

HAM10000 — 10,000 real dermoscopy images across 7 skin lesion categories.

Download from: https://www.kaggle.com/datasets/kmader/skin-lesion-analysis-toward-melanoma-detection



\## Tech Stack

\- Python

\- PyTorch

\- Torchvision

\- NumPy / Pandas

\- Matplotlib

\- scikit-learn

\- Google Colab (for GPU training)



\## Project Structure

SkinGen\_CGAN\_Skin\_Cancer/

├── README.md

├── requirements.txt

├── models/

├── notebooks/

└── utils/



\## How It Works

1\. Train a CGAN on HAM10000 images conditioned on lesion class label

2\. Generate synthetic images for rare classes

3\. Train a classifier on real + synthetic images together

4\. Improves rare skin cancer detection accuracy



\## Author

Your Name — GitHub: https://github.com/yourusername

