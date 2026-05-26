"""
=============================================================================
AI-Based Smart Home Energy Consumption Forecasting & Waste Pattern Analysis
=============================================================================
Complete end-to-end ML pipeline covering:
  1. Imports
  2. Data Loading
  3. Exploratory Data Analysis (EDA)
  4. Data Preprocessing
  5. Feature Engineering
  6. PCA (Principal Component Analysis)
  7. Model Training — BEFORE Feature Engineering
  8. Model Training — AFTER Feature Engineering
  9. Model Comparison Table
 10. Waste Pattern Analysis (KMeans Clustering)
 11. Time Series Forecasting (ARIMA)
 12. Model Saving
 13. Prediction Function
=============================================================================
"""

# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 1: IMPORTS                                  ║
# ╚═══════════════════════════════════════════════════════╝

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
import joblib

# Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score
)

# XGBoost (optional — skipped gracefully if not installed)
try:
    from xgboost import XGBRegressor
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("[INFO] XGBoost not installed — skipping XGBoost model.")

# Time‑series
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")
sns.set_style("whitegrid")

# ── Directories ──────────────────────────────────────────
PLOT_DIR = os.path.join(os.path.dirname(__file__), "plots")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

def save_plot(fig, name):
    """Save a matplotlib figure to the plots directory."""
    path = os.path.join(PLOT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔ Plot saved → {path}")


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 2: DATA LOADING                             ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 2: DATA LOADING")
print("=" * 60)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "energydata_complete.csv")

# Try multiple encodings
for enc in ["utf-8", "latin-1", "cp1252"]:
    try:
        df = pd.read_csv(DATA_PATH, encoding=enc)
        print(f"  Loaded with encoding: {enc}")
        break
    except UnicodeDecodeError:
        continue

# Clean column names (remove invisible characters)
df.columns = df.columns.str.strip().str.replace('\u00b0', '°')

print(f"  Shape: {df.shape}")
print(f"  Columns: {list(df.columns)}")
print(df.head())


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 3: EXPLORATORY DATA ANALYSIS (EDA)          ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 3: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# --- 3a. Basic Info ---
print("\n── Dataset Info ──")
print(df.dtypes)
print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\n── Statistical Summary ──")
print(df.describe())

# --- 3b. Missing Values ---
print(f"\n── Missing Values ──")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "  No missing values ✔")

# --- 3c. Distribution of Target Variable ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df["Energy Consumption (kWh)"], bins=50, kde=True, ax=ax, color="#3498db")
ax.set_title("Distribution of Energy Consumption (kWh)", fontsize=14)
ax.set_xlabel("Energy Consumption (kWh)")
save_plot(fig, "01_energy_distribution.png")

# --- 3d. Appliance-wise Box Plot ---
fig, ax = plt.subplots(figsize=(12, 5))
sns.boxplot(x="Appliance Type", y="Energy Consumption (kWh)", data=df, ax=ax, palette="Set2")
ax.set_title("Energy Consumption by Appliance Type", fontsize=14)
plt.xticks(rotation=45, ha="right")
save_plot(fig, "02_appliance_boxplot.png")

# --- 3e. Season-wise Bar Plot (Season used from the start) ---
fig, ax = plt.subplots(figsize=(8, 5))
season_avg = df.groupby("Season")["Energy Consumption (kWh)"].mean().sort_values(ascending=False)
season_avg.plot(kind="bar", color=["#e74c3c", "#f39c12", "#2ecc71", "#3498db"], ax=ax)
ax.set_title("Average Energy Consumption by Season", fontsize=14)
ax.set_ylabel("Avg Energy (kWh)")
plt.xticks(rotation=0)
save_plot(fig, "03_season_bar.png")

# --- 3f. Correlation Heatmap (numeric columns only) ---
fig, ax = plt.subplots(figsize=(10, 8))
numeric_cols = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax, linewidths=0.5)
ax.set_title("Correlation Heatmap", fontsize=14)
save_plot(fig, "04_correlation_heatmap.png")

