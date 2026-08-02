"""Demonstrate successful and failed dataset validation."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PIPELINE_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PIPELINE_DIR.parents[1]

if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from data_validator import DataValidator


def main() -> None:
    config_path = (
        PIPELINE_DIR
        / "configs"
        / "constellation_schema.json"
    )

    dataset_path = (
        REPOSITORY_ROOT
        / "Constellation_Classification"
        / "constellations.csv"
    )

    reports_directory = PIPELINE_DIR / "reports"
    reports_directory.mkdir(parents=True, exist_ok=True)

    validator = DataValidator.from_json(config_path)
    dataframe = pd.read_csv(dataset_path)

    print("\nPASS DEMONSTRATION")
    print("-" * 72)

    pass_report = validator.validate_dataframe(
        dataframe=dataframe,
        source_name=str(dataset_path),
        report_path=reports_directory / "demo_validation_pass.json",
    )

    if not pass_report["success"]:
        raise RuntimeError(
            "The original constellation dataset unexpectedly failed."
        )

    invalid_dataframe = dataframe.drop(
        columns=["Constellation"]
    ).copy()

    invalid_dataframe.loc[
        invalid_dataframe.index[0],
        "Visual Magnitude",
    ] = "99"

    print("\nFAIL DEMONSTRATION")
    print("-" * 72)

    fail_report = validator.validate_dataframe(
        dataframe=invalid_dataframe,
        source_name="intentionally_broken_constellations",
        report_path=reports_directory / "demo_validation_fail.json",
    )

    if fail_report["success"]:
        raise RuntimeError(
            "The intentionally damaged dataset unexpectedly passed."
        )

    print(
        "\nTraining blocked because the input dataset "
        "failed validation."
    )


if __name__ == "__main__":
    main()