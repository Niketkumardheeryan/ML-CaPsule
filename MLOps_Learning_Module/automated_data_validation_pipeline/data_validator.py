"""Reusable dataset validation pipeline powered by Great Expectations."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import great_expectations as gx
import pandas as pd
from pandas.api import types as pandas_types


class DataValidationError(RuntimeError):
    """Raised when a dataset fails one or more validation checks."""

    def __init__(self, report: dict[str, Any]) -> None:
        self.report = report
        super().__init__(
            f"Dataset validation failed for {report.get('source', 'unknown source')}."
        )


class DataValidator:
    """Validate pandas DataFrames and CSV files against a JSON schema."""

    _NUMERIC_PATTERN = re.compile(
        r"^\s*[~≈<>]?\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))"
    )

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    @classmethod
    def from_json(cls, config_path: str | Path) -> "DataValidator":
        """Build a validator from a JSON configuration file."""
        path = Path(config_path)

        with path.open("r", encoding="utf-8-sig") as file:
            config = json.load(file)

        return cls(config)

    @staticmethod
    def _check(
        name: str,
        success: bool,
        observed: Any,
        expected: Any,
        details: str,
    ) -> dict[str, Any]:
        return {
            "name": name,
            "success": bool(success),
            "observed": observed,
            "expected": expected,
            "details": details,
        }

    @staticmethod
    def _dtype_matches(series: pd.Series, allowed_types: list[str]) -> bool:
        allowed = {str(value).lower() for value in allowed_types}
        actual = str(series.dtype).lower()

        if actual in allowed:
            return True

        if "object" in allowed and pandas_types.is_object_dtype(series.dtype):
            return True

        if "string" in allowed and (
            pandas_types.is_string_dtype(series.dtype)
            or pandas_types.is_object_dtype(series.dtype)
        ):
            return True

        if (
            {"numeric", "number"} & allowed
            and pandas_types.is_numeric_dtype(series.dtype)
        ):
            return True

        if "integer" in allowed and pandas_types.is_integer_dtype(series.dtype):
            return True

        if "float" in allowed and pandas_types.is_float_dtype(series.dtype):
            return True

        if "boolean" in allowed and pandas_types.is_bool_dtype(series.dtype):
            return True

        if "datetime" in allowed and pandas_types.is_datetime64_any_dtype(
            series.dtype
        ):
            return True

        return False

    @classmethod
    def _parse_numeric(cls, series: pd.Series) -> pd.Series:
        """Extract the leading numeric value without changing source data."""
        cleaned = (
            series.astype("string")
            .str.strip()
            .str.replace("−", "-", regex=False)
            .str.replace("–", "-", regex=False)
            .str.replace("—", "-", regex=False)
            .str.replace(",", "", regex=False)
        )

        extracted = cleaned.str.extract(
            cls._NUMERIC_PATTERN,
            expand=False,
        )

        return pd.to_numeric(extracted, errors="coerce")

    def _run_native_checks(
        self,
        dataframe: pd.DataFrame,
    ) -> tuple[list[dict[str, Any]], pd.DataFrame]:
        checks: list[dict[str, Any]] = []
        validation_frame = dataframe.copy()

        required_columns = self.config.get("required_columns", [])
        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        checks.append(
            self._check(
                name="required_columns",
                success=not missing_columns,
                observed=missing_columns,
                expected="No required columns missing",
                details=(
                    "All required columns are present."
                    if not missing_columns
                    else f"Missing columns: {missing_columns}"
                ),
            )
        )

        allow_extra = bool(self.config.get("allow_extra_columns", True))
        extra_columns = [
            column
            for column in dataframe.columns
            if column not in required_columns
        ]

        checks.append(
            self._check(
                name="unexpected_columns",
                success=allow_extra or not extra_columns,
                observed=extra_columns,
                expected=(
                    "Additional columns allowed"
                    if allow_extra
                    else "No additional columns"
                ),
                details=(
                    "No unexpected columns found."
                    if not extra_columns
                    else f"Unexpected columns: {extra_columns}"
                ),
            )
        )

        checks.append(
            self._check(
                name="dataset_not_empty",
                success=not dataframe.empty,
                observed=int(len(dataframe)),
                expected="At least one row",
                details=f"Dataset contains {len(dataframe)} rows.",
            )
        )

        max_duplicate_percentage = float(
            self.config.get("max_duplicate_percentage", 100.0)
        )

        duplicate_count = int(dataframe.duplicated().sum())
        duplicate_percentage = (
            duplicate_count / len(dataframe) * 100
            if len(dataframe)
            else 0.0
        )

        checks.append(
            self._check(
                name="duplicate_rows",
                success=duplicate_percentage <= max_duplicate_percentage,
                observed={
                    "count": duplicate_count,
                    "percentage": round(duplicate_percentage, 4),
                },
                expected={
                    "maximum_percentage": max_duplicate_percentage,
                },
                details=(
                    f"Found {duplicate_count} duplicate rows "
                    f"({duplicate_percentage:.4f}%)."
                ),
            )
        )

        column_rules = self.config.get("columns", {})

        for column, rule in column_rules.items():
            if column not in dataframe.columns:
                continue

            allowed_types = rule.get("allowed_dtypes", [])

            if allowed_types:
                actual_dtype = str(dataframe[column].dtype)
                dtype_success = self._dtype_matches(
                    dataframe[column],
                    allowed_types,
                )

                checks.append(
                    self._check(
                        name=f"dtype::{column}",
                        success=dtype_success,
                        observed=actual_dtype,
                        expected=allowed_types,
                        details=(
                            f"{column} has dtype {actual_dtype}; "
                            f"allowed types are {allowed_types}."
                        ),
                    )
                )

        numeric_rules = self.config.get("numeric_checks", {})

        for column, rule in numeric_rules.items():
            if column not in dataframe.columns:
                continue

            parsed = self._parse_numeric(dataframe[column])
            validation_frame[column] = parsed

            original_non_null = int(dataframe[column].notna().sum())
            parsed_non_null = int(parsed.notna().sum())
            parse_failures = max(
                original_non_null - parsed_non_null,
                0,
            )

            parse_failure_percentage = (
                parse_failures / original_non_null * 100
                if original_non_null
                else 0.0
            )

            maximum_failure = float(
                rule.get("max_parse_failure_percentage", 0.0)
            )

            checks.append(
                self._check(
                    name=f"numeric_parsing::{column}",
                    success=parse_failure_percentage <= maximum_failure,
                    observed={
                        "failed_values": parse_failures,
                        "failure_percentage": round(
                            parse_failure_percentage,
                            4,
                        ),
                    },
                    expected={
                        "maximum_failure_percentage": maximum_failure,
                    },
                    details=(
                        f"Parsed {parsed_non_null} of "
                        f"{original_non_null} non-null values in {column}."
                    ),
                )
            )

        unique_rules = self.config.get("unique_count_checks", {})

        for column, rule in unique_rules.items():
            if column not in dataframe.columns:
                continue

            unique_count = int(dataframe[column].nunique(dropna=True))
            minimum = rule.get("min")
            maximum = rule.get("max")

            minimum_ok = minimum is None or unique_count >= minimum
            maximum_ok = maximum is None or unique_count <= maximum

            checks.append(
                self._check(
                    name=f"unique_count::{column}",
                    success=minimum_ok and maximum_ok,
                    observed=unique_count,
                    expected={
                        "min": minimum,
                        "max": maximum,
                    },
                    details=(
                        f"{column} contains {unique_count} unique "
                        "non-null values."
                    ),
                )
            )

        return checks, validation_frame

    def _run_great_expectations(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, Any]:
        token = uuid.uuid4().hex[:10]

        context = gx.get_context(mode="ephemeral")

        data_source = context.data_sources.add_pandas(
            name=f"validation_source_{token}"
        )

        data_asset = data_source.add_dataframe_asset(
            name=f"validation_asset_{token}"
        )

        batch_definition = data_asset.add_batch_definition_whole_dataframe(
            name=f"validation_batch_{token}"
        )

        batch = batch_definition.get_batch(
            batch_parameters={"dataframe": dataframe}
        )

        suite = context.suites.add(
            gx.ExpectationSuite(
                name=f"{self.config.get('name', 'dataset')}_{token}"
            )
        )

        required_columns = self.config.get("required_columns", [])
        strict_order = bool(
            self.config.get("strict_column_order", False)
        )
        allow_extra = bool(
            self.config.get("allow_extra_columns", True)
        )

        if strict_order:
            suite.add_expectation(
                gx.expectations.ExpectTableColumnsToMatchOrderedList(
                    column_list=required_columns
                )
            )
        else:
            suite.add_expectation(
                gx.expectations.ExpectTableColumnsToMatchSet(
                    column_set=required_columns,
                    exact_match=not allow_extra,
                )
            )

        row_rule = self.config.get("row_count", {})

        suite.add_expectation(
            gx.expectations.ExpectTableRowCountToBeBetween(
                min_value=row_rule.get("min", 1),
                max_value=row_rule.get("max"),
            )
        )

        column_rules = self.config.get("columns", {})

        for column, rule in column_rules.items():
            if column not in dataframe.columns:
                continue

            max_null_percentage = float(
                rule.get("max_null_percentage", 100.0)
            )

            if max_null_percentage < 100:
                mostly = max(
                    0.0,
                    1.0 - max_null_percentage / 100.0,
                )

                suite.add_expectation(
                    gx.expectations.ExpectColumnValuesToNotBeNull(
                        column=column,
                        mostly=mostly,
                    )
                )

        numeric_rules = self.config.get("numeric_checks", {})

        for column, rule in numeric_rules.items():
            if column not in dataframe.columns:
                continue

            allowed_out_of_range = float(
                rule.get(
                    "max_out_of_range_percentage",
                    0.0,
                )
            )

            suite.add_expectation(
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column=column,
                    min_value=rule.get("min"),
                    max_value=rule.get("max"),
                    mostly=max(
                        0.0,
                        1.0 - allowed_out_of_range / 100.0,
                    ),
                )
            )

        validation_result = batch.validate(suite)

        if hasattr(validation_result, "to_json_dict"):
            raw_result = validation_result.to_json_dict()
        else:
            raw_result = dict(validation_result)

        checks: list[dict[str, Any]] = []

        for result in raw_result.get("results", []):
            expectation_config = result.get(
                "expectation_config",
                {},
            )

            expectation_type = (
                expectation_config.get("type")
                or expectation_config.get("expectation_type")
                or "unknown_expectation"
            )

            kwargs = expectation_config.get("kwargs", {})
            result_details = result.get("result", {})

            checks.append(
                {
                    "name": expectation_type,
                    "column": kwargs.get("column"),
                    "success": bool(result.get("success", False)),
                    "observed_value": result_details.get(
                        "observed_value"
                    ),
                    "unexpected_count": result_details.get(
                        "unexpected_count"
                    ),
                    "unexpected_percent": result_details.get(
                        "unexpected_percent"
                    ),
                    "partial_unexpected_list": result_details.get(
                        "partial_unexpected_list",
                        [],
                    ),
                }
            )

        return {
            "success": bool(raw_result.get("success", False)),
            "statistics": raw_result.get("statistics", {}),
            "checks": checks,
        }

    @staticmethod
    def _write_report(
        report: dict[str, Any],
        report_path: str | Path,
    ) -> None:
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                report,
                file,
                indent=2,
                ensure_ascii=False,
                default=str,
            )

    @staticmethod
    def print_report(report: dict[str, Any]) -> None:
        separator = "=" * 72

        print(separator)
        print("AUTOMATED DATA VALIDATION REPORT")
        print(separator)
        print(f"Source: {report['source']}")
        print(f"Rows: {report['dataset']['rows']}")
        print(f"Columns: {report['dataset']['columns']}")
        print(f"Status: {report['status']}")
        print(
            "Native checks: "
            f"{report['summary']['native_passed']}/"
            f"{report['summary']['native_total']} passed"
        )
        print(
            "Great Expectations checks: "
            f"{report['summary']['gx_passed']}/"
            f"{report['summary']['gx_total']} passed"
        )

        failures = [
            check
            for check in report["native_checks"]
            if not check["success"]
        ]

        failures.extend(
            check
            for check in report["great_expectations"]["checks"]
            if not check["success"]
        )

        if failures:
            print("\nFailed checks:")

            for check in failures:
                column = check.get("column")
                label = check.get("name", "unknown")

                if column:
                    label = f"{label} [{column}]"

                details = (
                    check.get("details")
                    or check.get("observed_value")
                    or check.get("partial_unexpected_list")
                    or "See JSON report"
                )

                print(f"  - {label}: {details}")
        else:
            print("\nAll configured validation checks passed.")

        print(separator)

    def validate_dataframe(
        self,
        dataframe: pd.DataFrame,
        source_name: str = "dataframe",
        report_path: str | Path | None = None,
        raise_on_failure: bool = False,
        display_report: bool = True,
    ) -> dict[str, Any]:
        """Validate a pandas DataFrame and return a structured report."""
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("dataframe must be a pandas DataFrame")

        native_checks, validation_frame = self._run_native_checks(
            dataframe
        )

        gx_report = self._run_great_expectations(
            validation_frame
        )

        native_passed = sum(
            1 for check in native_checks if check["success"]
        )

        gx_checks = gx_report["checks"]
        gx_passed = sum(
            1 for check in gx_checks if check["success"]
        )

        native_success = native_passed == len(native_checks)
        overall_success = native_success and gx_report["success"]

        report = {
            "schema": self.config.get("name", "unnamed_schema"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": source_name,
            "status": "PASS" if overall_success else "FAIL",
            "success": overall_success,
            "dataset": {
                "rows": int(dataframe.shape[0]),
                "columns": int(dataframe.shape[1]),
                "column_names": dataframe.columns.tolist(),
            },
            "summary": {
                "native_total": len(native_checks),
                "native_passed": native_passed,
                "native_failed": len(native_checks) - native_passed,
                "gx_total": len(gx_checks),
                "gx_passed": gx_passed,
                "gx_failed": len(gx_checks) - gx_passed,
            },
            "native_checks": native_checks,
            "great_expectations": gx_report,
        }

        if report_path is not None:
            self._write_report(report, report_path)

        if display_report:
            self.print_report(report)

        if raise_on_failure and not overall_success:
            raise DataValidationError(report)

        return report

    def validate_csv(
        self,
        csv_path: str | Path,
        report_path: str | Path | None = None,
        raise_on_failure: bool = False,
        display_report: bool = True,
        **read_csv_kwargs: Any,
    ) -> dict[str, Any]:
        """Read and validate a CSV dataset."""
        path = Path(csv_path)

        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        dataframe = pd.read_csv(path, **read_csv_kwargs)

        return self.validate_dataframe(
            dataframe=dataframe,
            source_name=str(path),
            report_path=report_path,
            raise_on_failure=raise_on_failure,
            display_report=display_report,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a CSV dataset using native schema checks "
            "and Great Expectations."
        )
    )

    parser.add_argument(
        "--data",
        required=True,
        help="Path to the CSV dataset.",
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the JSON validation configuration.",
    )

    parser.add_argument(
        "--report",
        help="Optional output path for the JSON report.",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Do not print the human-readable report.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    arguments = parser.parse_args()

    try:
        validator = DataValidator.from_json(arguments.config)

        report = validator.validate_csv(
            csv_path=arguments.data,
            report_path=arguments.report,
            display_report=not arguments.quiet,
        )

        return 0 if report["success"] else 1

    except Exception as error:
        print(
            f"Validation could not be completed: {error}",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
