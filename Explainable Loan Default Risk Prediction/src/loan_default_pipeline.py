from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "age",
    "annual_income",
    "employment_length_years",
    "loan_amount",
    "loan_term_months",
    "interest_rate",
    "debt_to_income_ratio",
    "credit_score",
    "credit_history_years",
    "previous_missed_payments",
]

CATEGORICAL_FEATURES = [
    "employment_status",
    "education_level",
    "loan_purpose",
    "property_area",
]

TARGET_COLUMN = "default"


@dataclass
class TrainingResult:
    best_model_name: str
    model: Pipeline
    metrics: pd.DataFrame
    confusion_matrices: dict[str, np.ndarray]
    x_train: pd.DataFrame
    x_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def build_dataset(n_samples: int = 1200, random_state: int = 42) -> pd.DataFrame:
    """Create a reproducible loan-default dataset for demos and local training."""
    rng = np.random.default_rng(random_state)

    age = rng.integers(21, 68, n_samples)
    annual_income = rng.lognormal(mean=10.9, sigma=0.45, size=n_samples).clip(18000, 220000)
    employment_length = rng.integers(0, 28, n_samples)
    loan_amount = rng.lognormal(mean=10.2, sigma=0.5, size=n_samples).clip(2500, 85000)
    loan_term = rng.choice([36, 48, 60, 84], size=n_samples, p=[0.38, 0.2, 0.34, 0.08])
    credit_score = rng.normal(680, 72, n_samples).clip(300, 850)
    credit_history = rng.integers(1, 31, n_samples)
    missed_payments = rng.poisson(0.35, n_samples).clip(0, 6)
    debt_to_income = (loan_amount / annual_income * 0.55 + rng.normal(0.18, 0.08, n_samples)).clip(0.02, 0.75)
    interest_rate = (
        0.07
        + (760 - credit_score) / 3000
        + debt_to_income * 0.08
        + missed_payments * 0.01
        + rng.normal(0, 0.012, n_samples)
    ).clip(0.045, 0.29)

    employment_status = rng.choice(
        ["Full-time", "Part-time", "Self-employed", "Unemployed"],
        n_samples,
        p=[0.58, 0.16, 0.18, 0.08],
    )
    education_level = rng.choice(
        ["High School", "Bachelor", "Master", "Doctorate"],
        n_samples,
        p=[0.32, 0.43, 0.2, 0.05],
    )
    loan_purpose = rng.choice(
        ["Debt consolidation", "Home improvement", "Medical", "Education", "Business"],
        n_samples,
        p=[0.42, 0.2, 0.12, 0.14, 0.12],
    )
    property_area = rng.choice(["Urban", "Semiurban", "Rural"], n_samples, p=[0.48, 0.32, 0.2])

    logits = (
        -2.4
        + debt_to_income * 3.2
        + (loan_amount / annual_income) * 1.7
        + (680 - credit_score) / 95
        + missed_payments * 0.55
        + (interest_rate - 0.11) * 5.0
        - employment_length * 0.025
        - credit_history * 0.018
    )
    logits += np.where(employment_status == "Unemployed", 0.8, 0)
    logits += np.where(employment_status == "Part-time", 0.25, 0)
    logits += np.where(loan_purpose == "Business", 0.22, 0)
    logits += np.where(property_area == "Rural", 0.12, 0)

    default_probability = 1 / (1 + np.exp(-logits))
    default = rng.binomial(1, default_probability)

    return pd.DataFrame(
        {
            "age": age,
            "annual_income": annual_income.round(2),
            "employment_length_years": employment_length,
            "loan_amount": loan_amount.round(2),
            "loan_term_months": loan_term,
            "interest_rate": interest_rate.round(4),
            "debt_to_income_ratio": debt_to_income.round(3),
            "credit_score": credit_score.round().astype(int),
            "credit_history_years": credit_history,
            "previous_missed_payments": missed_payments,
            "employment_status": employment_status,
            "education_level": education_level,
            "loan_purpose": loan_purpose,
            "property_area": property_area,
            "default": default,
        }
    )


def load_or_build_dataset(csv_path: str | None = None) -> pd.DataFrame:
    if csv_path:
        return pd.read_csv(csv_path)
    return build_dataset()


def make_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def make_models() -> dict[str, Pipeline]:
    return {
        "Logistic Regression": Pipeline(
            steps=[
                ("preprocessor", make_preprocessor()),
                ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
            ]
        ),
        "Random Forest": Pipeline(
            steps=[
                ("preprocessor", make_preprocessor()),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=220,
                        max_depth=10,
                        class_weight="balanced",
                        random_state=42,
                    ),
                ),
            ]
        ),
        "Gradient Boosting": Pipeline(
            steps=[
                ("preprocessor", make_preprocessor()),
                ("classifier", GradientBoostingClassifier(random_state=42)),
            ]
        ),
    }


def train_models(data: pd.DataFrame) -> TrainingResult:
    x = data[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = data[TARGET_COLUMN]
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    rows: list[dict[str, Any]] = []
    confusion_matrices: dict[str, np.ndarray] = {}
    trained_models = make_models()

    for name, model in trained_models.items():
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        probabilities = model.predict_proba(x_test)[:, 1]
        confusion_matrices[name] = confusion_matrix(y_test, predictions)
        rows.append(
            {
                "model": name,
                "accuracy": accuracy_score(y_test, predictions),
                "precision": precision_score(y_test, predictions, zero_division=0),
                "recall": recall_score(y_test, predictions, zero_division=0),
                "f1_score": f1_score(y_test, predictions, zero_division=0),
                "roc_auc": roc_auc_score(y_test, probabilities),
            }
        )

    metrics = pd.DataFrame(rows).sort_values("roc_auc", ascending=False).reset_index(drop=True)
    best_model_name = str(metrics.loc[0, "model"])

    return TrainingResult(
        best_model_name=best_model_name,
        model=trained_models[best_model_name],
        metrics=metrics,
        confusion_matrices=confusion_matrices,
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
    )


def predict_default(model: Pipeline, applicant: dict[str, Any]) -> tuple[float, str]:
    frame = pd.DataFrame([applicant])
    probability = float(model.predict_proba(frame)[0, 1])

    if probability >= 0.65:
        risk = "High"
    elif probability >= 0.35:
        risk = "Medium"
    else:
        risk = "Low"

    return probability, risk


def get_feature_names(model: Pipeline) -> list[str]:
    preprocessor = model.named_steps["preprocessor"]
    return list(preprocessor.get_feature_names_out())
