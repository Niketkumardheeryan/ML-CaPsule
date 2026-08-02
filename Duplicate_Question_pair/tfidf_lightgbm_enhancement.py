import os
import re
import time
import json
import pickle
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier

# Ensure output directory exists
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# English Stopwords set
STOP_WORDS = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
    "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
    "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should",
    "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
    "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
])

CONTRACTIONS = {
    "ain't": "am not", "aren't": "are not", "can't": "can not", "can't've": "can not have",
    "'cause": "because", "could've": "could have", "couldn't": "could not", "couldn't've": "could not have",
    "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not",
    "hasn't": "has not", "haven't": "have not", "he'd": "he would", "he'll": "he will", "he's": "he is",
    "how'd": "how did", "how's": "how is", "i'd": "i would", "i'll": "i will", "i'm": "i am", "i've": "i have",
    "isn't": "is not", "it'd": "it would", "it'll": "it will", "it's": "it is", "let's": "let us",
    "ma'am": "madam", "mayn't": "may not", "might've": "might have", "mightn't": "might not",
    "must've": "must have", "mustn't": "must not", "needn't": "need not", "shan't": "shall not",
    "she'd": "she would", "she'll": "she will", "she's": "she is", "should've": "should have",
    "shouldn't": "should not", "that's": "that is", "there's": "there is", "they'd": "they would",
    "they'll": "they will", "they're": "they are", "they've": "they have", "wasn't": "was not",
    "we'd": "we would", "we'll": "we will", "we're": "we are", "we've": "we have", "weren't": "were not",
    "what's": "what is", "where's": "where is", "who's": "who is", "why's": "why is", "won't": "will not",
    "wouldn't": "would not", "you'd": "you would", "you'll": "you will", "you're": "you are", "you've": "you have"
}

PATTERN_PUNCT = re.compile(r'\W')
PATTERN_SPACES = re.compile(r'\s+')

def preprocess(q):
    q = str(q).lower().strip()
    try:
        q = BeautifulSoup(q, "html.parser").get_text(separator=" ")
    except Exception:
        pass

    q = q.replace('%', ' percent ').replace('$', ' dollar ').replace('₹', ' rupee ').replace('€', ' euro ').replace('@', ' at ')
    for contraction, expansion in CONTRACTIONS.items():
        q = q.replace(contraction, expansion)

    q = PATTERN_PUNCT.sub(' ', q)
    q = PATTERN_SPACES.sub(' ', q).strip()
    return q

def get_longest_common_substring_ratio(q1, q2):
    matcher = SequenceMatcher(None, q1, q2)
    match = matcher.find_longest_match(0, len(q1), 0, len(q2))
    if match.size == 0:
        return 0.0
    return match.size / (min(len(q1), len(q2)) + 1.0)

def compute_fuzzy_features(q1, q2):
    # Pure Python fuzzy ratio approximations for high-performance cross-platform execution
    seq = SequenceMatcher(None, q1, q2)
    qratio = seq.ratio() * 100.0

    # Partial ratio: match substring
    if len(q1) == 0 or len(q2) == 0:
        partial_ratio = 0.0
    elif len(q1) <= len(q2):
        short_s, long_s = q1, q2
    else:
        short_s, long_s = q2, q1
    
    match = SequenceMatcher(None, short_s, long_s).find_longest_match(0, len(short_s), 0, len(long_s))
    partial_ratio = (match.size / max(len(short_s), 1)) * 100.0

    # Token Sort Ratio
    t1_sorted = " ".join(sorted(q1.split()))
    t2_sorted = " ".join(sorted(q2.split()))
    token_sort_ratio = SequenceMatcher(None, t1_sorted, t2_sorted).ratio() * 100.0

    # Token Set Ratio
    tokens1 = set(q1.split())
    tokens2 = set(q2.split())
    intersection = tokens1.intersection(tokens2)
    diff1 = tokens1 - tokens2
    diff2 = tokens2 - tokens1

    sorted_inter = " ".join(sorted(intersection))
    sorted_inter_d1 = " ".join(sorted(intersection.union(diff1)))
    sorted_inter_d2 = " ".join(sorted(intersection.union(diff2)))

    r1 = SequenceMatcher(None, sorted_inter, sorted_inter_d1).ratio()
    r2 = SequenceMatcher(None, sorted_inter, sorted_inter_d2).ratio()
    r3 = SequenceMatcher(None, sorted_inter_d1, sorted_inter_d2).ratio()
    token_set_ratio = max(r1, r2, r3) * 100.0

    return [qratio, partial_ratio, token_sort_ratio, token_set_ratio]

