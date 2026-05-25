import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dataset", "housing.csv")
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Model")


def load_data():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}. "
            "Make sure Dataset/housing.csv exists in the project directory."
        )
    return pd.read_csv(DATASET_PATH)


def stratified_split(housing):
    housing = housing.copy()
    housing["incom_cat"] = pd.cut(
        housing["median_income"],
        bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
        labels=[1, 2, 3, 4, 5],
    )
    splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_idx, test_idx in splitter.split(housing, housing["incom_cat"]):
        strat_train = housing.loc[train_idx]
        strat_test = housing.loc[test_idx]
    return strat_train, strat_test


def build_pipeline(num_attribs):
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("std_scaler", StandardScaler()),
    ])
    return ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        ("cat", OneHotEncoder(), ["ocean_proximity"]),
    ])


def cv_rmse(model, X, y, cv=10):
    scores = cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=cv)
    return np.sqrt(-scores)


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    print("Loading dataset from:", DATASET_PATH)
    housing = load_data()
    print(f"  {len(housing)} rows loaded.\n")

    strat_train, strat_test = stratified_split(housing)

    X_train = strat_train.drop("median_house_value", axis=1)
    y_train = strat_train["median_house_value"].copy()
    X_test = strat_test.drop("median_house_value", axis=1)
    y_test = strat_test["median_house_value"].copy()

    # Numeric columns = all columns except the categorical one
    num_attribs = list(X_train.drop("ocean_proximity", axis=1).columns)

    full_pipeline = build_pipeline(num_attribs)
    X_train_prep = full_pipeline.fit_transform(X_train)
    X_test_prep = full_pipeline.transform(X_test)

    # ── Linear Regression ────────────────────────────────────────────────────
    print("Training Linear Regression...")
    lin_reg = LinearRegression()
    lin_reg.fit(X_train_prep, y_train)
    rmse_scores = cv_rmse(lin_reg, X_train_prep, y_train)
    print(f"  CV RMSE — mean: {rmse_scores.mean():.2f}, std: {rmse_scores.std():.2f}")
    joblib.dump(lin_reg, os.path.join(MODEL_DIR, "lin_reg.pkl"))
    print("  Saved -> Model/lin_reg.pkl\n")

    # ── Decision Tree Regressor ───────────────────────────────────────────────
    print("Training Decision Tree Regressor...")
    des_tree = DecisionTreeRegressor(random_state=42)
    des_tree.fit(X_train_prep, y_train)
    rmse_scores = cv_rmse(des_tree, X_train_prep, y_train)
    print(f"  CV RMSE — mean: {rmse_scores.mean():.2f}, std: {rmse_scores.std():.2f}")
    joblib.dump(des_tree, os.path.join(MODEL_DIR, "des_tree.pkl"))
    print("  Saved -> Model/des_tree.pkl\n")

    # ── Random Forest + GridSearchCV ─────────────────────────────────────────
    print("Training Random Forest with GridSearchCV (this may take a few minutes)...")
    param_grid = [
        {"n_estimators": [3, 10, 30], "max_features": [2, 4, 6, 8]},
        {"bootstrap": [False], "n_estimators": [3, 10], "max_features": [2, 3, 4]},
    ]
    grid_search = GridSearchCV(
        RandomForestRegressor(random_state=42),
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        return_train_score=True,
    )
    grid_search.fit(X_train_prep, y_train)
    best_forest = grid_search.best_estimator_
    print(f"  Best params: {grid_search.best_params_}")
    joblib.dump(best_forest, os.path.join(MODEL_DIR, "forest_reg.pkl"))
    print("  Saved -> Model/forest_reg.pkl\n")

    # ── Final test-set evaluation ─────────────────────────────────────────────
    print("-" * 50)
    print("Final Test Set Evaluation (Random Forest)")
    preds = best_forest.predict(X_test_prep)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds) * 100
    print(f"  RMSE : {rmse:,.2f}")
    print(f"  R²   : {r2:.2f}%")
    print("-" * 50)
    print("\nAll models retrained and saved to Model/")


if __name__ == "__main__":
    main()
