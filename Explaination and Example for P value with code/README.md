# P-Value: Explanation and Examples with Code

## Overview
This folder contains detailed explanations, mathematical concepts, and practical code examples for understanding **P-values** in statistical hypothesis testing.

## Contents

### What is a P-Value?
A **p-value** is the probability of obtaining results as extreme as (or more extreme than) the observed results, assuming the null hypothesis is true. It quantifies the strength of evidence against the null hypothesis.

or 

p-value is the cumulative probability (area under the curve) of the values to the right of the threshold($$\alpha$$).

### Key Concepts

- **Null Hypothesis (H₀)**: The default assumption that there is no effect or difference
- **Alternative Hypothesis (H₁)**: The hypothesis that challenges the null hypothesis
- **Significance Level (α)**: Typically 0.05, the threshold for rejecting the null hypothesis
- **Decision Rule**: 
  - If p-value < α: Reject the null hypothesis (statistically significant)
  - If p-value ≥ α: Fail to reject the null hypothesis

### Interpretation

| P-Value Range | Interpretation |
|---|---|
| p < 0.001 | Very strong evidence against null hypothesis |
| 0.001 ≤ p < 0.01 | Strong evidence against null hypothesis |
| 0.01 ≤ p < 0.05 | Moderate evidence against null hypothesis |
| 0.05 ≤ p < 0.10 | Weak evidence against null hypothesis |
| p ≥ 0.10 | Insufficient evidence against null hypothesis |

## Common Statistical Tests(For Future Exploration)

- **T-tests** (one-sample, two-sample, paired)
- **Chi-square tests**
- **ANOVA** (Analysis of Variance)
- **Correlation tests**
- **Regression analysis**

## Files in This Folder

- `*.ipynb` - Jupyter notebooks with visualizations and explanations

## How to Use

1. Start with the conceptual explanations and visualizations
2. Review the code implementations
3. Run the examples with your own data
4. Interpret results using the guidelines provided

## Important Notes

⚠️ **Common Misinterpretations:**
- A p-value is NOT the probability that the null hypothesis is true
- A p-value is NOT the probability that the result occurred by chance
- Statistical significance ≠ Practical significance

## Requirements

```
python >= 3.7
scipy
numpy
pandas
matplotlib
```

## References

- [Statistics How To - P-Value](https://www.statisticshowto.com/p-value/)
- [R.A. Fisher - Statistical Methods for Research Workers](https://en.wikipedia.org/wiki/Statistical_Methods_for_Research_Workers)

---
