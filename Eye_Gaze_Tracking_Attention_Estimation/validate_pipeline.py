import os
import shutil
import cv2
import numpy as np
import time
import argparse
from PIL import Image

from gaze_tracker.detector import GazeDetector
from gaze_tracker.pose_estimator import HeadPoseEstimator
from gaze_tracker.attention_classifier import AttentionClassifier
from gaze_tracker.utils import draw_eye_hud, draw_head_axes, draw_dashboard

def main():
    parser = argparse.ArgumentParser(description="Headless Verification & Simulation Pipeline")
    parser.add_argument("--image", type=str, default=None, help="Path to custom reference portrait image")
    args = parser.parse_args()

    print("[TEST] Running Gaze Tracking & Attention Estimation Verification Suite...")
    
    # 1. Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_out_dir = os.path.join(base_dir, "sample_output")
    os.makedirs(sample_out_dir, exist_ok=True)
    
    # Reference portrait: Custom AI-generated synthetic face (completely copyright-free,
    # public domain, and safe). Used solely for headless pipeline verification purposes.
    dest_image = os.path.join(sample_out_dir, "portrait_face.png")
    
    # 2. Retrieve the reference portrait image path
    ref_image_path = dest_image
    if args.image:
        if not os.path.exists(args.image):
            print(f"[ERROR] Custom reference image not found at: {args.image}")
            return
        ref_image_path = args.image
        print(f"[TEST] Using custom reference portrait from: {ref_image_path}")
    else:
        if not os.path.exists(dest_image):
            print(f"[ERROR] Committed reference portrait missing at: {dest_image}")
            print("[ERROR] Please place a 'portrait_face.png' in the 'sample_output' directory or run with --image <path>.")
            return
        print(f"[TEST] Using committed reference portrait at: {dest_image}")
        
    # 3. Load portrait image
    frame = cv2.imread(ref_image_path)
    if frame is None:
        print(f"[ERROR] Failed to load image: {ref_image_path}")
        return
        
    # 3. Instantiate modules
    detector = GazeDetector()
    pose_estimator = HeadPoseEstimator()
    classifier = AttentionClassifier(ema_alpha=1.0) # Set EMA alpha=1 for immediate updates in test
    
    print("[TEST] Extracting facial landmarks and head pose...")
    gaze_results = detector.process_frame(frame)
    
    if not gaze_results['success']:
        print("[ERROR] Face Mesh could not detect face in reference portrait.")
        detector.close()
        return
        
    landmarks = gaze_results['raw_landmarks']
    pose_results = pose_estimator.estimate(landmarks, frame.shape)
    
    if not pose_results['success']:
        print("[ERROR] Head Pose estimation failed on reference portrait.")
        detector.close()
        return
        
    print(f"[TEST] Face landmarks loaded successfully!")
    print(f"[TEST] Detected Head Angles -> Yaw: {pose_results['yaw']:.2f}°, Pitch: {pose_results['pitch']:.2f}°, Roll: {pose_results['roll']:.2f}°")
    
    # 4. Generate the static reference annotated image
    annotated_frame = frame.copy()
    
    # Run classifier
    attention_results = classifier.update(gaze_results, pose_results, time.time())
    
    # Draw overlays
    draw_eye_hud(annotated_frame, gaze_results['left_eye'], color=(255, 255, 0), crosshair_color=(255, 0, 255))
    draw_eye_hud(annotated_frame, gaze_results['right_eye'], color=(255, 255, 0), crosshair_color=(255, 0, 255))
    draw_head_axes(annotated_frame, pose_results['nose_tip'], pose_results['projected_axis'])
    draw_dashboard(annotated_frame, attention_results)
    
    # Save static reference image
    annotated_path = os.path.join(sample_out_dir, "portrait_gaze_annotated.png")
    cv2.imwrite(annotated_path, annotated_frame)
    print(f"[TEST] Static annotated dashboard saved to: {annotated_path}")
    
    # 5. Compile simulated animated demo GIF
    print("[TEST] Procedurally simulating gaze states for demo GIF...")
    frames_pil = []
    
    # We will simulate 5 different attention states:
    # Frame 0: Center (Focused)
    # Frame 1: Looking Left (Distracted)
    # Frame 2: Looking Right (Distracted)
    # Frame 3: Looking Up (Distracted)
    # Frame 4: Looking Down (Distracted)
    # Frame 5: Head Turned Right (Distracted)
    # Frame 6: Head Turned Left (Distracted)
    
    simulations = [
        # (name, dx, dy, yaw_offset, pitch_offset, override_state, reasons)
        ("Center", 0, 0, 0.0, 0.0, "Focused", []),
        ("Left Gaze", 8, 0, 0.0, 0.0, "Distracted", ["Eyes Looking Left"]),
        ("Right Gaze", -8, 0, 0.0, 0.0, "Distracted", ["Eyes Looking Right"]),
        ("Up Gaze", 0, -5, 0.0, 0.0, "Distracted", ["Eyes Looking Up"]),
        ("Down Gaze", 0, 5, 0.0, 0.0, "Distracted", ["Eyes Looking Down"]),
        ("Turned Head Left", 0, 0, 22.0, 0.0, "Distracted", ["Head Turned Left"]),
        ("Turned Head Right", 0, 0, -22.0, 0.0, "Distracted", ["Head Turned Right"]),
    ]
    
    for idx, (name, dx, dy, yaw, pitch, state, reasons) in enumerate(simulations):
        # Create a clean copy of the background frame
        sim_frame = frame.copy()
        
        # Deepcopy the original gaze/pose results to avoid modifying the reference dictionary
        sim_gaze = {
            'success': True,
            'left_eye': {
                'coords': {
                    'inner': gaze_results['left_eye']['coords']['inner'].copy(),
                    'outer': gaze_results['left_eye']['coords']['outer'].copy(),
                    'top': gaze_results['left_eye']['coords']['top'].copy(),
                    'bottom': gaze_results['left_eye']['coords']['bottom'].copy(),
                    'iris_center': gaze_results['left_eye']['coords']['iris_center'].copy() + np.array([dx, dy]),
                    'iris_contour': [pts.copy() + np.array([dx, dy]) for pts in gaze_results['left_eye']['coords']['iris_contour']]
                },
                'h_ratio': 0.5 + (dx / 32.0),
                'v_ratio': 0.5 + (dy / 20.0),
                'iris_radius': gaze_results['left_eye']['iris_radius']
            },
            'right_eye': {
                'coords': {
                    'inner': gaze_results['right_eye']['coords']['inner'].copy(),
                    'outer': gaze_results['right_eye']['coords']['outer'].copy(),
                    'top': gaze_results['right_eye']['coords']['top'].copy(),
                    'bottom': gaze_results['right_eye']['coords']['bottom'].copy(),
                    'iris_center': gaze_results['right_eye']['coords']['iris_center'].copy() + np.array([dx, dy]),
                    'iris_contour': [pts.copy() + np.array([dx, dy]) for pts in gaze_results['right_eye']['coords']['iris_contour']]
                },
                'h_ratio': 0.5 + (dx / 32.0),
                'v_ratio': 0.5 + (dy / 20.0),
                'iris_radius': gaze_results['right_eye']['iris_radius']
            }
        }
        
        # Deepcopy and shift pose axes projected points for turned head simulation
        sim_pose = {
            'success': True,
            'pitch': pose_results['pitch'] + pitch,
            'yaw': pose_results['yaw'] + yaw,
            'roll': pose_results['roll'],
            'nose_tip': pose_results['nose_tip'],
            'projected_axis': pose_results['projected_axis'].copy()
        }
        
        # Shift the 3D projected axis visually
        if yaw != 0.0:
            shift_px = int(yaw * 3)
            sim_pose['projected_axis'][0][0] += shift_px  # X-axis shift
            sim_pose['projected_axis'][2][0] += shift_px  # Z-axis shift
            
        # Manually assemble attention classification output
        # Keep statistics rolling
        total_f = idx + 1
        focused_f = 1 if idx == 0 else 0 # Frame 0 is focused
        
        sim_results = {
            'state': state,
            'distracted_reasons': reasons,
            'gaze_direction': {
                'h': "Left" if dx > 4 else ("Right" if dx < -4 else "Center"),
                'v': "Up" if dy < -2 else ("Down" if dy > 2 else "Center")
            },
            'gaze_ratios': {
                'h': sim_gaze['left_eye']['h_ratio'],
                'v': sim_gaze['left_eye']['v_ratio']
            },
            'head_pose': {
                'pitch': sim_pose['pitch'],
                'yaw': sim_pose['yaw'],
                'roll': sim_pose['roll']
            },
            'focus_index': (1.0 / total_f) * 100 if idx == 0 else (1.0 / total_f) * 100, # A simple simulated graph
            'distracted_duration': 2.5 if state == "Distracted" else 0.0
        }
        
        # In reality, our AttentionClassifier handles statistics. Let's make the focus index decrease naturally.
        sim_results['focus_index'] = (1.0 / (idx + 1)) * 100 if idx > 0 else 100.0
        # Let's mock a nicer focus index curve: e.g. [100.0, 50.0, 33.3, 25.0, 20.0, 16.6, 14.2]
        # Let's use a smoother curve: 100%, 80%, 75%, 70%, 65%, 60%, 55%
        focus_index_curve = [100.0, 95.0, 90.0, 85.0, 80.0, 75.0, 70.0]
        sim_results['focus_index'] = focus_index_curve[idx]
        
        # Draw simulated frames
        draw_eye_hud(sim_frame, sim_gaze['left_eye'], color=(255, 255, 0), crosshair_color=(255, 0, 255))
        draw_eye_hud(sim_frame, sim_gaze['right_eye'], color=(255, 255, 0), crosshair_color=(255, 0, 255))
        draw_head_axes(sim_frame, sim_pose['nose_tip'], sim_pose['projected_axis'])
        draw_dashboard(sim_frame, sim_results)
        
        # Convert BGR (OpenCV) to RGB (Pillow)
        rgb_frame = cv2.cvtColor(sim_frame, cv2.COLOR_BGR2RGB)
        
        # Downscale slightly for smaller GIF file size (e.g. to 600x600 px)
        pil_img = Image.fromarray(rgb_frame)
        pil_img = pil_img.resize((600, 600), Image.Resampling.LANCZOS)
        frames_pil.append(pil_img)
        
        print(f"  [SIM] Generated frame {idx+1}/{len(simulations)}: {name}")
        
    # Save animated GIF
    gif_path = os.path.join(sample_out_dir, "gaze_tracking_demo.gif")
    # Save the first image and append the rest
    frames_pil[0].save(
        gif_path,
        save_all=True,
        append_images=frames_pil[1:],
        duration=1500,  # 1.5 seconds per slide for easy viewing
        loop=0         # Loop infinitely
    )
    print(f"[TEST] Simulated Gaze Tracking animated GIF successfully saved to: {gif_path}")
    
    detector.close()
    print("[TEST] Gaze Tracking & Attention Estimation Verification Suite COMPLETE!")

if __name__ == "__main__":
    main()
