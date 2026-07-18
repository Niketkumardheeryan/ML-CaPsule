# 🖼️ Test Images — Explanation Guide

> This document explains the three ImageNet classes used as test images in the Grad-CAM notebook, what visual features the model has learned to detect, and what to expect from the heatmap output.

---

## 📌 What are ImageNet synsets?

ImageNet organises its 1,000 classes using **WordNet synset IDs** (e.g., `n02099712`). Each ID maps to a specific animal, object, or scene. When you download the ImageNet Mini dataset, images are stored in folders named by synset ID.

---

## 🐕 Class 1 — Labrador Retriever (`n02099712`)

| Property | Detail |
|---|---|
| **ImageNet Class Index** | 208 |
| **WordNet Synset** | `n02099712` |
| **Common name** | Labrador Retriever |
| **Dataset path** | `train/n02099712/*.JPEG` |

### About the class

The Labrador Retriever is one of the most common dog breeds in ImageNet. The model has seen thousands of images of Labs — including yellow, black, and chocolate variants — so it has learned rich visual features for this class.

### What Grad-CAM typically highlights

- ✅ **Face and muzzle** — the most discriminative region; ear shape and eye placement
- ✅ **Fur texture** — especially wavy or short coat patterns
- ✅ **Body posture** — sitting, lying, or standing poses
- ❌ Background elements (grass, furniture) are suppressed (low activation)

### Interpretation

If the heatmap concentrates on the **dog's face or upper body**, the model is reasoning correctly. If it lights up the background, the model may be relying on spurious correlations (common in early ImageNet models).

---

## 🐱 Class 2 — Siamese Cat (`n02123597`)

| Property | Detail |
|---|---|
| **ImageNet Class Index** | 284 |
| **WordNet Synset** | `n02123597` |
| **Common name** | Siamese cat |
| **Dataset path** | `train/n02123597/*.JPEG` |

### About the class

Siamese cats are recognisable by their **colour-point pattern** (darker face, ears, paws, tail) and striking **blue eyes**. They are a distinct ImageNet class from other domestic cats (`n02123045`).

### What Grad-CAM typically highlights

- ✅ **Eyes** — blue eyes are a unique discriminative feature
- ✅ **Face mask** — the dark coloured face/ears contrast strongly with the body
- ✅ **Whisker area** — fine-grained texture around the muzzle
- ❌ Body and limbs tend to have lower activations

### Interpretation

Strong activation around the **eye + face region** indicates the model correctly identifies Siamese-specific features rather than just "generic cat". This is a great example of Grad-CAM distinguishing fine-grained sub-categories.

---

## 🐘 Class 3 — African Elephant (`n02504458`)

| Property | Detail |
|---|---|
| **ImageNet Class Index** | 386 |
| **WordNet Synset** | `n02504458` |
| **Common name** | African elephant |
| **Dataset path** | `train/n02504458/*.JPEG` |

### About the class

The African elephant is the largest land animal and one of the most visually distinctive ImageNet classes. It is a separate class from the Indian elephant (`n02504013`). Key distinguishing features include **larger ears**, **two-fingered trunk tip**, and skin texture.

### What Grad-CAM typically highlights

- ✅ **Trunk** — the most structurally unique feature; long, curved, and highly textured
- ✅ **Tusks** — ivory tusks are a strong discriminative signal (African > Indian elephant)
- ✅ **Large, fan-shaped ears** — distinguishes African from Indian elephant
- ✅ **Rough, wrinkled skin** — especially around the knees and head
- ❌ Savannah/grass background is suppressed

### Interpretation

Broad activation across the **entire elephant silhouette** is normal due to the animal's size filling the frame. High activation on the trunk or tusks specifically indicates the model uses class-specific anatomy, not just overall shape.

---

## 🔬 How to Read the Grad-CAM Output

The notebook produces a **3-panel figure** for each image:

```
┌─────────────────┬─────────────────┬─────────────────┐
│  Original Image │  Grad-CAM       │  Overlay        │
│                 │  Heatmap        │                 │
│  (as fed to     │  (jet colormap) │  (heatmap 40% + │
│   the model)    │                 │   original 60%) │
└─────────────────┴─────────────────┴─────────────────┘
```

**Colour scale (jet):**

| Colour | Meaning |
|---|---|
| 🔴 **Red / Yellow** | High activation — model focuses here strongly |
| 🟢 **Green** | Moderate activation |
| 🔵 **Blue / Violet** | Low activation — model largely ignores this region |

---

## ✅ Things to Try

1. **Change the target class** — pass `target_class=<index>` to `run_gradcam()` to see what regions would "fire" for a wrong class.
2. **Use your own images** — provide any URL or local file path to `run_gradcam()`.
3. **Try a different layer** — change `model.features[28]` to `model.features[21]` to see earlier (coarser) features.
4. **Compare with Indian Elephant** (`n02504013`, class index 385) — spot which features differ.

---

## 📚 Further Reading

- [Original Grad-CAM paper (arXiv)](https://arxiv.org/abs/1610.02391)
- [ImageNet class index list](https://gist.github.com/yrevar/942d3a0ac09ec9e5eb3a)
- [WordNet synset browser](http://www.image-net.org/synset?wnid=n02099712)
