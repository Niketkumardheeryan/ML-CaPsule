import pandas as pd
import joblib

try:
    lr_model = joblib.load(
        '../../models/logistic_regression_model.joblib'
    )

    scaler = joblib.load(
        '../../models/logistic_regression_scaler.joblib'
    )

except FileNotFoundError:
    print("\nError: Model files not found.")
    print("Please run 'lr_training.py' first.")
    exit()

feature_names = [
    'rainfall',
    'temperature_c',
    'humidity',
    'water_level_m',
    'elevation_m'
]

def predict_flood():

    print("Please enter the following values:\n")

    try:
        rainfall = float(input("Rainfall (mm): "))
        temperature = float(input("Temperature (C): "))
        humidity = float(input("Humidity (%): "))
        water_level = float(input("Water Level (m): "))
        elevation = float(input("Elevation (m): "))

        new_data = pd.DataFrame(
            [[
                rainfall,
                temperature,
                humidity,
                water_level,
                elevation
            ]],
            columns=feature_names
        )

        new_data_scaled = scaler.transform(new_data)

        prediction = lr_model.predict(new_data_scaled)

        probability = lr_model.predict_proba(new_data_scaled)

        flood_probability = probability[0][1] * 100

        result = (
            "\nFlood is likely to occur."
            if prediction[0] == 1
            else "\nFlood is not likely to occur."
        )

        print(result)

        print(f"Flood Probability: {flood_probability:.2f}%\n")

    except ValueError:
        print("\nError: Please enter numeric values only.")

if __name__ == "__main__":
    predict_flood()