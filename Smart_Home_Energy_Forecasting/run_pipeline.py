import os
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, confusion_matrix
)
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Create output directories
os.makedirs("models", exist_ok=True)
os.makedirs("static/images/plots", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Set style
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    'figure.facecolor': '#121212',
    'axes.facecolor': '#1e1e1e',
    'text.color': '#e0e0e0',
    'axes.labelcolor': '#e0e0e0',
    'xtick.color': '#b0b0b0',
    'ytick.color': '#b0b0b0',
    'grid.color': '#333333',
    'font.size': 10
})

print("Loading dataset...")
df = pd.read_csv("data/smart_home_energy_dataset.csv")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# ----------------- SECTION 3: EDA & PLOTS -----------------
print("Generating 17+ EDA and Analysis plots...")

# Plot 1: Distplot of Total_Energy_kWh
plt.figure(figsize=(10, 5))
sns.histplot(df['Total_Energy_kWh'], kde=True, color='#00adb5', bins=50)
plt.title("Distribution of Total Energy Consumption (kWh)", color='#ffffff')
plt.xlabel("Total Energy (kWh)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("static/images/plots/plot1_dist_total_energy.png", facecolor='#121212')
plt.close()

# Plot 2: Boxplot of Total_Energy_kWh by Home_ID
plt.figure(figsize=(12, 5))
sns.boxplot(x='Home_ID', y='Total_Energy_kWh', data=df, palette='viridis')
plt.title("Energy Consumption Distribution by Home", color='#ffffff')
plt.xlabel("Home ID")
plt.ylabel("Total Energy (kWh)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("static/images/plots/plot2_box_energy_by_home.png", facecolor='#121212')
plt.close()

# Plot 3: Boxplot of Total_Energy_kWh by Hour_Of_Day
plt.figure(figsize=(12, 5))
sns.boxplot(x='Hour_Of_Day', y='Total_Energy_kWh', data=df, palette='magma')
plt.title("Energy Consumption by Hour of Day", color='#ffffff')
plt.xlabel("Hour of Day")
plt.ylabel("Total Energy (kWh)")
plt.tight_layout()
plt.savefig("static/images/plots/plot3_box_energy_by_hour.png", facecolor='#121212')
plt.close()

# Plot 4: Boxplot of Total_Energy_kWh by Day_Of_Week
plt.figure(figsize=(10, 5))
sns.boxplot(x='Day_Of_Week', y='Total_Energy_kWh', data=df, palette='coolwarm')
plt.title("Energy Consumption by Day of Week (0=Monday, 6=Sunday)", color='#ffffff')
plt.xlabel("Day of Week")
plt.ylabel("Total Energy (kWh)")
plt.tight_layout()
plt.savefig("static/images/plots/plot4_box_energy_by_dayofweek.png", facecolor='#121212')
plt.close()

# Plot 5: Monthly average energy consumption (line plot)
df_monthly = df.groupby(df['Timestamp'].dt.month)['Total_Energy_kWh'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(x='Timestamp', y='Total_Energy_kWh', data=df_monthly, marker='o', color='#ff5722', linewidth=2.5)
plt.title("Monthly Average Energy Consumption", color='#ffffff')
plt.xlabel("Month")
plt.ylabel("Average Energy (kWh)")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.savefig("static/images/plots/plot5_line_monthly_avg_energy.png", facecolor='#121212')
plt.close()

# Plot 6: Hourly average energy consumption (line plot)
df_hourly = df.groupby('Hour_Of_Day')['Total_Energy_kWh'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(x='Hour_Of_Day', y='Total_Energy_kWh', data=df_hourly, marker='s', color='#4caf50', linewidth=2.5)
plt.title("Hourly Average Energy Consumption Profile", color='#ffffff')
plt.xlabel("Hour of Day")
plt.ylabel("Average Energy (kWh)")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig("static/images/plots/plot6_line_hourly_avg_energy.png", facecolor='#121212')
plt.close()

# Plot 7: Temperature vs. Total Energy
plt.figure(figsize=(10, 6))
# Subsample for scatter plot clarity
sample_df = df.sample(n=2000, random_state=42) if len(df) > 2000 else df
sns.scatterplot(x='Temperature', y='Total_Energy_kWh', data=sample_df, hue='Hour_Of_Day', palette='Spectral', alpha=0.6)
plt.title("Temperature vs. Total Energy Consumption", color='#ffffff')
plt.xlabel("Temperature (°C)")
plt.ylabel("Total Energy (kWh)")
plt.tight_layout()
plt.savefig("static/images/plots/plot7_scatter_temp_vs_energy.png", facecolor='#121212')
plt.close()

# Plot 8: Correlation Heatmap of numerical features
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
# Remove static ID indexes or raw dates if any
plt.figure(figsize=(12, 10))
sns.heatmap(df[num_cols].corr(), annot=True, cmap='mako', fmt='.2f', linewidths=0.5, cbar=True)
plt.title("Correlation Matrix of Features", color='#ffffff')
plt.tight_layout()
plt.savefig("static/images/plots/plot8_heatmap_correlation.png", facecolor='#121212')
plt.close()

# Plot 9: Distribution of appliance energy consumption
appliances = [c for c in df.columns if 'Appliance_' in c]
df_appliances = df[appliances].mean().reset_index()
df_appliances.columns = ['Appliance', 'Average_Consumption_kWh']
df_appliances['Appliance'] = df_appliances['Appliance'].str.replace('Appliance_', '').str.replace('_kWh', '')
plt.figure(figsize=(10, 5))
sns.barplot(x='Appliance', y='Average_Consumption_kWh', data=df_appliances, palette='deep')
plt.title("Average Energy Consumption by Appliance Type", color='#ffffff')
plt.xlabel("Appliance")
plt.ylabel("Average Energy (kWh)")
plt.tight_layout()
plt.savefig("static/images/plots/plot9_bar_appliance_distribution.png", facecolor='#121212')
plt.close()

# Plot 10: Pairplot of major features
plt.figure(figsize=(10, 10))
pair_features = ['Temperature', 'Humidity', 'Total_Energy_kWh', 'Appliance_HVAC_kWh']
g = sns.pairplot(sample_df[pair_features], diag_kind='kde', plot_kws={'alpha': 0.5, 'color': '#ffb400'})
g.fig.suptitle("Pairplot of Key Environmental and Energy Variables", color='#ffffff', y=1.02)
g.fig.patch.set_facecolor('#121212')
for ax in g.axes.flatten():
    ax.set_facecolor('#1e1e1e')
plt.tight_layout()
plt.savefig("static/images/plots/plot10_pairplot_key_features.png", facecolor='#121212')
plt.close()


# ----------------- SECTION 5: FEATURE ENGINEERING -----------------
print("Engineering features...")
df['Month'] = df['Timestamp'].dt.month
# Cosine & Sine encoding of cyclic features
df['Hour_Sin'] = np.sin(2 * np.pi * df['Hour_Of_Day'] / 24.0)
df['Hour_Cos'] = np.cos(2 * np.pi * df['Hour_Of_Day'] / 24.0)
df['Month_Sin'] = np.sin(2 * np.pi * df['Month'] / 12.0)
df['Month_Cos'] = np.cos(2 * np.pi * df['Month'] / 12.0)

# Interaction terms
df['Temp_Hum_Interaction'] = df['Temperature'] * df['Humidity']
df['Density_SqFt_Occupants'] = df['Square_Footage'] / (df['Occupants'] + 1e-5)

# Lags (using group lags to avoid leakage across homes)
df = df.sort_values(by=['Home_ID', 'Timestamp']).reset_index(drop=True)
df['Energy_Lag1'] = df.groupby('Home_ID')['Total_Energy_kWh'].shift(1)
df['Energy_Lag2'] = df.groupby('Home_ID')['Total_Energy_kWh'].shift(2)
df['Energy_RollingMean3'] = df.groupby('Home_ID')['Total_Energy_kWh'].shift(1).rolling(3).mean()

# Fill NaNs created by shifts
df = df.dropna().reset_index(drop=True)

# ----------------- SECTION 6: FEATURE SCALING & PCA -----------------
print("Applying Scaling and PCA...")
features_to_scale = [
    'Temperature', 'Humidity', 'Square_Footage', 'Occupants', 
    'Hour_Sin', 'Hour_Cos', 'Month_Sin', 'Month_Cos',
    'Temp_Hum_Interaction', 'Density_SqFt_Occupants',
    'Energy_Lag1', 'Energy_Lag2', 'Energy_RollingMean3'
]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[features_to_scale])
joblib.dump(scaler, "models/scaler.joblib")

pca = PCA(n_components=5)
pca_features = pca.fit_transform(scaled_features)
joblib.dump(pca, "models/pca.joblib")

# Plot 11: PCA Explained Variance Scree Plot
plt.figure(figsize=(8, 4))
plt.bar(range(1, 6), pca.explained_variance_ratio_, alpha=0.7, align='center', label='Individual explained variance', color='#00adb5')
plt.step(range(1, 6), np.cumsum(pca.explained_variance_ratio_), where='mid', label='Cumulative explained variance', color='#e23e57')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal component index')
plt.title('PCA Explained Variance Scree Plot', color='#ffffff')
plt.xticks(range(1, 6))
plt.legend(loc='best')
plt.tight_layout()
plt.savefig("static/images/plots/plot11_pca_scree.png", facecolor='#121212')
plt.close()

# Plot 12: 2D PCA Projection
plt.figure(figsize=(10, 6))
plt.scatter(pca_features[:2000, 0], pca_features[:2000, 1], c=df['Total_Energy_kWh'][:2000], cmap='viridis', alpha=0.7)
plt.colorbar(label='Total Energy (kWh)')
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.title('PCA 2D Projection Colored by Energy Consumption', color='#ffffff')
plt.tight_layout()
plt.savefig("static/images/plots/plot12_pca_2d.png", facecolor='#121212')
plt.close()


# ----------------- SECTION 7: KMEANS CLUSTERING (WASTE CLASSIFICATION) -----------------
print("Running KMeans Clustering for waste classification...")
# Cluster based on energy features and environmental state
cluster_features = ['Total_Energy_kWh', 'Appliance_HVAC_kWh', 'Temperature', 'Occupants']
scaler_cluster = StandardScaler()
scaled_cluster_data = scaler_cluster.fit_transform(df[cluster_features])

# Plot 13: KMeans Elbow Curve
distortions = []
K = range(1, 8)
for k in K:
    kmeanModel = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeanModel.fit(scaled_cluster_data[:10000]) # Sample for speed
    distortions.append(kmeanModel.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(K, distortions, 'bx-', color='#ff5722')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k', color='#ffffff')
plt.tight_layout()
plt.savefig("static/images/plots/plot13_kmeans_elbow.png", facecolor='#121212')
plt.close()

# Fit optimal KMeans (k=3)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_transform(scaled_cluster_data).argmin(axis=1) # Let's label cluster IDs
joblib.dump(kmeans, "models/kmeans.joblib")
joblib.dump(scaler_cluster, "models/scaler_cluster.joblib")

# Determine cluster semantics (Efficient, Normal, Wasteful)
# We look at mean energy consumption per cluster
cluster_means = df.groupby('Cluster')['Total_Energy_kWh'].mean().sort_values()
# cluster_means index 0: Efficient, 1: Normal, 2: Wasteful
cluster_mapping = {
    cluster_means.index[0]: 0, # Efficient
    cluster_means.index[1]: 1, # Normal
    cluster_means.index[2]: 2  # Wasteful
}
df['Waste_Label'] = df['Cluster'].map(cluster_mapping)

# Plot 14: KMeans cluster visualization on PCA space
plt.figure(figsize=(10, 6))
scatter = plt.scatter(pca_features[:2000, 0], pca_features[:2000, 1], c=df['Waste_Label'][:2000], cmap='Set1', alpha=0.7)
plt.legend(*scatter.legend_elements(), title="Usage Profile\n(0=Eff, 1=Norm, 2=Waste)")
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.title('KMeans Clusters Visualized on PCA Space', color='#ffffff')
plt.tight_layout()
plt.savefig("static/images/plots/plot14_kmeans_pca_scatter.png", facecolor='#121212')
plt.close()

# Plot 15: Wasteful vs Efficient Boxplot
plt.figure(figsize=(8, 5))
sns.boxplot(x='Waste_Label', y='Total_Energy_kWh', data=df, palette='Set2')
plt.title("Total Energy Consumption across Classified Profiles", color='#ffffff')
plt.xlabel("Usage Profile (0=Efficient, 1=Normal, 2=Wasteful)")
plt.ylabel("Total Energy (kWh)")
plt.tight_layout()
plt.savefig("static/images/plots/plot15_waste_profile_box.png", facecolor='#121212')
plt.close()


# ----------------- SECTION 8: REGRESSION (ENERGY PREDICTION) -----------------
print("Training regression models...")
X_reg = df[features_to_scale]
y_reg = df['Total_Energy_kWh']

X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

# Scale train/test
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 1. Linear Regression
lr_reg = LinearRegression()
lr_reg.fit(X_train_scaled, y_train)
y_pred_lr = lr_reg.predict(X_test_scaled)

# 2. Random Forest Regressor
rf_reg = RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1)
rf_reg.fit(X_train_scaled, y_train)
y_pred_rf = rf_reg.predict(X_test_scaled)

# 3. XGBoost Regressor
xgb_reg = XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1)
xgb_reg.fit(X_train_scaled, y_train)
y_pred_xgb = xgb_reg.predict(X_test_scaled)

# Save best regressor (XGBoost usually, let's save both)
joblib.dump(xgb_reg, "models/xgb_regressor.joblib")
joblib.dump(rf_reg, "models/rf_regressor.joblib")

# Evaluate Regressors
reg_results = {
    'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
    'RMSE': [
        np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        np.sqrt(mean_squared_error(y_test, y_pred_xgb))
    ],
    'MAE': [
        mean_absolute_error(y_test, y_pred_lr),
        mean_absolute_error(y_test, y_pred_rf),
        mean_absolute_error(y_test, y_pred_xgb)
    ],
    'R2': [
        r2_score(y_test, y_pred_lr),
        r2_score(y_test, y_pred_rf),
        r2_score(y_test, y_pred_xgb)
    ]
}
df_reg_metrics = pd.DataFrame(reg_results)
print("Regression metrics:")
print(df_reg_metrics)

# Plot 16: Regressor Model Comparison
plt.figure(figsize=(10, 5))
x = np.arange(len(df_reg_metrics['Model']))
width = 0.35
plt.bar(x - width/2, df_reg_metrics['RMSE'], width, label='RMSE', color='#ff5722')
plt.bar(x + width/2, df_reg_metrics['MAE'], width, label='MAE', color='#00adb5')
plt.ylabel('Error Rate')
plt.title('Regression Models Error Comparison', color='#ffffff')
plt.xticks(x, df_reg_metrics['Model'])
plt.legend()
plt.tight_layout()
plt.savefig("static/images/plots/plot16_reg_comparison.png", facecolor='#121212')
plt.close()


# ----------------- SECTION 9: CLASSIFICATION (WASTE DETECTION) -----------------
print("Training classification models...")
y_clf = df['Waste_Label']
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_reg, y_clf, test_size=0.2, random_state=42)

# Scale
X_train_c_scaled = scaler.transform(X_train_c)
X_test_c_scaled = scaler.transform(X_test_c)

# 1. Logistic Regression
lr_clf = LogisticRegression(max_iter=1000, random_state=42)
lr_clf.fit(X_train_c_scaled, y_train_c)
y_pred_lr_c = lr_clf.predict(X_test_c_scaled)

# 2. Random Forest Classifier
rf_clf = RandomForestClassifier(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1)
rf_clf.fit(X_train_c_scaled, y_train_c)
y_pred_rf_c = rf_clf.predict(X_test_c_scaled)

# 3. XGBoost Classifier
xgb_clf = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1)
xgb_clf.fit(X_train_c_scaled, y_train_c)
y_pred_xgb_c = xgb_clf.predict(X_test_c_scaled)

