import sys
import os


sys.path.append(os.path.abspath(".."))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from ml_utils.ml_data_validators import (
    check_missing_values,
    check_duplicates,
    validate_schema
)

from ml_utils.ml_reproducibility import (
    set_seed,
    get_environment_info
)

from ml_utils.ml_metrics import classification_metrics

set_seed(42)

df = pd.read_csv("../sample_data/sample_dataset.csv")

print("Missing Values:")
print(check_missing_values(df))

print("\nDuplicates:")
print(check_duplicates(df))

print("\nSchema:")
print(validate_schema(df))

X = df[["feature1", "feature2"]]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

metrics = classification_metrics(y_test, predictions)

print("\nMetrics:")
print(metrics)

print("\nEnvironment Info:")
print(get_environment_info())