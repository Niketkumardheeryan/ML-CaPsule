"""
hand_tracking_module.py

A reusable wrapper around MediaPipe Hands that detects hand landmarks
in a video frame and exposes convenience methods to fetch landmark
positions and finger states.

Author: Aditya Pandey
"""

import cv2
import mediapipe as mp
import math


class HandDetector:
    """Detects a hand in a BGR frame and tracks 21 landmarks per hand."""

    def __init__(self, mode=False, max_hands=1, detection_confidence=0.7,
                 tracking_confidence=0.7):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Landmark indices for fingertips: thumb, index, middle, ring, pinky
        self.tip_ids = [4, 8, 12, 16, 20]
        self.landmark_list = []
        self.results = None

    def find_hands(self, frame, draw=True):
        """Runs detection on the frame and optionally draws landmarks."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
        return frame

    def find_position(self, frame, hand_index=0, draw=True):
        """Returns a list of [id, x, y] for each landmark of the detected hand."""
        self.landmark_list = []

        if self.results and self.results.multi_hand_landmarks:
            if hand_index >= len(self.results.multi_hand_landmarks):
                return self.landmark_list

            hand = self.results.multi_hand_landmarks[hand_index]
            h, w, _ = frame.shape

            for lm_id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.landmark_list.append([lm_id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return self.landmark_list

    def fingers_up(self):
        """Returns a list of 5 booleans indicating which fingers are extended.
        Order: [thumb, index, middle, ring, pinky]."""
        fingers = []
        if not self.landmark_list:
            return [0, 0, 0, 0, 0]

        # Thumb: compare x-coordinates (works for a right hand facing camera)
        if self.landmark_list[self.tip_ids[0]][1] > self.landmark_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers: tip above the pip joint (lower y = up, image coords)
        for finger_id in range(1, 5):
            tip_y = self.landmark_list[self.tip_ids[finger_id]][2]
            pip_y = self.landmark_list[self.tip_ids[finger_id] - 2][2]
            fingers.append(1 if tip_y < pip_y else 0)

        return fingers

    def find_distance(self, point1, point2, frame, draw=True):
        """Returns euclidean distance between two landmark ids, plus drawing data."""
        x1, y1 = self.landmark_list[point1][1], self.landmark_list[point1][2]
        x2, y2 = self.landmark_list[point2][1], self.landmark_list[point2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, frame, [x1, y1, x2, y2, cx, cy]
