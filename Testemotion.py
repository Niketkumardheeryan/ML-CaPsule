import cv2
import numpy as np
from keras.models import model_from_json
import os

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# Load json and create model
try:
    with open('emotion_model.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    
    emotion_model = model_from_json(loaded_model_json)
    
    # Load weights into new model
    emotion_model.load_weights("final_train.h5")
    print("Loaded model from disk")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Start the webcam feed
cap = cv2.VideoCapture(0)

# Load Haar cascade
cascade_path = 'haarcascade_frontalface_default.xml'
if not os.path.exists(cascade_path):
    print(f"Error: Could not find {cascade_path}")
    exit(1)
    
face_detector = cv2.CascadeClassifier(cascade_path)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (1280, 720))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces available on camera
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # Take each face available on the camera and preprocess it
    for (x, y, w, h) in num_faces:
        # Adjust the rectangle to make it slightly larger
        padding = 20
        cv2.rectangle(frame, (x - padding, y - 40 - padding), (x + w + padding, y + h + 10 + padding), (0, 255, 0), 4)
        
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        if roi_gray_frame.shape[0] > 0 and roi_gray_frame.shape[1] > 0:
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # Predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            
            # Adjust the text position to come out of the box
            cv2.putText(frame, emotion_dict[maxindex], (x + 5, y - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Emotion Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