# --- 3g. Create datetime for time-based analysis ---
df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors="coerce")
df["Hour"] = df["Datetime"].dt.hour
df["Day"] = df["Datetime"].dt.day
df["Month"] = df["Datetime"].dt.month
df["Weekday"] = df["Datetime"].dt.weekday  # 0=Monday … 6=Sunday

# --- 3h. Hourly Trend ---
fig, ax = plt.subplots(figsize=(10, 5))
hourly = df.groupby("Hour")["Energy Consumption (kWh)"].mean()
ax.plot(hourly.index, hourly.values, marker="o", color="#9b59b6", linewidth=2)
ax.set_title("Average Energy Consumption by Hour of Day", fontsize=14)
ax.set_xlabel("Hour")
ax.set_ylabel("Avg Energy (kWh)")
ax.set_xticks(range(0, 24))
save_plot(fig, "05_hourly_trend.png")

# --- 3i. Monthly Trend ---
fig, ax = plt.subplots(figsize=(10, 5))
monthly = df.groupby("Month")["Energy Consumption (kWh)"].mean()
ax.bar(monthly.index, monthly.values, color="#1abc9c")
ax.set_title("Average Energy Consumption by Month", fontsize=14)
ax.set_xlabel("Month")
ax.set_ylabel("Avg Energy (kWh)")
ax.set_xticks(range(1, 13))
save_plot(fig, "06_monthly_trend.png")

# --- 3j. Day of Week Trend ---
fig, ax = plt.subplots(figsize=(10, 5))
day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
weekday_avg = df.groupby("Weekday")["Energy Consumption (kWh)"].mean()
ax.bar(weekday_avg.index, weekday_avg.values, color="#e67e22", tick_label=day_names)
ax.set_title("Average Energy Consumption by Day of Week", fontsize=14)
ax.set_ylabel("Avg Energy (kWh)")
save_plot(fig, "07_weekday_trend.png")

# --- 3k. Temperature vs Energy Scatter ---
fig, ax = plt.subplots(figsize=(10, 5))
temp_col = [c for c in df.columns if "Temperature" in c][0]
ax.scatter(df[temp_col], df["Energy Consumption (kWh)"], alpha=0.1, s=5, color="#e74c3c")
ax.set_title("Outdoor Temperature vs Energy Consumption", fontsize=14)
ax.set_xlabel(temp_col)
ax.set_ylabel("Energy Consumption (kWh)")
save_plot(fig, "08_temp_vs_energy.png")

print("  ✔ All EDA plots saved to notebooks/plots/")


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 4: DATA PREPROCESSING                       ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 4: DATA PREPROCESSING")
print("=" * 60)

# --- 4a. Handle Missing Values ---
# Fill numeric missing with median, categorical with mode
for col in df.select_dtypes(include=[np.number]).columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)
        print(f"  Filled {col} missing values with median")

for col in df.select_dtypes(include=["object"]).columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mode()[0], inplace=True)
        print(f"  Filled {col} missing values with mode")

# Drop rows where datetime could not be parsed
df.dropna(subset=["Datetime"], inplace=True)

print(f"  Shape after cleaning: {df.shape}")
print(f"  Missing values remaining: {df.isnull().sum().sum()}")

# --- 4b. Datetime features are already extracted in EDA ---
# Hour, Day, Month, Weekday are ready

# --- 4c. Season is used from the original column (NOT derived) ---
print(f"  Seasons in data: {df['Season'].unique()}")

# --- 4d. Save a copy BEFORE feature engineering for model comparison ---
df_before_fe = df.copy()

print("  ✔ Preprocessing complete")


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 5: FEATURE ENGINEERING                      ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 5: FEATURE ENGINEERING")
print("=" * 60)

# --- 5a. Peak Hour Flag (6PM – 10PM) ---
df["Peak_Hour"] = df["Hour"].apply(lambda h: 1 if 18 <= h <= 22 else 0)

