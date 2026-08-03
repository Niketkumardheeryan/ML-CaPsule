import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)

cx, cy, w, h = 100, 100, 200, 200

# FIX 1: Prevent crash if webcam is not accessible/plugged in
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

try:
    # FIX 2: Replaced 'while 1:' with 'while True:'
    while True:
        success, img = cap.read()
        
        # FIX 3: Check 'success' to handle missing frames cleanly without crashing
        if not success:
            print("Failed to read frame from camera.")
            break
            
        img = cv2.flip(img, 1)
        
        # Find hands and their landmarks
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            # Information for the first hand detected
            hand1 = hands[0]
            lmList = hand1["lmList"]  # List of 21 Landmark points
            
            # Find Distance between index finger tip (8) and middle finger tip (12)
            length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
            
            # If distance is short, consider it a "click"
            if length < 30:
                # Check if click is inside the rectangle region
                if cx - w // 2 < lmList[8][0] < cx + w // 2 and cy - h // 2 < lmList[8][1] < cy + h // 2:
                    colorR = (0, 255, 0)
                    cx, cy = lmList[8][0], lmList[8][1]
            else:
                colorR = (255, 0, 255)

        # Draw the rectangle
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        
        # Display the image
        cv2.imshow("Image", img)
        
        # FIX 4: Listen for 'q' or 'Esc' keypress to break loop safely
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            print("Exiting...")
            break

# FIX 5: Cleanly release the camera and destroy windows under ALL conditions
finally:
    print("Releasing camera and closing windows...")
    cap.release()
    cv2.destroyAllWindows()