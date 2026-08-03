# 🔵 Clustering Algorithms

A comprehensive implementation of **10 clustering algorithms** from scratch using Python and Scikit-learn, with scatter plot visualizations for each algorithm. Ideal for understanding unsupervised machine learning techniques.

---

## 📌 Project Description

Clustering is an unsupervised machine learning technique that groups unlabeled data points based on similarity. This project implements and visualizes the following clustering algorithms:

| Algorithm | Type | Key Parameter |
|-----------|------|---------------|
| **K-Means** | Centroid-based | `n_clusters=2` |
| **Mini-Batch K-Means** | Centroid-based (faster) | `n_clusters=2` |
| **BIRCH** | Hierarchical | `threshold=0.01, n_clusters=2` |
| **DBSCAN** | Density-based | `eps=0.30, min_samples=9` |
| **OPTICS** | Density-based | `eps=0.8, min_samples=10` |
| **Mean Shift** | Centroid/Hierarchical | Auto-detects clusters |
| **Spectral Clustering** | Graph-based | `n_clusters=2` |
| **Gaussian Mixture Model** | Distribution-based | `n_components=2` |
| **Agglomerative Hierarchical** | Hierarchical | Bottom-up |
| **Divisive Hierarchical** | Hierarchical | Top-down |

Each algorithm is applied to the **same synthetic dataset** and outputs a **scatter plot** showing the discovered clusters.

---

## 📂 Dataset

> ✅ **No external dataset needed** — all algorithms use synthetically generated data via `sklearn.datasets.make_classification`

```python
X, _ = make_classification(
    n_samples=1000,       # 1000 data points
    n_features=2,         # 2 features (for 2D visualization)
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    random_state=4
)
```

The same dataset is reused across all algorithms, making it easy to **visually compare** how each algorithm clusters the same data differently.

---

## 🛠️ Dependencies

Install all required libraries with a single command:

```bash
pip install numpy scikit-learn matplotlib
```

| Library | Version | Purpose |
|---------|---------|---------|
| `numpy` | 1.23.5 | Array operations, finding unique clusters |
| `scikit-learn` | 1.2.2 | All clustering algorithm implementations + dataset generation |
| `matplotlib` | 3.6.3 | Scatter plot visualizations |

> 💡 Check your installed versions with `pip show <library-name>`

---

## 🚀 How to Run

> ✅ Works on **Google Colab**, **Jupyter Notebook**, or **VS Code**

### Option A — Google Colab (easiest, no setup)

1. Open [colab.research.google.com](https://colab.research.google.com/)
2. Upload `Clustering_Algorithms.ipynb`
3. Run all cells via `Runtime` → `Run all`
4. Each algorithm cell outputs a scatter plot inline

### Option B — Local Jupyter Notebook

1. Clone the repository:
   ```bash
   git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
   cd "ML-CaPsule/Clustering Algorithms"
   ```

2. Install dependencies:
   ```bash
   pip install numpy scikit-learn matplotlib
   ```

3. Launch Jupyter:
   ```bash
   jupyter notebook Clustering_Algorithms.ipynb
   ```

4. Run each cell individually to see the scatter plot for each algorithm

### Option C — VS Code

1. Open `Clustering_Algorithms.ipynb` in VS Code
2. Select your Python interpreter (with dependencies installed)
3. Click `Run All` or run each cell individually

---

## 📊 Sample Output

Each algorithm produces a **2D scatter plot** where different colours represent different clusters discovered in the data.

For example, K-Means with `n_clusters=2`:
- Generates 1000 data points in 2D space
- Groups them into 2 clusters
- Plots each cluster in a different colour

The same data run through DBSCAN with `eps=0.30` may discover a different cluster boundary, making the visual comparison very informative.

---

## 📁 Project Structure

```
Clustering Algorithms/
├── Clustering_Algorithms.ipynb   ← Main notebook with all algorithm implementations
├── Clustering Algorithms.md      ← Theory reference document
└── README.md
```

---

## 📚 Reference

- [Clustering Algorithms with Python — Machine Learning Mastery](https://machinelearningmastery.com/clustering-algorithms-with-python/)

---

## 👤 Contributor

- Theory by [Shreya Ghosh](https://github.com/Niketkumardheeryan/ML-CaPsule)
- README added as part of [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) open-source contribution
