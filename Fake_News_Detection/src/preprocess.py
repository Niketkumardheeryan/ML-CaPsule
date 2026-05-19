import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Ensure required NLTK resources are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def preprocess_text(text):
    """
    Cleans and preprocesses the input text.
    - Converts to lowercase
    - Removes punctuation
    - Tokenizes text
    - Removes stopwords
    - Applies stemming
    """
    if not isinstance(text, str):
        return ""
        
    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 3. Tokenization
    tokens = word_tokenize(text)
    
    # 4. Remove stopwords & 5. Stemming
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    
    cleaned_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    
    # Join tokens back to a single string
    return " ".join(cleaned_tokens)