joblib.dump(xgb_clf, "models/xgb_classifier.joblib")

# Evaluate Classifiers
clf_results = {
    'Model': ['Logistic Regression', 'Random Forest', 'XGBoost'],
    'Accuracy': [
        accuracy_score(y_test_c, y_pred_lr_c),
        accuracy_score(y_test_c, y_pred_rf_c),
        accuracy_score(y_test_c, y_pred_xgb_c)
    ],
    'F1_Macro': [
        f1_score(y_test_c, y_pred_lr_c, average='macro'),
        f1_score(y_test_c, y_pred_rf_c, average='macro'),
        f1_score(y_test_c, y_pred_xgb_c, average='macro')
    ]
}
df_clf_metrics = pd.DataFrame(clf_results)
print("Classification metrics:")
print(df_clf_metrics)

# Plot 17: Classifier Model Comparison
plt.figure(figsize=(10, 5))
x_clf = np.arange(len(df_clf_metrics['Model']))
plt.bar(x_clf - width/2, df_clf_metrics['Accuracy'], width, label='Accuracy', color='#4caf50')
plt.bar(x_clf + width/2, df_clf_metrics['F1_Macro'], width, label='F1 Macro', color='#ffb400')
plt.ylabel('Score')
plt.title('Classification Models Performance Comparison', color='#ffffff')
plt.xticks(x_clf, df_clf_metrics['Model'])
plt.ylim(0, 1.05)
plt.legend()
plt.tight_layout()
plt.savefig("static/images/plots/plot17_clf_comparison.png", facecolor='#121212')
plt.close()


