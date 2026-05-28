# 🏏 Batter vs Bowler Analytics — IPL Player Matchup Intelligence

> An extension to the [IPL Cricket Match Win Prediction](../) project.  
> Adds **player-level dismissal probability prediction** and matchup analytics using LightGBM.

---

## Overview

While the parent project predicts overall match win probability, this module drills down to
**individual batter–bowler matchups** — answering questions like:

- *How likely is Bumrah to dismiss Kohli on the 16th over?*
- *Which bowlers pose the highest threat to a given batter?*
- *What does the historical head-to-head record look like?*

---

## Features

| Feature | Description |
|---|---|
| **Head-to-Head Stats** | Balls, runs, SR, dot ball %, boundaries, dismissal rate |
| **Dismissal Probability** | LightGBM model predicts per-ball P(wicket) |
| **Top Threat Chart** | Ranks bowlers by dismissal rate vs a batter |
| **Top Matchups Table** | All pairs sorted by historical dismissal rate |
| **Streamlit Frontend** | Interactive app with tabs, charts, and prediction UI |
| **Evaluation Plots** | Confusion matrix, ROC curve, feature importance |

---

## Files

```
Batter vs Bowler Analytics/
├── batter_vs_bowler_analytics.py   # Core module (data, features, model, plots)
├── app.py                          # Streamlit frontend
├── Batter_vs_Bowler_Analytics.ipynb  # Jupyter notebook walkthrough
└── README.md                       # This file
```

---

## Dataset

Uses the standard **Cricsheet** ball-by-ball IPL CSV format.

Download: https://cricsheet.org/downloads/ipl_csv2.zip  
Extract `deliveries.csv` and place it in this folder.

Expected columns (among others):
```
match_id, inning, batting_team, bowling_team, over, ball,
batter, bowler, batsman_runs, extra_runs, total_runs,
is_wicket, player_dismissed, dismissal_kind
```

---

## Installation

```bash
pip install lightgbm scikit-learn pandas numpy matplotlib seaborn streamlit
```

---

## Usage

### Run the Streamlit App
```bash
streamlit run app.py
```

### Run the Python Module Directly
```bash
python batter_vs_bowler_analytics.py
```
> Edit `DATA_PATH`, `BATTER`, and `BOWLER` at the bottom of the file before running.

### Jupyter Notebook
Open `Batter_vs_Bowler_Analytics.ipynb` in Jupyter or VS Code and run all cells.

---

## Model Details

**Algorithm:** `LGBMClassifier` (same framework as the parent project)

**Features:**

| Feature | Description |
|---|---|
| `batter_career_sr` | Batter's overall IPL strike rate |
| `batter_career_avg` | Batter's overall IPL average |
| `bowler_career_econ` | Bowler's career economy rate |
| `bowler_career_wkt_rate` | Bowler's wickets per ball |
| `h2h_sr` | Batter's SR specifically vs this bowler |
| `h2h_dismissal_rate` | Historical dismissal rate in this matchup |
| `h2h_balls` | Sample size for the matchup |
| `over` | Current over number (1–20) |
| `phase_encoded` | Powerplay=0, Middle=1, Death=2 |

**Typical Performance:**
- Accuracy: ~93% (class-imbalanced; dismissals are ~7% of balls)
- ROC-AUC: 0.68–0.74

---

## Example Output

```
V Kohli  vs  SL Malinga — Head-to-Head Stats
balls_faced              : 42
runs_scored              : 38
dismissals               : 4
strike_rate              : 90.48
dismissal_rate           : 0.0952
dot_ball_pct             : 42.86%
boundary_count           : 7

Dismissal probability (over 15, death):  18.4%
```

---

## Visualizations

- `matchup_summary.png` — Bar charts of scoring & dismissal patterns
- `top_threats.png`     — Ranked bowler threat chart for a batter
- `confusion_matrix.png` — Model evaluation
- `roc_curve.png`        — ROC curve with AUC score
- `feature_importance.png` — LGBM feature importances

---

## Contribution

This feature was added as part of a PR to enhance the ML-CaPsule IPL project with
deeper player analytics. The issue proposed adding batter vs bowler matchup statistics
and dismissal probability prediction using ML, making the project more interactive
and informative for fans, analysts, and developers.
