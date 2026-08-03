import cv2
import numpy as np

class HeadPoseEstimator:
    """
    Estimates 3D head pose (Pitch, Yaw, Roll) using 2D face mesh landmarks
    and a generic 3D human face model via OpenCV's solvePnP.
    """
    
    # Standard 3D model points of a human face in millimeters
    # Origin (0,0,0) is at the tip of the nose
    MODEL_POINTS = np.array([
        (0.0, 0.0, 0.0),             # 1: Nose tip
        (0.0, 330.0, -65.0),         # 199: Chin (below nose, positive Y)
        (-225.0, -170.0, -135.0),    # 33: Right eye outer corner (above nose, negative Y, screen-left, negative X)
        (225.0, -170.0, -135.0),     # 263: Left eye outer corner (above nose, negative Y, screen-right, positive X)
        (-150.0, 150.0, -125.0),     # 61: Right mouth corner (below nose, positive Y, screen-left, negative X)
        (150.0, 150.0, -125.0)       # 291: Left mouth corner (below nose, positive Y, screen-right, positive X)
    ], dtype=np.float32)

    # 3D points for projecting a 3D coordinate axis on the nose tip (for visualization)
    AXIS_POINTS = np.array([
        (100.0, 0.0, 0.0),   # X axis (Red) - points to person's left (screen-right)
        (0.0, 100.0, 0.0),   # Y axis (Green) - points down (towards chin)
        (0.0, 0.0, 100.0)    # Z axis (Blue) - points straight out of face
    ], dtype=np.float32)

    def __init__(self):
        pass

    def estimate(self, landmarks, frame_shape):
        """
        Estimate Pitch, Yaw, and Roll from landmarks.
        
        Args:
            landmarks: MediaPipe Face Mesh landmarks list
            frame_shape: (height, width, channels)
            
        Returns:
            dict: Euler angles in degrees, camera matrix, and rotation/translation vectors
        """
        h, w, c = frame_shape
        
        # Extract corresponding 2D screen coordinate points
        # Landmark indices used: 1 (nose), 199 (chin), 33 (R eye outer), 263 (L eye outer), 61 (R mouth), 291 (L mouth)
        indices = [1, 199, 33, 263, 61, 291]
        image_points = np.array([
            [landmarks[idx].x * w, landmarks[idx].y * h] for idx in indices
        ], dtype=np.float32)
        
        # Camera intrinsic matrix (approximated)
        focal_length = w
        center = (w / 2.0, h / 2.0)
        camera_matrix = np.array([
            [focal_length, 0.0, center[0]],
            [0.0, focal_length, center[1]],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)
        
        # Zero distortion coefficients assumed
        dist_coeffs = np.zeros((4, 1), dtype=np.float32)
        
        # Solve the PnP problem (Perspective-n-Point)
        success, rot_vec, trans_vec = cv2.solvePnP(
            self.MODEL_POINTS,
            image_points,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        if not success:
            return {
                'success': False,
                'pitch': 0.0,
                'yaw': 0.0,
                'roll': 0.0,
                'projected_axis': None
            }
            
        # Convert rotation vector to rotation matrix
        rot_mat, _ = cv2.Rodrigues(rot_vec)
        
        # Decompose rotation matrix into Euler angles
        # We can extract them mathematically
        sy = np.sqrt(rot_mat[0, 0] ** 2 + rot_mat[1, 0] ** 2)
        singular = sy < 1e-6
        
        if not singular:
            x = np.arctan2(rot_mat[2, 1], rot_mat[2, 2])
            y = np.arctan2(-rot_mat[2, 0], sy)
            z = np.arctan2(rot_mat[1, 0], rot_mat[0, 0])
        else:
            x = np.arctan2(-rot_mat[1, 2], rot_mat[1, 1])
            y = np.arctan2(-rot_mat[2, 0], sy)
            z = 0
            
        # Convert radians to degrees
        # Standardize angle conventions for intuitive attention tracking telemetry:
        # - Pitch (rotation about X): positive = looking up, negative = looking down
        # - Yaw (rotation about Y):   positive = turning left (screen-right), negative = turning right (screen-left)
        # - Roll (rotation about Z):  positive = tilting left (screen-right), negative = tilting right (screen-left)
        pitch = np.degrees(x)
        yaw = np.degrees(y)
        roll = np.degrees(z)
        
        # Wrap roll to the [-90, 90] interval to normalize front-facing cameras
        if roll > 90.0:
            roll -= 180.0
        elif roll < -90.0:
            roll += 180.0
        
        # Invert Pitch direction so that positive indicates looking up and negative indicates looking down
        pitch = -pitch
        
        # Project the 3D axis points onto the 2D frame
        proj_axis, _ = cv2.projectPoints(
            self.AXIS_POINTS,
            rot_vec,
            trans_vec,
            camera_matrix,
            dist_coeffs
        )
        
        # Extract pixel coordinates of the nose tip (used as coordinate origin base)
        nose_base = tuple(image_points[0].astype(int))
        
        return {
            'success': True,
            'pitch': pitch,
            'yaw': yaw,
            'roll': roll,
            'nose_tip': nose_base,
            'projected_axis': proj_axis.reshape(-1, 2).astype(int),
            'rot_vec': rot_vec,
            'trans_vec': trans_vec,
            'camera_matrix': camera_matrix,
            'dist_coeffs': dist_coeffs
        }
