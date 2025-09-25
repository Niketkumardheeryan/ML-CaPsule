import tkinter as tk
from threading import Thread
import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
from brightnes_lefthand import Brightness
from volume_control_righthand import Volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from zoominout import ZoomInOut
from virtualmouse import VirtualMouse

# Audio settings for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

# Initialize mediapipe hands
mphands = mp.solutions.hands
hands = mphands.Hands(static_image_mode=False, model_complexity=1, max_num_hands=2, 
                      min_detection_confidence=0.75, min_tracking_confidence=0.5)
Draw = mp.solutions.drawing_utils
cap = None

# Flag to control webcam process
running = False

def start_camera():
    global cap, running
    if running:
        return
    running = True
    cap = cv2.VideoCapture(0)
    process_video()

def process_video():
    global running
    left_hand_all_closed = False
    while running:
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = MessageToDict(hand_handedness)['classification'][0]['label']

                # Process left hand gestures
                if label == 'Left':
                    landmarks = hand_landmarks.landmark
                    thumb_tip = landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP]
                    index_tip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_tip = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
                    ring_tip = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
                    pinky_tip = landmarks[mp.solutions.hands.HandLandmark.PINKY_TIP]

                    # Check if all fingers are closed
                    all_closed = all(tip.y > landmarks[mp.solutions.hands.HandLandmark.WRIST].y
                                     for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip])

                    # If all fingers are closed, stop ongoing operations one by one with a delay
                    if all_closed and not left_hand_all_closed:
                        left_hand_all_closed = True
                        for operation in ["Zoom", "Brightness", "Volume", "Virtual Mouse"]:
                            print(f"Stopping {operation} operation...")
                            cv2.putText(img, f"Stopping {operation}", (10, 100),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                            cv2.imshow('Hand Control', img)
                            cv2.waitKey(1000)  # Wait for 1 second before moving to the next operation
                        left_hand_all_closed = False

                    # Check if only the index finger and thumb are open for brightness control
                    thumb_open = thumb_tip.y < landmarks[mp.solutions.hands.HandLandmark.THUMB_IP].y
                    index_open = index_tip.y < landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP].y
                    other_fingers_closed = all(
                        tip.y > landmarks[mp.solutions.hands.HandLandmark.WRIST].y
                        for tip in [middle_tip, ring_tip, pinky_tip]
                    )

                    if index_open and thumb_open and other_fingers_closed:
                        Brightness(img, imgRGB, results, Draw, mphands, hands)
                        cv2.putText(img, 'Brightness Control Active', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 255, 255), 2)

                # Process right hand gestures for volume control and virtual mouse control
                if label == 'Right':
                    landmarks = hand_landmarks.landmark
                    index_tip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP]
                    index_dip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_DIP]
                    thumb_ip = landmarks[mp.solutions.hands.HandLandmark.THUMB_IP]

                    index_thumb_distance = ((index_tip.x - thumb_tip.x) ** 2 + (
                            index_tip.y - thumb_tip.y) ** 2) ** 0.5
                    index_dip_distance = ((index_tip.x - index_dip.x) ** 2 + (
                            index_tip.y - index_dip.y) ** 2) ** 0.5

                    index_open_threshold = 0.05
                    index_thumb_open_threshold = 0.1

                    if index_dip_distance > index_open_threshold and index_thumb_distance > index_thumb_open_threshold:
                        VirtualMouse(img, imgRGB, results, Draw, mphands, hands)
                        cv2.putText(img, 'Virtual Mouse Active', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (255, 0, 0), 2)

                    if index_dip_distance > index_open_threshold and index_thumb_distance < index_thumb_open_threshold:
                        Volume(img, imgRGB, results, Draw, mphands, hands)
                        cv2.putText(img, 'Volume Control Active', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 255, 0), 2)

        cv2.imshow('Hand Control', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    stop_camera()

def stop_camera():
    global cap, running
    running = False
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()

# Disable minimize button by overriding protocol
def disable_minimize(root):
    root.update_idletasks()
    root.attributes('-toolwindow', 1)  # Prevents minimize
    root.attributes('-topmost', True)  # Keeps window always on top

# Function to create a 3D-looking button
def create_3d_button(canvas, x, y, width, height, text, command, bg_color, fg_color):
    # Create shadow effect
    shadow_offset = 4
    shadow = canvas.create_rectangle(x + shadow_offset, y + shadow_offset, x + width + shadow_offset, y + height + shadow_offset, fill="gray", outline="")

    # Create main button rectangle
    button = canvas.create_rectangle(x, y, x + width, y + height, fill=bg_color, outline="darkgray", width=2)

    # Create the text for the button
    button_text = canvas.create_text(x + width / 2, y + height / 2, text=text, fill=fg_color, font=("Helvetica", 12, "bold"))

    # Button hover effect (lighten color)
    def on_enter(event):
        canvas.itemconfig(button, fill="#85C1E9")

    def on_leave(event):
        canvas.itemconfig(button, fill=bg_color)

    canvas.tag_bind(button, "<Enter>", on_enter)
    canvas.tag_bind(button_text, "<Enter>", on_enter)
    canvas.tag_bind(button, "<Leave>", on_leave)
    canvas.tag_bind(button_text, "<Leave>", on_leave)

    # Button click binding
    canvas.tag_bind(button, "<Button-1>", lambda e: command())
    canvas.tag_bind(button_text, "<Button-1>", lambda e: command())

# GUI code using tkinter
def create_gui():
    root = tk.Tk()
    root.title("Hand Control for Brightness and Volume")
    root.geometry("500x350")

    # Disable minimize, keep maximize and close
    disable_minimize(root)

    # Create a canvas to handle custom designs like gradient and shadows
    canvas = tk.Canvas(root, width=500, height=350)
    canvas.pack()

    # Create a gradient background
    for i in range(350):
        r = int(44 + (46 * (i / 350)))  # from #2C3E50 to #34495E
        g = int(62 + (59 * (i / 350)))
        b = int(80 + (66 * (i / 350)))
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, 500, i, fill=color)

    # Add title with a shadow effect for 3D look
    title_shadow_offset = 2
    title_font = ("Helvetica", 20, "bold")
    canvas.create_text(252 + title_shadow_offset, 52 + title_shadow_offset, text="Hand Control System", fill="gray", font=title_font)
    canvas.create_text(252, 52, text="Hand Control System", fill="#FFFFFF", font=title_font)

    # Create 3D buttons
    create_3d_button(canvas, 100, 150, 150, 50, "B/V Control", lambda: Thread(target=start_camera).start(), "#2980B9", "white")
    create_3d_button(canvas, 260, 150, 150, 50, "Stop Control", stop_camera, "#E74C3C", "white")

    root.mainloop()

if __name__ == "__main__":
    create_gui()