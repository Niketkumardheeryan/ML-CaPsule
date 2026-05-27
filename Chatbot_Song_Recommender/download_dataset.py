import urllib.request
import os

url = "https://raw.githubusercontent.com/sushmaakoju/spotify-tracks-data-analysis/main/SpotifyFeatures.csv"
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'data', 'SpotifyFeatures.csv')

print(f"Downloading dataset from {url}...")
try:
    urllib.request.urlretrieve(url, data_path)
    print(f"Dataset downloaded successfully to {data_path}!")
except Exception as e:
    print(f"Error downloading dataset: {e}")
