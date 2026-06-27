"""
Hailo-8 accelerated YOLOv8 detector for Raspberry Pi 5
Optimized for license plate detection at 30+ FPS
"""

import os
import numpy as np
import cv2
from typing import List, Tuple

try:
    from hailo_platform import (
        HEF,
        ConfigureParams,
        VDevice,
        HailoStreamInterface,
        InferVStreams,
        InputVStreamParams,
        OutputVStreamParams,
    )
    HAILO_AVAILABLE = True
except ImportError:
    HAILO_AVAILABLE = False


class HailoYOLODetector:
    """
    Hailo-8 accelerated YOLOv8 detector for license plates.
    Runs at 30-40 FPS on Raspberry Pi 5.
    """
    
    def __init__(
        self,
        hef_path: str,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.5,
        input_size: int = 640,
    ):
        """
        Initialize Hailo YOLOv8 detector.
        
        Args:
            hef_path: Path to compiled HEF model
            conf_threshold: Confidence threshold for detections
            iou_threshold: IoU threshold for NMS
            input_size: Model input size (640 or 512)
        """
        if not HAILO_AVAILABLE:
            raise RuntimeError("HailoRT not available. Install hailo-platform package.")
        
        if not os.path.exists(hef_path):
            raise FileNotFoundError(f"HEF model not found: {hef_path}")
        
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.input_size = input_size
        
        # Load HEF model
        print(f"🚀 Loading Hailo YOLOv8 detector: {hef_path}")
        self.hef = HEF(hef_path)
        
        # Create VDevice
        self.target = VDevice()
        
        # Configure network group
        self.network_group = self._configure_network_group()
        self.network_group_params = self.network_group.create_params()
        
        # Get input/output specs
        self.input_vstreams_params = InputVStreamParams.make_from_network_group(
            self.network_group, quantized=False, format_type=HailoStreamInterface.FLOAT32
        )
        self.output_vstreams_params = OutputVStreamParams.make_from_network_group(
            self.network_group, quantized=False, format_type=HailoStreamInterface.FLOAT32
        )
        
        print(f"✅ Hailo YOLOv8 initialized - Input: {input_size}x{input_size}")
    
    def _configure_network_group(self):
        """Configure Hailo network group."""
        configure_params = ConfigureParams.create_from_hef(
            self.hef, interface=HailoStreamInterface.PCIe
        )
        network_groups = self.target.configure(self.hef, configure_params)
        if not network_groups:
            raise RuntimeError("Failed to configure Hailo network group")
        return network_groups[0]
    
    def _preprocess(self, image_bgr: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Preprocess image for YOLOv8 inference.
        
        Args:
            image_bgr: Input image in BGR format
        
        Returns:
            (preprocessed_image, scale) tuple
        """
        # Convert BGR to RGB
        img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        
        # Letterbox resize (maintain aspect ratio)
        h, w = img.shape[:2]
        scale = self.input_size / max(h, w)
        nh, nw = int(h * scale), int(w * scale)
        resized = cv2.resize(img, (nw, nh))
        
        # Create padded image (letterbox)
        padded = np.full((self.input_size, self.input_size, 3), 114, dtype=np.uint8)
        padded[:nh, :nw] = resized
        
        # Normalize to [0, 1]
        normalized = padded.astype(np.float32) / 255.0
        
        # Transpose to CHW format: (H, W, C) -> (C, H, W)
        normalized = normalized.transpose(2, 0, 1)
        
        return normalized, scale
    
    def _nms(self, boxes: np.ndarray, scores: np.ndarray) -> List[int]:
        """
        Non-Maximum Suppression (NMS) to remove overlapping boxes.
        
        Args:
            boxes: Bounding boxes (N, 4) in [x1, y1, x2, y2] format
            scores: Confidence scores (N,)
        
        Returns:
            List of indices to keep
        """
        if len(boxes) == 0:
            return []
        
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        
        areas = (x2 - x1) * (y2 - y1)
        order = scores.argsort()[::-1]
        
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            
            # Calculate IoU with remaining boxes
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            
            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)
            inter = w * h
            
            iou = inter / (areas[i] + areas[order[1:]] - inter)
            
            # Keep boxes with IoU below threshold
            inds = np.where(iou <= self.iou_threshold)[0]
            order = order[inds + 1]
        
        return keep
    
    def _postprocess_yolo(
        self,
        predictions: np.ndarray,
        orig_shape: Tuple[int, int],
        scale: float
    ) -> Tuple[List[List[float]], List[float]]:
        """
        Post-process YOLOv8 output to get bounding boxes.
        
        Args:
            predictions: Model output (1, 84, 8400) or similar
            orig_shape: Original image shape (H, W)
            scale: Scale factor used in preprocessing
        
        Returns:
            (boxes, scores) - boxes in [x1, y1, x2, y2] format
        """
        # YOLOv8 output format: (batch, 4+num_classes, num_predictions)
        # predictions[0]: (4+num_classes, num_predictions)
        pred = predictions[0]  # Remove batch dimension
        
        # Transpose to (num_predictions, 4+num_classes)
        if pred.shape[0] < pred.shape[1]:
            pred = pred.T
        
        # Extract boxes and scores
        # Format: [cx, cy, w, h, class_scores...]
        boxes_cxcywh = pred[:, :4]  # Center x, y, width, height
        class_scores = pred[:, 4:]  # Class scores
        
        # Get max class score and class index
        max_scores = np.max(class_scores, axis=1)
        
        # Filter by confidence threshold
        mask = max_scores >= self.conf_threshold
        boxes_cxcywh = boxes_cxcywh[mask]
        scores = max_scores[mask]
        
        if len(boxes_cxcywh) == 0:
            return [], []
        
        # Convert from cxcywh to xyxy format
        boxes = np.zeros_like(boxes_cxcywh)
        boxes[:, 0] = boxes_cxcywh[:, 0] - boxes_cxcywh[:, 2] / 2  # x1
        boxes[:, 1] = boxes_cxcywh[:, 1] - boxes_cxcywh[:, 3] / 2  # y1
        boxes[:, 2] = boxes_cxcywh[:, 0] + boxes_cxcywh[:, 2] / 2  # x2
        boxes[:, 3] = boxes_cxcywh[:, 1] + boxes_cxcywh[:, 3] / 2  # y2
        
        # Scale boxes back to original image size
        boxes /= scale
        
        # Clip to image boundaries
        orig_h, orig_w = orig_shape
        boxes[:, [0, 2]] = np.clip(boxes[:, [0, 2]], 0, orig_w)
        boxes[:, [1, 3]] = np.clip(boxes[:, [1, 3]], 0, orig_h)
        
        # Apply NMS
        keep_indices = self._nms(boxes, scores)
        
        boxes = boxes[keep_indices].tolist()
        scores = scores[keep_indices].tolist()
        
        return boxes, scores
    
    def detect(self, image_bgr: np.ndarray) -> Tuple[List[List[float]], List[float]]:
        """
        Detect license plates in image using Hailo inference.
        
        Args:
            image_bgr: Input image in BGR format
        
        Returns:
            (boxes, scores) - boxes in [x1, y1, x2, y2] format
        """
        if image_bgr.size == 0:
            return [], []
        
        try:
            # Preprocess
            input_data, scale = self._preprocess(image_bgr)
            
            # Add batch dimension: (C, H, W) -> (1, C, H, W)
            input_batch = np.expand_dims(input_data, axis=0)
            
            # Run inference on Hailo
            with InferVStreams(
                self.network_group,
                self.input_vstreams_params,
                self.output_vstreams_params
            ) as infer_pipeline:
                # Prepare input dict
                input_dict = {
                    self.input_vstreams_params[0].name: input_batch
                }
                
                # Infer
                output_dict = infer_pipeline.infer(input_dict)
                
                # Get output (model predictions)
                predictions = list(output_dict.values())[0]
            
            # Post-process to get boxes
            boxes, scores = self._postprocess_yolo(
                predictions,
                image_bgr.shape[:2],
                scale
            )
            
            return boxes, scores
            
        except Exception as e:
            print(f"❌ Hailo detector inference error: {e}")
            return [], []
    
    def __del__(self):
        """Cleanup Hailo resources."""
        try:
            if hasattr(self, 'network_group'):
                self.network_group.release()
            if hasattr(self, 'target'):
                del self.target
        except Exception:
            pass
