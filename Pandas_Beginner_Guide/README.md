# 🐼 Pandas Beginner Guide — Comprehensive Tutorial

A complete beginner-friendly tutorial on **Pandas** — the most popular Python library for data manipulation and analysis.

## 🎯 Goal
Help beginners understand and practice the most commonly used Pandas operations through clear, well-commented examples with real-world datasets.

## 📊 Datasets Used
- `employee_data.csv` — Employee records with ID, Name, Age, Department, Salary
- `raw_data.csv` — Raw dataset with country, age, gender, income data

## 📚 Topics Covered

| # | Topic | Key Functions |
|---|-------|---------------|
| 1 | **Series in Pandas** | `pd.Series()`, indexing, vectorized ops |
| 2 | **DataFrame Creation** | `pd.DataFrame()`, from dict/list |
| 3 | **Reading Files** | `pd.read_csv()`, `pd.read_json()` |
| 4 | **DataFrame Methods** | `head()`, `tail()`, `info()`, `describe()` |
| 5 | **Handle Missing Values** | `isnull()`, `fillna()`, `dropna()`, `ffill()` |
| 6 | **Handle Duplicates** | `duplicated()`, `drop_duplicates()` |
| 7 | **Filtering & Indexing** | `.loc[]`, `.iloc[]`, `.query()`, boolean masks |
| 8 | **Data Types** | `dtypes`, `astype()`, string operations |
| 9 | **Feature Engineering** | `apply()`, `map()`, `assign()`, `replace()` |
| 10 | **Sorting & Ranking** | `sort_values()`, `rank()`, `reset_index()` |
| 11 | **GroupBy & Aggregation** | `groupby()`, `.agg()`, `.mean()`, `.count()` |
| 12 | **Melt & Pivot** | `df.melt()`, `df.pivot()` |
| 13 | **Merge & Join** | `pd.merge()` — inner/left/right/outer |
| 14 | **Concatenation** | `pd.concat()` — row/column wise |
| 15 | **Visualization** | `df.plot()`, `df.hist()` |
| 16 | **Writing Files** | `to_csv()`, `to_json()` |

## 🚀 How to Run

1. Clone this repository
2. Install dependencies:
3. Open `Pandas_Beginner_Guide.ipynb` in Jupyter Notebook or VS Code
4. Run all cells from top to bottom

## 💡 Who is this for?
- 🎓 Students learning data science
- 🔰 Beginners new to Pandas
- 👩‍💻 Anyone who wants a quick reference for common Pandas operations

## 👤 Author
**Akshata J** — GSSoC 2026 Contributor

## 🔗 Issue Reference
Closes #1244