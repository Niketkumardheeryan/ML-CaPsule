# Automated Data Validation Pipeline

This module adds a reusable data-integrity checkpoint to tabular machine-learning workflows in ML-CaPsule.

## Purpose

Machine-learning pipelines may continue running even when an upstream dataset changes unexpectedly. Missing columns, changed data types, excessive null values, duplicate records, and invalid numeric ranges can cause failures or silently produce unreliable models.

The validator creates a gate between data ingestion and model training:

~~~text
Incoming dataset
       |
       v
Schema and integrity validation
       |
       +---- FAIL ---> Stop pipeline and inspect report
       |
       +---- PASS ---> Continue preprocessing and training
~~~

## Validation checks

The framework supports:

- Required-column validation
- Unexpected-column detection
- Configurable column-order validation
- Pandas datatype checks
- Minimum and maximum row counts
- Duplicate-row percentage limits
- Maximum null percentage per column
- Numeric parsing-quality checks
- Numeric minimum and maximum ranges
- Unique-value count constraints
- Great Expectations validation suites

## Outputs

The validator produces:

- Human-readable PASS/FAIL console output
- Machine-readable JSON reports
- Exit code `0` when validation passes
- Exit code `1` when validation fails
- Exit code `2` when validation cannot execute

## Project structure

~~~text
automated_data_validation_pipeline/
|-- .gitignore
|-- __init__.py
|-- data_validator.py
|-- README.md
|-- requirements.txt
|-- configs/
|   `-- constellation_schema.json
|-- examples/
|   `-- demo_validation.py
|-- reports/
|   `-- .gitignore
`-- tests/
    |-- __init__.py
    `-- test_data_validator.py
~~~

## Installation

From the repository root:

~~~powershell
python -m pip install -r MLOps_Learning_Module\automated_data_validation_pipeline\requirements.txt
~~~

## Command-line usage

~~~powershell
python MLOps_Learning_Module\automated_data_validation_pipeline\data_validator.py `
  --data Constellation_Classification\constellations.csv `
  --config MLOps_Learning_Module\automated_data_validation_pipeline\configs\constellation_schema.json `
  --report MLOps_Learning_Module\automated_data_validation_pipeline\reports\constellation_validation.json
~~~

## Python usage

~~~python
from data_validator import DataValidator

validator = DataValidator.from_json(
    "configs/constellation_schema.json"
)

report = validator.validate_dataframe(
    dataframe=df_raw,
    source_name="constellations.csv",
    report_path="reports/validation.json",
    raise_on_failure=True,
)
~~~

Using `raise_on_failure=True` prevents preprocessing and model training from beginning when any configured validation check fails.

## Constellation dataset integration

The constellation dataset contains 14 raw string-like columns. Some fields representing numerical values contain Unicode minus signs, approximation symbols, ranges, and uncertainty annotations.

The validator therefore:

1. Validates the original raw schema.
2. Creates an internal validation-only copy.
3. Parses configured numeric fields.
4. Measures numeric-conversion failures.
5. Applies numeric range expectations.
6. Leaves the source DataFrame unchanged.
7. Allows training to continue only after validation succeeds.

## PASS/FAIL demonstration

~~~powershell
python MLOps_Learning_Module\automated_data_validation_pipeline\examples\demo_validation.py
~~~

The demonstration first validates the original constellation dataset and produces a PASS report. It then validates an intentionally damaged in-memory copy and produces a FAIL report, proving that invalid data blocks model training.

## Running tests

~~~powershell
python -m pytest MLOps_Learning_Module\automated_data_validation_pipeline\tests -v
~~~

The automated tests cover:

- Valid input data
- Missing required columns
- Excessive null values
- Out-of-range numeric values
- Incorrect datatypes
- Duplicate rows
- Pipeline interruption after validation failure

## Exit codes

| Exit code | Meaning |
|---|---|
| `0` | Validation completed successfully and all checks passed |
| `1` | Validation completed, but one or more checks failed |
| `2` | Validation could not run because of a configuration or execution error |

## Generated reports

Runtime JSON reports are written inside the `reports` directory. These reports are excluded from Git because they contain generated timestamps and are recreated whenever validation runs.

## MLOps benefit

Adding validation before preprocessing provides an early warning when the input dataset changes. This prevents invalid data from silently entering feature engineering, train-test splitting, model fitting, evaluation, or deployment workflows.