# --- 5b. Night Usage Flag (11PM – 5AM) ---
df["Night_Usage"] = df["Hour"].apply(lambda h: 1 if h >= 23 or h <= 5 else 0)

# --- 5c. Temperature Squared ---
df["Temp_Squared"] = df[temp_col] ** 2

# --- 5d. Temperature × Household Size Interaction ---
df["Temp_x_HouseholdSize"] = df[temp_col] * df["Household Size"]

# --- 5e. Rolling Average Consumption (3-period) ---
df = df.sort_values("Datetime").reset_index(drop=True)
df["Rolling_Avg_3"] = (
    df.groupby("Home ID")["Energy Consumption (kWh)"]
    .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
)

# --- 5f. Lag Features ---
for lag in [1, 2, 3]:
    df[f"Lag_{lag}"] = (
        df.groupby("Home ID")["Energy Consumption (kWh)"]
        .transform(lambda x: x.shift(lag))
    )

# Fill NaN created by shift with 0
df.fillna(0, inplace=True)

new_features = ["Peak_Hour", "Night_Usage", "Temp_Squared",
                "Temp_x_HouseholdSize", "Rolling_Avg_3",
                "Lag_1", "Lag_2", "Lag_3"]
print(f"  ✔ Created features: {new_features}")
print(f"  Shape after FE: {df.shape}")


# ╔═══════════════════════════════════════════════════════╗
# ║  HELPER: Prepare X, y with encoding & scaling        ║
# ╚═══════════════════════════════════════════════════════╝

def prepare_features(dataframe, label="Energy Consumption (kWh)"):
    """
    OneHotEncode categorical columns, StandardScale numeric columns.
    Returns X_train, X_test, y_train, y_test, feature_names, scaler.
    """
    drop_cols = [label, "Datetime", "Date", "Time"]
    drop_cols = [c for c in drop_cols if c in dataframe.columns]
    
    X = dataframe.drop(columns=drop_cols)
    y = dataframe[label]

    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()

    # Column transformer: one-hot for categorical, scale for numeric
    ct = ColumnTransformer([
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ("scaler", StandardScaler(), num_cols)
    ], remainder="drop")

    X_transformed = ct.fit_transform(X)

    # Get feature names
    ohe_names = (ct.named_transformers_["onehot"]
                   .get_feature_names_out(cat_cols).tolist() if cat_cols else [])
    feature_names = ohe_names + num_cols

    X_train, X_test, y_train, y_test = train_test_split(
        X_transformed, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, feature_names, ct


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 6: PCA (Principal Component Analysis)       ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 6: PCA — Principal Component Analysis")
print("=" * 60)

X_tr_after, X_te_after, y_tr_after, y_te_after, feat_names_after, ct_after = prepare_features(df)

# Fit PCA on the full feature set
pca_full = PCA()
pca_full.fit(X_tr_after)
cum_var = np.cumsum(pca_full.explained_variance_ratio_)

# --- Explained Variance Plot ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(1, len(cum_var) + 1), cum_var, marker="o", color="#8e44ad")
ax.axhline(y=0.95, color="red", linestyle="--", label="95% threshold")
ax.set_title("PCA — Cumulative Explained Variance", fontsize=14)
ax.set_xlabel("Number of Components")
ax.set_ylabel("Cumulative Explained Variance")
ax.legend()
save_plot(fig, "09_pca_variance.png")

# Select components that explain 95% variance
n_components_95 = np.argmax(cum_var >= 0.95) + 1
print(f"  Components for 95% variance: {n_components_95} out of {X_tr_after.shape[1]}")

pca = PCA(n_components=n_components_95)
X_tr_pca = pca.fit_transform(X_tr_after)
X_te_pca = pca.transform(X_te_after)

# --- Compare Before vs After PCA ---
print(f"  Before PCA: {X_tr_after.shape[1]} features")
print(f"  After  PCA: {X_tr_pca.shape[1]} components")

# Quick model test with PCA
rf_pca = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf_pca.fit(X_tr_pca, y_tr_after)
pred_pca = rf_pca.predict(X_te_pca)
r2_pca = r2_score(y_te_after, pred_pca)

rf_no_pca = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf_no_pca.fit(X_tr_after, y_tr_after)
pred_no_pca = rf_no_pca.predict(X_te_after)
r2_no_pca = r2_score(y_te_after, pred_no_pca)

print(f"\n  R² WITHOUT PCA: {r2_no_pca:.4f}")
print(f"  R² WITH    PCA: {r2_pca:.4f}")

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(["Without PCA", "With PCA"], [r2_no_pca, r2_pca], color=["#3498db", "#e74c3c"])
ax.set_title("Random Forest R² — Before vs After PCA", fontsize=13)
ax.set_ylabel("R² Score")
for bar, val in zip(bars, [r2_no_pca, r2_pca]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f"{val:.4f}", ha="center", fontsize=11)
save_plot(fig, "10_pca_comparison.png")


# ╔═══════════════════════════════════════════════════════╗
# ║  HELPER: Train & Evaluate All Models                 ║
# ╚═══════════════════════════════════════════════════════╝

def train_evaluate_models(X_train, X_test, y_train, y_test):
    """Train 5 models and return a results DataFrame."""
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=10, min_samples_split=10,
                                               random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=10,
                                                min_samples_split=10, random_state=42),
        "KNN": KNeighborsRegressor(n_neighbors=5),
    }
    if HAS_XGBOOST:
        models["XGBoost"] = XGBRegressor(
            n_estimators=200, max_depth=6, learning_rate=0.05,
            subsample=0.8, random_state=42, verbosity=0
        )

    results = []
    trained_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        mse = mean_squared_error(y_test, preds)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, preds)
        results.append({"Model": name, "MAE": mae, "MSE": mse,
                        "RMSE": rmse, "R²": r2})
        trained_models[name] = model

    return pd.DataFrame(results), trained_models


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 7: MODEL TRAINING — BEFORE Feature Eng.     ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 7: MODEL TRAINING — BEFORE Feature Engineering")
print("=" * 60)

