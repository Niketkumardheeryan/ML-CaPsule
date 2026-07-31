import re
import numpy as np
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Fallback datasets/lexicon for offline/lightweight mode
MENTAL_HEALTH_LEXICON = {
    "depression": [
        "sad", "depressed", "hopeless", "lonely", "crying", "worthless", "empty",
        "darkness", "pain", "suicide", "die", "give up", "exhausted", "numb",
        "hurt", "alone", "miserable", "grief", "tear", "heavy", "shadow"
    ],
    "anxiety": [
        "anxious", "worry", "panic", "fear", "scared", "shake", "chest pain",
        "breathing", "heart racing", "nervous", "dread", "terror", "paralyzed",
        "overthinking", "sweat", "future", "uneasy", "restless", "tense"
    ],
    "stress": [
        "stress", "overwhelmed", "pressure", "deadline", "workload", "tired",
        "busy", "headache", "demand", "struggle", "coping", "tension", "burden",
        "exhausting", "sleep deprivation", "unwind", "heavy", "crushing"
    ],
    "burnout": [
        "burnout", "burnt out", "no energy", "unmotivated", "caring less",
        "cynical", "fatigue", "drain", "exhaust", "give up", "meaningless",
        "workspace", "job", "career", "detached", "empty", "overworked", "weary"
    ]
}

class MentalHealthScorer:
    def __init__(self):
        self.categories = ["Depression", "Anxiety", "Stress", "Burnout"]
        self.use_transformer = False
        self.tokenizer = None
        self.model = None
        
        # Initialize ML fallback model
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        # Create a small synthetic dataset to pre-train the fallback model
        self._init_fallback_model()
        
        # Try loading transformer model
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            # Use a tiny sentiment model or similar, but since we need 4 labels,
            # we'll define a custom classification pipeline or load a pre-trained multi-label one.
            # To avoid huge download overhead on startup, we lazy-load or use fallback first.
        except ImportError:
            pass

    def _init_fallback_model(self):
        # Generate representative synthetic texts for training the fallback model
        texts = []
        labels = []
        
        # Add pure neutral texts
        neutral_texts = [
            "Today I went to the park and saw some dogs.",
            "I had a sandwich for lunch and it was quite good.",
            "The weather today is sunny and mild.",
            "I am planning to read a book this evening.",
            "We discussed the new project requirements at work."
        ]
        for t in neutral_texts:
            texts.append(t)
            labels.append([0.0, 0.0, 0.0, 0.0])
            
        # Add category-specific texts
        for i, cat in enumerate(self.categories):
            keywords = MENTAL_HEALTH_LEXICON[cat.lower()]
            for kw in keywords:
                texts.append(f"I feel extremely {kw} today, everything is so difficult.")
                lbl1 = [0.0, 0.0, 0.0, 0.0]
                lbl1[i] = 0.8
                labels.append(lbl1)
                
                texts.append(f"My {kw} is getting worse and I cannot handle it.")
                lbl2 = [0.0, 0.0, 0.0, 0.0]
                lbl2[i] = 0.8
                labels.append(lbl2)
                
                # Joint categories
                for j, cat2 in enumerate(self.categories):
                    if i != j:
                        kw2 = MENTAL_HEALTH_LEXICON[cat2.lower()][0]
                        texts.append(f"Dealing with {kw} and {kw2} at the same time is crushing.")
                        lbl2 = [0.0, 0.0, 0.0, 0.0]
                        lbl2[i] = 0.7
                        lbl2[j] = 0.7
                        labels.append(lbl2)
                        
        X = self.vectorizer.fit_transform(texts)
        y = np.array(labels)
        
        # Train individual logistic regressions for each label
        self.classifiers = []
        for col in range(4):
            clf = LogisticRegression(C=1.0, max_iter=200)
            # Binary classification (high vs low sentiment contribution)
            # We map target score to binary label for training
            y_bin = (y[:, col] > 0.3).astype(int)
            clf.fit(X, y_bin)
            self.classifiers.append(clf)

    def load_transformer_model(self, model_name="distilbert-base-uncased"):
        """Attempts to load a fine-tuned transformer model."""
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=4)
            self.use_transformer = True
            return True
        except Exception as e:
            print(f"Could not load transformer model: {e}. Falling back to ML Lexicon Model.")
            self.use_transformer = False
            return False

    def predict(self, text):
        """Returns risk scores (0-100) for each of the 4 dimensions."""
        if not text.strip():
            return {cat: 0.0 for cat in self.categories}
            
        if self.use_transformer and self.model is not None:
            try:
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    logits = outputs.logits
                    probs = torch.sigmoid(logits).cpu().numpy()[0]
                
                return {self.categories[i]: float(probs[i] * 100) for i in range(4)}
            except Exception:
                # Fallback on transformer failure
                pass
                
        # ML Fallback Prediction
        X_vec = self.vectorizer.transform([text])
        scores = {}
        for i, cat in enumerate(self.categories):
            clf = self.classifiers[i]
            # Probabilities of class 1
            prob = clf.predict_proba(X_vec)[0][1]
            
            # Boost score based on keyword matches for accuracy in short inputs
            words = re.findall(r'\b\w+\b', text.lower())
            matches = sum(1 for w in words if w in MENTAL_HEALTH_LEXICON[cat.lower()])
            boost = min(0.3, matches * 0.1)
            
            final_prob = min(1.0, prob + boost)
            scores[cat] = float(final_prob * 100)
            
        return scores

    def get_severity(self, score):
        if score < 35:
            return "Low", "green"
        elif score < 70:
            return "Moderate", "orange"
        else:
            return "High", "red"

    def explain_text(self, text, target_category):
        """
        Simple LIME-like text explainer that perturbs the input by removing words
        to calculate each word's contribution to the target category score.
        """
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return []
            
        base_scores = self.predict(text)
        base_score = base_scores[target_category]
        
        word_contributions = []
        
        # Perturb by removing one word at a time
        for i, word in enumerate(words):
            # Form clean text without word i
            perturbed_words = words[:i] + words[i+1:]
            perturbed_text = " ".join(perturbed_words)
            
            perturbed_scores = self.predict(perturbed_text)
            perturbed_score = perturbed_scores[target_category]
            
            # Contribution is how much score dropped when word was removed
            diff = base_score - perturbed_score
            word_contributions.append((word, diff))
            
        # Normalize contributions for visualization
        max_diff = max(abs(c[1]) for c in word_contributions) if word_contributions else 0
        normalized = []
        for word, diff in word_contributions:
            weight = diff / max_diff if max_diff > 0 else 0.0
            normalized.append({"word": word, "weight": weight})
            
        return normalized
