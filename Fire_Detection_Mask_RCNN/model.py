"""
Mask R-CNN for Fire Detection & Image Segmentation
Modular implementation using TensorFlow/Keras
"""

import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers, models

def create_synthetic_fire_image(img_size=(128, 128)):
    """
    Generates a synthetic image with a simulated fire region and its binary mask & bounding box.
    """
    img = np.zeros((*img_size, 3), dtype=np.uint8)
    
    # Background noise / ambient lighting
    bg_color = np.random.randint(20, 60, size=(3,), dtype=np.uint8)
    img[:] = bg_color
    
    # Random fire center and radius
    cx = np.random.randint(30, img_size[1] - 30)
    cy = np.random.randint(30, img_size[0] - 30)
    rx = np.random.randint(15, 30)
    ry = np.random.randint(15, 30)
    
    mask = np.zeros((img_size[0], img_size[1]), dtype=np.uint8)
    cv2.ellipse(mask, (cx, cy), (rx, ry), angle=np.random.randint(0, 180), startAngle=0, endAngle=360, color=1, thickness=-1)
    
    # Add fire color (bright yellow-red gradients) where mask == 1
    fire_pixels = mask == 1
    num_pixels = np.sum(fire_pixels)
    
    red_channel = np.random.randint(220, 256, size=num_pixels)
    green_channel = np.random.randint(100, 220, size=num_pixels)
    blue_channel = np.random.randint(0, 50, size=num_pixels)
    
    img[fire_pixels, 0] = red_channel
    img[fire_pixels, 1] = green_channel
    img[fire_pixels, 2] = blue_channel
    
    # Bounding box [ymin, xmin, ymax, xmax] normalized
    y_indices, x_indices = np.where(mask == 1)
    ymin, ymax = np.min(y_indices) / img_size[0], np.max(y_indices) / img_size[0]
    xmin, xmax = np.min(x_indices) / img_size[1], np.max(x_indices) / img_size[1]
    bbox = np.array([ymin, xmin, ymax, xmax], dtype=np.float32)
    
    return img, mask, bbox

def generate_dataset(num_samples=100, img_size=(128, 128)):
    """
    Generate dataset of synthetic fire images, masks, and bounding boxes.
    """
    images = []
    masks = []
    bboxes = []
    
    for _ in range(num_samples):
        img, mask, bbox = create_synthetic_fire_image(img_size)
        images.append(img / 255.0)
        masks.append(np.expand_dims(mask, axis=-1))
        bboxes.append(bbox)
        
    return np.array(images, dtype=np.float32), np.array(masks, dtype=np.float32), np.array(bboxes, dtype=np.float32)

class SimpleMaskRCNN(tf.keras.Model):
    """
    Simplified Multi-Task Mask R-CNN Architecture for Fire Image Segmentation & Localization.
    Combines Feature Extraction (CNN Backbone), Bounding Box Regression Head, and Mask Segmentation Head.
    """
    def __init__(self, input_shape=(128, 128, 3)):
        super(SimpleMaskRCNN, self).__init__()
        
        # Shared CNN Backbone (Feature Extractor)
        self.backbone = models.Sequential([
            layers.Input(shape=input_shape),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2))
        ], name="backbone")
        
        # Bounding Box Detection & Classification Head
        self.bbox_head = models.Sequential([
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(4, activation='sigmoid') # [ymin, xmin, ymax, xmax]
        ], name="bbox_head")
        
        # Mask Segmentation Head (FCN / Deconv decoder)
        self.mask_head = models.Sequential([
            layers.Conv2DTranspose(64, (3, 3), strides=2, padding='same', activation='relu'), # 16 -> 32
            layers.Conv2DTranspose(32, (3, 3), strides=2, padding='same', activation='relu'), # 32 -> 64
            layers.Conv2DTranspose(16, (3, 3), strides=2, padding='same', activation='relu'), # 64 -> 128
            layers.Conv2D(1, (1, 1), activation='sigmoid', padding='same') # Single channel mask output
        ], name="mask_head")

    def call(self, inputs):
        features = self.backbone(inputs)
        pred_bbox = self.bbox_head(features)
        pred_mask = self.mask_head(features)
        return {"bbox": pred_bbox, "mask": pred_mask}

def calculate_iou(mask_true, mask_pred, threshold=0.5):
    """
    Computes Intersection over Union (IoU) metric for binary masks.
    """
    pred_binary = (mask_pred > threshold).astype(np.uint8)
    true_binary = (mask_true > 0.5).astype(np.uint8)
    
    intersection = np.logical_and(true_binary, pred_binary).sum()
    union = np.logical_or(true_binary, pred_binary).sum()
    
    if union == 0:
        return 1.0
    return intersection / union

def detect_fire_rgb_heuristic(img_rgb):
    """
    RGB Chromatic Fire Detection Rule:
    Fire pixels typically satisfy: R > G > B and R > R_threshold.
    """
    R = img_rgb[:, :, 0].astype(np.float32)
    G = img_rgb[:, :, 1].astype(np.float32)
    B = img_rgb[:, :, 2].astype(np.float32)
    
    # Heuristic fire mask
    fire_rule = (R > G) & (G > B) & (R > 150)
    return fire_rule.astype(np.uint8)
