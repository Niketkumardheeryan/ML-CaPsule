import argparse
import os
import random
from datetime import datetime
import cv2
import numpy as np

STATES = [
    "KA", "TN", "MH", "DL", "GJ", "UP", "RJ", "PB", "HR", "KL", "AP", "TS", "WB", "MP", "CG"
]


def random_plate():
    state = random.choice(STATES)
    dist = f"{random.randint(1, 99):02d}"
    series = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.choice([1, 2])))
    number = f"{random.randint(1, 9999):04d}"
    return f"{state}{dist}{series}{number}"


def render_plate(text: str, w=320, h=80):
    img = np.full((h, w, 3), 240, dtype=np.uint8)
    cv2.rectangle(img, (0, 0), (w - 1, h - 1), (0, 0, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1.4
    thickness = 2
    size = cv2.getTextSize(text, font, scale, thickness)[0]
    org = ((w - size[0]) // 2, (h + size[1]) // 2 - 5)
    cv2.putText(img, text, org, font, scale, (0, 0, 0), thickness, cv2.LINE_AA)
    # random perspective
    pts1 = np.float32([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]])
    jitter = 0.08
    def j(x, y):
        return [x + random.uniform(-jitter, jitter) * w, y + random.uniform(-jitter, jitter) * h]
    pts2 = np.float32([j(0, 0), j(w - 1, 0), j(0, h - 1), j(w - 1, h - 1)])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(img, M, (w, h))
    # blur/noise
    if random.random() < 0.5:
        warped = cv2.GaussianBlur(warped, (3, 3), 0)
    noise = np.random.normal(0, 8, warped.shape).astype(np.int16)
    warped = np.clip(warped.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return warped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="datasets/samples")
    ap.add_argument("--num", type=int, default=10)
    ap.add_argument("--video", type=str, default="")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    frames = []
    for i in range(args.num):
        text = random_plate()
        img = render_plate(text)
        path = os.path.join(args.out, f"plate_{i:03d}_{text}.png")
        cv2.imwrite(path, img)
        frames.append(img)
    if args.video:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        h, w = frames[0].shape[:2]
        vw = cv2.VideoWriter(args.video, fourcc, 20.0, (w, h))
        for fr in frames:
            # simulate jitter
            M = np.float32([[1, 0, random.randint(-5, 5)], [0, 1, random.randint(-2, 2)]])
            vw.write(cv2.warpAffine(fr, M, (w, h)))
        vw.release()


if __name__ == "__main__":
    main()


