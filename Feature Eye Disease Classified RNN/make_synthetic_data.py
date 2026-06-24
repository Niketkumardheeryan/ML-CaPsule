from PIL import Image
import os
import numpy as np


def make_image(path, size=(224,224)):
    arr = (np.random.rand(size[0], size[1], 3) * 255).astype('uint8')
    img = Image.fromarray(arr)
    img.save(path)


def make_dataset(root='data', classes=('diseaseA','diseaseB'), n_per_class=8):
    for split in ('train','val'):
        for c in classes:
            d = os.path.join(root, split, c)
            os.makedirs(d, exist_ok=True)
            for i in range(n_per_class if split=='train' else max(2, n_per_class//4)):
                make_image(os.path.join(d, f'{c}_{i}.png'))


if __name__ == '__main__':
    make_dataset()
    print('Synthetic dataset created under ./data (train/ and val/)')
