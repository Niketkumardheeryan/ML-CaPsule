# 📐 Math for ML

> Maths for ML  

This section fills that gap with three focused Jupyter notebooks that explain the math, show it in code, and connect it **directly to algorithms present in this repo**.

---

## 📂 Notebooks in this folder

| Notebook | Math Covered | ML Connection in this Repo |
|---|---|---|
| `Linear_Algebra/Linear_Algebra.ipynb` | Vectors, matrices, dot products, matrix multiplication, transposition | Neural network weight matrices · `sklearn` LinearRegression under the hood |
| `Calculus/Calculus.ipynb` | Derivatives, partial derivatives, chain rule | Directly bridges to the **GradientDescent/** folder in this repo |
| `Probability/Probability.ipynb` | Bayes theorem, conditional probability, Normal distribution, PDF/CDF | Directly bridges to the **Naive_Bayes/** folder in this repo |

---

## Who is this for?

- Complete beginners following this repo **without a mentor**
- Anyone who has hit a wall trying to understand *why* Gradient Descent or Naive Bayes works
- Self-learners who want worked examples tied to code, not just external links

---

## 📺 Curated Video Resources

Each notebook links to these at the relevant section, but here they are up front:

| Topic | Resource | Why it's great |
|---|---|---|
| Linear Algebra | [3Blue1Brown — Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) | Visual intuition, builds geometric understanding |
| Calculus | [3Blue1Brown — Essence of Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) | Builds intuition for derivatives from scratch |
| Probability & Stats | [StatQuest with Josh Starmer](https://www.youtube.com/c/joshstarmer) | Clear, step-by-step stats explanations for ML |

---

## 🗂️ How each notebook is structured

Every notebook follows the same pattern, consistent with how `Statistical_modeling_python` and `Chi-Square Test` are done in this repo:

```
1. Concept explained in plain English
2. Math shown with LaTeX + intuitive examples
3. Code implementation from scratch (NumPy)
4. Real ML connection demonstrated (sklearn / existing repo folder)
5. Video resource linked at the relevant section
```

---

## ✅ Prerequisites

- Python basics (loops, functions)
- NumPy (basic arrays) — introduced within each notebook if needed

---

## 🔗 Related folders in this repo

- [`GradientDescent/`](../GradientDescent/) — Notebook Calculus is the conceptual intro to this
- [`Naive_Bayes/`](../Naive_Bayes/) — Notebook Probability  is the conceptual intro to this

---

*Part of [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) — ML for everyone, with or without a mentor.*