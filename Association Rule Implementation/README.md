# 🛒 Association Rule Implementation

A data mining project implementing **Apriori** and **ECLAT** association rule algorithms to discover frequent itemsets and buying patterns from real bakery and grocery transaction datasets.

---

## 📌 Project Description

Association Rule Mining finds relationships between items in large datasets — for example, *"customers who buy bread also tend to buy coffee."*

This project implements two popular algorithms:

| Algorithm | Description |
|-----------|-------------|
| **Apriori** | Finds frequent itemsets level by level using a bottom-up approach |
| **ECLAT** | Uses vertical data format for faster frequent itemset mining |

> 💡 Key insight from the project: Confidence should not be set too high — some items appear together simply because they are popular (e.g. mineral water + toilet paper), not because they are truly associated.

---

## 📂 Datasets

### 1. Bakery Dataset (`Bakery.csv`) — included in the folder
Real bakery transaction data with the following columns:

| Column | Description |
|--------|-------------|
| `TransactionNo` | Unique transaction ID |
| `Items` | Item purchased |
| `DateTime` | Date and time of purchase |
| `Daypart` | Morning / Afternoon / Evening |
| `DayType` | Weekend / Weekday |

**Sample data:**

| TransactionNo | Items | DateTime | Daypart | DayType |
|---|---|---|---|---|
| 1 | Bread | 2016-10-30 09:58 | Morning | Weekend |
| 2 | Scandinavian | 2016-10-30 10:05 | Morning | Weekend |
| 3 | Hot chocolate | 2016-10-30 10:07 | Morning | Weekend |

### 2. Groceries Dataset (`Groceries_dataset.csv`) — included in the folder
Grocery store transaction data used for Apriori implementation.

> ✅ Both datasets are already included in the project folder — no external download needed.

---

## 🛠️ Dependencies

Install the required libraries:

```bash
pip install pandas numpy mlxtend apyori matplotlib seaborn
```

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading and manipulation |
| `mlxtend` | Apriori and association rules implementation |
| `apyori` | Alternative Apriori implementation ([source](https://github.com/ymoch/apyori)) |
| `matplotlib` / `seaborn` | Visualization |

---

## 🚀 How to Run

> ✅ This project can be run on **Google Colab** or **locally with Jupyter Notebook**.

### Option A — Google Colab (easier)
1. Open [colab.research.google.com](https://colab.research.google.com/)
2. Upload the notebook (`Apriori_and_ECLAT.ipynb` or `19csu207.ipynb`)
3. Upload `Bakery.csv` and `Groceries_dataset.csv` to the Colab session
4. Run all cells via `Runtime` → `Run all`

### Option B — Local Jupyter Notebook
1. Clone the repository:
   ```bash
   git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
   cd "ML-CaPsule/Association Rule Implementation"
   ```
2. Install dependencies:
   ```bash
   pip install pandas numpy mlxtend apyori matplotlib seaborn
   ```
3. Launch Jupyter:
   ```bash
   jupyter notebook Apriori_and_ECLAT.ipynb
   ```
4. Run all cells in order

---

## 📊 Sample Output

The algorithms output association rules in the form:

```
{coffee} → {bread}   | Support: 0.32 | Confidence: 0.71 | Lift: 1.84
{cake}   → {coffee}  | Support: 0.21 | Confidence: 0.65 | Lift: 1.62
```

| Metric | Meaning |
|--------|---------|
| **Support** | How often the itemset appears in all transactions |
| **Confidence** | How often the rule is correct |
| **Lift** | How much more likely items are bought together vs. independently |

---

## 📁 Project Structure

```
Association Rule Implementation/
├── Apriori_and_ECLAT.ipynb     ← Main notebook (Apriori + ECLAT)
├── 19csu207.ipynb              ← Additional implementation notebook
├── Bakery.csv                  ← Bakery transactions dataset
├── Groceries_dataset.csv       ← Groceries transactions dataset
└── README.md
```

---

## 👤 Contributor

- README added as part of [ML-CaPsule](https://github.com/Niketkumardheeryan/ML-CaPsule) open-source contribution
