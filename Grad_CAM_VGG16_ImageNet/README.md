# 🔥 Grad-CAM with VGG16 on ImageNet

> **Grad-CAM** (Gradient-weighted Class Activation Mapping) produces visual explanations for decisions made by CNN-based models. This project replicates the original paper by Selvaraju et al. (ICCV 2017) using a pretrained **VGG16** on the ImageNet dataset.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1JuvQPM2u5Sczw-6zPmPGC1xDcZA5NC56)

---

## 📖 What is Grad-CAM?

Grad-CAM highlights **which regions of an image** a CNN focused on when making a prediction. It works by:

1. Running a forward pass to get the prediction.
2. Computing gradients of the target class score with respect to the **last convolutional layer**.
3. Averaging those gradients (Global Average Pooling) to get importance weights **α**.
4. Multiplying the weights by the feature maps and applying **ReLU**.
5. Upsampling the resulting heatmap to the original image size.

```
L_Grad-CAM = ReLU( Σ_k α_k · A^k )
```

The heatmap is then overlaid on the original image — **hot colours = important regions**.

---

## 📁 Project Structure

```
Grad_CAM_VGG16_ImageNet/
├── GRAD_CAM.ipynb       # 📓 Main notebook (run this in Colab)
├── grad_cam.py          # 🐍 Python script version of the notebook
├── requirements.txt     # 📦 Python dependencies
├── .env.example         # 🔐 Secret variables template (copy → .env)
└── README.md            # 📄 This file
```

---

## 🚀 How to Run

### Option A — Google Colab (Recommended for beginners)

1. Click the **"Open in Colab"** badge at the top of this README.
2. Go to **Runtime → Change runtime type** and select **GPU** (T4 recommended).
3. Set up your Kaggle credentials (see [🔐 Secrets Setup](#-secrets-setup) below).
4. Click **Runtime → Run all** (or press `Ctrl+F9`).

That's it — the notebook downloads the dataset, runs Grad-CAM on sample images, and displays the heatmap visualizations automatically.

---

### Option B — Run the Python script locally

**Prerequisites:** Python ≥ 3.8, pip

```bash
# 1. Clone the repo
git clone https://github.com/Aditri-web/ML-CaPsule.git
cd ML-CaPsule/Grad_CAM_VGG16_ImageNet

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install python-dotenv        # for loading .env secrets

# 4. Set up your secrets (see Secrets Setup below)
cp .env.example .env
# → open .env and fill in your KAGGLE_USERNAME and KAGGLE_KEY

# 5. Run the script
python grad_cam.py
```

---

## 🔐 Secrets Setup

This project needs a **Kaggle API key** to download the ImageNet Mini dataset.

### Get your Kaggle API key

1. Log in to [kaggle.com](https://www.kaggle.com).
2. Go to **Account Settings** → scroll to **API** → click **Create New Token**.
3. This downloads a `kaggle.json` file containing your `username` and `key`.

### In Google Colab

1. Click the **🔑 key icon** in the left sidebar ("Secrets").
2. Add two secrets:
   - Name: `KAGGLE_USERNAME` → Value: your Kaggle username
   - Name: `KAGGLE_KEY` → Value: the key string from `kaggle.json`
3. Toggle **"Notebook access"** ON for both.

> ⚠️ **Never paste your API key directly into the notebook cell or commit it to GitHub.**

### Locally

```bash
cp .env.example .env
```

Open `.env` and fill in:

```
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key_here
```

The `.env` file is listed in `.gitignore` and will **never** be committed.

---

## 📊 Test Images

The notebook uses the **ImageNet Mini** dataset (`ifigotin/imagenetmini-1000` on Kaggle). After downloading, it picks sample validation images automatically.

Three representative classes used for demonstration:

| Class | ImageNet ID | What Grad-CAM shows |
|---|---|---|
| 🐕 Labrador Retriever | `n02099712` | Face and fur texture highlighted |
| 🐱 Siamese Cat | `n02123597` | Eyes and face region highlighted |
| 🐘 African Elephant | `n02504458` | Trunk and tusks highlighted |

See [`test_images_explanation.md`](./test_images_explanation.md) for a detailed description of each test image class, what features the model focuses on, and what the Grad-CAM heatmap reveals.

---

## 🛠 Technologies Used

| Library | Purpose |
|---|---|
| `torch` / `torchvision` | VGG16 model + transforms |
| `opencv-python-headless` | Heatmap generation & image manipulation |
| `matplotlib` | 3-panel visualization |
| `Pillow` | Image loading |
| `requests` | Fetching ImageNet labels |
| `kaggle` | Dataset download via CLI |
| `python-dotenv` | Loading secrets from `.env` (local only) |

---

## 📦 Dependencies

Install everything with:

```bash
pip install -r requirements.txt
```

`requirements.txt` contents:

```
torch
torchvision
opencv-python-headless
matplotlib
Pillow
requests
kaggle
python-dotenv
pytorch-grad-cam
```

---

## 🗺 How the Code Works — Step by Step

### Step 1 · Install & Import

```python
!pip install torch torchvision pytorch-grad-cam opencv-python-headless
import torch, torchvision.models as models, cv2, numpy as np
```

Installs all required libraries and imports them.

### Step 2 · Load VGG16

```python
model = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
model.eval()
```

Downloads the pretrained VGG16 weights. `.eval()` disables dropout and batch norm training behaviour.

### Step 3 · Define the Grad-CAM class

The `GradCAM` class attaches **hooks** to `model.features[28]` — VGG16's last convolutional layer. Hooks capture:
- **Forward activations** (feature map values)
- **Backward gradients** (how each neuron influenced the prediction)

### Step 4 · Preprocess images

```python
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```

Standard ImageNet preprocessing — same values used during VGG16 training.

### Step 5 · Generate the heatmap

```python
cam, target_class = gradcam.generate_cam(input_tensor)
```

Runs forward + backward passes, pools the gradients, and returns a normalised 224×224 heatmap.

### Step 6 · Visualise

```python
visualize_gradcam(original_img, cam, target_class, confidence)
```

Produces a 3-panel plot: **Original | Heatmap | Overlay**.

---

## 📚 Reference

> Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., & Batra, D. (2017).  
> **Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization.**  
> *ICCV 2017.* [Paper link](https://arxiv.org/abs/1610.02391)

---

## 🤝 Contributing

Pull requests and issues are welcome! Please read [`CONTRIBUTING.md`](../CONTRIBUTING.md) before submitting.
