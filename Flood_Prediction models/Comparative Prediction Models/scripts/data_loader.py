import os
import pandas as pd

# Default Kaggle Dataset Slug or Direct URL (set via environment variable or code)
DEFAULT_KAGGLE_HANDLE = os.environ.get("KAGGLE_DATASET_HANDLE", "varshithnagubandi/flood-prediction")
DEFAULT_REMOTE_URL = os.environ.get("FLOOD_DATASET_URL", "")

def load_flood_data(dataset_handle=None, remote_url=None, file_name="flood.csv", local_path=None):
    """
    Loads flood dataset dynamically without requiring a local CSV file on disk:
    1. Tries Kagglehub if dataset_handle or KAGGLE_DATASET_HANDLE is set.
    2. Tries direct remote URL if remote_url or FLOOD_DATASET_URL is set.
    3. Falls back to local CSV file path if present.
    """
    if local_path is None:
        local_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)

    # 1. Try Kagglehub
    handle = dataset_handle or DEFAULT_KAGGLE_HANDLE
    if handle:
        try:
            import kagglehub
            print(f"Fetching dataset '{handle}' via kagglehub...")
            dataset_dir = kagglehub.dataset_download(handle)
            kaggle_file_path = os.path.join(dataset_dir, file_name)
            if os.path.exists(kaggle_file_path):
                print(f"Successfully loaded '{file_name}' from Kaggle cache.")
                return pd.read_csv(kaggle_file_path)
        except Exception as e:
            print(f"Kagglehub fetch skipped ({e}). Trying next data source...")

    # 2. Try Direct Remote HTTP/HTTPS URL
    url = remote_url or DEFAULT_REMOTE_URL
    if url:
        try:
            print(f"Fetching dataset dynamically from URL: {url}...")
            return pd.read_csv(url)
        except Exception as e:
            print(f"Could not load dataset from URL ({e}).")

    # 3. Local File Fallback
    if os.path.exists(local_path):
        print(f"Loading local dataset from '{os.path.abspath(local_path)}'...")
        return pd.read_csv(local_path)

    raise FileNotFoundError(
        f"Dataset '{file_name}' could not be loaded dynamically or locally.\n"
        "Please specify a valid KAGGLE_DATASET_HANDLE (e.g. 'username/dataset-name') or FLOOD_DATASET_URL."
    )