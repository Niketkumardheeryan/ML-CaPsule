# IPL 2026 Player Tier Classification

![Python](https://img.shields.io/badge/Python-3.x-blue) ![ML](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green) ![Accuracy](https://img.shields.io/badge/Accuracy-97%25-brightgreen)

## Overview
This project classifies IPL 2026 batsmen and bowlers into performance tiers (Elite, Good, Average) using Random Forest Classifier. It also computes an All-rounder Score by combining batting and bowling statistics.

## Dataset
- **Source:** [IPL 2026 Season Stats - Batting & Bowling](https://www.kaggle.com/datasets/wisdomsiddharth/ipl-2026-season-stats-batting-and-bowling) (Kaggle)
- **Batting Dataset:** 167 players
- **Bowling Dataset:** 104 players
- **Season:** 2026
- **Source Website:** iplt20.com

## Models
| Model | Algorithm | Accuracy |
|---|---|---|
| Batting Tier Classifier | Random Forest | 97% |
| Bowling Tier Classifier | Random Forest | 95% |

## Tier Labels
**Batting:**
- Elite: 500+ runs
- Good: 300-499 runs
- Average: <300 runs

**Bowling:**
- Elite: 20+ wickets
- Good: 12-19 wickets
- Average: <12 wickets

## Features Used
**Batting:** runs, matches, innings, average, strike rate, 4s, 6s, 50s, 100s

**Bowling:** wickets, matches, innings, average, economy, strike rate, 4-wicket hauls, 5-wicket hauls

## Key Insights
- Vaibhav Sooryavanshi is the top run scorer with 776 runs
- Kagiso Rabada is the top wicket taker with 29 wickets
- Most important batting feature: Runs (39.6%)
- Most important bowling feature: Wickets (42.8%)

## Files
- `ipl_player_tier_classification.ipynb` — Main notebook
- `ipl_2026_batting.csv` — Batting dataset
- `ipl_2026_bowling.csv` — Bowling dataset

## How to Run
```bash
pip install pandas numpy scikit-learn matplotlib
jupyter notebook ipl_player_tier_classification.ipynb
```

[<img height="30" src="https://img.shields.io/badge/linkedin-blue.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />][LinkedIn]
[<img height="30" src="https://img.shields.io/badge/github-black.svg?&style=for-the-badge&logo=github&logoColor=white" />][Github]

[linkedin]: https://www.linkedin.com/in/siddharthmac/
[github]: https://github.com/SiddharthRiot/