X_tr_before, X_te_before, y_tr_before, y_te_before, feat_names_before, ct_before = prepare_features(df_before_fe)
results_before, models_before = train_evaluate_models(
    X_tr_before, X_te_before, y_tr_before, y_te_before
)

print("\n  Results BEFORE Feature Engineering:")
print(results_before.to_string(index=False))


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 8: MODEL TRAINING — AFTER Feature Eng.      ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 8: MODEL TRAINING — AFTER Feature Engineering")
print("=" * 60)

results_after, models_after = train_evaluate_models(
    X_tr_after, X_te_after, y_tr_after, y_te_after
)

print("\n  Results AFTER Feature Engineering:")
print(results_after.to_string(index=False))


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 9: MODEL COMPARISON TABLE                   ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 9: MODEL COMPARISON — BEFORE vs AFTER FE")
print("=" * 60)

comparison = results_before[["Model", "R²"]].rename(columns={"R²": "R²_Before"}).merge(
    results_after[["Model", "R²"]].rename(columns={"R²": "R²_After"}),
    on="Model"
)
comparison["Improvement"] = comparison["R²_After"] - comparison["R²_Before"]
print()
print(comparison.to_string(index=False))

# --- Grouped Bar Chart ---
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(comparison))
width = 0.35
bars1 = ax.bar(x - width / 2, comparison["R²_Before"], width, label="Before FE", color="#3498db")
bars2 = ax.bar(x + width / 2, comparison["R²_After"], width, label="After FE", color="#e74c3c")
ax.set_xticks(x)
ax.set_xticklabels(comparison["Model"], rotation=20, ha="right")
ax.set_ylabel("R² Score")
ax.set_title("Model R² — Before vs After Feature Engineering", fontsize=14)
ax.legend()
ax.set_ylim(0, max(comparison["R²_After"].max(), comparison["R²_Before"].max()) * 1.15)

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f"{bar.get_height():.3f}", ha="center", fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f"{bar.get_height():.3f}", ha="center", fontsize=9)
save_plot(fig, "11_model_comparison.png")

