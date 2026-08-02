import pandas as pd
import joblib
import warnings

# Suppress a specific warning about feature names from scikit-learn
warnings.filterwarnings("ignore",category=UserWarning,module='sklearn')

try:
    #Load pre-trained model and scaler
    svm_model=joblib.load('../../models/svm_model.joblib')
    scaler=joblib.load('../../models/svm_scaler.joblib')
except FileNotFoundError:
    print("\nError: Model files not found.")
    print("Please run the 'train_model.py' script first to create them.")
    exit()
feature_names=['rainfall','temperature_c','humidity','water_level_m','elevation_m']

def predict_flood():
    print("Please enter the following values:")
    try:
        #rainfall = float(input("Enter Rainfall (e.g., 250): "))
        # temperature = float(input("Enter Temperature in Celsius (e.g., 32): "))
        # humidity = float(input("Enter Humidity in % (e.g., 85): "))
        # water_level = float(input("Enter Water Level in meters (e.g., 8.5): "))
        # elevation = float(input("Enter Elevation in meters (e.g., 500): "))
        rainfall=float(input("Rainfall (mm):"))
        temperature=float(input("Temperature (C): "))
        humidity=float(input("Humidity (%): "))
        water_level=float(input("Water Level (m): "))
        elevation=float(input("Elevation(m):"))
        new_data=pd.DataFrame(
            [[rainfall,temperature,humidity,water_level, elevation]],
            columns=feature_names)
        new_data_scaled=scaler.transform(new_data)
        prediction=svm_model.predict(new_data_scaled)
        result="\n\t1-Flood is likely to occur."if prediction[0]==1 else "\n\t0-Flood is not likely to occur."
        print(result,"\n")

    except ValueError:
        print("\nError: Invalid input. Please enter numeric values only.")
if __name__=="__main__":
    predict_flood()