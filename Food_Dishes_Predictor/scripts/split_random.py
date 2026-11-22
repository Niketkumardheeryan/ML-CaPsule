import os, shutil, random

base = "dataset/raw"
train_base = "dataset/train"
val_base = "dataset/val"

os.makedirs(train_base, exist_ok=True)
os.makedirs(val_base, exist_ok=True)

for cls in os.listdir(base):
    imgs = os.listdir(os.path.join(base, cls))
    random.shuffle(imgs)

    split = int(0.8 * len(imgs))
    train_imgs = imgs[:split]
    val_imgs = imgs[split:]

    os.makedirs(os.path.join(train_base, cls), exist_ok=True)
    os.makedirs(os.path.join(val_base, cls), exist_ok=True)

    for img in train_imgs:
        shutil.copy(
            os.path.join(base, cls, img),
            os.path.join(train_base, cls, img)
        )

    for img in val_imgs:
        shutil.copy(
            os.path.join(base, cls, img),
            os.path.join(val_base, cls, img)
        )
