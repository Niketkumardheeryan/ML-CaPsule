import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_diabetes, load_iris
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    LabelEncoder,
    OneHotEncoder,
    PolynomialFeatures,
    StandardScaler,
)
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

try:
    from sklearn.metrics import root_mean_squared_error
except ImportError:
    root_mean_squared_error = None


st.set_page_config(page_title="Model Selection Tool", layout="wide")


@st.cache_data
def load_sample_dataset(name: str) -> pd.DataFrame:
    if name == "Iris (classification)":
        data = load_iris(as_frame=True)
    else:
        data = load_diabetes(as_frame=True)
    return data.frame.copy()


def infer_problem_type(target: pd.Series) -> str:
    if (
        pd.api.types.is_object_dtype(target)
        or pd.api.types.is_categorical_dtype(target)
        or pd.api.types.is_bool_dtype(target)
    ):
        return "classification"
    unique_count = target.nunique(dropna=True)
    threshold = min(20, max(2, int(0.1 * len(target))))
    if unique_count <= threshold:
        return "classification"
    return "regression"


def build_preprocessor(
    features: pd.DataFrame,
    use_polynomial: bool,
    poly_degree: int,
) -> ColumnTransformer:
    numeric_features = features.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = [
        column for column in features.columns if column not in numeric_features
    ]

    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if use_polynomial:
        numeric_steps.append(
            ("poly", PolynomialFeatures(degree=poly_degree, include_bias=False))
        )
    numeric_steps.append(("scaler", StandardScaler()))

    numeric_transformer = Pipeline(steps=numeric_steps)
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )


def build_model(model_name: str, problem_type: str, params: dict):
    if problem_type == "classification":
        if model_name in [
            "Linear Regression",
            "Multiple Linear Regression",
            "Polynomial Regression",
        ]:
            return LogisticRegression(max_iter=2000)
        if model_name == "Random Forest":
            return RandomForestClassifier(
                n_estimators=params["rf_estimators"],
                max_depth=params["rf_max_depth"],
                random_state=params["random_state"],
            )
        if model_name == "KNN":
            return KNeighborsClassifier(n_neighbors=params["knn_neighbors"])
        if model_name == "SVM":
            return SVC(kernel=params["svm_kernel"])
        if model_name == "Decision Tree":
            return DecisionTreeClassifier(
                max_depth=params["dt_max_depth"],
                random_state=params["random_state"],
            )
    else:
        if model_name in [
            "Linear Regression",
            "Multiple Linear Regression",
            "Polynomial Regression",
        ]:
            return LinearRegression()
        if model_name == "Random Forest":
            return RandomForestRegressor(
                n_estimators=params["rf_estimators"],
                max_depth=params["rf_max_depth"],
                random_state=params["random_state"],
            )
        if model_name == "KNN":
            return KNeighborsRegressor(n_neighbors=params["knn_neighbors"])
        if model_name == "SVM":
            return SVR(kernel=params["svm_kernel"])
        if model_name == "Decision Tree":
            return DecisionTreeRegressor(
                max_depth=params["dt_max_depth"],
                random_state=params["random_state"],
            )
    return None


def plot_relationship(data: pd.DataFrame, x_col: str, y_col: str):
    x_numeric = pd.api.types.is_numeric_dtype(data[x_col])
    y_numeric = pd.api.types.is_numeric_dtype(data[y_col])

    fig, ax = plt.subplots()
    if x_numeric and y_numeric:
        sns.scatterplot(data=data, x=x_col, y=y_col, ax=ax)
        sns.regplot(data=data, x=x_col, y=y_col, ax=ax, scatter=False, color="orange")
    elif x_numeric and not y_numeric:
        sns.boxplot(data=data, x=y_col, y=x_col, ax=ax)
    else:
        sns.countplot(data=data, x=x_col, hue=y_col, ax=ax)
    ax.set_title(f"{x_col} vs {y_col}")
    st.pyplot(fig, use_container_width=True)


st.title("Model Selection Tool")
st.write(
    "Select features, target, test split, and models to compare."
    " The app shows the trend plot and the best model score."
)

model_options = [
    "Linear Regression",
    "Multiple Linear Regression",
    "Polynomial Regression",
    "Random Forest",
    "KNN",
    "SVM",
    "Decision Tree",
]

with st.sidebar:
    st.header("Data")
    dataset_source = st.radio(
        "Dataset source",
        [
            "Upload CSV",
            "Sample: Iris (classification)",
            "Sample: Diabetes (regression)",
        ],
    )

    st.header("Models")
    selected_models = st.multiselect(
        "Choose models",
        model_options,
        default=["Linear Regression", "Random Forest", "KNN", "SVM"],
    )

    st.header("Split")
    test_size = st.slider("Test size", 0.1, 0.4, 0.2, 0.05)
    random_state = st.number_input("Random state", min_value=0, value=42, step=1)

    with st.expander("Model settings"):
        poly_degree = st.slider("Polynomial degree", 2, 5, 2)
        knn_neighbors = st.slider("KNN neighbors", 1, 20, 5)
        rf_estimators = st.slider("Random Forest trees", 50, 300, 150, step=50)
        rf_max_depth_raw = st.slider("Random Forest max depth (0 = None)", 0, 30, 0)
        svm_kernel = st.selectbox("SVM kernel", ["rbf", "linear", "poly"])
        dt_max_depth_raw = st.slider("Decision Tree max depth (0 = None)", 0, 30, 0)

