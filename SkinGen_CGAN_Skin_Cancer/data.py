import numpy as np
import torch
from pathlib import Path

DATASET = "marmal88/skin_cancer"
IMAGE_SIZE = 64
CACHE = Path(__file__).resolve().parent / "cache" / f"ham10000_{IMAGE_SIZE}.pt"

CLASSES = [
    "actinic_keratoses",
    "basal_cell_carcinoma",
    "benign_keratosis-like_lesions",
    "dermatofibroma",
    "melanoma",
    "melanocytic_Nevi",
    "vascular_lesions",
]

SHORT_NAMES = {
    "actinic_keratoses": "akiec",
    "basal_cell_carcinoma": "bcc",
    "benign_keratosis-like_lesions": "bkl",
    "dermatofibroma": "df",
    "melanoma": "mel",
    "melanocytic_Nevi": "nv",
    "vascular_lesions": "vasc",
}

RARE_CLASSES = ["df", "vasc", "akiec"]


def build_cache(max_per_class=700, cache_path=CACHE, image_size=IMAGE_SIZE):
    from datasets import load_dataset

    cache_path.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
    index = {name: i for i, name in enumerate(CLASSES)}
    kept = {name: 0 for name in CLASSES}
    images, labels = [], []

    stream = load_dataset(DATASET, split="train", streaming=True)
    for row in stream:
        name = row["dx"]
        if name not in index or kept[name] >= max_per_class:
            continue
        picture = row["image"].convert("RGB").resize((image_size, image_size))
        images.append(np.asarray(picture, dtype=np.uint8))
        labels.append(index[name])
        kept[name] += 1

    tensor = torch.from_numpy(np.stack(images)).permute(0, 3, 1, 2).contiguous()
    payload = {"images": tensor, "labels": torch.tensor(labels), "classes": CLASSES}
    torch.save(payload, cache_path)
    return payload


def load_data(cache_path=CACHE, max_per_class=700):
    if Path(cache_path).exists():
        return torch.load(cache_path, weights_only=False)
    return build_cache(max_per_class=max_per_class, cache_path=Path(cache_path))


def to_float(images, image_size=None):
    scaled = images.float().div(127.5).sub(1.0)
    if image_size and image_size != scaled.shape[-1]:
        scaled = torch.nn.functional.interpolate(
            scaled, size=image_size, mode="area"
        )
    return scaled


def stratified_split(labels, test_fraction=0.2, seed=42):
    generator = np.random.default_rng(seed)
    train_index, test_index = [], []
    labels = labels.numpy()

    for label in np.unique(labels):
        positions = np.flatnonzero(labels == label)
        generator.shuffle(positions)
        cut = max(1, int(round(len(positions) * test_fraction)))
        test_index.extend(positions[:cut])
        train_index.extend(positions[cut:])

    train_index = np.array(train_index)
    test_index = np.array(test_index)
    generator.shuffle(train_index)
    generator.shuffle(test_index)
    return torch.tensor(train_index), torch.tensor(test_index)


def class_counts(labels):
    counts = torch.bincount(labels, minlength=len(CLASSES))
    return {SHORT_NAMES[CLASSES[i]]: int(counts[i]) for i in range(len(CLASSES))}
