# NLP Techniques

This repository contains comprehensive Jupyter notebooks exploring various Natural Language Processing (NLP) techniques using Python libraries like NLTK, Gensim, and NumPy.

## Contents

### 1. **Word Similarities** (`word_similarities.ipynb`)
Explores word similarity metrics using pre-trained GloVe embeddings:
- **Cosine Similarity**: Measures semantic meaning based on vector direction
- **Jaccard Similarity**: Evaluates character-level spelling overlap
- **Euclidean Distance**: Calculates spatial distance between word vectors

Demonstrates the difference between semantic and lexical similarity across four GloVe model dimensions (50, 100, 200, 300).

---

### 2. **Language Modelling using N-grams** (`language_modelling .ipynb`)
Builds and compares N-gram language models trained on the Plain Text Wikipedia corpus:
- **Unigram Model**: Selects words based on frequency alone (no word order)
- **Bigram Model**: Considers immediate preceding word
- **Trigram Model**: Uses two-word context for generation

Includes:
- Sentence generation from each model
- Perplexity evaluation with Add-1 smoothing
- Analysis of data sparsity effects on model performance

---

### 3. **Word Embeddings** (`word_embedding.ipynb`)
Trains and compares Word2Vec models on Wikipedia data:
- **CBOW (Continuous Bag of Words)**: Predicts current word from context words
- **Skip-gram**: Predicts context words from current word

Evaluates models using:
- Most similar word rankings
- Analogy tasks (e.g., "king" - "man" + "woman" = "queen")
- Semantic coherence and confidence in predictions

---

### 4. **Smoothing Techniques** (`smoothing_techniques.ipynb`)
Addresses the zero probability problem in language modeling with six smoothing methods:
1. **Laplace Smoothing (Add-1)**: Adds 1 to all counts
2. **Add-k Smoothing**: Adds tunable constant k (0 < k < 1)
3. **Good-Turing Smoothing**: Redistributes probability using frequency-of-frequencies
4. **Simple Backoff Smoothing**: Falls back to lower-order n-grams for unseen events
5. **Interpolation Smoothing**: Weighted combination of unigram and bigram probabilities
6. **Kneser-Ney Smoothing**: Advanced method using discounting and continuation probabilities

Includes comparative analysis and practical examples on Wikipedia data.

---

## Key Datasets
- **Plain Text Wikipedia 2020-11**: Used for language modeling, embeddings, and smoothing experiments

## Technologies Used
- **NLTK**: Tokenization, n-gram generation, and language processing utilities
- **Gensim**: Pre-trained word embeddings (GloVe) and Word2Vec model training
- **NumPy**: Numerical computations (cosine similarity, Euclidean distance)
- **Pandas**: Data manipulation and analysis
- **Kaggle Hub**: Dataset downloading