rf_max_depth = None if rf_max_depth_raw == 0 else rf_max_depth_raw
dt_max_depth = None if dt_max_depth_raw == 0 else dt_max_depth_raw

params = {
    "poly_degree": poly_degree,
    "knn_neighbors": knn_neighbors,
    "rf_estimators": rf_estimators,
    "rf_max_depth": rf_max_depth,
    "svm_kernel": svm_kernel,
    "dt_max_depth": dt_max_depth,
    "random_state": random_state,
}

df = None
if dataset_source == "Upload CSV":
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
else:
    sample_name = dataset_source.replace("Sample: ", "")
    df = load_sample_dataset(sample_name)

if df is None:
    st.info("Upload a CSV file or choose a sample dataset to continue.")
    st.stop()

st.subheader("Dataset")
st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
with st.expander("Preview data"):
    st.dataframe(df.head(50), use_container_width=True)

all_columns = df.columns.tolist()
if not all_columns:
    st.error("Dataset has no columns.")
    st.stop()

default_target = all_columns[-1]
target_col = st.selectbox("Target (y)", all_columns, index=len(all_columns) - 1)
feature_candidates = [column for column in all_columns if column != target_col]
feature_cols = st.multiselect(
    "Features (X)",
    feature_candidates,
    default=feature_candidates,
)

if not feature_cols:
    st.warning("Select at least one feature column to continue.")
    st.stop()

plot_feature = st.selectbox("X axis for trend plot", feature_cols)
plot_relationship(df, plot_feature, target_col)

problem_type = infer_problem_type(df[target_col])
st.caption(f"Detected problem type: {problem_type.capitalize()}")

if not selected_models:
    st.warning("Select at least one model to compare.")
    st.stop()

if st.button("Train and compare"):
    data = df[feature_cols + [target_col]].dropna(subset=[target_col]).copy()
    if data[target_col].nunique(dropna=True) < 2:
        st.error("Target column needs at least two unique values.")
        st.stop()

    X = data[feature_cols]
    y = data[target_col]

    label_encoder = None
    if problem_type == "classification" and not pd.api.types.is_numeric_dtype(y):
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))

    stratify = y if problem_type == "classification" else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )

    if label_encoder is not None:
        with st.expander("Class mapping"):
            mapping = {
                index: label for index, label in enumerate(label_encoder.classes_)
            }
            st.write(mapping)

    results = []
    model_runs = {}

    for model_name in selected_models:
        use_polynomial = model_name == "Polynomial Regression"
        preprocessor = build_preprocessor(X_train, use_polynomial, poly_degree)
        estimator = build_model(model_name, problem_type, params)

        if estimator is None:
            continue

        pipeline = Pipeline(
            steps=[("preprocess", preprocessor), ("model", estimator)]
        )
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        if problem_type == "classification":
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
            score = accuracy
            results.append(
                {
                    "Model": model_name,
                    "Accuracy": accuracy,
                    "F1": f1,
                    "Score": score,
                }
            )
        else:
            r2 = r2_score(y_test, y_pred)
            if root_mean_squared_error is not None:
                rmse = root_mean_squared_error(y_test, y_pred)
            else:
                rmse = mean_squared_error(y_test, y_pred) ** 0.5
            score = r2
            results.append(
                {"Model": model_name, "R2": r2, "RMSE": rmse, "Score": score}
            )

        model_runs[model_name] = {
            "pipeline": pipeline,
            "y_pred": y_pred,
            "y_test": y_test,
        }

    if not results:
        st.error("No models could be trained. Check your selections.")
        st.stop()

    results_df = pd.DataFrame(results).sort_values("Score", ascending=False)
    st.subheader("Model comparison")
    st.dataframe(results_df, use_container_width=True)

    score_label = "Accuracy" if problem_type == "classification" else "R2"
    st.bar_chart(results_df.set_index("Model")["Score"], height=300)

    best_model_name = results_df.iloc[0]["Model"]
    st.success(f"Best model: {best_model_name} ({score_label})")

    best_run = model_runs[best_model_name]
    if problem_type == "classification":
        fig, ax = plt.subplots()
        cm = confusion_matrix(best_run["y_test"], best_run["y_pred"])
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion Matrix")
        st.pyplot(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots()
        y_test = best_run["y_test"]
        y_pred = best_run["y_pred"]
        ax.scatter(y_test, y_pred, alpha=0.6)
        min_val = np.min([y_test, y_pred])
        max_val = np.max([y_test, y_pred])
        ax.plot([min_val, max_val], [min_val, max_val], "r--")
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title("Actual vs Predicted")
        st.pyplot(fig, use_container_width=True)
