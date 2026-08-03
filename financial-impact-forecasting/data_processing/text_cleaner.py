import re
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class FinancialTextPreprocessor:
    def __init__(self, max_words=5000, max_len=50):
        self.max_words = max_words
        self.max_len = max_len
        self.tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")

    def clean_text(self, text):
        """Cleans news text by removing special characters and lowering case."""
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text

    def fit_transform(self, texts):
        """Fits tokenizer and converts text data into padded sequences."""
        cleaned_texts = [self.clean_text(t) for t in texts]
        self.tokenizer.fit_on_texts(cleaned_texts)
        sequences = self.tokenizer.texts_to_sequences(cleaned_texts)
        return pad_sequences(sequences, maxlen=self.max_len, padding='post')

    def transform(self, texts):
        """Transforms new text using the already fitted tokenizer."""
        cleaned_texts = [self.clean_text(t) for t in texts]
        sequences = self.tokenizer.texts_to_sequences(cleaned_texts)
        return pad_sequences(sequences, maxlen=self.max_len, padding='post')
