import pandas as pd


CYBERBULLYING_TYPES = [
    "not_cyberbullying",
    "gender",
    "religion",
    "age",
    "ethnicity",
    "other_cyberbullying",
]

# Defing our custom prediction function
def predict(model, vectorizer, texts):
    """Classify texts using explicitly supplied, cached model artifacts."""
    text_data = vectorizer.transform(texts)
    prediction = model.predict(text_data)
    result = pd.DataFrame({"text": texts, "type": prediction})
    if result["type"].dtype.kind in "iu":
        result["type"] = result["type"].replace(
            dict(enumerate(CYBERBULLYING_TYPES))
        )
    return result
