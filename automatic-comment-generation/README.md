# Automatic Comment Generation

This project generates short Python docstrings/comments for functions using a pretrained code language model. The notebook reads Python functions from a sample source file, sends each function to a Hugging Face model, and saves the generated documentation text to an output file.

## Project Structure

```text
Automatic Comment Generation/
+-- data/
|   +-- sample_code_snippets.py       # Input Python functions
+-- model/
|   +-- commentGeneration.ipynb       # Main notebook
+-- outputs/
|   +-- generated_docstrings.txt      # Generated comments/docstrings
+-- requirements.txt
+-- README.md
```

## How It Works

1. The notebook imports `ast` to parse `data/sample_code_snippets.py`.
2. It extracts every top-level Python function from the file.
3. Each function is formatted into a prompt.
4. The prompt is passed to `Qwen/Qwen2.5-Coder-1.5B-Instruct` using Hugging Face Transformers.
5. The generated text is cleaned and written to `outputs/generated_docstrings.txt`.

## Model Used

The notebook uses:

```text
Qwen/Qwen2.5-Coder-1.5B-Instruct
```

This is a causal language model suitable for code understanding and generation tasks.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Usage

Open the notebook:

```bash
jupyter notebook model/commentGeneration.ipynb
```

Run all cells in order. The notebook expects this input file:

```text
data/sample_code_snippets.py
```

The generated output is saved here:

```text
outputs/generated_docstrings.txt
```

## Input Example

```python
def add_numbers(a, b):
    return a + b
```

## Output Example

```text
FUNCTION:
def add_numbers(a, b):
    return a + b

GENERATED DOCSTRING:
The function `add_numbers` takes two parameters `a` and `b`, and returns their sum.
```
