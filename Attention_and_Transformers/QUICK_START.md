# 🚀 Quick Start Guide

Get up and running with the Attention & Transformers project in 5 minutes!

## Installation (2 minutes)

### 1. Clone & Setup

```bash
# Create project directory
mkdir attention-transformers
cd attention-transformers

# Copy all files from the project
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Download Datasets (Optional, auto-downloads on first use)

```bash
python scripts/download_datasets.py
```

## Running the Project

### Option 1: Streamlit Dashboard (Recommended for Interactive Learning)

```bash
streamlit run app.py
```

Opens at: http://localhost:8501

Features:
- 🎨 Interactive visualizations
- 📊 Real-time experiments
- 🎓 Step-by-step tutorials
- 📈 Analysis tools

### Option 2: Jupyter Notebooks (Recommended for Deep Learning)

```bash
jupyter notebook
```

Then open any notebook from the `notebooks/` folder:

1. **`01_attention_basics.ipynb`** - Start here! (15 min)
2. **`02_scaled_dot_product.ipynb`** - Core mechanism (20 min)
3. **`03_multi_head_attention.ipynb`** - Multiple heads (20 min)
4. **`04_transformers_intro.ipynb`** - Full architecture (25 min)
5. **`05_positional_encoding.ipynb`** - Position info (15 min)
6. **`06_training_guide.ipynb`** - Training from scratch (40 min)
7. **`07_applications.ipynb`** - Real applications (30 min)

### Option 3: Python Scripts

```bash
# Run specific modules
python -c "from src.data import get_mnist; loader = get_mnist(); print(loader)"

# Run tests
pytest tests/
```

---

## Learning Path

### 🟢 Quick Overview (30 minutes)

```bash
# Best for: Understanding the basics quickly
# Steps:
1. Read this file (5 min)
2. Start Streamlit app → Go to "Home" (5 min)
3. Streamlit app → "Attention Mechanics" tab (15 min)
4. FAQ & Resources page (5 min)
```

### 🟡 Standard Learning (4 hours)

```bash
# Best for: Comprehensive understanding
# Steps:
1. Notebook 01: Attention Basics (15 min)
2. Notebook 02: Scaled Dot-Product (20 min)
3. Streamlit: Transformer Architecture (30 min)
4. Notebook 03: Multi-Head Attention (20 min)
5. Notebook 04: Transformers Intro (25 min)
6. Streamlit: Interactive Tutorial (30 min)
7. Notebook 07: Applications (30 min)

Total: ~3.5 hours
```

### 🔴 Expert Deep-Dive (8 hours)

```bash
# Best for: Implementing from scratch
# Steps:
1. All 7 notebooks (3 hours)
2. Streamlit: All sections (2 hours)
3. Notebook 06: Training Guide (40 min)
4. Streamlit: Experiments section (1.5 hours)
5. Modify code and experiment (1 hour)

Total: ~8 hours
```

---

## File Structure Overview

```
📦 attention-transformers/
├── 📄 app.py                  # Streamlit dashboard (start here!)
├── 📄 README.md               # Full documentation
├── 📄 requirements.txt        # Dependencies
│
├── 📁 notebooks/              # Jupyter tutorials
│   ├── 01_attention_basics.ipynb
│   ├── 02_scaled_dot_product.ipynb
│   └── ... (7 total)
│
├── 📁 src/                    # Source code
│   ├── attention.py           # Attention implementations
│   ├── data.py                # Data loading
│   ├── visualization.py       # Plotting utilities
│   └── utils.py               # Helper functions
│
└── 📁 data/                   # Datasets (auto-created)
```

---

## Key Concepts (TL;DR)

### What is Attention?

**Weighted average** of values based on query-key similarity.

```
Simple Example:
Sentence: "The cat sat on the mat"
Query (word 3: "sat"):
  - Focus on "cat" (30%)
  - Focus on "mat" (20%)
  - Focus on "on" (15%)
  - Others (35%)

Result: Weighted combination of embeddings
```

### Why Transformers?

- ✅ **Parallel processing**: No recurrence (faster)
- ✅ **Long-range deps**: Direct connections (better)
- ✅ **Interpretable**: See attention weights (explainable)
- ✅ **Scalable**: Works with huge datasets

### Core Formula

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

Where:
- Q = Query (what we look for)
- K = Key (what each position has)
- V = Value (information to aggregate)
- d_k = Key dimension (for scaling)

---

## Common Tasks

### Task 1: Understand Attention in 15 Minutes

```bash
# Option A: Streamlit
streamlit run app.py
# → Click "Attention Mechanics" → "Intuition" tab

