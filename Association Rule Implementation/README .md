Association Rule Mining using Apriori and ECLAT
This project demonstrates the implementation of Association Rule Mining techniques using the Apriori and ECLAT algorithms for Market Basket Analysis. The objective is to discover frequent itemsets and generate association rules from real bakery transaction data, enabling the identification of purchasing patterns and product associations.
Overview
Association Rule Mining is an unsupervised data mining technique used to uncover relationships among items frequently purchased together. This implementation applies two classical frequent pattern mining algorithms:

Apriori – Candidate generation with iterative pruning based on the downward closure property, implemented via mlxtend.
ECLAT – Depth-first frequent itemset mining using a vertical transaction database (item → transaction-ID sets) and set intersection, implemented from scratch.

The generated association rules are evaluated using Support, Confidence, and Lift, and the results from both algorithms are cross-checked against each other.

Dataset
The project uses the Bakery Dataset, containing real point-of-sale transaction records (20,507 line items across 9,465 transactions).
ColumnDescriptionTransactionNoUnique transaction identifierItemsPurchased productDateTimeTimestamp of purchaseDaypartTime segment of the dayDayTypeWeekday / Weekend

Project Structure
Association Rule Implementation/
│
├── Bakery.csv
├── bakery_association_rules.ipynb
└── README.md

Features

Transaction preprocessing and calendar feature extraction (day, month)
Exploratory data analysis: best-selling items, sales by day part, sales by weekday
Frequent itemset mining with Apriori (mlxtend)
Rule generation and refinement (filtering out trivial high-frequency consequents)
Frequent itemset mining with a hand-implemented ECLAT (vertical tidset intersection)
Rule ranking using Lift
Network graph visualization of top association rules
Comparative analysis of Apriori and ECLAT results


Tech Stack

Python 3.x
Pandas / NumPy
Matplotlib
mlxtend (Apriori + association rule generation)
NetworkX (rule network visualization)
Jupyter Notebook


Installation
Clone the repository:
git clone https://github.com/<repository-name>.git
cd <repository-name>
Install dependencies:
pip install pandas numpy matplotlib mlxtend networkx jupyter

Usage
Ensure Bakery.csv is in the same directory, then run:
bakery_association_rules.ipynb

Algorithm Workflow

Load and explore the transactional dataset
Extract calendar features and visualize sales patterns
Group transactions by TransactionNo into item sets
One-hot encode transactions for Apriori
Mine frequent itemsets and generate rules with Apriori (mlxtend)
Refine rules by removing trivial high-frequency consequents
Convert transactions into a vertical (item → tidset) format
Mine frequent itemsets with ECLAT via tidset intersection
Compare top itemsets from Apriori and ECLAT for consistency


Evaluation Metrics
MetricDescriptionSupportFrequency of an itemset in the datasetConfidenceConditional probability of consequent given antecedentLiftStrength of association relative to random occurrence

Key Findings

Coffee, Bread, and Tea dominate raw sales frequency; filtering Coffee out as a rule consequent was necessary to surface meaningful (non-trivial) associations.
(Bread, Coffee) is the strongest itemset, agreed upon by both Apriori and ECLAT.
Sales peak in the afternoon and on weekends.


Applications

Product Recommendation Systems
Market Basket Analysis
Retail Analytics
Cross-selling
Inventory Planning
Customer Purchase Behavior Analysis


Future Enhancements

FP-Growth implementation for comparison
Interactive (Plotly/Streamlit) visualizations
Time-segmented rule mining (e.g. rules specific to Daypart)
Performance benchmarking across algorithms
Hyperparameter sensitivity analysis (varying min_support/min_threshold)


References

Agrawal, R., Imieliński, T., & Swami, A. (1993). Mining Association Rules Between Sets of Items in Large Databases.
Borgelt, C. (2002). Efficient Implementations of Apriori and ECLAT.
mlxtend Documentation
NetworkX Documentation


Contributing
Contributions are welcome. Feel free to open an issue or submit a pull request for improvements, optimizations, or additional association rule mining algorithms.
License
This project is distributed under the MIT Licens
