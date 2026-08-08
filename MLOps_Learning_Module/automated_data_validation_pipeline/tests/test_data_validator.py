"""Tests for the automated data-validation pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

PIPELINE_DIR = Path(__file__).resolve().parents[1]

if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from data_validator import DataValidationError, DataValidator


@pytest.fixture
def validation_config() -> dict:
    return {
        "name": "test_dataset_schema",
        "strict_column_order": True,
        "allow_extra_columns": False,
        "required_columns": [
            "category",
            "amount",
            "comment",
        ],
        "row_count": {
            "min": 2,
            "max": 10,
        },
        "max_duplicate_percentage": 0.0,
        "columns": {
            "category": {
                "allowed_dtypes": ["object", "string"],
                "max_null_percentage": 0.0,
            },
            "amount": {
                "allowed_dtypes": [
                    "integer",
                    "float",
                    "numeric",
                ],
                "max_null_percentage": 0.0,
            },
            "comment": {
                "allowed_dtypes": ["object", "string"],
                "max_null_percentage": 50.0,
            },
        },
        "numeric_checks": {
            "amount": {
                "min": 0.0,
                "max": 100.0,
                "max_parse_failure_percentage": 0.0,
                "max_out_of_range_percentage": 0.0,
            }
        },
        "unique_count_checks": {
            "category": {
                "min": 1,
                "max": 5,
            }
        },
    }


@pytest.fixture
def valid_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "category": ["A", "B", "C"],
            "amount": [10, 20, 30],
            "comment": ["valid", None, "also valid"],
        }
    )


def test_valid_dataframe_passes(
    validation_config: dict,
    valid_dataframe: pd.DataFrame,
) -> None:
    validator = DataValidator(validation_config)

    report = validator.validate_dataframe(
        valid_dataframe,
        display_report=False,
    )

    assert report["success"] is True
    assert report["status"] == "PASS"
    assert report["summary"]["native_failed"] == 0
    assert report["summary"]["gx_failed"] == 0


def test_missing_required_column_fails(
    validation_config: dict,
    valid_dataframe: pd.DataFrame,
) -> None:
    validator = DataValidator(validation_config)
    invalid_dataframe = valid_dataframe.drop(columns=["category"])

    report = validator.validate_dataframe(
        invalid_dataframe,
        display_report=False,
    )

    assert report["success"] is False

    required_check = next(
        check
        for check in report["native_checks"]
        if check["name"] == "required_columns"
    )

    assert required_check["success"] is False
    assert "category" in required_check["observed"]


def test_excessive_null_percentage_fails(
    validation_config: dict,
    valid_dataframe: pd.DataFrame,
) -> None:
    validator = DataValidator(validation_config)
    invalid_dataframe = valid_dataframe.copy()
    invalid_dataframe.loc[0, "category"] = None

    report = validator.validate_dataframe(
        invalid_dataframe,
        display_report=False,
    )

    assert report["success"] is False
    assert report["summary"]["gx_failed"] >= 1


def test_out_of_range_numeric_value_fails(
    validation_config: dict,
    valid_dataframe: pd.DataFrame,
) -> None:
    validator = DataValidator(validation_config)
    invalid_dataframe = valid_dataframe.copy()
    invalid_dataframe.loc[0, "amount"] = 150

    report = validator.validate_dataframe(
        invalid_dataframe,
        display_report=False,
    )

    assert report["success"] is False
    assert report["summary"]["gx_failed"] >= 1


def test_incorrect_dtype_fails(
    validation_config: dict,
    valid_dataframe: pd.DataFrame,
) -> None:
    validator = DataValidator(validation_config)
    invalid_dataframe = valid_dataframe.copy()
    invalid_dataframe["category"] = [1, 2, 3]

    report = validator.validate_dataframe(
        invalid_dataframe,
        display_report=False,
    )

    dtype_check = next(
        check
        for check in report["native_checks"]
        if check["name"] == "dtype::category"
    )

    assert report["success"] is False
    assert dtype_check["success"] is False


def test_duplicate_rows_fail(
    validation_config: dict,
    valid_dataframe: pd.DataFrame,
) -> None:
    validator = DataValidator(validation_config)

    invalid_dataframe = pd.concat(
        [
            valid_dataframe,
            valid_dataframe.iloc[[0]],
        ],
        ignore_index=True,
    )

    report = validator.validate_dataframe(
        invalid_dataframe,
        display_report=False,
    )

    duplicate_check = next(
        check
        for check in report["native_checks"]
        if check["name"] == "duplicate_rows"
    )

    assert report["success"] is False
    assert duplicate_check["success"] is False
    assert duplicate_check["observed"]["count"] == 1


def test_raise_on_failure_blocks_pipeline(
    validation_config: dict,
    valid_dataframe: pd.DataFrame,
) -> None:
    validator = DataValidator(validation_config)
    invalid_dataframe = valid_dataframe.drop(columns=["category"])

    with pytest.raises(DataValidationError):
        validator.validate_dataframe(
            invalid_dataframe,
            display_report=False,
            raise_on_failure=True,
        )