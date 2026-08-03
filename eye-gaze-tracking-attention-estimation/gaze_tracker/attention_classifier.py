import time

class AttentionClassifier:
    """
    State machine that fuses gaze metrics and head pose angles.
    Applies Exponential Moving Average (EMA) smoothing, evaluates thresholds,
    and applies a temporal grace period before flagging distraction.
    """
    
    def __init__(self, 
                 ema_alpha=0.15,
                 yaw_thresh=18.0, 
                 pitch_thresh=15.0,
                 gaze_h_low=0.38, 
                 gaze_h_high=0.62,
                 gaze_v_low=0.40,
                 gaze_v_high=0.60,
                 distraction_time_thresh=1.5):
        """
        Args:
            ema_alpha (float): Smoothing factor for EMA [0, 1]. Smaller = smoother but more lag.
            yaw_thresh (float): Max head yaw angle (degrees) before flagged as turned.
            pitch_thresh (float): Max head pitch angle (degrees) before flagged as nodding up/down.
            gaze_h_low (float): Lower boundary for centered horizontal iris ratio.
            gaze_h_high (float): Upper boundary for centered horizontal iris ratio.
            gaze_v_low (float): Lower boundary for centered vertical iris ratio.
            gaze_v_high (float): Upper boundary for centered vertical iris ratio.
            distraction_time_thresh (float): Grace period (seconds) before marking 'Distracted'.
        """
        self.alpha = ema_alpha
        self.yaw_threshold = yaw_thresh
        self.pitch_threshold = pitch_thresh
        self.gaze_h_low = gaze_h_low
        self.gaze_h_high = gaze_h_high
        self.gaze_v_low = gaze_v_low
        self.gaze_v_high = gaze_v_high
        self.distraction_time_threshold = distraction_time_thresh
        
        # State variables
        self.yaw_ema = 0.0
        self.pitch_ema = 0.0
        self.roll_ema = 0.0
        self.gaze_h_ema = 0.5
        self.gaze_v_ema = 0.5
        self.initialized = False
        
        # Distraction tracking
        self.distraction_start_time = None
        self.current_state = "Focused"
        
        # Statistics
        self.total_frames = 0
        self.focused_frames = 0

    def update(self, gaze_data, pose_data, timestamp=None):
        """
        Update the classifier state with new gaze and head pose metrics.
        
        Args:
            gaze_data (dict): Output from GazeDetector.process_frame()
            pose_data (dict): Output from HeadPoseEstimator.estimate()
            timestamp (float): Current timestamp in seconds (default time.time())
            
        Returns:
            dict: Attention classification results, smoothed telemetry, and stats
        """
        if timestamp is None:
            timestamp = time.time()
            
        self.total_frames += 1
        
        # If face/landmarks are not detected, it is classified as distracted immediately (no face in frame)
        if not gaze_data.get('success', False) or not pose_data.get('success', False):
            if self.distraction_start_time is None:
                self.distraction_start_time = timestamp
                
            distracted_duration = timestamp - self.distraction_start_time
            if distracted_duration >= self.distraction_time_threshold:
                self.current_state = "Distracted"
            else:
                self.current_state = "Focused"  # Still in grace period
                
            return {
                'state': self.current_state,
                'distracted_reasons': ['Face Not Detected'],
                'gaze_direction': {'h': 'N/A', 'v': 'N/A'},
                'gaze_ratios': {'h': 0.5, 'v': 0.5},
                'head_pose': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
                'focus_index': (self.focused_frames / self.total_frames) * 100,
                'distracted_duration': distracted_duration
            }
            
        # Extract raw metrics
        raw_yaw = pose_data['yaw']
        raw_pitch = pose_data['pitch']
        raw_roll = pose_data['roll']
        raw_gaze_h = (gaze_data['left_eye']['h_ratio'] + gaze_data['right_eye']['h_ratio']) / 2.0
        raw_gaze_v = (gaze_data['left_eye']['v_ratio'] + gaze_data['right_eye']['v_ratio']) / 2.0
        
        # Apply Exponential Moving Average (EMA)
        if not self.initialized:
            self.yaw_ema = raw_yaw
            self.pitch_ema = raw_pitch
            self.roll_ema = raw_roll
            self.gaze_h_ema = raw_gaze_h
            self.gaze_v_ema = raw_gaze_v
            self.initialized = True
        else:
            self.yaw_ema = self.alpha * raw_yaw + (1 - self.alpha) * self.yaw_ema
            self.pitch_ema = self.alpha * raw_pitch + (1 - self.alpha) * self.pitch_ema
            self.roll_ema = self.alpha * raw_roll + (1 - self.alpha) * self.roll_ema
            self.gaze_h_ema = self.alpha * raw_gaze_h + (1 - self.alpha) * self.gaze_h_ema
            self.gaze_v_ema = self.alpha * raw_gaze_v + (1 - self.alpha) * self.gaze_v_ema
            
        # Determine Gaze directions (discrete states)
        # Horizontal
        if self.gaze_h_ema < self.gaze_h_low:
            gaze_h_dir = "Right"  # Screen-left / anatomically right
        elif self.gaze_h_ema > self.gaze_h_high:
            gaze_h_dir = "Left"   # Screen-right / anatomically left
        else:
            gaze_h_dir = "Center"
            
        # Vertical
        if self.gaze_v_ema < self.gaze_v_low:
            gaze_v_dir = "Up"
        elif self.gaze_v_ema > self.gaze_v_high:
            gaze_v_dir = "Down"
        else:
            gaze_v_dir = "Center"
            
        # Evaluate attention criteria
        reasons = []
        
        # 1. Head Pose checks
        if self.yaw_ema > self.yaw_threshold:
            reasons.append("Head Turned Left")
        elif self.yaw_ema < -self.yaw_threshold:
            reasons.append("Head Turned Right")
            
        if self.pitch_ema > self.pitch_threshold:
            reasons.append("Head Looking Up")
        elif self.pitch_ema < -self.pitch_threshold:
            reasons.append("Head Looking Down")
            
        # 2. Eye Gaze checks
        # Only flag eye distraction if the head pose is relatively centered.
        # If head is turned, eye ratios naturally shift, so head checks take priority.
        if abs(self.yaw_ema) <= self.yaw_threshold and abs(self.pitch_ema) <= self.pitch_threshold:
            if gaze_h_dir != "Center":
                reasons.append(f"Eyes Looking {gaze_h_dir}")
            if gaze_v_dir != "Center":
                reasons.append(f"Eyes Looking {gaze_v_dir}")
                
        # State decision logic (grace period)
        if len(reasons) > 0:
            if self.distraction_start_time is None:
                self.distraction_start_time = timestamp
                
            distracted_duration = timestamp - self.distraction_start_time
            if distracted_duration >= self.distraction_time_threshold:
                self.current_state = "Distracted"
            else:
                self.current_state = "Focused"  # Still in grace period
                self.focused_frames += 1
        else:
            self.distraction_start_time = None
            distracted_duration = 0.0
            self.current_state = "Focused"
            self.focused_frames += 1
            
        focus_index = (self.focused_frames / self.total_frames) * 100
        
        return {
            'state': self.current_state,
            'distracted_reasons': reasons,
            'gaze_direction': {'h': gaze_h_dir, 'v': gaze_v_dir},
            'gaze_ratios': {'h': self.gaze_h_ema, 'v': self.gaze_v_ema},
            'head_pose': {'pitch': self.pitch_ema, 'yaw': self.yaw_ema, 'roll': self.roll_ema},
            'focus_index': focus_index,
            'distracted_duration': distracted_duration
        }

    def reset_stats(self):
        self.total_frames = 0
        self.focused_frames = 0
