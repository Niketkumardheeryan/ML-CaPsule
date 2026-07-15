# Association Rule Mining using Apriori and ECLAT

This project demonstrates the implementation of **Association Rule Mining** techniques using the **Apriori** and **ECLAT** algorithms for Market Basket Analysis. The objective is to discover frequent itemsets and generate association rules from transactional retail data, enabling the identification of purchasing patterns and product associations.

## Overview

Association Rule Mining is an unsupervised data mining technique used to uncover relationships among items frequently purchased together. This implementation applies two classical frequent pattern mining algorithms:

- **Apriori** – Candidate generation with iterative pruning based on the downward closure property.
- **ECLAT** – Depth-first frequent itemset mining using a vertical transaction database representation.

The generated association rules are evaluated using **Support**, **Confidence**, and **Lift**.

---

## Dataset

The project uses the **Bakery Dataset**, containing customer transaction records.

| Column | Description |
|--------|-------------|
| TransactionNo | Unique transaction identifier |
| Items | Purchased product |
| DateTime | Timestamp of purchase |
| Daypart | Time segment of the day |
| DayType | Weekday / Weekend |

---

## Project Structure

```
Association Rule Implementation/
│
├── Bakery.csv
├── association.ipynb
├── Apriori_and_ECLAT.ipynb
└── README.md
```

---

## Features

- Transaction preprocessing
- Market Basket Analysis
- Frequent Itemset Mining
- Apriori implementation
- ECLAT implementation
- Association Rule Generation
- Rule ranking using Lift
- Comparative analysis of Apriori and ECLAT

---

## Tech Stack

- Python 3.x
- Pandas
- NumPy
- Matplotlib
- Apyori
- PyECLAT
- Jupyter Notebook

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<repository-name>.git
cd <repository-name>
```

Install dependencies:

```bash
pip install pandas numpy matplotlib apyori pyECLAT
```

---

## Usage

Run the notebooks sequentially:

```text
association.ipynb
```

or

```text
Apriori_and_ECLAT.ipynb
```

Ensure `Bakery.csv` is placed in the project directory before execution.

---

## Algorithm Workflow

1. Load transactional dataset
2. Preprocess transaction records
3. Transform transactions into list format
4. Mine frequent itemsets using Apriori
5. Generate association rules
6. Evaluate rules using Support, Confidence, and Lift
7. Mine frequent itemsets using ECLAT
8. Compare discovered patterns

---

## Evaluation Metrics

| Metric | Description |
|---------|-------------|
| Support | Frequency of an itemset in the dataset |
| Confidence | Conditional probability of consequent given antecedent |
| Lift | Strength of association relative to random occurrence |

---

## Applications

- Product Recommendation Systems
- Market Basket Analysis
- Retail Analytics
- Cross-selling
- Inventory Planning
- Customer Purchase Behavior Analysis

---

## Future Enhancements

- FP-Growth implementation
- Interactive visualizations
- Rule network graph generation
- Performance benchmarking
- Streamlit dashboard
- Hyperparameter optimization

---

## References

- Agrawal, R., Imieliński, T., & Swami, A. (1993). *Mining Association Rules Between Sets of Items in Large Databases.*
- Borgelt, C. (2002). *Efficient Implementations of Apriori and ECLAT.*
- Apyori Documentation
- PyECLAT Documentation

---

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request for improvements, optimizations, or additional association rule mining algorithms.

## License

This project is distributed under the MIT License.

