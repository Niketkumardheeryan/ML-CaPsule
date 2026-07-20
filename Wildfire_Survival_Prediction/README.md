# Wildfire Survival Prediction

## Overview
Predicts wildfire evacuation survival probabilities at 12, 24, 48, and 72-hour horizons using right-censored survival data (event start/end times, wind-fire alignment, terrain features).

## Problem Type
Survival analysis (time-to-event modeling) with right-censored data — not a standard classification problem.

## Project Structure
Wildfire_Survival_Prediction/
├── data/           # raw and processed datasets (not committed if large — see .gitignore)
├── notebooks/       # EDA and experimentation notebooks
├── requirements.txt
└── README.md
## Workflow
1. **EDA** — explore censoring patterns, event timing, terrain/wind features
2. **Baseline survival models** — Kaplan-Meier, Cox Proportional Hazards
3. **ML survival models** — e.g. Random Survival Forests, gradient-boosted survival models
4. **Calibration** — check predicted probabilities at each horizon against observed outcomes
5. **Ensembling** — combine models for final horizon-specific predictions

## Status
🚧 In progress — starter structure only, work-in-progress.

## References
- Inspired by the WiDS 2026 Global Datathon (Kaggle).

## Dataset

This project uses data from the [WiDS Global Datathon 2026](https://www.kaggle.com/competitions/WiDSWorldWide_GlobalDathon26) — "Predicting Time-to-Threat for Evacuation Zones Using Survival Analysis," in collaboration with Watch Duty.

- **Rows:** 221 training wildfires, 95 test wildfires
- **Features:** 34 features derived from the first 5 hours after ignition (fire growth, spread rate, wind-fire alignment, distance to evacuation zones, timing)
- **Target:** `time_to_hit_hours` (time until the fire threatens an evacuation zone) and `event` (1 = observed, 0 = right-censored)
- **Goal:** predict the probability a wildfire threatens an evacuation zone within 12, 24, 48, and 72 hours

**To use it:**
1. Join the competition on Kaggle and accept the rules: https://www.kaggle.com/competitions/WiDSWorldWide_GlobalDathon26
2. Download `train.csv`, `test.csv`, and `metaData.csv`
3. Place them in `Wildfire_Survival_Prediction/data/`
4. Run the notebooks in `notebooks/`