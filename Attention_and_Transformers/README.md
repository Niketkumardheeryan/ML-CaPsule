# 🤖 Attention & Transformers: Interactive Learning Dashboard

A comprehensive, interactive learning platform for understanding **Attention Mechanisms** and **Transformer Architectures** using Streamlit, Jupyter notebooks, and hands-on visualizations.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-latest-red)
![PyTorch](https://img.shields.io/badge/PyTorch-latest-orange)
![Transformers](https://img.shields.io/badge/Transformers-latest-brightgreen)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Streamlit Dashboard](#streamlit-dashboard)
  - [Jupyter Notebooks](#jupyter-notebooks)
- [Features](#features)
- [Datasets](#datasets)
- [Tutorial Modules](#tutorial-modules)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project provides an **interactive, visual introduction** to:

1. **Attention Mechanisms**
   - Scaled Dot-Product Attention
   - Multi-Head Attention
   - Attention visualization and interpretation
   - Attention weight heatmaps

2. **Transformer Architecture**
   - Encoder-Decoder architecture
   - Self-Attention layers
   - Feed-Forward Networks
   - Positional Encoding
   - Complete transformer pipeline

3. **Practical Applications**
   - Machine Translation
   - Text Classification
   - Sentiment Analysis
   - Named Entity Recognition (NER)
   - Question Answering

4. **Interactive Visualizations**
   - Real-time attention heatmaps
   - Token-to-token attention flows
   - Embedding space visualization (t-SNE/UMAP)
   - Model prediction explanations

---

## 📁 Project Structure

```
attention-transformers/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── app.py                             # Main Streamlit dashboard
│
├── notebooks/                         # Jupyter tutorials
│   ├── 01_attention_basics.ipynb      # Introduction to attention
│   ├── 02_scaled_dot_product.ipynb    # Scaled dot-product attention
│   ├── 03_multi_head_attention.ipynb  # Multi-head attention
│   ├── 04_transformers_intro.ipynb    # Transformer architecture
│   ├── 05_positional_encoding.ipynb   # Positional encoding explained
│   ├── 06_training_guide.ipynb        # Training transformers from scratch
│   └── 07_applications.ipynb          # Real-world applications
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── attention.py                   # Attention implementations
│   ├── transformers.py                # Transformer modules
│   ├── visualization.py               # Plotting utilities
│   ├── data.py                        # Dataset loading utilities
│   └── utils.py                       # Helper functions
│
├── data/                              # Data directory (downloaded at runtime)
│   ├── datasets/                      # Cached datasets
│   └── models/                        # Pretrained models
│
└── assets/                            # Images and static files
    ├── architecture_diagram.png
    ├── attention_mechanism.png
    └── example_outputs/
```

---

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda
- ~5GB free disk space (for models and datasets)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/attention-transformers.git
cd attention-transformers
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n transformers python=3.10
conda activate transformers
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Datasets (Optional)

```bash
python scripts/download_datasets.py
```

---

## 🚀 Usage

### Streamlit Dashboard

The interactive dashboard provides hands-on exploration of attention and transformers.

#### Start the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

#### Dashboard Sections

1. **🏠 Home**
   - Project overview
   - Quick start guide
   - Key concepts

2. **📚 Attention Mechanics**
   - Interactive attention visualization
   - Scaled dot-product attention
   - Multi-head attention demo
   - Attention weight analysis

3. **🏗️ Transformer Architecture**
   - Architecture diagram
   - Component breakdown
   - Data flow visualization
   - Position encoding demo

4. **🎓 Interactive Tutorial**
   - Step-by-step learning
   - Code visualization
   - Attention weight heatmaps
   - Model predictions with explanations

5. **🔬 Experiments**
   - Train attention from scratch
   - Compare attention types
   - Benchmark different models
   - Visualize learned patterns

6. **📊 Analysis Tools**
   - Attention pattern analysis
   - Token importance ranking
   - Embedding space visualization
   - Similarity matrices

7. **❓ FAQ & Resources**
   - Common questions
   - Research papers
   - External resources
   - Implementation tips

---

### Jupyter Notebooks

Comprehensive tutorials in Jupyter format for deeper learning.

#### Starting Jupyter

```bash
jupyter notebook
```

Then navigate to `notebooks/` and open any notebook.

#### Notebook Modules

| Notebook | Duration | Topics |
|----------|----------|--------|
| `01_attention_basics.ipynb` | 15 min | Motivation, attention concept, use cases |
| `02_scaled_dot_product.ipynb` | 20 min | Query-Key-Value, scoring, softmax |
| `03_multi_head_attention.ipynb` | 20 min | Multi-head attention, parallel heads |
| `04_transformers_intro.ipynb` | 25 min | Full architecture, encoder, decoder |
| `05_positional_encoding.ipynb` | 15 min | Sinusoidal encoding, variations |
| `06_training_guide.ipynb` | 40 min | Training from scratch, fine-tuning |
| `07_applications.ipynb` | 30 min | Translation, classification, NER |

---

## ✨ Features

### 🎨 Interactive Visualizations

- **Attention Heatmaps**: Real-time visualization of attention weights
- **Token Flow Diagrams**: Show how information flows through attention layers
- **Embedding Projections**: Visualize high-dimensional embeddings in 2D/3D
- **Attention Patterns**: Identify and analyze learned attention patterns
- **Model Predictions**: Explain predictions with attention-based saliency maps

### 📊 Educational Tools

- **Interactive Code**: Run and modify code snippets in real-time
- **Parameter Playground**: Adjust parameters and see effects instantly
- **Comparison Mode**: Compare different attention mechanisms side-by-side
- **Step-by-Step Debugging**: Trace execution step-by-step through layers

### 🧠 Learning Paths

1. **Beginner Path** (1-2 hours)
   - Notebooks 1-2
   - Dashboard: Attention Mechanics section
   - FAQ & Resources

2. **Intermediate Path** (3-4 hours)
   - Notebooks 3-5
   - Dashboard: Transformer Architecture section
   - Interactive Tutorial section

3. **Advanced Path** (6-8 hours)
   - Notebooks 6-7
   - Dashboard: Experiments section
   - Training from scratch with custom data

4. **Applied Path** (4-6 hours)
   - Notebooks 7
   - Dashboard: Applications section
   - Fine-tuning on custom datasets

### 🔬 Experimental Tools

- **Training from Scratch**: Implement and train a transformer model
- **Fine-tuning**: Transfer learning on different datasets
- **Benchmarking**: Compare model performance and speed
- **Ablation Studies**: Understand component importance

---

## 📦 Datasets

Datasets are automatically downloaded using `torch.hub` and `kagglehub` on first use.

### Included Datasets

#### 1. **MNIST** (Image Classification)
- **Source**: torch.hub
- **Size**: ~15MB
- **Use**: Simple attention-based image classification
- **Auto-download**: Yes

```python
from src.data import load_mnist
train_data, test_data = load_mnist()
```

#### 2. **Fashion-MNIST** (Image Classification)
- **Source**: torch.hub
- **Size**: ~30MB
- **Use**: Fashion item classification with attention
- **Auto-download**: Yes

```python
from src.data import load_fashion_mnist
train_data, test_data = load_fashion_mnist()
```

#### 3. **IWSLT2017** (Machine Translation)
- **Source**: torchtext / huggingface
- **Size**: ~100MB
- **Languages**: English ↔ German, French, Italian
- **Use**: Sequence-to-sequence with attention
- **Auto-download**: On demand

```python
from src.data import load_iwslt
train_data = load_iwslt(lang_pair="en-de")
```

#### 4. **AG News** (Text Classification)
- **Source**: torchtext
- **Size**: ~30MB
- **Use**: News classification with attention
- **Auto-download**: Yes

```python
from src.data import load_ag_news
train_data, test_data = load_ag_news()
```

#### 5. **Movie Reviews** (Sentiment Analysis)
- **Source**: kagglehub / Hugging Face
- **Size**: ~50MB
- **Use**: Sentiment analysis with attention
- **Auto-download**: On demand

```python
from src.data import load_movie_reviews
train_data, test_data = load_movie_reviews()
```

#### 6. **SQuAD** (Question Answering)
- **Source**: Hugging Face datasets
- **Size**: ~100MB
- **Use**: Reading comprehension with attention
- **Auto-download**: On demand

```python
from src.data import load_squad
train_data = load_squad(split="train", samples=5000)
```

### Custom Datasets

Load your own datasets:

```python
from src.data import DatasetLoader

loader = DatasetLoader()
data = loader.load_csv("path/to/data.csv")
```

---

## 🎓 Tutorial Modules

### Module 1: Attention Basics (Notebook 1)
- What is attention?
- Motivation and use cases
- Attention vs non-attention models
- When to use attention

### Module 2: Scaled Dot-Product Attention (Notebook 2)
```
Theory:
  Attention(Q, K, V) = softmax(QK^T / √d_k)V

Implementation:
  - Query-Key-Value computation
  - Scaling factor
  - Softmax normalization
  - Value weighting
```

### Module 3: Multi-Head Attention (Notebook 3)
- Multiple parallel attention heads
- Head combination strategies
- Benefits of multi-head attention
- Analyzing individual heads

### Module 4: Transformer Architecture (Notebook 4)
- Encoder layers
- Decoder layers
- Attention mechanisms in each
- Information flow
- Complete forward pass

### Module 5: Positional Encoding (Notebook 5)
- Why positional encoding is needed
- Sinusoidal encoding formula
- Alternative encoding schemes
- Visualizing position embeddings

### Module 6: Training (Notebook 6)
- Loss functions and optimization
- Training loop implementation
- Hyperparameter tuning
- Regularization techniques
- Monitoring and visualization

### Module 7: Applications (Notebook 7)
- Machine Translation
- Text Classification
- Sentiment Analysis
- Named Entity Recognition
- Question Answering

---

## 🔬 Advanced Features

### 1. Attention Visualization
```python
from src.visualization import plot_attention_heatmap

# Visualize attention weights
plot_attention_heatmap(
    attention_weights,
    tokens=tokens,
    layer=0,
    head=0
)
```

### 2. Model Interpretability
```python
from src.utils import get_attention_saliency

# Get token importance scores
saliency = get_attention_saliency(model, input_ids)
plot_saliency(tokens, saliency)
```

### 3. Embedding Visualization
```python
from src.visualization import plot_embeddings

# Project embeddings to 2D/3D
plot_embeddings(
    embeddings,
    labels=labels,
    method='tsne'  # or 'umap'
)
```

### 4. Attention Pattern Analysis
```python
from src.utils import analyze_attention_patterns

# Analyze what patterns the model learned
patterns = analyze_attention_patterns(model, data)
# Returns: diagonal patterns, token similarity, etc.
```

---

## 🛠️ Advanced Usage

### Training a Custom Transformer

```python
from src.transformers import TransformerModel
from src.data import load_ag_news
import torch

# Load data
train_data, test_data = load_ag_news()

# Create model
model = TransformerModel(
    vocab_size=10000,
    embed_dim=256,
    num_heads=8,
    num_layers=3,
    ff_dim=1024,
    max_seq_len=128
)

# Train
model.train_epoch(train_data, learning_rate=0.001)

# Evaluate
accuracy = model.evaluate(test_data)
print(f"Accuracy: {accuracy:.2%}")
```

### Fine-tuning Pretrained Models

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.data import load_custom_data

# Load pretrained model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")

# Load your data
train_data = load_custom_data("data/train.csv")

# Fine-tune
model.finetune(train_data, tokenizer)
```

### Using Pre-trained Models

```python
from src.models import load_pretrained_model

# Available: 'bert', 't5', 'gpt2', 'distilbert'
model = load_pretrained_model('bert-base-uncased')

# Get predictions
text = "This movie is amazing!"
predictions = model.predict(text)
```

---

## 📊 Streamlit Dashboard Pages

### Page 1: Home 🏠
- Welcome message
- Project overview
- Learning paths
- Quick stats

### Page 2: Attention Mechanics 📚
- **Interactive Attention Demo**
  - Input text
  - Real-time attention computation
  - Attention heatmap
  - Token-to-token flows

- **Scaled Dot-Product Attention**
  - Step-by-step computation
  - Parameter adjustment
  - Weight visualization

- **Multi-Head Attention**
  - Number of heads slider
  - Individual head visualization
  - Head specialization analysis

### Page 3: Transformer Architecture 🏗️
- **Architecture Diagram**
  - Encoder-decoder structure
  - Layer connections
  - Data shapes at each layer

- **Component Breakdown**
  - Self-attention
  - Feed-forward networks
  - Layer normalization
  - Residual connections

- **Positional Encoding**
  - Sine/cosine curves
  - Position embedding visualization
  - Encoding comparison

### Page 4: Tutorial 🎓
- **Learning Modules**
  - Select module (1-7)
  - Code explanation
  - Interactive visualization
  - Quiz/questions

- **Code Playground**
  - Edit and run code
  - See live outputs
  - Visualization updates

### Page 5: Experiments 🔬
- **Train from Scratch**
  - Dataset selection
  - Model configuration
  - Training progress
  - Performance metrics

- **Benchmarking**
  - Compare models
  - Speed tests
  - Memory usage
  - Accuracy comparison

- **Ablation Study**
  - Remove components
  - Analyze impact
  - Performance drops

### Page 6: Analysis Tools 📊
- **Attention Analysis**
  - Query which model
  - Select data sample
  - Visualize attention patterns
  - Export results

- **Token Importance**
  - Attention-based importance
  - Gradient-based importance
  - Top-k important tokens

- **Embedding Analysis**
  - t-SNE projection
  - UMAP projection
  - Cluster visualization
  - Similarity heatmaps

### Page 7: FAQ & Resources ❓
- Common questions answered
- Research papers
- Blog posts
- External resources

---

## 🐛 Troubleshooting

### Issue: "CUDA out of memory"
**Solution:** Use smaller batch sizes
```python
# In streamlit app config
streamlit run app.py --logger.level=debug --client.maxMessageSize=200
```

### Issue: Dataset download fails
**Solution:** Manual download
```bash
python scripts/download_datasets.py --dataset all
```

### Issue: Slow notebook execution
**Solution:** Use smaller samples
```python
from src.data import load_mnist
# Load only 1000 samples
data = load_mnist(samples=1000)
```

### Issue: Visualization not showing
**Solution:** Clear Streamlit cache
```bash
rm -rf ~/.streamlit/cache
streamlit run app.py --logger.level=debug
```

---

## 📚 Learning Resources

### Official Documentation
- [PyTorch Transformers](https://huggingface.co/docs/transformers/)
- [Attention is All You Need](https://arxiv.org/abs/1706.03762)
- [BERT Paper](https://arxiv.org/abs/1810.04805)

### Recommended Reading
1. Vaswani et al. (2017) - Attention is All You Need
2. Devlin et al. (2019) - BERT: Pre-training of Deep Bidirectional Transformers
3. Radford et al. (2019) - Language Models are Unsupervised Multitask Learners

### Online Courses
- [Stanford CS224N](http://web.stanford.edu/class/cs224n/)
- [MIT Deep Learning](https://deeplearning.mit.edu/)
- [Fast.ai](https://www.fast.ai/)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [PyTorch](https://pytorch.org/)
- [Streamlit](https://streamlit.io/)
- All researchers and contributors in the NLP community

---

## 📧 Contact & Support

- **Questions?** Open an issue on GitHub
- **Feature requests?** Start a discussion
- **Bug reports?** Submit with reproducible examples

---

## 🚀 Quick Start Commands

```bash
# Install
pip install -r requirements.txt

# Run dashboard
streamlit run app.py

# Run notebooks
jupyter notebook

# Download datasets
python scripts/download_datasets.py

# Run tests
pytest tests/

# Build documentation
cd docs && make html
```

---

**Happy Learning! 🎓**

Made with ❤️ for the NLP and ML community
