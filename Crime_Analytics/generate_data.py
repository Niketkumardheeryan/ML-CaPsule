import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_crime_dataset(num_records=2500, random_state=42):
    np.random.seed(random_state)
    
    districts = [
        {"id": "D1-Downtown", "base_lat": 40.7128, "base_lon": -74.0060, "risk_mult": 1.4},
        {"id": "D2-Northside", "base_lat": 40.7589, "base_lon": -73.9851, "risk_mult": 1.1},
        {"id": "D3-WestEnd", "base_lat": 40.7306, "base_lon": -74.0021, "risk_mult": 0.8},
        {"id": "D4-EastHarbor", "base_lat": 40.7831, "base_lon": -73.9712, "risk_mult": 1.3},
        {"id": "D5-SouthPark", "base_lat": 40.6782, "base_lon": -73.9442, "risk_mult": 0.9},
        {"id": "D6-Suburbs", "base_lat": 40.6501, "base_lon": -73.9496, "risk_mult": 0.5}
    ]
    
    crime_types = [
        {"category": "Theft/Larceny", "severity": 3, "weight": 0.30, "loc_types": ["Commercial", "Street", "Transit"]},
        {"category": "Burglary", "severity": 5, "weight": 0.20, "loc_types": ["Residence", "Storefront"]},
        {"category": "Vehicle Theft", "severity": 6, "weight": 0.15, "loc_types": ["Parking Lot", "Street"]},
        {"category": "Assault", "severity": 8, "weight": 0.15, "loc_types": ["Street", "Bar/Nightclub", "Residence"]},
        {"category": "Vandalism", "severity": 2, "weight": 0.10, "loc_types": ["Park", "Public Building", "Street"]},
        {"category": "Robbery", "severity": 7, "weight": 0.07, "loc_types": ["Bank/ATM", "Street", "Storefront"]},
        {"category": "Fraud", "severity": 4, "weight": 0.03, "loc_types": ["Online/Financial", "Commercial"]}
    ]
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 6, 30)
    total_days = (end_date - start_date).days
    
    records = []
    
    categories = [c["category"] for c in crime_types]
    weights = [c["weight"] for c in crime_types]
    cat_map = {c["category"]: c for c in crime_types}
    
    for i in range(1, num_records + 1):
        incident_id = f"INC-{20230000 + i}"
        
        # Random timestamp
        random_days = np.random.randint(0, total_days)
        # Add hour seasonality: more crimes at night/evening
        hour_weights = [1,1,1,1,1,1,2,3,4,4,5,5,6,6,7,7,8,8,9,9,10,9,7,4]
        hour_prob = np.array(hour_weights) / sum(hour_weights)
        hour = np.random.choice(range(24), p=hour_prob)
        minute = np.random.randint(0, 60)
        
        date_val = start_date + timedelta(days=int(random_days), hours=int(hour), minutes=int(minute))
        
        # District choice weighted by district risk multiplier
        dist_weights = [d["risk_mult"] for d in districts]
        dist_prob = np.array(dist_weights) / sum(dist_weights)
        district = np.random.choice(districts, p=dist_prob)
        
        # Crime type choice
        c_type = np.random.choice(categories, p=weights)
        c_meta = cat_map[c_type]
        
        # Location & Coordinates with noise
        loc_type = np.random.choice(c_meta["loc_types"])
        lat = district["base_lat"] + np.random.normal(0, 0.008)
        lon = district["base_lon"] + np.random.normal(0, 0.008)
        
        # Status
        status = np.random.choice(["Solved", "Under Investigation", "Closed", "Unsolved"], p=[0.45, 0.25, 0.15, 0.15])
        
        # Response time in minutes
        response_time = max(2, int(np.random.gamma(shape=3, scale=4)))
        
        records.append({
            "incident_id": incident_id,
            "timestamp": date_val.strftime("%Y-%m-%d %H:%M:%S"),
            "year": date_val.year,
            "month": date_val.month,
            "day_of_week": date_val.strftime("%A"),
            "hour": date_val.hour,
            "district": district["id"],
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "crime_type": c_type,
            "severity_score": c_meta["severity"],
            "location_type": loc_type,
            "status": status,
            "response_time_min": response_time
        })
        
    df = pd.DataFrame(records)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = generate_crime_dataset()
    df.to_csv("d:/GSSoC/ML-CaPsule/ML-CaPsule/Crime_Analytics/crime_dataset.csv", index=False)
    print(f"Dataset generated successfully with {len(df)} records.")
