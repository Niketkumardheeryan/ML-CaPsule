"""Real-time hand gesture Recognition system."""

import mediapipe as mp
import cv2
import numpy as np

from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions

from pathlib import Path
import os


def draw_info_text(frame, bbox, label, corner_length, color, hand_label):
    """Draw bounding box corners and classification label.

    Args:
        frame: Input video frame
        bbox: Bounding box coordinates (x1, y1, x2, y2)
        label: Classification label text
        corner_length: Length of corner lines
        color: Color in BGR format
        gesture_id: Gesture identifier
        hand_label: Hand side ('L' or 'R')
    """
    x1, y1, x2, y2 = bbox

    # Bottom-right corner
    cv2.line(frame, (x2 - corner_length, y2), (x2, y2), color, 3)
    cv2.line(frame, (x2, y2), (x2, y2 - corner_length), color, 3)

    # Bottom-left corner
    cv2.line(frame, (x1, y2), (x1 + corner_length, y2), color, 3)
    cv2.line(frame, (x1, y2), (x1, y2 - corner_length), color, 3)

    # Top-right corner
    cv2.line(frame, (x2 - corner_length, y1), (x2, y1), color, 3)
    cv2.line(frame, (x2, y1), (x2, y1 + corner_length), color, 3)

    # Top-left corner
    cv2.line(frame, (x1 + corner_length, y1), (x1, y1), color, 3)
    cv2.line(frame, (x1, y1), (x1, y1 + corner_length), color, 3)

    # Calculate label background dimensions
    (width, height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX, 0.8, 2)

    # Draw label background rectangle
    cv2.rectangle(
        frame,
        (x1, y1 - (height + baseline) - 20),
        (x1 + width + 60, y1 - 10),
        color,
        -1,
    )

    # Draw label text in white
    cv2.putText(
        frame,
        label,
        (x1 + 30, y1 - baseline // 2 - 15),
        cv2.FONT_HERSHEY_COMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )


# Config
IMAGE_SHAPE = (1280, 720)
MAX_HANDS = 2

PADDING = 20
BOXCOLOR = (255, 255, 0)
CORNER_LENGTH = 50

ROOT_DIR = Path(__file__).resolve().parent

# MediaPipe drawing utilities
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set camera resolution
cap.set(3, IMAGE_SHAPE[0])
cap.set(4, IMAGE_SHAPE[1])

# Configure MediaPipe hand landmark detector
options = vision.GestureRecognizerOptions(
    base_options=BaseOptions(
        model_asset_path=os.path.join(ROOT_DIR, "models/gesture_recognizer.task")
    ),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=MAX_HANDS,
)

with vision.GestureRecognizer.create_from_options(options) as recognizer:
    while cap.isOpened():
        # Read video frame
        ret, frame = cap.read()

        if not ret:
            continue

        # Mirror frame horizontally
        cv2.flip(frame, 1, frame)

        # Convert frame to MediaPipe format
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
        )

        # Detect hand landmarks
        result = recognizer.recognize_for_video(
            mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC))
        )

        if result.hand_landmarks:
            for i, hand_landmark in enumerate(result.hand_landmarks):
                if i >= MAX_HANDS:
                    break

                # Draw hand skeleton
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmark,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec((0, 0, 255), -1, 6),
                    mp_drawing.DrawingSpec((0, 255, 0), 3, -1),
                )

                # Convert landmark coordinates to pixel positions
                landmarks = np.array(
                    [
                        [landmark.x * frame.shape[1], landmark.y * frame.shape[0]]
                        for landmark in hand_landmark
                    ]
                )

                label = result.gestures[i][0].category_name

                # Calculate bounding box
                x_coords = landmarks[:, 0].astype(int)
                y_coords = landmarks[:, 1].astype(int)

                bbox = (
                    min(x_coords) - PADDING,
                    min(y_coords) - PADDING,
                    max(x_coords) + PADDING,
                    max(y_coords) + PADDING,
                )

                # Draw bounding box and label
                draw_info_text(
                    frame,
                    bbox,
                    label,
                    CORNER_LENGTH,
                    BOXCOLOR,
                    result.handedness[i][0].display_name[0],
                )

        # Display frame
        cv2.imshow("Hand Gestuer Classifier", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Cleanup resources
cap.release()
cv2.destroyAllWindows()
