import os
import warnings
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "Dataset", "housing.csv")
MODEL_DIR = os.path.join(BASE_DIR, "Model")

MODELS = {
    "LinearRegression":        "lin_reg.pkl",
    "DecisionTreeRegressor":   "des_tree.pkl",
    "RandomForestRegressor":   "forest_reg.pkl",
}


def build_test_data():
    housing = pd.read_csv(DATASET_PATH)
    housing["incom_cat"] = pd.cut(
        housing["median_income"],
        bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
        labels=[1, 2, 3, 4, 5],
    )
    splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_idx, test_idx in splitter.split(housing, housing["incom_cat"]):
        strat_train = housing.loc[train_idx]
        strat_test  = housing.loc[test_idx]

    X_train = strat_train.drop("median_house_value", axis=1)
    X_test  = strat_test.drop("median_house_value", axis=1)
    y_test  = strat_test["median_house_value"]

    num_attribs = list(X_train.drop("ocean_proximity", axis=1).columns)
    num_pipeline = Pipeline([
        ("imputer",    SimpleImputer(strategy="median")),
        ("std_scaler", StandardScaler()),
    ])
    full_pipeline = ColumnTransformer([
        ("num", num_pipeline,    num_attribs),
        ("cat", OneHotEncoder(), ["ocean_proximity"]),
    ])
    full_pipeline.fit(X_train)
    X_test_prep = full_pipeline.transform(X_test)
    return X_test_prep, y_test.values


def main():
    print("Loading test data...")
    X_test, y_test = build_test_data()
    print(f"  {len(y_test)} test samples, {X_test.shape[1]} features each.\n")

    all_passed = True

    for name, filename in MODELS.items():
        pkl_path = os.path.join(MODEL_DIR, filename)
        print(f"Testing {name} ({filename})")

        # 1. Load check - any warning means version mismatch
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                model = joblib.load(pkl_path)
            except Exception as e:
                print(f"  [FAIL] Could not load: {e}\n")
                all_passed = False
                continue

        version_warnings = [w for w in caught if "InconsistentVersionWarning" in str(w.category)]
        if version_warnings:
            print(f"  [WARN] InconsistentVersionWarning - pkl was saved with a different sklearn version.")
            print(f"         Run retrain_models.py to fix this.")
            all_passed = False
        else:
            print("  Load : OK (no version warnings)")

        # 2. Predict check
        try:
            preds = model.predict(X_test)
            rmse  = np.sqrt(mean_squared_error(y_test, preds))
            r2    = r2_score(y_test, preds) * 100
            print(f"  RMSE : {rmse:,.2f}")
            print(f"  R2   : {r2:.2f}%")
        except Exception as e:
            print(f"  [FAIL] predict() crashed: {e}")
            all_passed = False

        # 3. Sample predictions
        print("  Sample predictions (first 3):")
        print("    Predicted       Actual")
        for p, a in zip(preds[:3], y_test[:3]):
            print(f"    ${p:>10,.0f}    ${a:>10,.0f}")
        print()

    print("-" * 40)
    if all_passed:
        print("All models passed.")
    else:
        print("Some checks failed. Run retrain_models.py and try again.")


if __name__ == "__main__":
    main()
