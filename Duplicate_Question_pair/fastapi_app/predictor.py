import os
import re
import pickle
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

class DuplicateQuestionPredictor:
    def __init__(self, models_dir=None):
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
        
        self.models_dir = models_dir
        self.model_path = os.path.join(models_dir, "lgb_model.pkl")
        self.tfidf_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
        self.stopwords_path = os.path.join(models_dir, "stopwords.pkl")
        self.comparison_path = os.path.join(models_dir, "model_comparison.json")

        self.model = None
        self.tfidf_vectorizer = None
        self.stopwords = None
        self.is_loaded = False

        self.contractions = {
            "ain't": "am not", "aren't": "are not", "can't": "can not", "can't've": "can not have",
            "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not",
            "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not",
            "haven't": "have not", "he'd": "he would", "he'll": "he will", "he's": "he is",
            "i'd": "i would", "i'll": "i will", "i'm": "i am", "i've": "i have", "isn't": "is not",
            "it's": "it is", "let's": "let us", "she's": "she is", "should've": "should have",
            "shouldn't": "should not", "that's": "that is", "there's": "there is", "they're": "they are",
            "we're": "we are", "what's": "what is", "won't": "will not", "wouldn't": "would not",
            "you're": "you are", "you've": "you have"
        }

        self.pattern_punct = re.compile(r'\W')
        self.pattern_spaces = re.compile(r'\s+')

        self.load_artifacts()

    def load_artifacts(self):
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.tfidf_path):
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                with open(self.tfidf_path, "rb") as f:
                    self.tfidf_vectorizer = pickle.load(f)
                
                if os.path.exists(self.stopwords_path):
                    with open(self.stopwords_path, "rb") as f:
                        self.stopwords = pickle.load(f)
                else:
                    self.stopwords = set(["the", "a", "an", "is", "are", "in", "on", "of", "to", "and"])

                self.is_loaded = True
                print("ML Artifacts loaded successfully into DuplicateQuestionPredictor.")
            else:
                print(f"Model artifacts not found at {self.models_dir}. Please run model training first.")
        except Exception as e:
            print(f"Error loading model artifacts: {str(e)}")

    def preprocess(self, q):
        q = str(q).lower().strip()
        try:
            q = BeautifulSoup(q, "html.parser").get_text(separator=" ")
        except Exception:
            pass

        q = q.replace('%', ' percent ').replace('$', ' dollar ').replace('₹', ' rupee ').replace('€', ' euro ').replace('@', ' at ')
        for contraction, expansion in self.contractions.items():
            q = q.replace(contraction, expansion)

        q = self.pattern_punct.sub(' ', q)
        q = self.pattern_spaces.sub(' ', q).strip()
        return q

    def _get_lcs_ratio(self, q1, q2):
        matcher = SequenceMatcher(None, q1, q2)
        match = matcher.find_longest_match(0, len(q1), 0, len(q2))
        if match.size == 0:
            return 0.0
        return match.size / (min(len(q1), len(q2)) + 1.0)

    def _compute_fuzzy_features(self, q1, q2):
        seq = SequenceMatcher(None, q1, q2)
        qratio = seq.ratio() * 100.0

        if len(q1) == 0 or len(q2) == 0:
            partial_ratio = 0.0
        elif len(q1) <= len(q2):
            short_s, long_s = q1, q2
        else:
            short_s, long_s = q2, q1

        match = SequenceMatcher(None, short_s, long_s).find_longest_match(0, len(short_s), 0, len(long_s))
        partial_ratio = (match.size / max(len(short_s), 1)) * 100.0

        t1_sorted = " ".join(sorted(q1.split()))
        t2_sorted = " ".join(sorted(q2.split()))
        token_sort_ratio = SequenceMatcher(None, t1_sorted, t2_sorted).ratio() * 100.0

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

    def extract_pair_features(self, q1_raw, q2_raw):
        q1 = self.preprocess(q1_raw)
        q2 = self.preprocess(q2_raw)

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
        SAFE_DIV = 0.0001
        word_share = round(common_words / (total_words + SAFE_DIV), 4)

        if q1_num_words == 0 or q2_num_words == 0:
            token_feats = [0.0] * 8
            length_feats = [0.0, 0.0, 0.0]
        else:
            q1_words = set([w for w in q1_tokens if w not in self.stopwords])
            q2_words = set([w for w in q2_tokens if w not in self.stopwords])
            q1_stops = set([w for w in q1_tokens if w in self.stopwords])
            q2_stops = set([w for w in q2_tokens if w in self.stopwords])

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
            lcs_ratio = self._get_lcs_ratio(q1, q2)
            length_feats = [abs_len_diff, mean_len, lcs_ratio]

        fuzzy_feats = self._compute_fuzzy_features(q1, q2)

        base_feats = np.array([
            q1_len, q2_len, q1_num_words, q2_num_words,
            common_words, total_words, word_share
        ] + token_feats + length_feats + fuzzy_feats).reshape(1, -1)

        # Vectorization & Cosine Similarity
        if self.tfidf_vectorizer is not None:
            q1_tfidf = self.tfidf_vectorizer.transform([q1])
            q2_tfidf = self.tfidf_vectorizer.transform([q2])

            q1_norm = np.sqrt(q1_tfidf.multiply(q1_tfidf).sum())
            q2_norm = np.sqrt(q2_tfidf.multiply(q2_tfidf).sum())
            dot_prod = q1_tfidf.multiply(q2_tfidf).sum()
            denom = (q1_norm * q2_norm)
            cos_sim = float(dot_prod / (denom if denom != 0 else SAFE_DIV))

            q1_tfidf_dense = q1_tfidf.toarray()
            q2_tfidf_dense = q2_tfidf.toarray()
            tfidf_diff = np.abs(q1_tfidf_dense - q2_tfidf_dense)

            full_feats = np.hstack((base_feats, np.array([[cos_sim]]), tfidf_diff))
        else:
            full_feats = base_feats
            cos_sim = 0.0

        feature_summary = {
            "q1_clean": q1,
            "q2_clean": q2,
            "common_words": common_words,
            "word_share": word_share,
            "tfidf_cosine_similarity": round(float(cos_sim), 4),
            "fuzzy_ratio": round(fuzzy_feats[0], 2),
            "token_set_ratio": round(fuzzy_feats[3], 2)
        }

        return full_feats, feature_summary

    def predict(self, q1, q2):
        if not self.is_loaded:
            self.load_artifacts()
            if not self.is_loaded:
                # Heuristic fallback if model artifacts are not present
                q1_clean = self.preprocess(q1)
                q2_clean = self.preprocess(q2)
                sim = SequenceMatcher(None, q1_clean, q2_clean).ratio()
                is_dup = sim >= 0.70
                return {
                    "is_duplicate": bool(is_dup),
                    "duplicate_probability": round(float(sim), 4),
                    "confidence_label": "High" if sim > 0.85 or sim < 0.25 else "Moderate",
                    "model_used": "Fallback Heuristic",
                    "features": {
                        "q1_clean": q1_clean,
                        "q2_clean": q2_clean,
                        "similarity_score": round(float(sim), 4)
                    }
                }

        X, feature_summary = self.extract_pair_features(q1, q2)
        
        # Probabilities
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X)[0]
            dup_prob = float(probs[1])
        else:
            pred = self.model.predict(X)[0]
            dup_prob = float(pred)

        is_duplicate = dup_prob >= 0.5
        confidence = round(dup_prob if is_duplicate else (1.0 - dup_prob), 4)
        
        if confidence >= 0.85:
            conf_label = "Very High"
        elif confidence >= 0.70:
            conf_label = "High"
        elif confidence >= 0.55:
            conf_label = "Moderate"
        else:
            conf_label = "Low"

        return {
            "is_duplicate": bool(is_duplicate),
            "duplicate_probability": round(dup_prob, 4),
            "confidence_label": conf_label,
            "model_used": "LightGBM + TF-IDF Vectorizer ⚡",
            "features": feature_summary
        }
