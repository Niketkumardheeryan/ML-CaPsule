# Handle prediction on new user input.

'''
User Input
    ↓
Preprocessing
    ↓
Model Prediction
    ↓
Output Result
'''

from save_model import load_feature_columns_name, load_model, load_scaler
import pandas as pd 


scaler = load_scaler()

feature_columns = load_feature_columns_name()

model = load_model(model_name="random_forest")

def preprocess_user_input(user_input: dict):
    """
    Convert user input into model-compatible format.
    """

    # Convert dictionary into dataframe
    df = pd.DataFrame([user_input])

    # Apply one-hot encoding
    df = pd.get_dummies(df)

    # Add missing columns
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Keep only training columns order
    df = df[feature_columns]

    # Scale input
    scaled_input = scaler.transform(df)

    return scaled_input



def predict_autism(user_input: dict):
    """
    Predict autism based on user input.
    """

    processed_input = preprocess_user_input(user_input)

    prediction = model.predict(processed_input)[0]

    probability = None

    if hasattr(model, 'predict_proba'):
        probability = model.predict_proba(processed_input)[0][1]

    result = 'YES' if prediction == 1 else 'NO'

    print('\nPrediction Result')
    print('=' * 50)
    print(f'Autism Prediction : {result}')

    if probability is not None:
        print(f'Confidence Score : {round(probability * 100, 2)}%')

    return result


if __name__ == '__main__':
    
    sample_input = {
        'A1_Score': 1,
        'A2_Score': 1,
        'A3_Score': 1,
        'A4_Score': 1,
        'A5_Score': 0,
        'A6_Score': 1,
        'A7_Score': 0,
        'A8_Score': 1,
        'A9_Score': 0,
        'A10_Score': 1,
        'age': 25,
        'gender': 'm',
        'ethnicity': 'Others',
        'jundice': 'no',
        'austim': 'no',
        'contry_of_res': 'India',
        'relation': 'Self',
        'result': 6
    }
    predict_autism(sample_input)