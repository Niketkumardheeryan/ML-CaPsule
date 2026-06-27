import cv2
import numpy as np
import time

def draw_text_with_shadow(img, text, position, font_face, font_scale, color, thickness=1, shadow_offset=(2, 2)):
    """
    Renders text on an OpenCV image with a drop shadow for high readability on dynamic backgrounds.
    """
    x, y = position
    sx, sy = shadow_offset
    # Draw shadow (black)
    cv2.putText(img, text, (x + sx, y + sy), font_face, font_scale, (0, 0, 0), thickness + 1, cv2.LINE_AA)
    # Draw foreground text
    cv2.putText(img, text, position, font_face, font_scale, color, thickness, cv2.LINE_AA)

def draw_eye_hud(frame, eye_data, color=(0, 255, 255), crosshair_color=(0, 128, 255)):
    """
    Draws a glowing, high-tech target overlay on the eye and pupil.
    
    Args:
        frame: BGR frame to draw on
        eye_data (dict): The computed eye dictionary from GazeDetector
        color (tuple): Primary BGR color for eye contours
        crosshair_color (tuple): BGR color for pupil target crosshairs
    """
    if not eye_data or 'coords' not in eye_data:
        return
        
    coords = eye_data['coords']
    
    # 1. Convert coords to integer tuples
    inner = tuple(coords['inner'].astype(int))
    outer = tuple(coords['outer'].astype(int))
    top = tuple(coords['top'].astype(int))
    bottom = tuple(coords['bottom'].astype(int))
    iris_center = tuple(coords['iris_center'].astype(int))
    iris_radius = int(eye_data['iris_radius'])
    
    # 2. Draw eye outer contour points
    pts = np.array([inner, top, outer, bottom], dtype=np.int32)
    cv2.polylines(frame, [pts], True, color, 1, cv2.LINE_AA)
    
    # Draw small anchor circles on corners
    for pt in [inner, outer, top, bottom]:
        cv2.circle(frame, pt, 2, color, -1)
        
    # 3. Draw outer iris circle (Target Ring)
    cv2.circle(frame, iris_center, iris_radius, crosshair_color, 1, cv2.LINE_AA)
    cv2.circle(frame, iris_center, 2, crosshair_color, -1)  # Center point
    
    # 4. Draw Sci-Fi Crosshairs extending slightly outside the iris
    ch_length = int(iris_radius * 1.5)
    cv2.line(frame, (iris_center[0] - ch_length, iris_center[1]), 
             (iris_center[0] + ch_length, iris_center[1]), crosshair_color, 1, cv2.LINE_AA)
    cv2.line(frame, (iris_center[0], iris_center[1] - ch_length), 
             (iris_center[0], iris_center[1] + ch_length), crosshair_color, 1, cv2.LINE_AA)

def draw_head_axes(frame, nose_tip, projected_axis):
    """
    Draws 3D projected coordinate axes on the nose tip (X = Red, Y = Green, Z = Blue).
    """
    if projected_axis is None or nose_tip is None:
        return
        
    # Coordinates of projected axis points
    p_x = tuple(projected_axis[0])
    p_y = tuple(projected_axis[1])
    p_z = tuple(projected_axis[2])
    
    # Draw axes lines
    cv2.line(frame, nose_tip, p_x, (0, 0, 255), 2, cv2.LINE_AA)  # Red X
    cv2.line(frame, nose_tip, p_y, (0, 255, 0), 2, cv2.LINE_AA)  # Green Y
    cv2.line(frame, nose_tip, p_z, (255, 0, 0), 2, cv2.LINE_AA)  # Blue Z
    
    # Draw Axis labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    draw_text_with_shadow(frame, "X", p_x, font, 0.4, (0, 0, 255), 1)
    draw_text_with_shadow(frame, "Y", p_y, font, 0.4, (0, 255, 0), 1)
    draw_text_with_shadow(frame, "Z", p_z, font, 0.4, (255, 0, 0), 1)

