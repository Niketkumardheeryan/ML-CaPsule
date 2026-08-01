import pandas as pd
import numpy as np
import os

def generate_synthetic_cicids2017(num_samples=5000, random_state=42):
    """
    Generates a realistic synthetic network intrusion dataset based on the CICIDS2017 schema.
    Includes both normal network traffic (BENIGN) and various attack types.
    """
    np.random.seed(random_state)
    
    # We will simulate 5 classes: BENIGN, DoS, Brute Force, Botnet, Infiltration
    classes = ['BENIGN', 'DoS', 'Brute Force', 'Botnet', 'Infiltration']
    class_probs = [0.65, 0.20, 0.08, 0.05, 0.02]  # Simulating some class imbalance
    
    y = np.random.choice(classes, size=num_samples, p=class_probs)
    
    # Core features representing network flows
    features = {
        'Destination Port': np.zeros(num_samples, dtype=int),
        'Flow Duration': np.zeros(num_samples),
        'Total Fwd Packets': np.zeros(num_samples, dtype=int),
        'Total Backward Packets': np.zeros(num_samples, dtype=int),
        'Total Length of Fwd Packets': np.zeros(num_samples),
        'Total Length of Bwd Packets': np.zeros(num_samples),
        'Fwd Packet Length Mean': np.zeros(num_samples),
        'Bwd Packet Length Mean': np.zeros(num_samples),
        'Flow Bytes/s': np.zeros(num_samples),
        'Flow Packets/s': np.zeros(num_samples),
        'Flow IAT Mean': np.zeros(num_samples),
        'Packet Length Mean': np.zeros(num_samples),
        'Packet Length Std': np.zeros(num_samples),
        'Init_Win_bytes_forward': np.zeros(num_samples, dtype=int),
        'Init_Win_bytes_backward': np.zeros(num_samples, dtype=int),
        'Label': y
    }
    
    for i in range(num_samples):
        label = y[i]
        
        if label == 'BENIGN':
            # Typical web traffic (ports 80, 443, DNS 53, etc.)
            features['Destination Port'][i] = np.random.choice([80, 443, 53, 22, np.random.randint(1024, 65535)])
            features['Flow Duration'][i] = np.random.exponential(scale=100000) + 100
            features['Total Fwd Packets'][i] = np.random.randint(1, 20)
            features['Total Backward Packets'][i] = np.random.randint(1, 20)
            features['Total Length of Fwd Packets'][i] = features['Total Fwd Packets'][i] * np.random.normal(150, 50)
            features['Total Length of Bwd Packets'][i] = features['Total Backward Packets'][i] * np.random.normal(300, 100)
            features['Fwd Packet Length Mean'][i] = np.random.normal(100, 30)
            features['Bwd Packet Length Mean'][i] = np.random.normal(200, 50)
            features['Init_Win_bytes_forward'][i] = np.random.randint(2000, 65535)
            features['Init_Win_bytes_backward'][i] = np.random.randint(2000, 65535)
            
        elif label == 'DoS':
            # High rate of small packets targetting a single port (usually 80 or 443)
            features['Destination Port'][i] = np.random.choice([80, 443])
            features['Flow Duration'][i] = np.random.uniform(10, 5000)  # Very fast flows
            features['Total Fwd Packets'][i] = np.random.randint(20, 150)
            features['Total Backward Packets'][i] = np.random.randint(0, 5)  # Mostly one-way flooding
            features['Total Length of Fwd Packets'][i] = features['Total Fwd Packets'][i] * np.random.uniform(20, 60)
            features['Total Length of Bwd Packets'][i] = features['Total Backward Packets'][i] * np.random.uniform(0, 40)
            features['Fwd Packet Length Mean'][i] = np.random.uniform(20, 50)
            features['Bwd Packet Length Mean'][i] = np.random.uniform(0, 20)
            features['Init_Win_bytes_forward'][i] = np.random.choice([0, 256, 512, 1024])
            features['Init_Win_bytes_backward'][i] = 0
            
        elif label == 'Brute Force':
            # Systematic attempts on SSH (22) or FTP (21)
            features['Destination Port'][i] = np.random.choice([22, 21])
            features['Flow Duration'][i] = np.random.normal(150000, 30000)
            features['Total Fwd Packets'][i] = np.random.randint(5, 15)
            features['Total Backward Packets'][i] = np.random.randint(5, 15)
            features['Total Length of Fwd Packets'][i] = features['Total Fwd Packets'][i] * np.random.uniform(40, 80)
            features['Total Length of Bwd Packets'][i] = features['Total Backward Packets'][i] * np.random.uniform(40, 80)
            features['Fwd Packet Length Mean'][i] = np.random.uniform(40, 70)
            features['Bwd Packet Length Mean'][i] = np.random.uniform(40, 70)
            features['Init_Win_bytes_forward'][i] = np.random.randint(1000, 5000)
            features['Init_Win_bytes_backward'][i] = np.random.randint(1000, 5000)
            
        elif label == 'Botnet':
            # Automated tasks, specific ports (e.g. IRC 6667, or random high ports)
            features['Destination Port'][i] = np.random.choice([6667, 8080, np.random.randint(5000, 6000)])
            features['Flow Duration'][i] = np.random.exponential(scale=500000)
            features['Total Fwd Packets'][i] = np.random.randint(10, 40)
            features['Total Backward Packets'][i] = np.random.randint(10, 40)
            features['Total Length of Fwd Packets'][i] = features['Total Fwd Packets'][i] * np.random.uniform(50, 100)
            features['Total Length of Bwd Packets'][i] = features['Total Backward Packets'][i] * np.random.uniform(50, 100)
            features['Fwd Packet Length Mean'][i] = np.random.uniform(60, 90)
            features['Bwd Packet Length Mean'][i] = np.random.uniform(60, 90)
            features['Init_Win_bytes_forward'][i] = 8192
            features['Init_Win_bytes_backward'][i] = 8192
            
        elif label == 'Infiltration':
            # Inside job or compromise, large flows, ports like 443, 80
            features['Destination Port'][i] = np.random.choice([80, 443, np.random.randint(1024, 49151)])
            features['Flow Duration'][i] = np.random.uniform(500000, 2000000)  # Very long duration
            features['Total Fwd Packets'][i] = np.random.randint(50, 300)
            features['Total Backward Packets'][i] = np.random.randint(50, 300)
            features['Total Length of Fwd Packets'][i] = features['Total Fwd Packets'][i] * np.random.uniform(200, 800)
            features['Total Length of Bwd Packets'][i] = features['Total Backward Packets'][i] * np.random.uniform(500, 1500)
            features['Fwd Packet Length Mean'][i] = np.random.uniform(150, 600)
            features['Bwd Packet Length Mean'][i] = np.random.uniform(400, 1200)
            features['Init_Win_bytes_forward'][i] = np.random.randint(8192, 65535)
            features['Init_Win_bytes_backward'][i] = np.random.randint(8192, 65535)
        
        # Calculate derivative features
        features['Total Length of Fwd Packets'][i] = max(0, features['Total Length of Fwd Packets'][i])
        features['Total Length of Bwd Packets'][i] = max(0, features['Total Length of Bwd Packets'][i])
        
        # Avoid zero division
        duration_sec = features['Flow Duration'][i] / 1000000.0  # Convert microseconds to seconds
        if duration_sec <= 0:
            duration_sec = 0.000001
            
        features['Flow Bytes/s'][i] = (features['Total Length of Fwd Packets'][i] + features['Total Length of Bwd Packets'][i]) / duration_sec
        features['Flow Packets/s'][i] = (features['Total Fwd Packets'][i] + features['Total Backward Packets'][i]) / duration_sec
        
        total_pkts = max(1, features['Total Fwd Packets'][i] + features['Total Backward Packets'][i])
        features['Flow IAT Mean'][i] = features['Flow Duration'][i] / total_pkts
        
        # Packet length statistics
        all_pkt_len = [features['Fwd Packet Length Mean'][i]] * features['Total Fwd Packets'][i] + [features['Bwd Packet Length Mean'][i]] * features['Total Backward Packets'][i]
        if not all_pkt_len:
            all_pkt_len = [0]
        features['Packet Length Mean'][i] = np.mean(all_pkt_len)
        features['Packet Length Std'][i] = np.std(all_pkt_len)
        
    df = pd.DataFrame(features)
    
    # Replace NaNs/Infs if any
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)
    
    return df

if __name__ == '__main__':
    print("Generating synthetic CICIDS2017 dataset...")
    df = generate_synthetic_cicids2017(num_samples=6000)
    output_path = os.path.join(os.path.dirname(__file__), 'cicids2017_sample.csv')
    df.to_csv(output_path, index=False)
    print(f"Dataset saved successfully with shape {df.shape} to {output_path}")
    print("Class distribution:")
    print(df['Label'].value_counts())
