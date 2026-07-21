# 🌀 Unsupervised Learning Interview Questions

Unsupervised Learning is a type of machine learning that looks for previously undetected patterns in a data set with no pre-existing labels and with a minimum of human supervision. It focuses on grouping data (clustering) or reducing its dimensions (dimensionality reduction).

---

## 🔍 Core Concept Overview

- **Algorithms Covered**: K-Means, Hierarchical Clustering, DBSCAN, Principal Component Analysis (PCA), t-SNE.
- **Core Concepts**: Distance Metrics (Euclidean, Manhattan, Cosine), Silhouette Coefficient, Explained Variance, Curse of Dimensionality, Density-based clustering.

---

## 🙋 Interview Questions & Answers

### Q1: What is Unsupervised Learning, and what are its primary use cases? (Easy)
**Answer**:
Unsupervised Learning involves training algorithms on datasets that do not have labeled outputs. The model tries to learn the underlying structure, distribution, or relationships in the data on its own.

**Primary Use Cases**:
1. **Clustering**: Grouping data points into clusters based on similarity (e.g., customer segmentation, document categorization).
2. **Dimensionality Reduction**: Reducing the number of features while retaining essential information (e.g., PCA, visualization, compression).
3. **Anomaly Detection**: Finding data points that deviate significantly from the norm (e.g., credit card fraud detection, industrial equipment monitoring).
4. **Association Rule Learning**: Finding interesting relationships between variables in large databases (e.g., market basket analysis: "people who buy diapers also buy beer").

---

### Q2: Explain the step-by-step working of K-Means Clustering. (Easy)
**Answer**:
K-Means is a centroid-based, iterative clustering algorithm.
**Step-by-step algorithm**:
1. **Initialization**: Choose the number of clusters $K$ and randomly initialize $K$ centroids (or use K-Means++).
2. **Assignment**: Assign each data point to the nearest centroid based on a distance metric (usually Euclidean distance).
3. **Update**: Calculate the mean of all points assigned to each cluster, and move the centroid to this new mean position.
4. **Repeat**: Repeat steps 2 and 3 until convergence (centroids no longer change position, or maximum iterations are reached).

Objective function (Within-Cluster Sum of Squares - WCSS):
$$J = \sum_{i=1}^{K} \sum_{x \in S_i} ||x - \mu_i||^2$$
Where $\mu_i$ is the centroid of cluster $S_i$.

---

### Q3: How do you choose the optimal number of clusters $K$ in K-Means? (Easy)
**Answer**:
Two primary methods are used:

1. **The Elbow Method**:
   - Plot the WCSS (Within-Cluster Sum of Squares) against different values of $K$.
   - As $K$ increases, WCSS decreases because clusters get smaller.
   - Look for the "elbow" point—the point where the rate of WCSS decrease sharply slows down. This point represents a good balance between compactness and simplicity.

2. **Silhouette Analysis**:
   - Measures how similar an object is to its own cluster compared to other clusters.
   - The Silhouette Score ranges from $-1$ to $+1$. A score close to $+1$ indicates that the point is far away from neighboring clusters and well-matched to its own.
   - Choose $K$ that maximizes the average Silhouette Score across the dataset.

---

### Q4: What are the limitations of K-Means Clustering? (Medium)
**Answer**:
1. **Sensitive to Initialization**: Random initialization can lead to different final cluster configurations (local minima).
   - *Solution*: Use **K-Means++** initialization.
2. **Requires Prespecifying $K$**: You must know or estimate the number of clusters beforehand.
3. **Sensitive to Outliers**: Outliers can pull centroids far away from the actual center of dense groups.
   - *Solution*: Use K-Medoids or remove outliers.