def extract_features(df, tfidf_vectorizer=None, is_fit=True):
    print("Extracting NLP and string features...")
    df['q1_clean'] = df['question1'].apply(preprocess)
    df['q2_clean'] = df['question2'].apply(preprocess)

    features = []
    SAFE_DIV = 0.0001

    for idx, row in df.iterrows():
        q1 = row['q1_clean']
        q2 = row['q2_clean']

        q1_tokens = q1.split()
        q2_tokens = q2.split()

        q1_len = len(q1)
        q2_len = len(q2)
        q1_num_words = len(q1_tokens)
        q2_num_words = len(q2_tokens)

        w1_set = set(q1_tokens)
        w2_set = set(q2_tokens)
        common_words = len(w1_set & w2_set)
        total_words = len(w1_set) + len(w2_set)
        word_share = round(common_words / (total_words + SAFE_DIV), 4)

        if q1_num_words == 0 or q2_num_words == 0:
            token_feats = [0.0] * 8
            length_feats = [0.0, 0.0, 0.0]
        else:
            q1_words = set([w for w in q1_tokens if w not in STOP_WORDS])
            q2_words = set([w for w in q2_tokens if w not in STOP_WORDS])
            q1_stops = set([w for w in q1_tokens if w in STOP_WORDS])
            q2_stops = set([w for w in q2_tokens if w in STOP_WORDS])

            common_non_stop = len(q1_words.intersection(q2_words))
            common_stops = len(q1_stops.intersection(q2_stops))
            common_tokens = len(w1_set.intersection(w2_set))

            cwc_min = common_non_stop / (min(len(q1_words), len(q2_words)) + SAFE_DIV)
            cwc_max = common_non_stop / (max(len(q1_words), len(q2_words)) + SAFE_DIV)
            csc_min = common_stops / (min(len(q1_stops), len(q2_stops)) + SAFE_DIV)
            csc_max = common_stops / (max(len(q1_stops), len(q2_stops)) + SAFE_DIV)
            ctc_min = common_tokens / (min(len(q1_tokens), len(q2_tokens)) + SAFE_DIV)
            ctc_max = common_tokens / (max(len(q1_tokens), len(q2_tokens)) + SAFE_DIV)
            last_word_eq = float(q1_tokens[-1] == q2_tokens[-1])
            first_word_eq = float(q1_tokens[0] == q2_tokens[0])

            token_feats = [cwc_min, cwc_max, csc_min, csc_max, ctc_min, ctc_max, last_word_eq, first_word_eq]

            abs_len_diff = abs(q1_num_words - q2_num_words)
            mean_len = (q1_num_words + q2_num_words) / 2.0
            lcs_ratio = get_longest_common_substring_ratio(q1, q2)
            length_feats = [abs_len_diff, mean_len, lcs_ratio]

        fuzzy_feats = compute_fuzzy_features(q1, q2)

        row_feats = [
            q1_len, q2_len, q1_num_words, q2_num_words,
            common_words, total_words, word_share
        ] + token_feats + length_feats + fuzzy_feats

        features.append(row_feats)

    features_arr = np.array(features)

    # TF-IDF Feature Extraction
    if is_fit:
        all_text = pd.concat([df['q1_clean'], df['q2_clean']]).fillna('')
        tfidf_vectorizer = TfidfVectorizer(max_features=250, ngram_range=(1, 2))
        tfidf_vectorizer.fit(all_text)

    q1_tfidf = tfidf_vectorizer.transform(df['q1_clean'].fillna(''))
    q2_tfidf = tfidf_vectorizer.transform(df['q2_clean'].fillna(''))

    # Cosine Similarity between Question 1 & Question 2 TF-IDF vectors
    q1_norm = np.sqrt(q1_tfidf.multiply(q1_tfidf).sum(axis=1))
    q2_norm = np.sqrt(q2_tfidf.multiply(q2_tfidf).sum(axis=1))
    dot_prod = q1_tfidf.multiply(q2_tfidf).sum(axis=1)
    
    denom = np.array(q1_norm).flatten() * np.array(q2_norm).flatten()
    denom[denom == 0] = SAFE_DIV
    tfidf_cosine_sim = np.array(dot_prod).flatten() / denom
    tfidf_cosine_sim = tfidf_cosine_sim.reshape(-1, 1)

    q1_tfidf_dense = q1_tfidf.toarray()
    q2_tfidf_dense = q2_tfidf.toarray()
    tfidf_diff = np.abs(q1_tfidf_dense - q2_tfidf_dense)

    full_features = np.hstack((features_arr, tfidf_cosine_sim, tfidf_diff))

    return full_features, tfidf_vectorizer