# --- Full Metrics Comparison ---
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
for i, metric in enumerate(["MAE", "MSE", "RMSE", "R²"]):
    ax = axes[i]
    before_vals = results_before[metric].values
    after_vals = results_after[metric].values
    ax.bar(x - width / 2, before_vals, width, label="Before FE", color="#3498db")
    ax.bar(x + width / 2, after_vals, width, label="After FE", color="#e74c3c")
    ax.set_xticks(x)
    ax.set_xticklabels(comparison["Model"], rotation=30, ha="right", fontsize=8)
    ax.set_title(metric, fontsize=13)
    ax.legend(fontsize=8)
fig.suptitle("All Metrics — Before vs After Feature Engineering", fontsize=15, y=1.02)
plt.tight_layout()
save_plot(fig, "12_all_metrics_comparison.png")


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 10: WASTE PATTERN ANALYSIS (KMeans)         ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 10: WASTE PATTERN ANALYSIS — KMeans Clustering")
print("=" * 60)

# Aggregate per Home
home_agg = df.groupby("Home ID").agg(
    Avg_Consumption=("Energy Consumption (kWh)", "mean"),
    Total_Consumption=("Energy Consumption (kWh)", "sum"),
    Household_Size=("Household Size", "first"),
    Peak_Usage_Ratio=("Peak_Hour", "mean"),
    Night_Usage_Ratio=("Night_Usage", "mean"),
    Avg_Temperature=(temp_col, "mean"),
).reset_index()

# Scale for clustering
cluster_features = ["Avg_Consumption", "Total_Consumption", "Peak_Usage_Ratio",
                    "Night_Usage_Ratio", "Avg_Temperature"]
scaler_cluster = StandardScaler()
X_cluster = scaler_cluster.fit_transform(home_agg[cluster_features])

# --- Elbow Method ---
inertias = []
K_range = range(2, 8)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_cluster)
    inertias.append(km.inertia_)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(list(K_range), inertias, marker="o", color="#e74c3c")
ax.set_title("Elbow Method — Optimal K for Clustering", fontsize=14)
ax.set_xlabel("Number of Clusters (K)")
ax.set_ylabel("Inertia")
save_plot(fig, "13_elbow_method.png")

# --- KMeans with K=3 ---
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
home_agg["Cluster"] = kmeans.fit_predict(X_cluster)

# Label clusters by average consumption
cluster_means = home_agg.groupby("Cluster")["Avg_Consumption"].mean().sort_values()
label_map = {cluster_means.index[0]: "Efficient",
             cluster_means.index[1]: "Moderate",
             cluster_means.index[2]: "Wasteful"}
home_agg["Usage_Label"] = home_agg["Cluster"].map(label_map)

print("\n  Cluster Summary:")
print(home_agg.groupby("Usage_Label")[["Avg_Consumption", "Total_Consumption",
                                        "Peak_Usage_Ratio"]].mean().round(3))

# --- Cluster Scatter Plot ---
colors = {"Efficient": "#2ecc71", "Moderate": "#f39c12", "Wasteful": "#e74c3c"}
fig, ax = plt.subplots(figsize=(10, 6))
for label, color in colors.items():
    subset = home_agg[home_agg["Usage_Label"] == label]
    ax.scatter(subset["Avg_Consumption"], subset["Total_Consumption"],
               label=label, c=color, alpha=0.7, s=50, edgecolors="white")
ax.set_title("Home Energy Usage Clusters", fontsize=14)
ax.set_xlabel("Average Consumption (kWh)")
ax.set_ylabel("Total Consumption (kWh)")
ax.legend(title="Usage Pattern")
save_plot(fig, "14_clusters.png")

