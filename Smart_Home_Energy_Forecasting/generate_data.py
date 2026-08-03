import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_smart_home_data(num_rows=100000, num_homes=10, random_seed=42):
    np.random.seed(random_seed)
    
    # Calculate hours needed per home
    hours_per_home = int(np.ceil(num_rows / num_homes))
    start_date = datetime(2022, 1, 1, 0, 0, 0)
    
    # Home configurations
    homes_config = {
        f"Home_{i}": {
            "sqft": int(np.random.randint(1000, 4000)),
            "occupants": int(np.random.randint(1, 6)),
            "base_load": float(np.random.uniform(0.02, 0.08))
        }
        for i in range(num_homes)
    }
    
    data = []
    
    # Generate data
    for home_id, config in homes_config.items():
        sqft = config["sqft"]
        occupants = config["occupants"]
        base_load = config["base_load"]
        
        current_time = start_date
        for h in range(hours_per_home):
            # Temporal attributes
            hour = current_time.hour
            month = current_time.month
            day_of_week = current_time.weekday()
            is_weekend = 1 if day_of_week >= 5 else 0
            is_holiday = 1 if (is_weekend or (month == 12 and current_time.day in [24, 25, 31]) or (month == 1 and current_time.day == 1) or (month == 7 and current_time.day == 4)) else 0
            
            # Simulate Temperature (annual seasonality + daily variation + noise)
            # Base temp around 18°C, annual variation of 15°C, daily of 6°C
            annual_cycle = np.sin(2 * np.pi * (current_time.timetuple().tm_yday) / 365.0 - np.pi/2) # Peak in summer (July)
            daily_cycle = np.sin(2 * np.pi * (hour - 6) / 24.0) # Peak at 15:00
            
            temp = 18.0 + 15.0 * annual_cycle + 6.0 * daily_cycle + np.random.normal(0, 1.5)
            # Simulate Humidity (inversely proportional to temp + daily cycle + noise)
            humidity = 70.0 - 1.2 * (temp - 18.0) - 10.0 * daily_cycle + np.random.normal(0, 5.0)
            humidity = np.clip(humidity, 15.0, 98.0)
            
            # Simulate Appliance Energy Consumption (in kWh)
            # 1. Fridge: baseline cyclic load
            fridge = 0.08 + 0.03 * np.sin(2 * np.pi * hour / 6.0) + np.random.normal(0, 0.01)
            fridge = max(0.04, fridge)
            
            # 2. HVAC: depends on temperature deviation from comfort zone (20°C - 23°C)
            hvac = 0.0
            if temp < 18.0:
                hvac = 0.12 * (18.0 - temp) * (sqft / 2000.0) + np.random.normal(0, 0.05)
            elif temp > 24.0:
                hvac = 0.15 * (temp - 24.0) * (sqft / 2000.0) + np.random.normal(0, 0.05)
            hvac = max(0.0, hvac + 0.05 * occupants) # baseline circulation
            
            # 3. Lighting: active during morning and evening
            lighting = 0.01
            if 6 <= hour <= 8:
                lighting = 0.08 * (sqft / 1500.0) + np.random.normal(0, 0.01)
            elif 18 <= hour <= 23:
                lighting = 0.15 * (sqft / 1500.0) + np.random.normal(0, 0.02)
            else:
                lighting = 0.01 + np.random.normal(0, 0.003)
            lighting = max(0.005, lighting)
            
            # 4. Laundry: laundry events occur randomly, mostly on weekends
            laundry = 0.0
            if is_holiday and np.random.rand() < 0.25 and 9 <= hour <= 17:
                laundry = 0.8 + np.random.normal(0, 0.15)
            elif not is_holiday and np.random.rand() < 0.08 and 18 <= hour <= 21:
                laundry = 0.6 + np.random.normal(0, 0.10)
            
            # 5. Entertainment (TV, PC, Console): higher in evenings and holidays
            entertainment = 0.03
            if 17 <= hour <= 23:
                entertainment = 0.15 * occupants + np.random.normal(0, 0.03)
            elif is_holiday and 10 <= hour <= 17:
                entertainment = 0.10 * occupants + np.random.normal(0, 0.02)
            entertainment = max(0.01, entertainment)
            
            # Total energy is sum + baseline noise + background
            total_energy = base_load + fridge + hvac + lighting + laundry + entertainment + np.random.normal(0, 0.02)
            total_energy = max(0.05, total_energy)
            
            # Energy limit target (simulated daily/hourly budget)
            energy_limit = 0.3 + (sqft / 1500.0) * 0.2 + occupants * 0.1
            
            data.append({
                "Timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Home_ID": home_id,
                "Temperature": round(temp, 2),
                "Humidity": round(humidity, 2),
                "Square_Footage": sqft,
                "Occupants": occupants,
                "Appliance_Fridge_kWh": round(fridge, 4),
                "Appliance_HVAC_kWh": round(hvac, 4),
                "Appliance_Lighting_kWh": round(lighting, 4),
                "Appliance_Laundry_kWh": round(laundry, 4),
                "Appliance_Entertainment_kWh": round(entertainment, 4),
                "Total_Energy_kWh": round(total_energy, 4),
                "Energy_Limit_kWh": round(energy_limit, 3),
                "Is_Holiday": is_holiday,
                "Day_Of_Week": day_of_week,
                "Hour_Of_Day": hour
            })
            
            current_time += timedelta(hours=1)
            
    df = pd.DataFrame(data)
    # Shuffle or sort by Timestamp to make it realistic
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(by=['Timestamp', 'Home_ID']).reset_index(drop=True)
    
    # Trim to exactly num_rows
    if len(df) > num_rows:
        df = df.iloc[:num_rows]
        
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    print("Generating 100k smart home energy rows...")
    df = generate_smart_home_data()
    df.to_csv("data/smart_home_energy_dataset.csv", index=False)
    print(f"Dataset saved to data/smart_home_energy_dataset.csv. Shape: {df.shape}")
