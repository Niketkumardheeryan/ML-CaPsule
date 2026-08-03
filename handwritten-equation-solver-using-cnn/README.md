# Handwritten Equation Solver using CNN

This folder contains notebooks and a trained model for extracting and solving handwritten mathematical equations using a Convolutional Neural Network (CNN).

Contents
- `Equation solver CNN.ipynb` — end-to-end notebook for detection, segmentation, recognition, and solving equations.
- `Model/` — trained model files (`model_final.h5`, `model_final.json`) and training artifacts.

Quick setup

```bash
pip install tensorflow keras numpy opencv-python matplotlib
```

How to run
- Open `Equation solver CNN.ipynb` in Jupyter and run cells. If you want to load the trained model, use the `Model/model_final.h5` file.

Notes
- The notebook includes data extraction and training notebooks under `Model/` if you want to retrain or fine-tune the network.