def draw_dashboard(frame, results):
    """
    Draws a semi-transparent futuristic statistics dashboard,
    real-time progress bars, and high-fidelity text elements.
    """
    h, w, c = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # 1. Overlay bounding target corners (Sci-Fi Viewfinder brackets)
    bracket_len = 30
    color_hud = (128, 128, 128)
    
    # Top-Left Bracket
    cv2.line(frame, (10, 10), (10 + bracket_len, 10), color_hud, 1)
    cv2.line(frame, (10, 10), (10, 10 + bracket_len), color_hud, 1)
    # Top-Right Bracket
    cv2.line(frame, (w - 10, 10), (w - 10 - bracket_len, 10), color_hud, 1)
    cv2.line(frame, (w - 10, 10), (w - 10, 10 + bracket_len), color_hud, 1)
    # Bottom-Left Bracket
    cv2.line(frame, (10, h - 10), (10 + bracket_len, h - 10), color_hud, 1)
    cv2.line(frame, (10, h - 10), (10, h - 10 - bracket_len), color_hud, 1)
    # Bottom-Right Bracket
    cv2.line(frame, (w - 10, h - 10), (w - 10 - bracket_len, h - 10), color_hud, 1)
    cv2.line(frame, (w - 10, h - 10), (w - 10, h - 10 - bracket_len), color_hud, 1)
    
    # 2. Draw Dashboard Background Panel (Top Left)
    panel_w = 340
    panel_h = 240
    panel_overlay = frame.copy()
    cv2.rectangle(panel_overlay, (15, 15), (15 + panel_w, 15 + panel_h), (20, 20, 20), -1)
    cv2.rectangle(panel_overlay, (15, 15), (15 + panel_w, 15 + panel_h), (80, 80, 80), 1)
    cv2.addWeighted(panel_overlay, 0.45, frame, 0.55, 0, frame)
    
    # 3. Render Status Header
    state = results.get('state', 'Focused')
    if state == "Focused":
        status_color = (255, 215, 0)  # Bright Cyan (BGR: 255, 215, 0 is light blue, Cyan is 255,255,0)
        status_color = (255, 255, 0)  # Pure Cyan
        status_text = "STATE: FOCUSED"
    else:
        # Pulsing Red/Magenta based on time for distracted state
        pulse = int(time.time() * 5) % 2
        status_color = (0, 0, 255) if pulse == 0 else (128, 0, 255)  # Pulsing red/magenta
        status_text = "STATE: DISTRACTED"
        
    draw_text_with_shadow(frame, "TELEMETRY SYSTEM", (30, 40), font, 0.5, (180, 180, 180), 1)
    cv2.line(frame, (30, 48), (30 + panel_w - 30, 48), (80, 80, 80), 1)
    
    # Status Badge background
    cv2.rectangle(frame, (30, 58), (280, 93), (status_color[0]//5, status_color[1]//5, status_color[2]//5), -1)
    cv2.rectangle(frame, (30, 58), (280, 93), status_color, 1)
    draw_text_with_shadow(frame, status_text, (45, 82), font, 0.65, status_color, 2)
    
    # 4. Display Reasons if Distracted
    if state == "Distracted":
        reasons = results.get('distracted_reasons', [])
        reason_text = f"Reason: {', '.join(reasons)}" if reasons else "Reason: Unknown"
        # Wrap long reason text
        if len(reason_text) > 42:
            reason_text = reason_text[:39] + "..."
        draw_text_with_shadow(frame, reason_text, (30, 110), font, 0.4, (80, 80, 255), 1)
    else:
        # If in grace period, show warning
        dur = results.get('distracted_duration', 0.0)
        if dur > 0.1:
            draw_text_with_shadow(frame, f"WARNING: DISTRACTION IN {1.5 - dur:.1f}s", (30, 110), font, 0.4, (0, 165, 255), 1)
        else:
            draw_text_with_shadow(frame, "Attention checks nominal.", (30, 110), font, 0.45, (0, 255, 128), 1)

    # 5. Render Core Stats (Angles + Gaze Ratios)
    pose = results.get('head_pose', {'yaw': 0, 'pitch': 0, 'roll': 0})
    gaze = results.get('gaze_ratios', {'h': 0.5, 'v': 0.5})
    gaze_dir = results.get('gaze_direction', {'h': 'Center', 'v': 'Center'})
    
    draw_text_with_shadow(frame, f"Head Yaw:   {pose['yaw']:.1f} deg", (30, 132), font, 0.45, (230, 230, 230), 1)
    draw_text_with_shadow(frame, f"Head Pitch: {pose['pitch']:.1f} deg", (30, 150), font, 0.45, (230, 230, 230), 1)
    
    gaze_dir_str = f"{gaze_dir['h']} | {gaze_dir['v']}"
    draw_text_with_shadow(frame, f"Gaze H/V:   {gaze['h']:.2f} | {gaze['v']:.2f}", (30, 168), font, 0.45, (230, 230, 230), 1)
    draw_text_with_shadow(frame, f"Gaze Dir:   {gaze_dir_str}", (30, 186), font, 0.45, (230, 230, 230), 1)
    
    # 6. Session Focus Index Progress Bar
    focus_idx = results.get('focus_index', 100.0)
    draw_text_with_shadow(frame, f"SESSION FOCUS: {focus_idx:.1f}%", (30, 215), font, 0.45, (200, 200, 200), 1)
    
    # Progress Bar background
    bar_x, bar_y = 30, 225
    bar_w, bar_h = 280, 12
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (50, 50, 50), -1)
    
    # Progress Bar fill color (Cyan for high, Red for low focus)
    if focus_idx >= 75.0:
        bar_fill_color = (0, 255, 128)  # High focus green
    elif focus_idx >= 40.0:
        bar_fill_color = (0, 180, 255)  # Mid focus yellow/orange
    else:
        bar_fill_color = (0, 0, 255)    # Low focus red
        
    fill_w = int(bar_w * (focus_idx / 100.0))
    if fill_w > 0:
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), bar_fill_color, -1)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (120, 120, 120), 1)

    # 7. Real-Time Gauge Meter HUD (Bottom Left)
    # Visualizes horizontal eye ratios like a slider bar
    gauge_bg = frame.copy()
    cv2.rectangle(gauge_bg, (15, h - 85), (220, h - 15), (20, 20, 20), -1)
    cv2.rectangle(gauge_bg, (15, h - 85), (220, h - 15), (80, 80, 80), 1)
    cv2.addWeighted(gauge_bg, 0.45, frame, 0.55, 0, frame)
    
    draw_text_with_shadow(frame, "EYE GAZE GAUGES", (25, h - 70), font, 0.4, (160, 160, 160), 1)
    
    # Horizontal ratio gauge line
    gx, gy = 30, h - 45
    gw, gh = 160, 6
    cv2.rectangle(frame, (gx, gy), (gx + gw, gy + gh), (60, 60, 60), -1)
    cv2.line(frame, (gx + gw//2, gy - 2), (gx + gw//2, gy + gh + 2), (180, 180, 180), 1) # mid tick
    
    # Cursor position
    cursor_pos = int(gx + gw * np.clip(gaze['h'], 0, 1))
    cv2.circle(frame, (cursor_pos, gy + gh//2), 5, (255, 255, 0), -1) # Cyan cursor
    draw_text_with_shadow(frame, "H", (gx - 12, gy + 7), font, 0.35, (200, 200, 200), 1)
    
    # Vertical ratio gauge line
    gy2 = h - 25
    cv2.rectangle(frame, (gx, gy2), (gx + gw, gy2 + gh), (60, 60, 60), -1)
    cv2.line(frame, (gx + gw//2, gy2 - 2), (gx + gw//2, gy2 + gh + 2), (180, 180, 180), 1) # mid tick
    
    # Cursor position
    cursor_pos2 = int(gx + gw * np.clip(gaze['v'], 0, 1))
    cv2.circle(frame, (cursor_pos2, gy2 + gh//2), 5, (0, 128, 255), -1) # Orange cursor
    draw_text_with_shadow(frame, "V", (gx - 12, gy2 + 7), font, 0.35, (200, 200, 200), 1)
