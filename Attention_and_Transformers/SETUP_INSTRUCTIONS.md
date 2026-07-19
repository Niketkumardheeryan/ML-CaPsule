# 🔧 Complete Setup Instructions

## Prerequisites
- Python 3.8 or higher
- pip or conda
- ~5GB free disk space (for models and datasets)
- Git (optional, for cloning)

## Installation Steps

### 1. Create Project Directory
```bash
mkdir attention-transformers
cd attention-transformers
```

### 2. Create Virtual Environment

**Using venv (Python built-in):**
```bash
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**Using conda (if you prefer):**
```bash
conda create -n transformers python=3.10
conda activate transformers
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- PyTorch with torchvision
- Transformers and tokenizers
- Streamlit for dashboard
- Jupyter for notebooks
- Data science libraries (numpy, pandas, scikit-learn)
- Visualization libraries (matplotlib, seaborn, plotly)

### 4. Download Datasets (Optional)
```bash
# Datasets auto-download on first use, or download manually:
python -c "from src.data import DatasetLoader; DatasetLoader.load_mnist()"
```

## Running the Project

### Method 1: Streamlit Dashboard (🎨 Recommended for visualization)
```bash
streamlit run app.py
```
- Opens in browser: http://localhost:8501
- Interactive visualizations
- Real-time experiments
- Beginner friendly

### Method 2: Jupyter Notebooks (📚 Recommended for learning)
```bash
jupyter notebook
```
- Then open `notebooks/01_attention_basics.ipynb`
- Run cells interactively
- See code + output side by side
- Take notes

### Method 3: Python REPL (💻 For quick testing)
```python
python
>>> from src.attention import MultiHeadAttention
>>> from src.data import get_mnist
>>> # Your code here...
```

## Verification: Is Everything Working?

### Quick Test
```bash
python -c "
import torch
import streamlit as st
from src.attention import MultiHeadAttention
from src.data import get_mnist

print('✓ PyTorch version:', torch.__version__)
print('✓ Streamlit version:', st.__version__)
print('✓ Attention module loaded')
print('✓ Data loader available')
print()
print('🎉 Everything is working!')
"
```

### Run Full Tests
```bash
pytest tests/
```

## Troubleshooting

### Problem: "ModuleNotFoundError"
```bash
# Solution 1: Install requirements again
pip install -r requirements.txt

# Solution 2: Check virtual environment is activated
which python  # Should show path in venv/

# Solution 3: Reinstall in development mode
pip install -e .
```

### Problem: "CUDA/GPU not available"
```bash
# Solution: Use CPU (will be slower)
python -c "
import torch
print('CUDA available:', torch.cuda.is_available())
print('Using device: CPU (CUDA not needed for learning)')
"
```

### Problem: "Streamlit port already in use"
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Problem: "Jupyter not found"
```bash
# Install Jupyter
pip install jupyter jupyterlab

# Start Jupyter
jupyter notebook
```

### Problem: "Out of memory errors"
```bash
# Solution: Reduce dataset size in code
from src.data import get_mnist
loader = get_mnist(samples=1000)  # Instead of full dataset
```

## First Time Setup Checklist

- [ ] Created virtual environment
- [ ] Activated virtual environment
- [ ] Installed requirements (`pip install -r requirements.txt`)
- [ ] Verified installation (`python -c "import torch; print('OK')"`)
- [ ] Ran Streamlit dashboard (`streamlit run app.py`)
- [ ] Opened first notebook (`jupyter notebook`)

## Next Steps After Setup

1. **Quick Learning (15 min)**
   - Start Streamlit: `streamlit run app.py`
   - View "Home" page
   - Browse "Attention Mechanics"

2. **Deep Learning (1-4 hours)**
   - Open Notebook 1: `notebooks/01_attention_basics.ipynb`
   - Follow notebooks 1-4 in sequence
   - Run code cells and experiments

3. **Hands-on Practice (6+ hours)**
   - Notebook 5: Positional Encoding
   - Notebook 6: Training from scratch
   - Notebook 7: Applications
   - Streamlit: Experiments section

## Getting Help

1. **Check documentation**
   - README.md (comprehensive reference)
   - QUICK_START.md (5-minute overview)
   - Notebooks (step-by-step with explanations)

2. **Check Streamlit app**
   - Home page: Overview
   - FAQ section: Common questions
   - Resources: Links and papers

3. **Read docstrings**
   ```python
   from src.attention import MultiHeadAttention
   help(MultiHeadAttention)
   ```

4. **Check examples**
   - Look in `examples/` directory
   - Run example scripts

## File Locations

After setup, you should see:
```
attention-transformers/
├── venv/                 # Virtual environment
├── app.py                # Streamlit app
├── README.md             # Documentation
├── requirements.txt      # Dependencies
├── notebooks/            # Jupyter tutorials
│   └── 01_attention_basics.ipynb
└── src/                  # Source code
    ├── attention.py
    ├── data.py
    └── visualization.py
```

## Environment Variables (Optional)

For larger datasets or GPU usage:
```bash
# Use GPU if available
export CUDA_VISIBLE_DEVICES=0

# Set data directory
export DATA_DIR=/path/to/large/disk

# Streamlit config
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_HEADLESS=false
```

## Performance Tips

1. **Faster startup**: Preload datasets
```bash
python -c "from src.data import get_mnist; get_mnist(samples=1000)"
```

2. **Use GPU** (if available):
```python
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

3. **Reduce batch size** for memory:
```python
loader = get_mnist(batch_size=8)  # Instead of 32
```

## Next: Choose Your Learning Path

### 🟢 Quick (15 minutes)
```bash
streamlit run app.py
# Read: Home page + Attention Mechanics
```

### 🟡 Standard (4 hours)
```bash
jupyter notebook
# Follow: Notebooks 01-04
```

### 🔴 Deep Dive (8 hours)
```bash
# Do everything:
# - All 7 notebooks
# - All Streamlit sections
# - Experiments + custom training
```

---

**Ready?** Run: `streamlit run app.py` 🚀

**Questions?** Check: README.md 📚

**Let's learn!** 🎓
