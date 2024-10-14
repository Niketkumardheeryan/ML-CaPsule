import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load the dataset
data = pd.read_csv('your_dataset.csv')

# 2. Inspect the first few rows
print(data.head())

# 3. Prepare features (X) and target (y)
X = data[['carbohydrates', 'protein', 'fat']]
y = data['calories']

# 4. Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Scale the feature data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 6. Train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Make predictions on the test set
y_pred = model.predict(X_test)

# 8. Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

# 9. Predict calories for a new food [carbohydrates, protein, fat]
new_food = [[30, 15, 10]]
new_food_scaled = scaler.transform(new_food)
predicted_calories = model.predict(new_food_scaled)
print(f"Predicted Calories: {predicted_calories[0]:.2f}")