def run_model_training_pipeline():
    csv_path = os.path.join(os.path.dirname(__file__), "train.csv")
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)

    # Clean missing values
    df = df.dropna(subset=['question1', 'question2', 'is_duplicate']).reset_index(drop=True)

    # Sample for quick, robust benchmarking
    sample_size = min(15000, len(df))
    df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    print(f"Dataset sampled to {len(df)} question pairs for training and model benchmarking.")

    X, tfidf_vec = extract_features(df, is_fit=True)
    y = df['is_duplicate'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1),
        "SVM": LinearSVC(C=1.0, max_iter=2000, random_state=42),
        "XGBoost": xgb.XGBClassifier(n_estimators=120, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1),
        "CatBoost": CatBoostClassifier(iterations=120, depth=6, learning_rate=0.1, verbose=0, random_seed=42),
        "LightGBM": lgb.LGBMClassifier(n_estimators=150, max_depth=7, learning_rate=0.08, num_leaves=31, random_state=42, n_jobs=-1)
    }

    results = {}
    best_model_name = None
    best_f1 = 0.0
    trained_models = {}

    print("\n=======================================================")
    print("      DUPLICATE QUESTION PAIR MODEL EVALUATION         ")
    print("=======================================================")

    for name, model in models.items():
        t0 = time.time()
        model.fit(X_train, y_train)
        fit_time = time.time() - t0

        t0 = time.time()
        y_pred = model.predict(X_test)
        pred_time = time.time() - t0

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        results[name] = {
            "Accuracy": round(float(acc), 4),
            "Precision": round(float(prec), 4),
            "Recall": round(float(rec), 4),
            "F1-Score": round(float(f1), 4),
            "Training Time (s)": round(float(fit_time), 3),
            "Inference Time (s)": round(float(pred_time), 3)
        }
        trained_models[name] = model

        print(f"Model: {name}")
        print(f"  Accuracy:  {acc*100:.2f}%")
        print(f"  Precision: {prec*100:.2f}%")
        print(f"  Recall:    {rec*100:.2f}%")
        print(f"  F1-Score:  {f1*100:.2f}%")
        print(f"  Train Time:{fit_time:.2f}s | Infer Time: {pred_time:.3f}s\n")

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name

    # Train Stacking Classifier
    print("Training Stacking Classifier ...")
    base_estimators = [
        ('rf', RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)),
        ('xgb', xgb.XGBClassifier(n_estimators=60, max_depth=5, learning_rate=0.1, random_state=42, n_jobs=-1)),
        ('lgb', lgb.LGBMClassifier(n_estimators=80, max_depth=6, learning_rate=0.08, random_state=42, n_jobs=-1))
    ]
    stacking_clf = StackingClassifier(
        estimators=base_estimators,
        final_estimator=LogisticRegression(),
        cv=3,
        n_jobs=-1
    )
    t0 = time.time()
    stacking_clf.fit(X_train, y_train)
    fit_time = time.time() - t0
    y_pred_stack = stacking_clf.predict(X_test)
    pred_time = time.time() - t0

    acc_s = accuracy_score(y_test, y_pred_stack)
    prec_s = precision_score(y_test, y_pred_stack)
    rec_s = recall_score(y_test, y_pred_stack)
    f1_s = f1_score(y_test, y_pred_stack)

    results["Stacking Classifier"] = {
        "Accuracy": round(float(acc_s), 4),
        "Precision": round(float(prec_s), 4),
        "Recall": round(float(rec_s), 4),
        "F1-Score": round(float(f1_s), 4),
        "Training Time (s)": round(float(fit_time), 3),
        "Inference Time (s)": round(float(pred_time), 3)
    }

    print("Model: Stacking Classifier")
    print(f"  Accuracy:  {acc_s*100:.2f}%")
    print(f"  Precision: {prec_s*100:.2f}%")
    print(f"  Recall:    {rec_s*100:.2f}%")
    print(f"  F1-Score:  {f1_s*100:.2f}%\n")

    # Save trained LightGBM model as primary model and vectorizer
    lgb_model = trained_models["LightGBM"]
    lgb_path = os.path.join(MODELS_DIR, "lgb_model.pkl")
    tfidf_path = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
    stopwords_path = os.path.join(MODELS_DIR, "stopwords.pkl")
    results_path = os.path.join(MODELS_DIR, "model_comparison.json")

    with open(lgb_path, "wb") as f:
        pickle.dump(lgb_model, f)

    with open(tfidf_path, "wb") as f:
        pickle.dump(tfidf_vec, f)

    with open(stopwords_path, "wb") as f:
        pickle.dump(STOP_WORDS, f)

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved trained LightGBM model to {lgb_path}")
    print(f"Saved TF-IDF vectorizer to {tfidf_path}")
    print(f"Saved Stopwords set to {stopwords_path}")
    print(f"Saved evaluation metrics to {results_path}")

if __name__ == "__main__":
    run_model_training_pipeline()
