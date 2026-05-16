import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)

    df.dropna(inplace=True)

    X = df["email"]
    y = df["intent"]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.4,
        random_state=42,
        stratify=y_encoded
    )

    return X_train, X_test, y_train, y_test, label_encoder