# --- Cluster Distribution ---
fig, ax = plt.subplots(figsize=(6, 4))
home_agg["Usage_Label"].value_counts().plot(kind="bar", color=list(colors.values()), ax=ax)
ax.set_title("Distribution of Usage Patterns", fontsize=14)
ax.set_ylabel("Number of Homes")
plt.xticks(rotation=0)
save_plot(fig, "15_cluster_distribution.png")

print("  ✔ Clustering complete")


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 11: TIME SERIES FORECASTING (ARIMA)         ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 11: TIME SERIES FORECASTING — ARIMA")
print("=" * 60)

# Aggregate daily consumption
daily = (
    df.groupby(df["Datetime"].dt.date)["Energy Consumption (kWh)"]
    .sum()
    .reset_index()
)
daily.columns = ["Date", "Daily_Consumption"]
daily["Date"] = pd.to_datetime(daily["Date"])
daily = daily.sort_values("Date").set_index("Date")

# --- Daily Consumption Trend ---
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(daily.index, daily["Daily_Consumption"], color="#2c3e50", linewidth=0.8)
ax.set_title("Daily Total Energy Consumption — Trend", fontsize=14)
ax.set_xlabel("Date")
ax.set_ylabel("Total Consumption (kWh)")
save_plot(fig, "16_daily_trend.png")

# --- Fit ARIMA ---
print("  Fitting ARIMA(5,1,2) ... (this may take a minute)")
try:
    arima_model = ARIMA(daily["Daily_Consumption"], order=(5, 1, 2))
    arima_result = arima_model.fit()
    print(f"  AIC: {arima_result.aic:.2f}")

    # Forecast next 30 days
    forecast = arima_result.forecast(steps=30)
    forecast_index = pd.date_range(start=daily.index[-1] + pd.Timedelta(days=1), periods=30)
    forecast_series = pd.Series(forecast.values, index=forecast_index)

    # --- Forecast Plot ---
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily.index[-60:], daily["Daily_Consumption"].iloc[-60:],
            label="Historical (last 60 days)", color="#2c3e50")
    ax.plot(forecast_series.index, forecast_series.values,
            label="Forecast (30 days)", color="#e74c3c", linestyle="--", linewidth=2)
    ax.set_title("Energy Consumption Forecast — ARIMA (30 days)", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Consumption (kWh)")
    ax.legend()
    save_plot(fig, "17_arima_forecast.png")

    # Save forecast values
    forecast_series.to_csv(os.path.join(MODEL_DIR, "forecast_30days.csv"), header=["Forecast"])
    print("  ✔ Forecast saved to models/forecast_30days.csv")

except Exception as e:
    print(f"  ⚠ ARIMA failed: {e}")
    print("  Trying simpler ARIMA(1,1,1) ...")
    arima_model = ARIMA(daily["Daily_Consumption"], order=(1, 1, 1))
    arima_result = arima_model.fit()
    forecast = arima_result.forecast(steps=30)
    forecast_index = pd.date_range(start=daily.index[-1] + pd.Timedelta(days=1), periods=30)
    forecast_series = pd.Series(forecast.values, index=forecast_index)

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily.index[-60:], daily["Daily_Consumption"].iloc[-60:],
            label="Historical (last 60 days)", color="#2c3e50")
    ax.plot(forecast_series.index, forecast_series.values,
            label="Forecast (30 days)", color="#e74c3c", linestyle="--", linewidth=2)
    ax.set_title("Energy Consumption Forecast — ARIMA (30 days)", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Consumption (kWh)")
    ax.legend()
    save_plot(fig, "17_arima_forecast.png")
    forecast_series.to_csv(os.path.join(MODEL_DIR, "forecast_30days.csv"), header=["Forecast"])
    print("  ✔ Forecast saved")


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 12: MODEL SAVING                            ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 12: MODEL SAVING")
print("=" * 60)

# Find the best model (highest R²) from the AFTER FE results
best_model_name = results_after.loc[results_after["R²"].idxmax(), "Model"]
best_model = models_after[best_model_name]
best_r2 = results_after["R²"].max()

print(f"  Best model: {best_model_name} (R² = {best_r2:.4f})")

# Save model, column transformer, and feature names
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))
joblib.dump(ct_after, os.path.join(MODEL_DIR, "column_transformer.pkl"))
joblib.dump(feat_names_after, os.path.join(MODEL_DIR, "feature_names.pkl"))

