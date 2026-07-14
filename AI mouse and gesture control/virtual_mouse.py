"""
virtual_mouse.py

AI Virtual Mouse & Gesture Controller
--------------------------------------
Controls the system cursor using hand gestures captured from a webcam.

Gestures:
    - Index finger up only (middle down)  -> Move mode: cursor follows index fingertip
    - Index + middle fingers up            -> Click mode: pinch distance triggers left click

Tech stack: OpenCV, MediaPipe, PyAutoGUI

Author: Aditya Pandey
"""

import cv2
import time
import numpy as np
import pyautogui

from hand_tracking_module import HandDetector

# ---------------------- Configuration ----------------------
CAM_WIDTH, CAM_HEIGHT = 640, 480
FRAME_REDUCTION = 100          # Border margin so cursor can reach screen edges
SMOOTHENING = 5                # Higher = smoother but more lag
CLICK_DISTANCE_THRESHOLD = 35  # Pixel distance between thumb & index to register a click
CLICK_COOLDOWN = 0.4           # Seconds between allowed clicks
# -------------------------------------------------------------


def main():
    prev_x, prev_y = 0, 0
    curr_x, curr_y = 0, 0
    last_click_time = 0

    screen_width, screen_height = pyautogui.size()
    pyautogui.FAILSAFE = False  # allow cursor near screen corners without aborting

    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    detector = HandDetector(max_hands=1, detection_confidence=0.8)
    prev_time = 0

    print("AI Virtual Mouse started. Press 'q' to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame from webcam.")
            break

        frame = cv2.flip(frame, 1)  # mirror for natural interaction
        frame = detector.find_hands(frame)
        landmarks = detector.find_position(frame, draw=False)

        cv2.rectangle(
            frame,
            (FRAME_REDUCTION, FRAME_REDUCTION),
            (CAM_WIDTH - FRAME_REDUCTION, CAM_HEIGHT - FRAME_REDUCTION),
            (255, 0, 255), 2,
        )

        if landmarks:
            index_x, index_y = landmarks[8][1], landmarks[8][2]
            fingers = detector.fingers_up()

            # ---- MOVE MODE: only index finger extended ----
            if fingers[1] == 1 and fingers[2] == 0:
                mapped_x = np.interp(
                    index_x, (FRAME_REDUCTION, CAM_WIDTH - FRAME_REDUCTION), (0, screen_width)
                )
                mapped_y = np.interp(
                    index_y, (FRAME_REDUCTION, CAM_HEIGHT - FRAME_REDUCTION), (0, screen_height)
                )

                curr_x = prev_x + (mapped_x - prev_x) / SMOOTHENING
                curr_y = prev_y + (mapped_y - prev_y) / SMOOTHENING

                pyautogui.moveTo(screen_width - curr_x, curr_y)
                cv2.circle(frame, (index_x, index_y), 12, (255, 0, 255), cv2.FILLED)
                prev_x, prev_y = curr_x, curr_y

            # ---- CLICK MODE: index + middle extended, check pinch distance ----
            if fingers[1] == 1 and fingers[2] == 1:
                length, frame, line_info = detector.find_distance(8, 12, frame)

                if length < CLICK_DISTANCE_THRESHOLD:
                    now = time.time()
                    if now - last_click_time > CLICK_COOLDOWN:
                        cv2.circle(frame, (line_info[4], line_info[5]), 12, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()
                        last_click_time = now

        # ---- FPS overlay ----
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow("AI Virtual Mouse", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
