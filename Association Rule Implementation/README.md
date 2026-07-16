# Association Rule Implementation

This folder contains notebooks and data for performing association rule mining on transaction datasets (supermarket and bakery). The notebooks demonstrate Apriori and an ECLAT-style frequency analysis, exploratory data analysis (EDA), and visualization of item associations.

## Datasets
- `Market_Basket_Optimisation.csv` — weekly supermarket baskets (7,501 transactions). Each row is a customer's basket with up to 20 item columns.
- `Bakery.csv` — bakery transactions (20,507 rows, ~9,465 unique transactions) including `TransactionNo`, `Items`, `DateTime`, `Daypart`, and `DayType`.

## Notebooks

- `Apriori_and_ECLAT.ipynb`
	- Loads supermarket basket data and prepares transaction lists.
	- Runs Apriori (using `apyori`) to find frequent itemsets and association rules (min_support ~0.003, min_confidence=0.2, min_lift=3).
	- Implements an ECLAT-style frequency calculation (pairs and trios) to rank most common item combinations by raw frequency.
	- Compares Apriori results (association strength) with ECLAT frequency rankings.

- `association.ipynb`
	- Loads `Bakery.csv`, runs EDA (top items, peak sale hours, day/month trends) using `pandas` and `plotly`.
	- Prepares transactions and one-hot encodes items with `mlxtend.preprocessing.TransactionEncoder`.
	- Runs `mlxtend.frequent_patterns.apriori` and `mlxtend.frequent_patterns.association_rules` to generate and filter rules.
	- Visualizes item connections with `networkx` and interactive Plotly graphs.

## Key Methods and Libraries
- Apriori: discovers frequent itemsets and derives rules (support, confidence, lift).
- ECLAT-style frequency scoring: counts how often combinations appear across transactions.
- Libraries: `pandas`, `numpy`, `mlxtend`, `apyori`, `plotly`, `networkx`, `matplotlib`.

## Quick Usage
1. Install dependencies (recommended in a venv):

```bash
pip install pandas numpy mlxtend apyori plotly networkx matplotlib
```

2. Open the notebooks in Jupyter or VS Code and run cells in order. The notebooks load `Market_Basket_Optimisation.csv` and `Bakery.csv` from this folder.

## Example Findings (from notebooks)
- Supermarket data: combinations like `olive oil`, `whole wheat pasta`, and `mineral water` appear as strong association rules by Apriori.
- Bakery data: `Coffee` is the top-selling item and shows strong associations with cakes, pastries, and tea.

## Business Impact
- Use discovered rules for: product recommendations, bundle offers, targeted promotions, and strategic product placement in stores.

## Notes & Next Steps
- You can tune Apriori `min_support`, `min_confidence`, and `min_lift` to find more or fewer rules.
- Consider persisting rules and building a simple recommender that suggests items at checkout.

---

Contributed as part of the ML-CaPsule project.

