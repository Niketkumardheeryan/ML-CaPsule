# Visual Question Answering (VQA) using CNN (ResNet50) + LSTM

## In this notebook, a model is trained to answer natural language questions about an image by fusing image features (via transfer learning) and question features (via an LSTM).

## Pipeline
1. **Image Feature Extraction** - pretrained ResNet50 (transfer learning, frozen weights) extracts a 2048-d feature vector from each image
2. **Question Encoding** - questions are tokenized and passed through an Embedding layer + LSTM
3. **Multimodal Fusion** - image features and question features are concatenated and passed through Dense layers to predict the answer
4. **Dataset** - a small, self-contained synthetic dataset of colored-shape images with generated questions (kept lightweight so the notebook runs quickly and stays beginner-friendly; the same pipeline works with real datasets like VQA v2 by swapping the data-loading cell)
5. **Evaluation** - accuracy, top-3 accuracy, and sample predictions shown alongside their images
6. **Demo** - an interactive cell to test the model on any image + typed question

## About the Model
- Frozen pretrained **ResNet50** as the image feature extractor
- **Embedding + LSTM** for question encoding
- **Concatenate + Dense (softmax)** for multimodal fusion and answer prediction
- Trained for 15 epochs on ~1,000 generated (image, question, answer) samples
- Test accuracy ~ 92% (on the synthetic dataset; exact numbers vary slightly per run)

## Why a synthetic dataset?
Real VQA datasets (e.g. VQA v2) are tens of GBs and require heavy compute to train on, which isn't practical for a beginner-facing notebook or CI execution. This notebook generates a small, fast, self-contained dataset of colored shapes with template questions ("What color is the shape?", "Is the shape a circle?", etc.), so the full pipeline - feature extraction, encoding, fusion, training, and evaluation — runs end-to-end in well under a minute, while still demonstrating the complete VQA architecture end to end.

## Tech Stack
Python, TensorFlow/Keras, ResNet50, LSTM, Matplotlib, NumPy, scikit-learn, Pillow

### Contributed by Komal (Komal-11k)
