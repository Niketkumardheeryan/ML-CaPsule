# Association Rule Implementation

This folder contains notebooks and data for performing association rule mining on transaction datasets. The notebook demonstrates exploratory data analysis (EDA), association rule mining using the Apriori algorithm, and visualization of item associations.

## Dataset

- `Bakery.csv` — bakery transactions (20,507 rows, ~9,465 unique transactions) including `TransactionNo`, `Items`, `DateTime`, `Daypart`, and `DayType`.

## Notebook

- `association.ipynb`

  - Loads `Bakery.csv` and performs exploratory data analysis (EDA), including top-selling items, peak sale hours, and day/month trends using `pandas` and `plotly`.
  - Prepares transactions and one-hot encodes items using `mlxtend.preprocessing.TransactionEncoder`.
  - Applies the Apriori algorithm using `mlxtend.frequent_patterns.apriori`.
  - Generates association rules with `mlxtend.frequent_patterns.association_rules`.
  - Visualizes item relationships using `networkx` and interactive Plotly graphs.

## Key Methods and Libraries

- **Apriori Algorithm** for discovering frequent itemsets and generating association rules based on support, confidence, and lift.
- Libraries used:
  - pandas
  - numpy
  - mlxtend
  - plotly
  - networkx
  - matplotlib

## Quick Usage

### Prerequisites

Ensure Python is installed on your system. All required dependencies are listed in the `requirements.txt` file.

### Installation

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

### Run the Project

Open `association.ipynb` in Jupyter Notebook, JupyterLab, or Visual Studio Code and run the cells sequentially.

## Example Findings

- `Coffee` is the top-selling bakery item.
- Strong association rules are observed between coffee, cakes, pastries, and tea.
- Interactive network visualizations help identify relationships between frequently purchased items.

## Business Impact

The discovered association rules can be used for:

- Product recommendations
- Bundle offers
- Cross-selling strategies
- Targeted promotions
- Store layout optimization

## Notes & Future Improvements

- Tune `min_support`, `min_confidence`, and `min_lift` to discover different sets of association rules.
- Extend the project by building a recommendation system based on the generated rules.

---

Contributed as part of the ML-CaPsule project.