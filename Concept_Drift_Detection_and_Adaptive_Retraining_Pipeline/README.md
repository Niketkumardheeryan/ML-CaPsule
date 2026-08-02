# Concept Drift Detection and Adaptive Retraining Pipeline

In real-world machine learning systems, data is rarely static. Over time, the underlying data distributions change due to shifts in consumer behavior, economic factors, seasonal variations, or system changes. When this happens, a model trained on static historical data will experience performance degradation, commonly known as **Model Decay**.

This project implements an end-to-end pipeline to simulate, detect, and adaptively handle concept and data drift using statistical methods.

---

## 🌟 Key Features
- **Synthetic Data Stream Simulator**: Generates sequential batches of credit risk data containing covariate shift (data drift) and concept drift (relationship shifts).
- **Statistical Drift Detection**: Implements:
  - **Population Stability Index (PSI)** to monitor feature distribution shifts.
  - **Two-Sample Kolmogorov-Smirnov (KS) Test** to detect statistical changes in numerical features.
- **Performance-Aware Monitoring**: Tracks model F1-score and accuracy across batches to identify decay.
- **Adaptive Retraining Pipeline**: Automatically triggers retraining on the latest data when drift is detected, showing how model performance recovers.
- **Rich Visualizations**: Generates distribution plots, PSI trends, and performance comparison charts.

---

## 📐 Theoretical Background

### 1. Data Drift (Covariate Shift)
Covariate shift occurs when the distribution of the input features $P(X)$ changes over time, but the conditional probability $P(Y|X)$ (the relationship between input features and target labels) remains the same.
- **Example**: An economic downturn leads to lower average applicant incomes, but the threshold of income at which a borrower is likely to default does not change.

### 2. Concept Drift
Concept drift occurs when the statistical relationship between the input features and target variable $P(Y|X)$ changes over time, even if the input distribution $P(X)$ remains the same.
- **Example**: Due to high inflation, borrowers with previously "safe" debt-to-income ratios now start defaulting at a much higher rate.

### 3. Population Stability Index (PSI)
PSI measures the magnitude of change in distribution between two samples (a Reference dataset and a Target dataset).
$$\text{PSI} = \sum_{i=1}^{k} \left( T_i - R_i \right) \times \ln\left(\frac{T_i}{R_i}\right)$$
Where:
*   $R_i$ = Percentage of records in Reference bin $i$
*   $T_i$ = Percentage of records in Target bin $i$
*   $k$ = Total number of bins (usually 10 deciles)

**Threshold Interpretation**:
- $\text{PSI} < 0.1$: No significant change; stable distribution.
- $0.1 \le \text{PSI} < 0.25$: Moderate shift; warning limit.
- $\text{PSI} \ge 0.25$: Significant shift; action required (drift detected!).

### 4. Kolmogorov-Smirnov (KS) Test
The two-sample KS test is a non-parametric statistical test that compares the cumulative distribution functions (CDFs) of two continuous datasets.
- **Null Hypothesis ($H_0$)**: The two samples are drawn from the same continuous distribution.
- **Action**: If the computed p-value is less than a significance level (e.g., $0.05$), we reject the null hypothesis and conclude that a distribution shift has occurred.

---

## 📁 Directory Structure
```text
Concept_Drift_Detection_and_Adaptive_Retraining_Pipeline/
├── concept_drift_pipeline.ipynb # Executed Jupyter Notebook with inline visualizations
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 🚀 Execution Guide

### Prerequisites
Make sure you have Python 3.8+ installed. Install the dependencies:
```bash
pip install -r requirements.txt
```

### Running the Jupyter Notebook
Open the notebook in Jupyter or upload it directly to Google Colab:
```bash
jupyter notebook concept_drift_pipeline.ipynb
```

---

## 📊 Results & Visualizations

During execution, the notebook evaluates performance across 10 sequential batches:
- **Batches 1-3**: Stable baseline.
- **Batches 4-6**: Covariate shift (sudden drift detected by PSI and KS test).
- **Batches 7-10**: Concept drift (additional shift in classification boundaries).

### Model Performance Comparison
The interactive plots rendered directly inside `concept_drift_pipeline.ipynb` compare the accuracy/F1-score of a static model (trained once on Batch 1) vs. our adaptive model (which retrains when drift is detected).

* **Static Model (Red)**: Suffers from performance decay as the distribution and concept shift.
* **Adaptive Model (Green)**: Detects the shift, triggers retraining on the drifted batch, and recovers its high predictive accuracy/F1-score.

*All cell outputs, distribution charts, and accuracy comparison plots are pre-rendered directly inside the notebook.*
