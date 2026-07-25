import pandas as pd
import joblib


try:
    rf_model = joblib.load(
        '../../models/random_forest_model.joblib'
    )

    scaler = joblib.load(
        '../../models/random_forest_scaler.joblib'
    )

except FileNotFoundError:
    print("\nError: Model files not found.")
    print("Please run 'rf_training.py' first.")
    exit()
    
    


feature_names = [
    'rainfall',
    'temperature_c',
    'humidity',
    'water_level_m',
    'elevation_m'
]


def predict_flood():

    print("Please enter the following values:")

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

        prediction = rf_model.predict(new_data_scaled)


        result = (
            "\n1 - Flood is likely to occur."
            if prediction[0] == 1
            else "\n0 - Flood is not likely to occur."
        )

        print(result, "\n")


    except ValueError:

        print(
            "\nError: Invalid input."
            " Please enter numeric values only."
        )


if __name__ == "__main__":
    predict_flood()