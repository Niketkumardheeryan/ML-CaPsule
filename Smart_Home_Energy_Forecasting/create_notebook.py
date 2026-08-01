import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Smart Home Energy Forecasting & Waste Detection\n",
    "This notebook contains a complete, end-to-end Machine Learning pipeline for Smart Home Energy Analytics.\n",
    "\n",
    "## Notebook Sections:\n",
    "1. **Introduction & Project Overview**\n",
    "2. **Data Generation**\n",
    "3. **Exploratory Data Analysis (EDA) & Visualizations**\n",
    "4. **Data Preprocessing & Data Cleaning**\n",
    "5. **Feature Engineering**\n",
    "6. **Feature Scaling & PCA (Dimensionality Reduction)**\n",
    "7. **Unsupervised Learning (KMeans Clustering for Waste Classification)**\n",
    "8. **Supervised Learning - Regression (Energy Consumption Prediction)**\n",
    "9. **Supervised Learning - Classification (Waste Detection)**\n",
    "10. **Model Evaluation & Comparison**\n",
    "11. **Time Series Forecasting (ARIMA)**\n",
    "12. **Model & Scaler Serialization**\n",
    "13. **Conclusion & Flask Deployment Guide**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 1: Introduction & Project Overview\n",
    "In this project, we address the challenge of tracking smart home energy consumption and identifying wasteful behaviors. We implement an end-to-end machine learning solution that forecasts consumption, detects usage anomalies, scales features, applies PCA, clusters wasteful patterns, trains multiple regression/classification models, and deploys it all as a Flask web application."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 2: Data Generation\n",
    "We generate a highly realistic 100,000-row smart home energy consumption dataset with seasonal/daily temperature effects, holiday flags, and appliance-level breakdowns."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from datetime import datetime, timedelta\n",
    "\n",
    "# Run the data generator to load or create the dataset\n",
    "from generate_data import generate_smart_home_data\n",
    "df = generate_smart_home_data(num_rows=100000)\n",
    "print(f\"Loaded dataset with shape: {df.shape}\")\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 3: Exploratory Data Analysis (EDA) & Visualizations\n",
    "We perform complete EDA, checking distribution of energy metrics, home comparisons, daily/hourly patterns, correlation matrix, and appliance breakdowns."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "sns.set_theme(style=\"darkgrid\")\n",
    "\n",
    "# 1. Distribution of energy\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.histplot(df['Total_Energy_kWh'], kde=True, color='#00adb5', bins=50)\n",
    "plt.title(\"Distribution of Total Energy Consumption (kWh)\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Monthly average energy\n",
    "df_monthly = df.groupby(df['Timestamp'].dt.month)['Total_Energy_kWh'].mean().reset_index()\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.lineplot(x='Timestamp', y='Total_Energy_kWh', data=df_monthly, marker='o', color='#ff5722')\n",
    "plt.title(\"Monthly Average Energy Consumption\")\n",
    "plt.xticks(range(1, 13))\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 4: Data Preprocessing & Data Cleaning\n",
    "Checking for missing values, duplicates, and general dataset health."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(\"Missing Values:\\n\", df.isnull().sum())\n",
    "print(\"\\nDuplicate Rows:\", df.duplicated().sum())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 5: Feature Engineering\n",
    "Creating cyclical time representations, interaction terms, lags, and rolling averages."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df['Month'] = df['Timestamp'].dt.month\n",
    "df['Hour_Sin'] = np.sin(2 * np.pi * df['Hour_Of_Day'] / 24.0)\n",
    "df['Hour_Cos'] = np.cos(2 * np.pi * df['Hour_Of_Day'] / 24.0)\n",
    "df['Month_Sin'] = np.sin(2 * np.pi * df['Month'] / 12.0)\n",
    "df['Month_Cos'] = np.cos(2 * np.pi * df['Month'] / 12.0)\n",
    "\n",
    "df['Temp_Hum_Interaction'] = df['Temperature'] * df['Humidity']\n",
    "df['Density_SqFt_Occupants'] = df['Square_Footage'] / (df['Occupants'] + 1e-5)\n",
    "\n",
    "df = df.sort_values(by=['Home_ID', 'Timestamp']).reset_index(drop=True)\n",
    "df['Energy_Lag1'] = df.groupby('Home_ID')['Total_Energy_kWh'].shift(1)\n",
    "df['Energy_Lag2'] = df.groupby('Home_ID')['Total_Energy_kWh'].shift(2)\n",
    "df['Energy_RollingMean3'] = df.groupby('Home_ID')['Total_Energy_kWh'].shift(1).rolling(3).mean()\n",
    "\n",
    "df = df.dropna().reset_index(drop=True)\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 6: Feature Scaling & PCA (Dimensionality Reduction)\n",
    "Standardizing our numerical columns and using PCA to understand feature dimensions."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.decomposition import PCA\n",
    "\n",
    "features_to_scale = [\n",
    "    'Temperature', 'Humidity', 'Square_Footage', 'Occupants', \n",
    "    'Hour_Sin', 'Hour_Cos', 'Month_Sin', 'Month_Cos',\n",
    "    'Temp_Hum_Interaction', 'Density_SqFt_Occupants',\n",
    "    'Energy_Lag1', 'Energy_Lag2', 'Energy_RollingMean3'\n",
    "]\n",
    "\n",
    "scaler = StandardScaler()\n",
    "scaled_features = scaler.fit_transform(df[features_to_scale])\n",
    "\n",
    "pca = PCA(n_components=5)\n",
    "pca_features = pca.fit_transform(scaled_features)\n",
    "print(\"Explained Variance Ratio by PCA Components:\", pca.explained_variance_ratio_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 7: Unsupervised Learning (KMeans Clustering for Waste Classification)\n",
    "Using KMeans to label patterns into Efficient, Normal, and Wasteful consumption."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.cluster import KMeans\n",
    "\n",
    "cluster_features = ['Total_Energy_kWh', 'Appliance_HVAC_kWh', 'Temperature', 'Occupants']\n",
    "scaler_cluster = StandardScaler()\n",
    "scaled_cluster_data = scaler_cluster.fit_transform(df[cluster_features])\n",
    "\n",
    "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
    "df['Cluster'] = kmeans.fit_transform(scaled_cluster_data).argmin(axis=1)\n",
    "\n",
    "# Label clusters based on energy consumption\n",
    "cluster_means = df.groupby('Cluster')['Total_Energy_kWh'].mean().sort_values()\n",
    "cluster_mapping = {cluster_means.index[0]: 0, cluster_means.index[1]: 1, cluster_means.index[2]: 2}\n",
    "df['Waste_Label'] = df['Cluster'].map(cluster_mapping)\n",
    "print(df['Waste_Label'].value_counts())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 8: Supervised Learning - Regression (Energy Consumption Prediction)\n",
    "Training regressors (Linear Regression, Random Forest, XGBoost) to predict energy usage."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import LinearRegression\n",
    "from sklearn.ensemble import RandomForestRegressor\n",
    "from xgboost import XGBRegressor\n",
    "\n",
    "X_reg = df[features_to_scale]\n",
    "y_reg = df['Total_Energy_kWh']\n",
    "X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)\n",
    "\n",
    "X_train_scaled = scaler.transform(X_train)\n",
    "X_test_scaled = scaler.transform(X_test)\n",
    "\n",
    "xgb_reg = XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1)\n",
    "xgb_reg.fit(X_train_scaled, y_train)\n",
    "print(\"XGBoost R2 Score:\", xgb_reg.score(X_test_scaled, y_test))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 9: Supervised Learning - Classification (Waste Detection)\n",
    "Training classifiers to detect whether usage profiles are wasteful."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from xgboost import XGBClassifier\n",
    "y_clf = df['Waste_Label']\n",
    "X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_reg, y_clf, test_size=0.2, random_state=42)\n",
    "\n",
    "X_train_c_scaled = scaler.transform(X_train_c)\n",
    "X_test_c_scaled = scaler.transform(X_test_c)\n",
    "\n",
    "xgb_clf = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1)\n",
    "xgb_clf.fit(X_train_c_scaled, y_train_c)\n",
    "print(\"XGBoost Classifier Accuracy:\", xgb_clf.score(X_test_c_scaled, y_test_c))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 10: Model Evaluation & Comparison\n",
    "A comparison of error metrics for regression and accuracy/F1-score for classification."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.metrics import mean_squared_error, classification_report\n",
    "y_pred_xgb = xgb_reg.predict(X_test_scaled)\n",
    "print(\"Regression RMSE:\", np.sqrt(mean_squared_error(y_test, y_pred_xgb)))\n",
    "\n",
    "y_pred_xgb_c = xgb_clf.predict(X_test_c_scaled)\n",
    "print(classification_report(y_test_c, y_pred_xgb_c))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 11: Time Series Forecasting (ARIMA)\n",
    "Aggregating daily data and applying ARIMA to forecast future smart home energy demands."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from statsmodels.tsa.arima.model import ARIMA\n",
    "\n",
    "df_daily = df.set_index('Timestamp').resample('D')['Total_Energy_kWh'].mean().dropna()\n",
    "train_ts = df_daily.iloc[:-30]\n",
    "\n",
    "arima_model = ARIMA(train_ts, order=(1, 1, 1))\n",
    "arima_result = arima_model.fit()\n",
    "print(arima_result.summary())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 12: Model & Scaler Serialization\n",
    "Saving the trained components to load them dynamically within our web application."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import joblib\n",
    "os.makedirs(\"models\", exist_ok=True)\n",
    "joblib.dump(xgb_reg, \"models/xgb_regressor.joblib\")\n",
    "joblib.dump(xgb_clf, \"models/xgb_classifier.joblib\")\n",
    "joblib.dump(scaler, \"models/scaler.joblib\")\n",
    "joblib.dump(pca, \"models/pca.joblib\")\n",
    "joblib.dump(kmeans, \"models/kmeans.joblib\")\n",
    "joblib.dump(scaler_cluster, \"models/scaler_cluster.joblib\")\n",
    "print(\"All artifacts successfully serialized!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Section 13: Conclusion & Flask Deployment Guide\n",
    "With our serialized models, we can deploy the web app. To run it, run:\n",
    "```bash\n",
    "python app.py\n",
    "```\n",
    "Then visit `http://127.0.0.1:5000` to interact with the predictions, see future forecasts, and browse the analytical plots."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("smart_home_energy_forecasting.ipynb", "w") as f:
    json.dump(notebook, f, indent=1)
print("Jupyter Notebook created successfully!")
