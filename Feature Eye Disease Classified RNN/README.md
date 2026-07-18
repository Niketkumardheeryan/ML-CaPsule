Feature: Eye Disease Classified RNN

This feature implements a CNN+RNN (spatial RNN over CNN feature maps) pipeline to classify retinal images into eye disease categories such as diabetic retinopathy, glaucoma, and macular degeneration.

Quick start

- Install dependencies: `pip install -r requirements.txt`
- Prepare dataset: organize images in `data/train/<class_name>` and `data/val/<class_name>`
- Train: `python train.py --data_dir data --epochs 10 --batch_size 16`

Overview

- `data_preprocessing.py`: image loading and preprocessing utilities
- `model.py`: CNN + RNN model builder (TensorFlow Keras)
- `train.py`: training and evaluation script using `tf.data`
- `utils.py`: metric helpers
- `tests/test_model_import.py`: simple unit test to check model construction

Notes

- This implementation expects a folder-structured dataset. For EyePACS, convert CSV labels into folders or adapt `train.py` accordingly.

How to contribute

If you want to add improvements to this feature, please follow the repository CONTRIBUTING guidelines and create a focused feature branch. A minimal contribution flow:

- Fork the repo and clone your fork.
- Add upstream: `git remote add upstream https://github.com/Niketkumardheeryan/ML-CaPsule.git` and keep `main` up to date.
- Create a branch: `git checkout -b feature/eye-disease-rnn-yourname`.
- Commit changes with a concise message and push: `git push origin feature/eye-disease-rnn-yourname`.
- Open a PR to the main repo with a clear title and description.

See the top-level `CONTRIBUTING.md` for full details.

Local verification steps

1. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```

2. Generate a small synthetic dataset for smoke testing:

```bash
python make_synthetic_data.py
```

3. Run the unit test:

```bash
python -m pytest "Feature Eye Disease Classified RNN/tests/test_model_import.py" -q
```

4. Run a short smoke training (1-2 epochs):

```bash
python train.py --data_dir data --epochs 1 --batch_size 8
```

