# English-to-German Neural Machine Translation with Bahdanau Attention

## Overview

This project implements an **English-to-German Neural Machine Translation (NMT)** system using a **Sequence-to-Sequence (Seq2Seq)** architecture with **Bahdanau Attention**.

The model translates English sentences into German by learning contextual representations through an Encoder-Decoder architecture enhanced with an Attention mechanism.

---

## Features

* English-to-German Neural Machine Translation
* Seq2Seq Architecture
* GRU-based Encoder and Decoder
* Bahdanau Attention Mechanism
* Text Preprocessing
* Vocabulary Creation
* Tokenization and Padding
* Model Training
* Inference (Sentence Translation)
* Attention Heatmap Visualization
* Training Loss Visualization
* Model Saving and Loading

---

## Project Structure

```text
NMT_English_German_Attention/
│
├── data/
│   ├── eng.txt
│   ├── ger.txt
│   └── preprocess.py
│
├── models/
│   └── nmt_attention_model.pth
│
├── nmt_attention_model.ipynb
├── README.md
├── requirements.txt
├── attention_heatmap.png
└── training_loss.png
```

---

## Technologies Used

* Python
* PyTorch
* NumPy
* Pandas
* Matplotlib
* NLTK

---

## Model Architecture

```
English Sentence
        │
        ▼
Embedding Layer
        │
        ▼
Encoder (GRU)
        │
        ▼
Bahdanau Attention
        │
        ▼
Decoder (GRU)
        │
        ▼
German Translation
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project folder:

```bash
cd NMT_English_German_Attention
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Open:

```
nmt_attention_model.ipynb
```

Run every notebook cell from top to bottom.

---

## Example Translation

**Input**

```
I love machine learning
```

**Output**

```
Ich liebe maschinelles Lernen
```

---

## Attention Heatmap

The model visualizes the attention weights showing how the decoder focuses on different English words while generating the German translation.

Example:

```
English Words
<SOS> | I | love | machine | learning | <EOS>

↓

German Words

ich
liebe
maschinelles
lernen
```

*(Insert the generated `attention_heatmap.png` image here after uploading it to the repository.)*

---

## Training Loss

The model records training loss over epochs.

*(Insert the generated `training_loss.png` image here after uploading it to the repository.)*

---

## Future Improvements

* Train on the Multi30k English-German dataset
* Support beam search decoding
* Replace GRU with Transformer architecture
* Evaluate using BLEU score
* Deploy as a web application using Flask or Streamlit

---

## Author

**Akshita Goel**

GitHub: https://github.com/goelakshita708

LinkedIn: https://www.linkedin.com/in/akshita-goel-1a7626383
