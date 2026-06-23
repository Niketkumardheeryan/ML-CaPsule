# K-Means vs Spectral Clustering

## Overview

This project demonstrates the differences between **K-Means Clustering** and **Spectral Clustering** using visualization and experimentation on the Jain dataset.

The main objective is to help learners understand how different clustering algorithms behave on non-convex and irregularly shaped data distributions.

Through graphical comparisons and practical implementation, this notebook highlights:

* the limitations of centroid-based clustering methods,
* the importance of data geometry,
* and how graph-based clustering techniques can better capture complex structures.

---

## Dataset Used

### Jain Dataset

Dataset Link:
https://cs.joensuu.fi/sipu/datasets/jain.txt

Reference:
A. Jain and M. Law, *Data Clustering: A User’s Dilemma*, Lecture Notes in Computer Science, 2005.

### Why this dataset?

The Jain dataset contains:

* non-convex clusters,
* uneven cluster shapes,
* varying cluster densities.

This makes it an excellent benchmark for comparing clustering algorithms because:

* **K-Means** assumes spherical/convex clusters,
* while **Spectral Clustering** can better identify connected structures and irregular cluster boundaries.

---

## Algorithms Implemented

### 1. K-Means Clustering

K-Means partitions data by assigning points to the nearest centroid.

#### Characteristics

* Fast and simple
* Works well on convex/spherical clusters
* Sensitive to initialization and cluster shape

---

### 2. Spectral Clustering

Spectral Clustering uses graph connectivity and eigenvalue decomposition to identify clusters.

#### Characteristics

* Handles non-linear cluster boundaries
* Effective for non-convex datasets
* Captures connectivity between points

---

## Technologies Used

* Python
* NumPy
* Matplotlib
* Jupyter Notebook

---

## Project Structure

```bash
kmeans_vs_spectral_clustering/
│
├── README.md
├── kmeans_vs_spectral_clustering.ipynb
└── results/
```

---

## Results and Observations

### K-Means

* Performs well on simple convex structures
* Struggles with irregular and connected clusters
* Misclassifies non-convex regions in the Jain dataset

### Spectral Clustering

* Better captures the actual cluster structure
* Performs effectively on irregular cluster shapes
* Demonstrates advantages of graph-based clustering approaches

---

## Learning Outcomes

This project helps learners understand:

* clustering fundamentals,
* unsupervised learning concepts,
* geometric assumptions in ML algorithms,
* graph-based learning methods,
* strengths and weaknesses of clustering techniques,
* and the importance of visualization in machine learning.

---

## Future Improvements

Possible extensions to this project:

* Add DBSCAN comparison
* Include silhouette score evaluation
* Interactive visualizations
* Hyperparameter experimentation
* Compare performance on additional datasets

---

## Conclusion

This project provides a practical and beginner-friendly introduction to clustering algorithms through visualization and experimentation.

By comparing K-Means and Spectral Clustering on a challenging dataset, learners can develop stronger intuition about:

* how clustering algorithms work,
* when they fail,
* and how different approaches handle complex data structures.

---

## Author

Created as part of an open-source contribution under GSSoC.

Happy Learning 🚀