# Option B: Jupyter
jupyter notebook
# → Open 01_attention_basics.ipynb
# → Run first 3 cells
```

### Task 2: Visualize Attention Weights

```python
from src.visualization import plot_attention_heatmap
import numpy as np

# Create sample attention weights
tokens = ["The", "cat", "sat", "on", "the", "mat"]
attention = np.random.rand(6, 6)
attention = attention / attention.sum(axis=1, keepdims=True)

# Plot
plot_attention_heatmap(attention, tokens, title="Sentence Attention")
```

### Task 3: Load and Train on Data

```python
from src.data import get_mnist, get_copy_task
from src.attention import MultiHeadAttention
import torch

# Load data
train_loader = get_mnist("train", samples=5000)

# Create model
attention = MultiHeadAttention(d_model=64, num_heads=4)

# Quick test
for images, labels in train_loader:
    # Use attention model
    pass
```

### Task 4: Implement Custom Attention

```python
# Edit this file: src/attention.py
# Or create new file: my_custom_attention.py

import torch.nn as nn

class MyAttention(nn.Module):
    def forward(self, query, key, value):
        # Your implementation here
        pass
```

---

## Troubleshooting

### ❌ "CUDA out of memory"

**Solution**: Use CPU or smaller batch size

```python
# Use CPU
device = torch.device("cpu")

# Smaller batch
loader = get_mnist(batch_size=8)  # Instead of 32
```

### ❌ "Module not found"

**Solution**: Install requirements

```bash
pip install -r requirements.txt
```

### ❌ "Dataset download fails"

**Solution**: Manual download or use smaller dataset

```python
# Use smaller built-in dataset
train_loader = get_copy_task(num_samples=1000)
```

### ❌ "Streamlit not responding"

**Solution**: Clear cache and restart

```bash
rm -rf ~/.streamlit/cache
streamlit run app.py
```

---

## Next Steps

### After Completing Quick Overview

1. **Go Deeper**: Work through Notebooks 1-4 (~2 hours)
2. **Experiment**: Use Streamlit Experiments section
3. **Train Custom**: Notebook 6 shows full training loop
4. **Apply to Data**: Notebook 7 shows real applications

### Recommended Projects

1. **Build Sentiment Classifier**
   - Use attention on movie reviews
   - Fine-tune pretrained model

2. **Implement Machine Translation**
   - Encoder-decoder with attention
   - Train on small language pair

3. **Create Named Entity Recognizer**
   - Use attention for context
   - Test on custom data

4. **Analyze Attention Patterns**
   - Visualize what model learns
   - Compare different architectures

---

## Resources

### Documentation
- [PyTorch](https://pytorch.org/docs/)
- [Transformers (Hugging Face)](https://huggingface.co/docs/transformers/)
- [Streamlit](https://docs.streamlit.io/)

### Papers
- Vaswani et al. (2017) - [Attention is All You Need](https://arxiv.org/abs/1706.03762)
- Devlin et al. (2019) - [BERT](https://arxiv.org/abs/1810.04805)

### Visualizations
- [Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
- [Distill.pub](https://distill.pub/)

### Courses
- [Stanford CS224N](http://web.stanford.edu/class/cs224n/)
- [Fast.ai](https://www.fast.ai/)

---

## Getting Help

### In Streamlit
→ Click **"FAQ & Resources"** page

### In Jupyter
→ Each notebook has a **"Common Questions"** section

### Online
→ Check **README.md** for detailed docs

---

## Tips & Tricks

### 💡 Pro Tips

1. **Start small**: Test with `samples=1000` before full dataset
2. **Visualize first**: See attention before changing code
3. **Check shapes**: Print tensor shapes to debug
4. **Use comments**: Document what each line does

### ⚡ Speed Tips

1. Use GPU if available: `device = torch.device("cuda")`
2. Reduce sequence length: `seq_len = 50` instead of 512
3. Smaller models: `num_heads = 4` instead of 16
4. Fewer layers: `num_layers = 3` instead of 12

### 📊 Visualization Tips

1. Plot attention for first 5-10 tokens (clearer)
2. Use different colormaps for different datasets
3. Compare different models side-by-side
4. Save visualizations: `save_path="my_plot.png"`

---

## Contributing

Have improvements? Want to add content?

1. Fork the repository
2. Make changes
3. Test thoroughly
4. Submit pull request

---

## License

MIT License - See LICENSE file

---

## Summary

| Time | Path | What You Learn |
|------|------|----------------|
| 15 min | Quick | What is attention? |
| 1 hour | Quick+ | How does attention work? |
| 4 hours | Standard | Build transformers from scratch |
| 8 hours | Expert | Training & applications |

**Start now**: `streamlit run app.py` 🚀

**Questions?** Check FAQ in app or README.md 📚

**Ready to learn?** Pick your path above and start! 🎓
