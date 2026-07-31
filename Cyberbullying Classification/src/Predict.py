from src.preprocess import pre_processing_custom
import pickle
import pandas as pd
import joblib

tfidf = joblib.load("./models/tfidf.pkl")

cyberbullying_type = ['not_cyberbullying', 'gender', 'religion', 'age', 'ethnicity']

# Defing our custom prediction function
def predict(model, texts):
    clean_texts = [pre_processing_custom(text) for text in texts]
    text_data = tfidf.transform(clean_texts)
    prediction = model.predict(text_data)

    data = []
    for text, prediction in zip(texts, prediction):
        data.append((text, prediction))

    df = pd.DataFrame(data, columns = ['text','type'])
    df = df.replace([0,1,2,3,4], cyberbullying_type)
    return df