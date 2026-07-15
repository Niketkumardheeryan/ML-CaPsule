"""
save_model.py
-------------
Run this ONCE after training in spam_mail_detection.ipynb.
It saves the trained pipeline as a .pkl file so app.py can load it.

Instructions:
1. Run spam_mail_detection.ipynb fully first.
2. Copy-paste the Model() function call results into a variable (see below).
3. Then run this script.

OR — easier — just add the code block below directly at the END of your notebook.
"""

import pickle
import pandas as pd
import string
import warnings
warnings.filterwarnings("ignore")

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# ── 1. Load & clean data ────────────────────────────────────────────────────
data = pd.read_csv('dataset/spam.csv', encoding='latin-1')
data = data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)
data = data.rename({'v1': 'Class', 'v2': 'Message'}, axis=1)

X = data['Message']
y = data['Class']

# ── 2. Preprocessing function (must match app.py) ───────────────────────────
STOPWORDS = stopwords.words('english')

def message_text_process(mess):
    """Remove punctuation and stop words — same function used in the notebook."""
    no_punctuation = [char for char in mess if char not in string.punctuation]
    no_punctuation = ''.join(no_punctuation)
    return [word for word in no_punctuation.split() if word.lower() not in STOPWORDS]

# ── 3. Build the pipeline (CountVectorizer → TF-IDF → Naive Bayes) ──────────
pipeline_model = Pipeline([
    ('vect', CountVectorizer(analyzer=message_text_process)),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])

x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=30
)
pipeline_model.fit(x_train, y_train)

accuracy = pipeline_model.score(x_test, y_test) * 100
print(f"✅ Model trained — Accuracy: {accuracy:.2f}%")

# ── 4. Save pipeline to disk ─────────────────────────────────────────────────
with open('model/spam_model.pkl', 'wb') as f:
    pickle.dump(pipeline_model, f)

print("✅ Model saved to model/spam_model.pkl")
print("   You can now run:  streamlit run app.py")
