# t-SNE: t-Distributed Stochastic Neighbor Embedding

t-SNE is a popular unsupervised machine learning technique used to visualize 
high-dimensional data in 2D or 3D. Unlike PCA, it captures non-linear 
relationships, making it much better at revealing natural clusters in data.

## Contents

- Introduction to t-SNE and how it differs from PCA
- Implementation on the digits dataset using scikit-learn
- Side-by-side visual comparison with PCA
- Effect of perplexity on the output
- PCA → t-SNE pipeline for large datasets

## Dataset

Uses the digits dataset built into scikit-learn — 1797 handwritten digit 
images (0–9), each represented as 64 features.
