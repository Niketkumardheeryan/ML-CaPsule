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
├── cbow.py             # PyTorch CBOW model implementation (nn.Module)
├── dataset.py          # Preprocessing, vocabulary mappings, and PyTorch Dataset
├── train.py            # Training script with command line arguments
├── inference.py        # Prediction script (supports interactive and CLI modes)
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

---

## 🏋️ Training the Model

To train the CBOW model, run the `train.py` script. It parses the corpus, builds a vocabulary mapping, generates training samples, trains the network, and exports model files.

### Commands

**Train with default settings (epochs=100, embed_dim=50, window_size=2):**
```bash
python train.py
```

**Custom training settings:**
```bash
python train.py --epochs 150 --lr 0.005 --embed_dim 32 --window_size 2 --batch_size 16
```

### Options:
* `--corpus`: Path to the text corpus file (default: `sample_corpus.txt`).
* `--window_size`: Size of the context window on each side of the target word (default: `2`).
* `--embed_dim`: Size of the dense word embeddings (default: `50`).
* `--epochs`: Number of training iterations (default: `100`).
* `--lr`: Optimizer learning rate (default: `0.005`).
* `--batch_size`: Batch size for the PyTorch DataLoader (default: `32`).
* `--model_dir`: Directory to save model weights and config metadata (default: `saved_model`).

---

## 🔮 Inference & Predictions

After training, you can query the model to predict the missing word based on a given set of context words. 

The model expects exactly $2 \times C$ context words (where $C$ is the training window size). Out-of-vocabulary (OOV) words are automatically filtered out, and inputs are adjusted dynamically if they differ from the expected length.

### 1. Single Command CLI Mode
Pass the context words as a space-separated string using the `--context` argument:
```bash
python inference.py --context "the cbow the model" --top_k 3
```

### 2. Interactive Loop Mode
Run the script without the `--context` parameter to start an interactive console:
```bash
python inference.py --interactive
```
*Type `exit` or `quit` to exit interactive mode.*

---

## 📊 Example Output

### Training Log
```text
Using device: cpu
Reading corpus from: CBOW_PyTorch/sample_corpus.txt
Tokenized corpus: 141 total tokens.
Vocabulary size: 85 unique words.
Generated 137 context-target training pairs.

Starting training...
Epoch 001/100 - Loss: 4.4441
Epoch 010/100 - Loss: 1.4978
Epoch 020/100 - Loss: 0.3213
...
Epoch 100/100 - Loss: 0.0085
Training completed.

Model state dict saved to CBOW_PyTorch/saved_model\cbow_model.pt
Vocabulary and configuration metadata saved to CBOW_PyTorch/saved_model\metadata.json
```

### Querying the Model
```text
Model successfully loaded from 'CBOW_PyTorch/saved_model'
Model Vocabulary Size: 85
Expected Context Words: 4 words (window_size=2)

Context entered: 'the cbow the model'
Active context tokens: ['the', 'cbow', 'the', 'model']

--- Predictions ---
Rank 1: architecture    Prob: 0.9839 (Best Predict)
Rank 2: can             Prob: 0.0053 
Rank 3: predicts        Prob: 0.0032 
-------------------
```
