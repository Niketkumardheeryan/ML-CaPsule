"""Resume and job-description preprocessing utilities using spaCy and NLTK."""

from __future__ import annotations

import logging
import re
from functools import lru_cache
from typing import Optional

import nltk
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

logger = logging.getLogger(__name__)

DEFAULT_NOISE_WORDS = {"resume", "curriculum vitae", "cv"}


@lru_cache(maxsize=1)
def _get_nlp() -> "spacy.language.Language":
    """Load and cache the spaCy English model once per process."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError as exc:
        logger.warning("spaCy model 'en_core_web_sm' is not installed; attempting to download it.")
        try:
            from spacy.cli import download

            download("en_core_web_sm")
            return spacy.load("en_core_web_sm")
        except Exception as download_exc:  # pragma: no cover - depends on runtime environment
            raise RuntimeError(
                "The spaCy model 'en_core_web_sm' could not be loaded. Install it with 'python -m spacy download en_core_web_sm'."
            ) from download_exc


@lru_cache(maxsize=1)
def _get_nltk_stopwords() -> set[str]:
    """Load NLTK English stopwords once and return them as a normalized set."""
    try:
        from nltk.corpus import stopwords as nltk_stopwords

        return {word.lower() for word in nltk_stopwords.words("english")}
    except LookupError:
        try:
            nltk.download("stopwords", quiet=True)
            from nltk.corpus import stopwords as nltk_stopwords

            return {word.lower() for word in nltk_stopwords.words("english")}
        except Exception as exc:  # pragma: no cover - depends on runtime environment
            logger.warning("NLTK stopwords could not be loaded: %s", exc)
            return set()


def clean_text(text: str) -> str:
    """Lowercase text and remove URLs, emails, phone numbers, punctuation, and extra whitespace."""
    if not text:
        return ""

    cleaned = text.lower()
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)
    cleaned = re.sub(r"\S+@\S+", " ", cleaned)
    cleaned = re.sub(
        r"\b(?:\+?\d[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,3}\d{3,4}\b",
        " ",
        cleaned,
    )
    cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def tokenize_and_lemmatize(text: str) -> list[str]:
    """Tokenize and lemmatize text with spaCy, dropping punctuation and whitespace tokens."""
    if not text:
        return []

    nlp = _get_nlp()
    doc = nlp(text)
    tokens: list[str] = []

    for token in doc:
        if token.is_space or token.is_punct:
            continue

        lemma = token.lemma_.lower().strip()
        if not lemma or lemma == "-pron-":
            lemma = token.text.lower().strip()

        if lemma:
            tokens.append(lemma)

    return tokens


def remove_stopwords(tokens: list[str], custom_stopwords: Optional[set[str]] = None) -> list[str]:
    """Remove stopwords using spaCy's default stopword list plus optional custom noise terms."""
    if not tokens:
        return []

    stopword_set = set(STOP_WORDS)
    stopword_set.update(_get_nltk_stopwords())

    if custom_stopwords:
        stopword_set.update({word.lower().strip() for word in custom_stopwords if word and word.strip()})

    filtered = [token for token in tokens if token and token not in stopword_set]
    return filtered


def preprocess(text: str, custom_stopwords: Optional[set[str]] = None) -> str:
    """Clean, tokenize, lemmatize, and remove stopwords for downstream vectorization."""
    cleaned_text = clean_text(text)
    if not cleaned_text:
        return ""

    tokens = tokenize_and_lemmatize(cleaned_text)
    filtered_tokens = remove_stopwords(tokens, custom_stopwords=custom_stopwords)
    return " ".join(filtered_tokens)


if __name__ == "__main__":
    sample_resume = (
        "John Doe is a data scientist with experience in Python, machine learning, and NLP. "
        "He worked at Acme Corp from 2020 to 2024. Contact: +1 555-123-4567 | john.doe@example.com"
    )
    print(preprocess(sample_resume, custom_stopwords=DEFAULT_NOISE_WORDS))
