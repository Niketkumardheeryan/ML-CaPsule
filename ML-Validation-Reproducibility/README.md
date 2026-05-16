# ML Validation & Reproducibility Framework

A lightweight and reusable machine learning utility framework focused on improving data validation, evaluation consistency, and experiment reproducibility across ML pipelines.

## Features

- Data validation utilities
- Missing value detection
- Duplicate data checking
- Schema validation
- Reproducibility utilities with fixed random seeds
- Evaluation metrics for ML models
- Modular and reusable architecture
- Example demo pipeline included

## Project Structure

ML-Validation-Reproducibility/
│
├── examples/
│   └── demo_pipeline.py
│
├── ml_utils/
│   ├── __init__.py
│   ├── ml_data_validators.py
│   ├── ml_metrics.py
│   └── ml_reproducibility.py
│
├── sample_data/
│   └── sample_dataset.csv
│
├── requirements.txt
└── README.md

## Modules

### ml_data_validators.py
Contains utilities for:
- Missing value detection
- Duplicate row validation
- Schema checking

### ml_metrics.py
Provides:
- Accuracy
- Precision
- Recall
- F1-score

### ml_reproducibility.py
Handles:
- Random seed fixing
- Environment information collection

## Demo Pipeline

Run the example pipeline:

```bash
python examples/demo_pipeline.py