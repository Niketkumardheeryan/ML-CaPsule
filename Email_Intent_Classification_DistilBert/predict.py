from transformers import DistilBertTokenizerFast
from transformers import DistilBertForSequenceClassification

import torch

MODEL_PATH = "./saved_model"

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

labels = [
    "billing",
    "complaint",
    "feedback",
    "inquiry",
    "spam",
    "support"
]

def predict_intent(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    outputs = model(**inputs)

    prediction = torch.argmax(outputs.logits, dim=1).item()

    return labels[prediction]

# Example
sample_text = "I need help resetting my password"

result = predict_intent(sample_text)

print(f"\nPredicted Intent: {result}")