4. **Assumes Spherical Clusters**: It struggles with complex shapes (like nested circles or moons) and clusters of varying sizes and densities.
5. **Distance Dependency**: It suffers from the curse of dimensionality, and requires numerical features (distance metrics don't apply naturally to categorical variables).

---

### Q5: Compare K-Means and DBSCAN. In what scenarios would you choose DBSCAN? (Medium)
**Answer**:
DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points that are close together based on density, identifying outliers as noise.

| Feature | K-Means | DBSCAN |
| :--- | :--- | :--- |
| **Cluster Shape** | Assumes spherical clusters | Can find arbitrary shapes (non-convex) |
| **Number of Clusters $K$** | Must be specified | Automatically determined |
| **Noise/Outliers** | Force-assigns outliers to clusters | Classifies outliers as noise |
| **Parameters** | $K$ (clusters) | `eps` (neighborhood radius) and `min_samples` |
| **Density Variations** | Handles density variations | Struggles with varying density clusters |

**When to choose DBSCAN**:
Choose DBSCAN when your clusters are of irregular shapes (e.g., map data, planetary tracks), the data contains significant noise/outliers, and you do not know the expected number of clusters.

---

### Q6: Explain Hierarchical Clustering. What is the difference between Agglomerative and Divisive clustering? (Medium)
**Answer**:
Hierarchical clustering builds a tree of clusters (called a **dendrogram**).

- **Agglomerative (Bottom-Up)**:
  - Start by treating each data point as a single cluster.
  - Successively merge the two closest clusters based on a linkage criterion (e.g., Single, Complete, Average, Ward's linkage).
  - Repeat until all points are merged into one single cluster.
- **Divisive (Top-Down)**:
  - Start with all data points in a single cluster.
  - Iteratively split the cluster into smaller clusters.
  - Repeat until each data point is its own cluster.

You cut the dendrogram at a specific height to get the desired number of clusters.

---

### Q7: What is Principal Component Analysis (PCA) and how does it work conceptually? (Medium)
**Answer**:
PCA is an unsupervised dimensionality reduction technique. It projects high-dimensional data onto a lower-dimensional subspace while maximizing the variance of the projected data.

**Conceptual Workflow**:
1. **Standardize the data**: Ensure all features have a mean of $0$ and a standard deviation of $1$.
2. **Compute Covariance Matrix**: Understand how variables correlate with one another.
3. **Eigen Decomposition**: Compute the eigenvectors and eigenvalues of the covariance matrix.
   - **Eigenvectors** (Principal Components) represent the directions of maximum variance (axes).
   - **Eigenvalues** represent the magnitude of variance carried by each principal component.
4. **Sort and Select**: Sort eigenvectors by their eigenvalues in descending order. Select the top $k$ components.
5. **Project**: Multiply the original standardized data by the selected eigenvectors to transform it into the new $k$-dimensional space.

---

### Q8: What are the differences between PCA and t-SNE? When would you use t-SNE over PCA? (Hard)
**Answer**:

| Feature | PCA | t-SNE |
| :--- | :--- | :--- |
| **Type** | Linear projection | Non-linear, probabilistic |
| **Objective** | Maximizes global variance preservation | Preserves local distances/similarities |
| **Determinism** | Deterministic (same output every time) | Stochastic (results vary due to random initialization) |
| **Computational Speed** | Very fast, scalable | Slow, memory-intensive |
| **Model Reusability** | Learns a transformation matrix (can project new data) | Does not learn a reusable function (cannot easily project new data) |

**When to use t-SNE**:
Use t-SNE when you need to visualize high-dimensional clusters in 2D or 3D space. It is excellent at separating complex manifolds (like handwriting digits) that linear methods like PCA cannot separate.

---

### Q9: What are the mathematical meanings of Eigenvalues and Eigenvectors in the context of PCA? (Medium)
**Answer**:
Let $\Sigma$ be the covariance matrix of the standardized dataset.
An **eigenvector** $v$ and its corresponding **eigenvalue** $\lambda$ satisfy:

$$\Sigma v = \lambda v$$

In PCA:
- The **eigenvector** $v$ defines the direction of the principal component. These vectors are orthogonal to one another.
- The **eigenvalue** $\lambda$ represents the variance of the data along that eigenvector's direction.
- The **proportion of explained variance** by the $i$-th component is calculated as:
  $$\text{Explained Variance Ratio} = \frac{\lambda_i}{\sum_{j=1}^{F} \lambda_j}$$
  This helps determine how many components to keep (e.g., keeping components that explain $95\%$ of total variance).

---

### Q10: How does K-Means handle outliers, and how can we make it more robust? (Hard)
**Answer**:
In K-Means, outliers distort the cluster centroids because the centroid update step calculates the mean of all points assigned to that cluster. The mean is highly sensitive to extreme values.

**How to make it more robust**:
1. **K-Medoids (PAM - Partitioning Around Medoids)**: Instead of taking the mean of points (which can be a point that doesn't exist in the data), K-Medoids uses actual data points (medoids) as cluster centers. It minimizes the sum of absolute pairwise distances (Manhattan distance) rather than squared Euclidean distances, making it far less sensitive to outliers.
2. **K-Means++**: Improves the initialization step by choosing initial centroids that are far apart from each other, which prevents poor initializations from getting stuck in local minima caused by outliers.
3. **Pre-processing**: Detect and remove outliers using IQR (Interquartile Range) or Isolation Forests before clustering.

---

### Q11: What is the Silhouette Coefficient, and how is it calculated? (Hard)
**Answer**:
The Silhouette Coefficient is a metric used to calculate the goodness of a clustering technique. For a single data point $i$:

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$

Where:
- $a(i)$ is the mean distance between point $i$ and all other points in the same cluster. (Measures **cohesion**—should be small).
- $b(i)$ is the mean distance between point $i$ and all points in the nearest cluster that $i$ is not part of. (Measures **separation**—should be large).

**Interpretation**:
- $s(i) \approx +1$: Point is well clustered.
- $s(i) \approx 0$: Point is on the boundary between two clusters.
- $s(i) \approx -1$: Point is probably placed in the wrong cluster.

---

## ⚠️ Common Mistakes in Interviews

1. **Using t-SNE for Feature Engineering**: Candidates often suggest using t-SNE to reduce features prior to feeding them into a classification model. This is incorrect because t-SNE does not output a transformation matrix; you cannot transform new test data in the same way. Use PCA or Autoencoders instead.
2. **Applying PCA to Categorical Data**: Standard PCA calculates linear correlations (covariance) which assume continuous numerical variables. Using it on One-Hot encoded categorical data is mathematically incorrect. One should use Multiple Correspondence Analysis (MCA) instead.
3. **Forgetting to Scale before PCA/Clustering**: PCA is highly sensitive to feature variance. If one feature is measured in meters and another in kilometers, PCA will focus almost entirely on the meters feature because of its larger numerical variance.

---

## 📚 Additional Learning Resources

- **Interactive Visualizations**:
  - [Visualizing t-SNE (Distill.pub)](https://distill.pub/2016/misread-tsne/)
- **Documentation**:
  - [scikit-learn Clustering Guide](https://scikit-learn.org/stable/modules/clustering.html)
  - [scikit-learn PCA Guide](https://scikit-learn.org/stable/modules/decomposition.html#pca)
