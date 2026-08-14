# Troubleshooting & FAQ

Centralized answers to common problems when setting up, running, or contributing to
ML-CaPsule projects.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Environment & Setup](#environment--setup)
- [Runtime Errors](#runtime-errors)
- [Git & Contribution Issues](#git--contribution-issues)
- [FAQ](#faq)
- [Getting Further Help](#getting-further-help)

---

## Installation Issues

### `pip install` fails or a package isn't found
- Confirm Python 3.8+ is installed: `python --version`
- Upgrade pip first: `python -m pip install --upgrade pip`
- Install the common data science stack most projects rely on:
```bash
  pip install numpy pandas matplotlib seaborn scikit-learn jupyter
```
- If the specific project folder has its own `requirements.txt`, install from that
  instead:
```bash
  pip install -r requirements.txt
```

### A project needs a package not covered above
Check that project's own `README.md` inside its folder — many list additional
project-specific dependencies (e.g. `tensorflow`, `opencv-python`, `torch`).

### Jupyter kernel doesn't show the right environment
If you're using a virtual environment, register it as a Jupyter kernel:
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install ipykernel
python -m ipykernel install --user --name=ml-capsule
```
Then select that kernel from the Jupyter interface.

---

## Environment & Setup

### Cloning the full repo is slow or very large
The repo contains 500+ project folders. To work on just one project without cloning
everything:
```bash
git clone --filter=blob:none --sparse https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd ML-CaPsule
git sparse-checkout set "Project Folder Name"
```

### Dataset download links are broken or slow
- Most datasets link to Kaggle or UCI — these occasionally rate-limit or change URLs.
- Check the specific project's README for alternate download instructions.
- If a link is genuinely dead, please open an issue so it can be updated.

### Notebook won't run / kernel keeps dying
- Large datasets or deep learning models can exceed available RAM — try reducing
  batch size or sample size while testing.
- Restart the kernel and run cells from top to bottom; skipped cells are a common
  cause of `NameError` issues.

---

## Runtime Errors

### `ModuleNotFoundError` when running a notebook or script
Almost always means a required package isn't installed in your active environment.
Confirm your virtual environment is activated, then install the missing package.

### `FileNotFoundError` for a dataset
Datasets are usually not committed to the repo (too large). Check that project's
README for where to download the dataset and which folder to place it in.

### Notebook cell outputs don't match the README's example results
Results can vary slightly due to randomness (train/test splits, weight
initialization). If results are wildly different, check you're using the dataset
version and parameters specified in the project's README.

---

## Git & Contribution Issues

### My fork is out of sync with the main repo
```bash
git remote add upstream https://github.com/Niketkumardheeryan/ML-CaPsule.git
git fetch upstream
git checkout master
git merge upstream/master
```

### My PR shows unrelated file changes
This usually means your branch wasn't created from an up-to-date `master`. Sync first
(see above), then rebase your feature branch:
```bash
git checkout my-feature
git rebase master
```

### `build_readme.py` / project index issues
This script auto-generates parts of the root README's project listing. Avoid manually
editing the generated sections — raise an issue if the index looks incorrect.

---

## FAQ

**Q: How do I choose which project to start with?**
A: See [ROADMAP.md](ROADMAP.md), which sorts projects into Beginner, Intermediate, and
Advanced tiers.

**Q: What if a project has missing Python packages?**
A: Install the common stack (`numpy pandas matplotlib seaborn scikit-learn jupyter`),
or run `pip install -r requirements.txt` if the project folder has one.

**Q: Should I submit Jupyter Notebooks (`.ipynb`) or Python scripts (`.py`)?**
A: Notebooks are preferred since they combine code, outputs, and explanations. Run all
cells before committing so outputs are visible.

**Q: How do I add a new project?**
A: Follow [.github/readme_template.md](.github/readme_template.md) for your project's
own README, and see [CONTRIBUTING.md](CONTRIBUTING.md) for the full PR workflow.

**Q: Where do I ask questions that aren't covered here?**
A: Open a [GitHub Issue](https://github.com/Niketkumardheeryan/ML-CaPsule/issues) —
tag it with the project name if it's project-specific.

---

## Getting Further Help

- Search [existing Issues](https://github.com/Niketkumardheeryan/ML-CaPsule/issues) —
  your question may already be answered.
- When opening a new issue, include: the project folder name, your Python version,
  OS, the exact error message, and steps to reproduce.
- Read [CONTRIBUTING.md](CONTRIBUTING.md) and the
  [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a PR.