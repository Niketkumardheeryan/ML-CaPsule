import cv2
import numpy as np
from ultralytics import YOLO

# 1. Load the YOLOv8 model
model = YOLO('yolov8n.pt') 

# 2. Open the video file
cap = cv2.VideoCapture('parking_video.mp4')

# 3. Reordered coordinates to fix the bow-tie shape
# Order: Top-Left, Top-Right, Bottom-Right, Bottom-Left
parking_spot = np.array([[1482, 254], [1740, 349], [1697, 529], [1346, 424]], np.int32)
parking_spot = parking_spot.reshape((-1, 1, 2)) 

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
        
    # 4. Run YOLO inference
    results = model(frame, classes=[2, 5, 7])
    annotated_frame = results[0].plot()
    
    # 5. Default parking spot color is Green (Free)
    spot_color = (0, 255, 0) 
    
    # 6. Extract the bounding box data from YOLO
    # This gives us a list of coordinates for every detected car: [x1, y1, x2, y2]
    boxes = results[0].boxes.xyxy.cpu().numpy() 
    
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        
        # Calculate the exact center point of the car's bounding box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        
        # 7. The Mathematical Check: Is the center point inside the polygon?
        # Returns 1 if inside, -1 if outside, 0 if on the edge
        result = cv2.pointPolygonTest(parking_spot, (cx, cy), False)
        
        if result >= 0: 
            # The car is in the spot! Change the polygon color to Red
            spot_color = (0, 0, 255)
            
            # Let's also draw a tiny red dot at the center of the car so you can visualize the math working
            cv2.circle(annotated_frame, (cx, cy), 5, (0, 0, 255), -1)
            
    # 8. Draw the final polygon onto the frame with the dynamic color
    cv2.polylines(annotated_frame, [parking_spot], isClosed=True, color=spot_color, thickness=3)

    cv2.imshow("Smart Parking System", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()