# 🚨 Crime Analytics & Spatial-Temporal Risk Intelligence

## 🎯 Project Overview

The **Crime Analytics** module provides advanced analytical insights and spatial-temporal visualizations for historical crime datasets. It equips analysts, researchers, and public safety personnel with data-driven decision support tools to identify high-risk hotspots, monitor temporal trend shifts, calculate dynamic location risk scores, and automate summary observations.

---

## 🚀 Key Features

1. **Temporal Trend Analysis**: Analyzes crime volume fluctuations across custom time horizons (Monthly, Yearly, Daily).
2. **MoM & YoY Comparisons**: Computes Month-over-Month growth rates and Year-over-Year percentage changes to detect seasonal spikes.
3. **Geospatial Hotspot Detection**: Maps spatial incident densities using Kernel Density Estimation (KDE) and OpenStreetMap coordinate overlays.
4. **Category & Frequency Distribution**: Evaluates crime severity metrics, emergency response efficiency, and day-vs-hour intensity heatmaps.
5. **Location Risk Scoring Engine**: Calculates normalized multi-factor composite risk scores (0–100 scale) per district based on incident volume, average severity, and 90-day recency.
6. **Automated Insights**: Generates automated data-driven observations summarizing key findings.
7. **Interactive Dashboard**: Full-featured multi-tab Streamlit dashboard (`app.py`).

---

## 📁 Repository Structure

```
Crime_Analytics/
├── 📄 Crime_Analytics.ipynb     # Jupyter Notebook with full step-by-step EDA & workflow
├── 📄 app.py                    # Interactive Streamlit dashboard UI
├── 📄 crime_analytics.py        # Core analytics, hotspot detector, risk scorer, and insight functions
├── 📄 crime_dataset.csv         # Multi-year synthetic crime dataset (2,500+ records)
├── 📄 generate_data.py          # Dataset generator script
├── 📄 test_crime_analytics.py   # Unit test suite verifying logic & metrics
└── 📄 README.md                 # Project documentation
```

---

## 📊 Dataset Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| `incident_id` | String | Unique identifier for each crime incident |
| `timestamp` | Datetime | Date and time of incident occurrence |
| `year` / `month` | Integer | Year and Month extraction |
| `day_of_week` / `hour`| String / Int | Day of week and hour of day (0-23) |
| `district` | String | Geographic area / district code |
| `latitude` / `longitude` | Float | GPS location coordinates |
| `crime_type` | String | Category (e.g. Theft, Burglary, Robbery, Assault) |
| `severity_score` | Integer | Crime severity rating (Scale 1-10) |
| `location_type` | String | Commercial, Street, Residence, Parking Lot, etc. |
| `status` | String | Case resolution status (Solved, Under Investigation, etc.) |
| `response_time_min` | Integer | Emergency response time in minutes |

---

## 🧮 Mathematical & Risk Scoring Formulation

The composite location risk index $R_d \in [0, 100]$ for district $d$ is formulated as a weighted linear combination of normalized metrics:

$$R_d = 100 \times \left( w_{\text{vol}} \cdot \tilde{V}_d + w_{\text{sev}} \cdot \tilde{S}_d + w_{\text{rec}} \cdot \tilde{C}_d \right)$$

Where:
- $\tilde{V}_d$: Min-Max normalized total incident volume in district $d$.
- $\tilde{S}_d$: Min-Max normalized average severity score in district $d$.
- $\tilde{C}_d$: Min-Max normalized 90-day recent incident count in district $d$.
- Weights satisfy $w_{\text{vol}} + w_{\text{sev}} + w_{\text{rec}} = 1.0$ (Default: $0.4, 0.3, 0.3$).

---

## 🛠️ How to Run

### 1. Run Interactive Streamlit Dashboard
```bash
streamlit run app.py
```

### 2. Run Jupyter Notebook
```bash
jupyter notebook Crime_Analytics.ipynb
```

### 3. Run Automated Unit Tests
```bash
python test_crime_analytics.py
```

---

## 👤 Author & Contribution
Contributed to **ML-CaPsule** as part of GSSoC 2026.
