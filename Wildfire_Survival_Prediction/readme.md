# Wildfire Survival Prediction

## Overview
Predicts wildfire evacuation survival probabilities at 12, 24, 48, and 72-hour horizons using right-censored survival data (event start/end times, wind-fire alignment, terrain features).

## Problem Type
Survival analysis (time-to-event modeling) with right-censored data — not a standard classification problem.

## Project Structure
Wildfire_Survival_Prediction/
├── data/           # raw and processed datasets (not committed if large — see .gitignore)
├── notebooks/       # EDA and experimentation notebooks
├── src/            # reusable Python modules (data prep, models, evaluation)
├── requirements.txt
└── readme.md
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