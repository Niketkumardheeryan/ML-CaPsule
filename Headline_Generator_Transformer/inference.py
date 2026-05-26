from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/bart-large-cnn"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_headline(article):

    inputs = tokenizer(
        article,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=6,
        max_length=10,
        min_length=3,
        length_penalty=3.0,
        repetition_penalty=2.5,
        early_stopping=True
    )

    headline = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return headline