# ----------------- SECTION 11: TIME SERIES FORECASTING (ARIMA) -----------------
print("Fitting ARIMA time series model...")
# Resample to daily average of all homes
df_daily = df.set_index('Timestamp').resample('D')['Total_Energy_kWh'].mean().dropna()

# Check stationarity
adf_result = adfuller(df_daily)
print(f"ADF Statistic: {adf_result[0]}")
print(f"p-value: {adf_result[1]}")

# Train-test split for ARIMA (last 30 days as test)
train_ts = df_daily.iloc[:-30]
test_ts = df_daily.iloc[-30:]

# Simple ARIMA(1,1,1) model for quick execution and stability
arima_model = ARIMA(train_ts, order=(1, 1, 1))
arima_result = arima_model.fit()
joblib.dump(arima_result, "models/arima_model.joblib")

# Plot 18: ARIMA Actual vs Fitted
plt.figure(figsize=(12, 5))
plt.plot(train_ts.index[-90:], train_ts.values[-90:], label='Actual (Train)', color='#00adb5')
plt.plot(train_ts.index[-90:], arima_result.fittedvalues[-90:], label='Fitted Values', color='#ff5722', linestyle='--')
plt.title("ARIMA In-Sample Fitted Values (Last 90 Days of Training)", color='#ffffff')
plt.xlabel("Date")
plt.ylabel("Daily Average Energy (kWh)")
plt.legend()
plt.tight_layout()
plt.savefig("static/images/plots/plot18_arima_fitted.png", facecolor='#121212')
plt.close()

# Plot 19: ARIMA Forecast
forecast_steps = 30
forecast = arima_result.get_forecast(steps=forecast_steps)
forecast_mean = forecast.predicted_mean
forecast_ci = forecast.conf_int()

plt.figure(figsize=(12, 5))
plt.plot(df_daily.index[-60:], df_daily.values[-60:], label='Actual Daily Energy', color='#00adb5')
plt.plot(test_ts.index, forecast_mean, label='Forecast', color='#ffb400', linewidth=2)
plt.fill_between(test_ts.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='#ffb400', alpha=0.15, label='95% Confidence Interval')
plt.title("ARIMA Out-of-Sample Energy Forecast vs. Actuals", color='#ffffff')
plt.xlabel("Date")
plt.ylabel("Daily Average Energy (kWh)")
plt.legend()
plt.tight_layout()
plt.savefig("static/images/plots/plot19_arima_forecast.png", facecolor='#121212')
plt.close()

print("Pipeline execution completed successfully. All models, scalers, and plots generated!")
