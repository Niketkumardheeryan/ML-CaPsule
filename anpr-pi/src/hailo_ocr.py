"""
Hailo-8 accelerated OCR recognition for Raspberry Pi 5
Supports CRNN models compiled to HEF format for Hailo inference
"""

import os
import numpy as np
import cv2
from typing import Tuple, Optional

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
    print("⚠️  HailoRT not available. Install: pip install hailo-platform")


class HailoOCR:
    """
    Hailo-8 accelerated OCR recognizer using compiled HEF model.
    Optimized for license plate recognition on Raspberry Pi 5.
    """
    
    def __init__(
        self,
        hef_path: str,
        charset: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        input_height: int = 32,
        input_width: int = 100,
        apply_clahe: bool = True,
    ):
        """
        Initialize Hailo OCR recognizer.
        
        Args:
            hef_path: Path to compiled HEF model file
            charset: Character set for CTC decoding
            input_height: Model input height (typically 32 for CRNN)
            input_width: Model input width (typically 100 for plates)
            apply_clahe: Apply CLAHE preprocessing
        """
        if not HAILO_AVAILABLE:
            raise RuntimeError(
                "HailoRT not available. Install hailo-platform package."
            )
        
        if not os.path.exists(hef_path):
            raise FileNotFoundError(f"HEF model not found: {hef_path}")
        
        self.charset = charset
        self.blank_idx = len(charset)  # CTC blank token
        self.input_height = input_height
        self.input_width = input_width
        self.apply_clahe = apply_clahe
        
        # Load HEF model
        print(f"🚀 Loading Hailo OCR model: {hef_path}")
        self.hef = HEF(hef_path)
        
        # Create VDevice (Hailo device interface)
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
        
        print(f"✅ Hailo OCR initialized - Input: {input_width}x{input_height}")
    
    def _configure_network_group(self):
        """Configure Hailo network group with optimal settings."""
        configure_params = ConfigureParams.create_from_hef(self.hef, interface=HailoStreamInterface.PCIe)
        network_groups = self.target.configure(self.hef, configure_params)
        if not network_groups:
            raise RuntimeError("Failed to configure Hailo network group")
        return network_groups[0]
    
    def _preprocess(self, image_bgr: np.ndarray) -> np.ndarray:
        """
        Preprocess image for Hailo OCR inference.
        Matches the preprocessing used during CRNN training.
        
        Args:
            image_bgr: Input image in BGR format
        
        Returns:
            Preprocessed image (H, W, 1) float32
        """
        # Apply CLAHE if enabled (improves contrast)
        if self.apply_clahe:
            lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            image_bgr = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        
        # Bilateral filter (reduces noise, preserves edges)
        denoised = cv2.bilateralFilter(gray, 5, 50, 50)
        
        # Sharpen edges (helps distinguish similar characters like D/0/O)
        kernel_sharpen = np.array([[-1, -1, -1],
                                   [-1,  9, -1],
                                   [-1, -1, -1]])
        sharpened = cv2.filter2D(denoised, -1, kernel_sharpen)
        
        # Enhance contrast
        clahe_gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe_gray.apply(sharpened)
        
        # Resize to model input size
        resized = cv2.resize(enhanced, (self.input_width, self.input_height))
        
        # Normalize to [-1, 1] (standard CRNN preprocessing)
        normalized = resized.astype(np.float32) / 255.0
        normalized = (normalized - 0.5) / 0.5
        
        # Add channel dimension: (H, W) -> (H, W, 1)
        normalized = np.expand_dims(normalized, axis=-1)
        
        return normalized
    
    def _ctc_decode(self, predictions: np.ndarray) -> Tuple[str, float]:
        """
        CTC greedy decoder for sequence predictions.
        
        Args:
            predictions: Model output (time_steps, num_classes)
        
        Returns:
            (decoded_text, confidence)
        """
        # Get best class for each timestep
        indices = np.argmax(predictions, axis=-1)
        
        # CTC collapse: remove consecutive duplicates and blanks
        decoded = []
        prev_idx = -1
        confidences = []
        
        for idx in indices:
            if idx != prev_idx and idx != self.blank_idx:
                decoded.append(self.charset[idx])
                # Get confidence for this character
                conf = predictions[len(confidences), idx]
                confidences.append(conf)
            prev_idx = idx
        
        text = ''.join(decoded)
        
        # Average confidence across all characters
        confidence = float(np.mean(confidences)) if confidences else 0.0
        
        return text, confidence
    
    def recognize(self, image_bgr: np.ndarray) -> Tuple[str, float]:
        """
        Recognize text from license plate crop using Hailo inference.
        
        Args:
            image_bgr: Cropped plate image in BGR format
        
        Returns:
            (text, confidence) tuple
        """
        if image_bgr.size == 0:
            return "", 0.0
        
        # Resize if too small
        h, w = image_bgr.shape[:2]
        if h < 20 or w < 60:
            scale = max(20/h, 60/w)
            new_h, new_w = int(h * scale), int(w * scale)
            image_bgr = cv2.resize(image_bgr, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        
        try:
            # Preprocess image
            input_data = self._preprocess(image_bgr)
            
            # Add batch dimension: (H, W, 1) -> (1, H, W, 1)
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
                
                # Get output (time_steps, num_classes)
                output_data = list(output_dict.values())[0][0]  # Remove batch dim
            
            # CTC decode
            text, confidence = self._ctc_decode(output_data)
            
            return text, confidence
            
        except Exception as e:
            print(f"❌ Hailo OCR inference error: {e}")
            return "", 0.0
    
    def __del__(self):
        """Cleanup Hailo resources."""
        try:
            if hasattr(self, 'network_group'):
                self.network_group.release()
            if hasattr(self, 'target'):
                del self.target
        except Exception:
            pass


def apply_clahe(img_bgr):
    """Helper function for CLAHE preprocessing (shared with other backends)."""
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
