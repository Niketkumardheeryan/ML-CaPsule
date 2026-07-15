# Association Rule Mining using Apriori and ECLAT

Association Rule Mining is an unsupervised machine learning technique used to discover hidden relationships and co-occurrence patterns among items within transactional datasets. This project implements the **Apriori** and **ECLAT (Equivalence Class Clustering and Bottom-up Lattice Traversal)** algorithms to identify frequent itemsets and generate high-quality association rules from a retail bakery transaction dataset.

The objective is to analyze customer purchasing behavior through **Market Basket Analysis (MBA)** by extracting statistically significant associations between products. The resulting patterns can be leveraged for recommendation systems, cross-selling strategies, inventory optimization, and retail merchandising.

---

## Features

* Implementation of the Apriori algorithm for frequent itemset generation
* Implementation of the ECLAT algorithm using a vertical transaction representation
* Market Basket Analysis on real-world transactional data
* Association rule generation using Support, Confidence, and Lift metrics
* Ranking of discovered rules based on Lift
* Data preprocessing for transactional datasets
* Comparative analysis of Apriori and ECLAT

---

## Dataset

The project utilizes the **Bakery Dataset**, where each record represents an item purchased within a customer transaction.

### Dataset Attributes

| Attribute     | Description                   |
| ------------- | ----------------------------- |
| TransactionNo | Unique transaction identifier |
| Items         | Purchased product             |
| DateTime      | Timestamp of transaction      |
| Daypart       | Morning, Afternoon, Evening   |
| DayType       | Weekday or Weekend            |

The transactional dataset is transformed into a list-based representation required by association rule mining algorithms.

---

## Project Structure

```
Association Rule Implementation/
│
├── Bakery.csv
├── association.ipynb
├── Apriori_and_ECLAT.ipynb
├── README.md
```

---

## Methodology

The overall workflow consists of the following stages:

1. Data acquisition and preprocessing
2. Transaction encoding
3. Frequent itemset mining using Apriori
4. Frequent itemset mining using ECLAT
5. Association rule generation
6. Rule evaluation using interestingness measures
7. Rule ranking and interpretation

---

## Algorithms

### Apriori

Apriori follows a level-wise candidate generation approach based on the **downward closure property**, which states that every subset of a frequent itemset must also be frequent. Candidate itemsets are iteratively generated and pruned according to a minimum support threshold.

### ECLAT

ECLAT adopts a depth-first search strategy using a **vertical data format (Transaction ID Sets)** instead of candidate generation. This approach significantly reduces computational overhead for dense transactional datasets and generally outperforms Apriori in terms of execution speed.

---

## Evaluation Metrics

Association rules are evaluated using the following metrics:

### Support

Measures the frequency of occurrence of an itemset within the dataset.

[
Support(A \rightarrow B)=\frac{Transactions(A \cup B)}{Total\ Transactions}
]

### Confidence

Represents the conditional probability of purchasing item **B** given that item **A** has already been purchased.

[
Confidence(A \rightarrow B)=\frac{Support(A \cup B)}{Support(A)}
]

### Lift

Measures the strength of an association relative to random chance.

[
Lift(A \rightarrow B)=\frac{Confidence(A \rightarrow B)}{Support(B)}
]

A Lift value greater than **1** indicates a positive association between items.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Apyori
* PyECLAT
* Jupyter Notebook

---

## Installation

Clone the repository:

```bash
git clone https://github.com/nitikasingh12/ML-CaPsule.git
```

Navigate to the project directory:

```bash
cd ML-CaPsule
```

Install the required dependencies:

```bash
pip install pandas numpy matplotlib apyori pyECLAT
```

---

## Usage

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Execute the notebooks sequentially:

* `association.ipynb`
* `Apriori_and_ECLAT.ipynb`

---

## Results

The implementation generates:

* Frequent Itemsets
* Association Rules
* Support Scores
* Confidence Scores
* Lift Values
* Ranked Association Rules
* Comparative analysis between Apriori and ECLAT

The extracted rules reveal statistically significant product co-occurrence patterns that can support data-driven retail decision making.

---

## Applications

* Market Basket Analysis
* Recommendation Systems
* Product Bundling
* Cross-selling and Up-selling
* Shelf Space Optimization
* Customer Purchase Behavior Analysis
* Inventory Management
* Retail Analytics

---

## Future Work

* FP-Growth implementation for improved scalability
* Interactive visualization dashboard using Streamlit
* Rule network visualization using NetworkX
* Hyperparameter optimization
* Comparative benchmarking across multiple frequent pattern mining algorithms
* Integration with real-time recommendation systems

---

## References

* Agrawal, R., Imieliński, T., & Swami, A. (1993). *Mining Association Rules Between Sets of Items in Large Databases.*
* Borgelt, C. (2002). *Efficient Implementations of Apriori and ECLAT.*
* Apyori Documentation
* PyECLAT Documentation

---

## Author

**Nitika Singh**

* GitHub: https://github.com/nitikasingh12
* LinkedIn: https://www.linkedin.com/in/nitika-singh-497534312

