# 🧠 Continuous Bag-of-Words (CBOW) in PyTorch

A clean, modular, and beginner-friendly implementation of the **Continuous Bag-of-Words (CBOW)** word embedding algorithm using PyTorch. This project serves as an educational introduction to vector representation of words, custom datasets, and simple neural network models in PyTorch.

---

## 📖 Introduction to CBOW

### What is CBOW?
The **Continuous Bag-of-Words (CBOW)** model is a neural network architecture introduced by Mikolov et al. in 2013 for learning dense vector representations of words (word embeddings). 

The core task of CBOW is to **predict a target word given its surrounding context words**. For example, in the sentence:
> *"The cat sat on the mat"*

If the target word is **"sat"** and we have a context window of $C = 2$ words:
* **Context words (Input)**: `["the", "cat", "on", "the"]`
* **Target word (Label)**: `"sat"`

Because it averages the context embeddings, it treats the context as a "bag of words"—order of context words does not affect the prediction, hence the name.

---

### CBOW vs. Skip-Gram

The Word2Vec framework includes two main architectures: **CBOW** and **Skip-Gram**. They are mirror images of each other:

| Feature | Continuous Bag-of-Words (CBOW) | Skip-Gram |
| :--- | :--- | :--- |
| **Objective** | Predict **one target word** from context words. | Predict **context words** from a single target word. |
| **Input** | Multiple context words ($2 \times C$ words). | Single target word ($1$ word). |
| **Output** | Single target word. | Multiple context words. |
| **Speed** | Faster to train; converges quickly on common words. | Slower to train; requires more training samples. |
| **Performance** | Performs slightly better on frequent words. | Performs better with infrequent/rare words and small datasets. |

---

## 🏗️ Model Architecture

The CBOW architecture implemented in this project is structured as follows:

1. **Input Layer**: A sequence of indices corresponding to context words: shape `[BatchSize, 2 * C]`.
2. **Embedding Layer**: A lookup table of size `[VocabSize, EmbedDim]` that maps indices to dense vector representations: shape `[BatchSize, 2 * C, EmbedDim]`.
3. **Average Pooling (Mean)**: Combines context word embeddings by averaging them along the context length dimension: shape `[BatchSize, EmbedDim]`.
4. **Linear Projection Layer**: Projects the averaged vector representation back to vocabulary size to compute logits: shape `[BatchSize, VocabSize]`.
5. **Loss Computation**: Cross-entropy loss compares logits against target word labels during training.

```
Context Word Indices [x_1, x_2, ..., x_2C]
                 ↓
      [ Embedding Lookup ]
                 ↓
      Context Embeddings Matrix
                 ↓
         [ Average Pool ]
                 ↓
         Context Vector (mean)
                 ↓
        [ Linear Projection ]
                 ↓
            Word Logits
```

---

## 📁 Project Structure

```
CBOW_PyTorch/
├── .gitignore          # Ignores generated weight binaries and cache files
├── README.md           # This educational guide & documentation
├── CBOW_PyTorch.ipynb  # Primary implementation in a Jupyter Notebook
├── requirements.txt    # Project dependencies
└── sample_corpus.txt   # Default text corpus for model training
```

---

## 🚀 Setup & Installation

1. **Navigate to the project folder**:
   ```bash
   cd CBOW_PyTorch
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment (e.g., `venv` or `conda`):
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure you also have `jupyter` or `notebook` installed to run the notebook.*

---

## 📖 Running the Notebook

This project has been consolidated into a single Jupyter Notebook to make it easy to follow and execute interactively.

To run the notebook:
1. Start Jupyter Notebook/JupyterLab:
   ```bash
   jupyter notebook
   ```
2. Open **`CBOW_PyTorch.ipynb`**.
3. Run the cells from top to bottom.

The notebook contains:
- **Load Dataset & Preprocessing**: Clean text and generate vocabulary mappings.
- **Context-Target Pair Generation**: Generate inputs and labels using a sliding window.
- **Dataset Class**: Custom PyTorch dataset and dataloader mappings.
- **Model Definition**: The PyTorch CBOW neural network structure.
- **Training**: Set hyperparameters and optimize the model weights.
- **Save Model**: Save weights and vocabulary metadata for future use.
- **Inference & Sample Predictions**: Query the model with context phrases to predict the missing target word.