# Save training metadata
metadata = {
    "best_model_name": best_model_name,
    "r2_score": float(best_r2),
    "n_features": len(feat_names_after),
    "feature_names": feat_names_after,
    "temp_column": temp_col,
}
joblib.dump(metadata, os.path.join(MODEL_DIR, "metadata.pkl"))

print("  ✔ Saved to models/:")
print("      best_model.pkl")
print("      column_transformer.pkl")
print("      feature_names.pkl")
print("      metadata.pkl")


# ╔═══════════════════════════════════════════════════════╗
# ║  SECTION 13: PREDICTION FUNCTION                     ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("SECTION 13: PREDICTION FUNCTION")
print("=" * 60)


def predict_energy(temperature, appliance_type, household_size, hour, season):
    """
    Predict energy consumption for a single input.

    Parameters:
    -----------
    temperature    : float  – Outdoor temperature in °C
    appliance_type : str    – e.g. 'Heater', 'AC', 'Fridge', etc.
    household_size : int    – Number of people in household
    hour           : int    – Hour of day (0–23)
    season         : str    – 'Winter', 'Spring', 'Summer', 'Fall'

    Returns:
    --------
    float – Predicted energy consumption in kWh
    """
    model_path = os.path.join(MODEL_DIR, "best_model.pkl")
    ct_path = os.path.join(MODEL_DIR, "column_transformer.pkl")
    meta_path = os.path.join(MODEL_DIR, "metadata.pkl")

    model = joblib.load(model_path)
    ct = joblib.load(ct_path)
    meta = joblib.load(meta_path)
    temp_column = meta["temp_column"]

    # Build a single-row DataFrame matching the training features
    row = {
        "Home ID": 0,
        "Appliance Type": appliance_type,
        temp_column: temperature,
        "Season": season,
        "Household Size": household_size,
        "Hour": hour,
        "Day": 15,
        "Month": 6,
        "Weekday": 2,
        "Peak_Hour": 1 if 18 <= hour <= 22 else 0,
        "Night_Usage": 1 if hour >= 23 or hour <= 5 else 0,
        "Temp_Squared": temperature ** 2,
        "Temp_x_HouseholdSize": temperature * household_size,
        "Rolling_Avg_3": 0.0,
        "Lag_1": 0.0,
        "Lag_2": 0.0,
        "Lag_3": 0.0,
    }

    input_df = pd.DataFrame([row])
    X_input = ct.transform(input_df)
    prediction = model.predict(X_input)[0]
    return round(float(prediction), 4)


# --- Quick Test ---
test_result = predict_energy(
    temperature=25.0,
    appliance_type="Heater",
    household_size=4,
    hour=19,
    season="Winter"
)
print(f"  Test prediction: {test_result} kWh")
print(f"  (Temperature=25°C, Appliance=Heater, HH Size=4, Hour=19, Season=Winter)")


# ╔═══════════════════════════════════════════════════════╗
# ║  PIPELINE COMPLETE                                   ║
# ╚═══════════════════════════════════════════════════════╝

print("\n" + "=" * 60)
print("✅ PIPELINE COMPLETE")
print("=" * 60)
print(f"  Plots:     {PLOT_DIR}")
print(f"  Models:    {MODEL_DIR}")
print(f"  Best:      {best_model_name} (R² = {best_r2:.4f})")
print("=" * 60)
