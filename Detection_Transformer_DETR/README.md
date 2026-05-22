# Detection Transformer (DETR)

An end-to-end object detection pipeline implemented using Facebook AI's **DETR (DEtection TRansformer)** — a transformer-based approach to object detection that eliminates the need for hand-crafted components like anchor boxes and non-maximum suppression (NMS).

---

## 📌 Overview

DETR reformulates object detection as a direct set prediction problem. It uses a standard **CNN backbone** (ResNet) to extract image features, followed by a **Transformer encoder-decoder** that attends over these features to predict a fixed set of bounding boxes and class labels in a single forward pass.

This repository demonstrates:
- Loading a pretrained DETR model from `torch.hub`
- Running inference on custom images
- Visualizing predicted bounding boxes and class labels
- Understanding attention maps from the Transformer decoder
- **Interactive Gradio UI for real-time object detection**

---

## 🧠 How DETR Works
Image → CNN Backbone (ResNet-50) → Positional Encoding
→ Transformer Encoder → Transformer Decoder (with learned queries)
→ Feed-Forward Network → (Class Labels + Bounding Boxes)


Unlike traditional detectors (Faster R-CNN, YOLO), DETR:
- Uses **bipartite matching** (Hungarian algorithm) between predictions and ground-truth during training
- Requires **no anchor boxes** or **NMS post-processing**
- Treats detection as a **set prediction** problem

---

## 📁 Repository Structure
Detection_Transformer_DETR/
├── DETR.ipynb         # Notebook: inference, visualization, attention maps
├── app.py             # Gradio UI for interactive object detection
└── README.md          # Project documentation


---

## 🚀 Getting Started

### Prerequisites

```bash
pip install torch torchvision
pip install matplotlib pillow requests
pip install gradio
```

### Run the Notebook

```bash
git clone https://github.com/Raghav0079/Detection-Transformer.git
cd Detection-Transformer
jupyter notebook DETR.ipynb
```

### Run the Gradio UI

```bash
python app.py
```

Then open your browser at `http://localhost:7860` and upload any image to detect objects interactively.

---

## 🎨 Gradio UI Features

- 📤 Upload any image for instant object detection
- 🎚️ Adjustable **confidence threshold** slider (0.3 → 0.99)
- 🟩 Colored bounding boxes per detected class
- 🏷️ Class label + confidence score on each box
- 📋 Detection summary listing all detected objects

---

## 🔧 Usage

### Notebook Inference

The notebook uses a pretrained DETR model loaded directly from `torch.hub`:

```python
import torch
model = torch.hub.load('facebookresearch/detr', 'detr_resnet50', pretrained=True)
model.eval()
```

Pass any image through the model to get bounding box predictions:

```python
outputs = model(img_tensor)
# outputs contains:
#   pred_logits: class probabilities for each query
#   pred_boxes:  normalized (cx, cy, w, h) bounding boxes
```

### Gradio UI

```bash
python app.py
# Upload an image → adjust threshold → click "Detect Objects 🚀"
```

---

## 📊 Model Details

| Property         | Value                      |
|------------------|---------------------------|
| Backbone         | ResNet-50                 |
| Encoder Layers   | 6                         |
| Decoder Layers   | 6                         |
| Object Queries   | 100                       |
| Dataset          | COCO 2017 (pretrained)    |
| Classes          | 91 (COCO categories)      |
| Input Resolution | Variable (min side ~800px)|

---

## 🎓 What You'll Learn

- How transformers replace anchor boxes and NMS in object detection
- Bipartite matching with the Hungarian algorithm
- Attention map visualization from the transformer decoder
- Loading and running pretrained models via `torch.hub`
- Building an interactive ML UI with Gradio

---

## 📷 Example Output

After running inference, detected objects are visualized with:
- Colored bounding boxes per class
- Class label and confidence score on each box
- Adjustable confidence threshold to filter detections
- Detection summary with all identified objects

---

## 📚 References

- [End-to-End Object Detection with Transformers (Carion et al., 2020)](https://arxiv.org/abs/2005.12872)
- [Facebook Research DETR GitHub](https://github.com/facebookresearch/detr)
- [COCO Dataset](https://cocodataset.org/)
- [Gradio Documentation](https://www.gradio.app/docs)

---

## 🙋 Author

**Raghav** — [@Raghav0079](https://github.com/Raghav0079)

---

## 📄 License

This project is for educational purposes. The pretrained DETR model is released under the [Apache 2.0 License](https://github.com/facebookresearch/detr/blob/main/LICENSE) by Facebook AI Research.

