# 🧮 Math for Machine Learning

> [!NOTE]
> This section covers the three mathematical pillars that form the foundation of almost all Machine Learning algorithms: Linear Algebra, Calculus, and Probability. Understanding these concepts is essential to grasp *how* algorithms like Gradient Descent and Neural Networks actually learn.

---

## 🛤️ Learning Roadmap & Notebook Order

We recommend following these notebooks in sequence. Each notebook explains the concepts, demonstrates the math with Python code, and directly connects it to a real-world ML application present in this repository.

### 1. [Linear Algebra for ML](Linear_Algebra_for_ML.ipynb)
* **Concepts:** Vectors, Matrices, Dot Products, Matrix Multiplication, Transposition.
* **ML Connection:** Learn how weight matrices work in Neural Networks and how algorithms like scikit-learn's `LinearRegression` use vector dot products to generate predictions.

### 2. [Calculus for ML](Calculus_for_ML.ipynb)
* **Concepts:** Derivatives, Partial Derivatives, Gradients, Chain Rule.
* **ML Connection:** Unpack the math behind **Gradient Descent** and loss minimization. Understand how the chain rule powers backpropagation in Neural Networks to update weights.
* **Key Formula:** $\frac{\partial L}{\partial w}$ (Partial derivative of the Loss function with respect to weight).

### 3. [Probability & Distributions for ML](Probability_for_ML.ipynb)
* **Concepts:** Conditional Probability, Bayes Theorem, Normal (Gaussian) Distribution, PDF/CDF.
* **ML Connection:** Discover the probabilistic foundation of the **Naive Bayes** classifier.
* **Key Formula:** $P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}$ (Bayes' Theorem).

---

## 📚 Recommended Curated Resources
If you want to dive deeper into the intuition behind the math, these external resources are highly recommended for visual learners:

1. **[3Blue1Brown: Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)** 
   * *The best visual explanation of what vectors and matrices actually represent.*
2. **[3Blue1Brown: Essence of Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)** 
   * *Develop an intuitive understanding of derivatives and the chain rule.*
3. **[StatQuest with Josh Starmer](https://www.youtube.com/user/joshstarmer)** 
   * *Phenomenal, easy-to-understand breakdowns of Probability and Statistics for ML.*
4. **Khan Academy** 
   * *Excellent for foundational practice problems across all three subjects.*
