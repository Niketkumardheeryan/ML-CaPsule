#!/usr/bin/env python3
import cv2
import argparse
import time
import sys

from gaze_tracker.detector import GazeDetector
from gaze_tracker.pose_estimator import HeadPoseEstimator
from gaze_tracker.attention_classifier import AttentionClassifier
from gaze_tracker.utils import draw_eye_hud, draw_head_axes, draw_dashboard, draw_text_with_shadow

def main():
    parser = argparse.ArgumentParser(
        description="Real-Time Eye Gaze Tracking & Attention Estimation System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input options
    parser.add_argument("--source", type=str, default="0",
                        help="Video source index (e.g., 0 for webcam) or file path.")
    
    # Attention classifier thresholds
    parser.add_argument("--ema-alpha", type=float, default=0.15,
                        help="Smoothing factor for Exponential Moving Average [0.0 - 1.0].")
    parser.add_argument("--yaw-thresh", type=float, default=18.0,
                        help="Max yaw (left/right) rotation angle before flagging distraction.")
    parser.add_argument("--pitch-thresh", type=float, default=15.0,
                        help="Max pitch (up/down) rotation angle before flagging distraction.")
    parser.add_argument("--gaze-h-low", type=float, default=0.38,
                        help="Lower limit for centered horizontal gaze ratio.")
    parser.add_argument("--gaze-h-high", type=float, default=0.62,
                        help="Upper limit for centered horizontal gaze ratio.")
    parser.add_argument("--gaze-v-low", type=float, default=0.40,
                        help="Lower limit for centered vertical gaze ratio.")
    parser.add_argument("--gaze-v-high", type=float, default=0.60,
                        help="Upper limit for centered vertical gaze ratio.")
    parser.add_argument("--distraction-thresh", type=float, default=1.5,
                        help="Distraction duration threshold (seconds) before state changes to Distracted.")
    
    # Visual options
    parser.add_argument("--no-eye-mesh", action="store_true",
                        help="Disable tech overlays on eyelids and iris targets.")
    parser.add_argument("--no-pose-axis", action="store_true",
                        help="Disable 3D head pose coordinate axis projection.")
    
    args = parser.parse_args()
    
    # Resolve source type
    if args.source.isdigit():
        source = int(args.source)
        is_webcam = True
    else:
        source = args.source
        is_webcam = False
        
    print("[INFO] Initializing Computer Vision Models...")
    detector = GazeDetector()
    pose_estimator = HeadPoseEstimator()
    classifier = AttentionClassifier(
        ema_alpha=args.ema_alpha,
        yaw_thresh=args.yaw_thresh,
        pitch_thresh=args.pitch_thresh,
        gaze_h_low=args.gaze_h_low,
        gaze_h_high=args.gaze_h_high,
        gaze_v_low=args.gaze_v_low,
        gaze_v_high=args.gaze_v_high,
        distraction_time_thresh=args.distraction_thresh
    )
    
    print(f"[INFO] Opening video source: {source}...")
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERROR] Could not open video source {source}.", file=sys.stderr)
        sys.exit(1)
        
    # Optional camera config
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    window_name = "Real-Time Eye Gaze & Attention Tracker"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    print("\n" + "="*50)
    print("  Gaze Tracker Online. Press 'Q' inside window to quit.")
    print("="*50 + "\n")
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[INFO] End of video feed or empty frame.")
                break
                
            frame_count += 1
            
            # Flip frame horizontally for a more natural mirror experience on webcams
            if is_webcam:
                frame = cv2.flip(frame, 1)
                
            curr_timestamp = time.time()
            
            # 1. Process facial landmarks and eye metrics
            gaze_results = detector.process_frame(frame)
            
            # 2. Process 3D head pose and attention heuristics
            if gaze_results['success']:
                landmarks = gaze_results['raw_landmarks']
                pose_results = pose_estimator.estimate(landmarks, frame.shape)
                
                # Update classifier state
                attention_results = classifier.update(gaze_results, pose_results, curr_timestamp)
                
                # 3. Draw tech HUD elements
                # Draw eye overlays (pupil target + eyelid borders)
                if not args.no_eye_mesh:
                    draw_eye_hud(frame, gaze_results['left_eye'], color=(255, 255, 0), crosshair_color=(255, 0, 255))
                    draw_eye_hud(frame, gaze_results['right_eye'], color=(255, 255, 0), crosshair_color=(255, 0, 255))
                    
                # Draw 3D coordinate axes from nose tip
                if not args.no_pose_axis and pose_results['success']:
                    draw_head_axes(frame, pose_results['nose_tip'], pose_results['projected_axis'])
                    
                # Draw high-fidelity HUD statistics panel
                draw_dashboard(frame, attention_results)
            else:
                # If face is lost, pass empty dicts to let the state machine handle the timeout
                attention_results = classifier.update({'success': False}, {'success': False}, curr_timestamp)
                draw_dashboard(frame, attention_results)
                
            # Render simple real-time FPS counter
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0.05 else 30.0
            draw_text_with_shadow(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 100, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
            
            cv2.imshow(window_name, frame)
            
            # Key checks
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
                
    except KeyboardInterrupt:
        print("[INFO] Execution interrupted by keyboard.")
    finally:
        print("\n" + "="*50)
        print("  Terminating Tracker Feed...")
        if classifier.total_frames > 0:
            final_focus = (classifier.focused_frames / classifier.total_frames) * 100
            print(f"  Total Session Frames: {classifier.total_frames}")
            print(f"  Average Focus Index:  {final_focus:.1f}%")
        print("="*50 + "\n")
        
        cap.release()
        cv2.destroyAllWindows()
        detector.close()

if __name__ == "__main__":
    main()
