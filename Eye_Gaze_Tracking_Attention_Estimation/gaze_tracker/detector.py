import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os
import sys
import ssl

# NOTE: Bypassing SSL verification is required exclusively on macOS systems because the
# standard Python installer for macOS does not install or configure local root CA certificates
# by default. Without this bypass, downloading the model binary from the storage.googleapis.com
# CDN fails with a SSL: CERTIFICATE_VERIFY_FAILED error in out-of-the-box macOS setups.
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class GazeDetector:
    """
    Wrapper for MediaPipe FaceLandmarker Tasks API.
    Extracts facial landmarks and calculates horizontal/vertical eye gaze ratios 
    using robust vector projection to handle head tilt and rotations.
    """
    
    # Anatomical Left Eye (Screen Right):
    # - Inner corner (towards nose): 362
    # - Outer corner (away from nose): 263
    # - Top eyelid: 386
    # - Bottom eyelid: 374
    # - Iris center: 473
    LEFT_EYE_LANDMARKS = {
        'inner': 362,
        'outer': 263,
        'top': 386,
        'bottom': 374,
        'iris_center': 473,
        'iris_contour': [474, 475, 476, 477]
    }
    
    # Anatomical Right Eye (Screen Left):
    # - Inner corner (towards nose): 133
    # - Outer corner (away from nose): 33
    # - Top eyelid: 159
    # - Bottom eyelid: 145
    # - Iris center: 468
    RIGHT_EYE_LANDMARKS = {
        'inner': 133,
        'outer': 33,
        'top': 159,
        'bottom': 145,
        'iris_center': 468,
        'iris_contour': [469, 470, 471, 472]
    }

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        # 1. Resolve model file path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, "face_landmarker.task")
        
        # 2. Automatically download the model if missing
        if not os.path.exists(self.model_path):
            print(f"[INFO] face_landmarker.task model file not found in package. Downloading...")
            model_url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
            try:
                # Simple progress hook for console friendliness
                def progress_hook(count, block_size, total_size):
                    percent = int(count * block_size * 100 / total_size)
                    sys.stdout.write(f"\r  Downloading face mesh model: {percent}%")
                    sys.stdout.flush()
                
                urllib.request.urlretrieve(model_url, self.model_path, progress_hook)
                print("\n[INFO] Model download complete!")
            except Exception as e:
                print(f"\n[ERROR] Failed to download model: {e}", file=sys.stderr)
                raise e
                
        # 3. Configure and initialize the FaceLandmarker task
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
            num_faces=1,
            min_face_detection_confidence=min_detection_confidence,
            min_face_presence_confidence=min_tracking_confidence
        )
        self.landmarker = vision.FaceLandmarker.create_from_options(options)

    def process_frame(self, frame):
        """
        Process an image frame, extract landmarks, and compute gaze ratios.
        
        Args:
            frame: BGR image from OpenCV (webcam or video)
            
        Returns:
            dict: Gaze tracking metrics and raw landmark coordinates
        """
        h, w, c = frame.shape
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Run detection
        detection_result = self.landmarker.detect(mp_image)
        
        output = {
            'success': False,
            'left_eye': {},
            'right_eye': {},
            'raw_landmarks': None
        }
        
        if not detection_result.face_landmarks:
            return output
            
        landmarks = detection_result.face_landmarks[0]
        output['raw_landmarks'] = landmarks
        output['success'] = True
        
        # Helper function to get 2D pixel coordinates
        def get_pixel_coords(idx):
            lm = landmarks[idx]
            return np.array([lm.x * w, lm.y * h])
            
        # Helper function to compute horizontal and vertical gaze ratios using vector projection
        def compute_gaze_ratios(eye_config):
            # Coordinates
            p_inner = get_pixel_coords(eye_config['inner'])
            p_outer = get_pixel_coords(eye_config['outer'])
            p_top = get_pixel_coords(eye_config['top'])
            p_bottom = get_pixel_coords(eye_config['bottom'])
            p_iris = get_pixel_coords(eye_config['iris_center'])
            
            # 1. Horizontal Ratio (Project iris onto the eye's horizontal axis)
            # Right eye in image: Leftmost is outer (33), Rightmost is inner (133). 
            # Left eye in image: Leftmost is inner (362), Rightmost is outer (263).
            if eye_config == self.RIGHT_EYE_LANDMARKS:
                p_left = p_outer  # Outer corner (33) has smaller X
                p_right = p_inner # Inner corner (133) has larger X
            else:
                p_left = p_inner  # Inner corner (362) has smaller X
                p_right = p_outer # Outer corner (263) has larger X
                
            u_horiz = p_right - p_left
            v_horiz = p_iris - p_left
            h_ratio = np.dot(v_horiz, u_horiz) / (np.linalg.norm(u_horiz) ** 2 + 1e-6)
            
            # 2. Vertical Ratio (Project iris onto the eye's vertical axis: Top -> Bottom)
            u_vert = p_bottom - p_top
            v_vert = p_iris - p_top
            v_ratio = np.dot(v_vert, u_vert) / (np.linalg.norm(u_vert) ** 2 + 1e-6)
            
            # Calculate Pupil Diameter (approximation by bounding iris contour)
            iris_contour_pts = [get_pixel_coords(idx) for idx in eye_config['iris_contour']]
            (cx, cy), radius = cv2.minEnclosingCircle(np.array(iris_contour_pts, dtype=np.float32))
            
            return {
                'coords': {
                    'inner': p_inner,
                    'outer': p_outer,
                    'top': p_top,
                    'bottom': p_bottom,
                    'iris_center': p_iris,
                    'iris_contour': iris_contour_pts
                },
                'h_ratio': h_ratio,
                'v_ratio': v_ratio,
                'iris_radius': radius
            }
            
        output['left_eye'] = compute_gaze_ratios(self.LEFT_EYE_LANDMARKS)
        output['right_eye'] = compute_gaze_ratios(self.RIGHT_EYE_LANDMARKS)
        
        return output

    def close(self):
        self.landmarker.close()
