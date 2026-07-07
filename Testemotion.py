# import cv2
# import numpy as np
# from keras.models import model_from_json


# emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# # load json and create model
# json_file = open('emotion_model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# emotion_model = model_from_json(loaded_model_json)

# # load weights into new model
# emotion_model.load_weights("emotion_model.h5")
# print("Loaded model from disk")

# # start the webcam feed
# #cap = cv2.VideoCapture(0)

# # pass here your video path
# # you may download one from here : https://www.pexels.com/video/three-girls-laughing-5273028/
# cap = cv2.VideoCapture(r"C:\Users\Admin\emotiontrain\WIN_20240630_00_58_04_Pro.mp4")

# while True:
#     # Find haar cascade to draw bounding box around face
#     ret, frame = cap.read()
#     frame = cv2.resize(frame, (1280, 720))
#     if not ret:
#         break
#     face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # detect faces available on camera
#     num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

#     # take each face available on the camera and Preprocess it
#     for (x, y, w, h) in num_faces:
#         cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
#         roi_gray_frame = gray_frame[y:y + h, x:x + w]
#         cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

#         # predict the emotions
#         emotion_prediction = emotion_model.predict(cropped_img)
#         maxindex = int(np.argmax(emotion_prediction))
#         cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

#     cv2.imshow('Emotion Detection', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



import cv2
import numpy as np
from keras.models import model_from_json

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# Load json and create model
json_file = open('emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# Load weights into new model
emotion_model.load_weights("final_train.h5")
print("Loaded model from disk")

# Start the webcam feed
cap = cv2.VideoCapture(0)

# Pass here your video path
#cap = cv2.VideoCapture(r"C:\Users\Admin\emotiontrain\WIN_20240630_00_58_04_Pro.mp4")

while True:
    # Find Haar cascade to draw bounding box around face
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    if not ret:
        break
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces available on camera
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # Take each face available on the camera and preprocess it
    for (x, y, w, h) in num_faces:
        # Adjust the rectangle to make it slightly larger
        padding = 20
        cv2.rectangle(frame, (x - padding, y - 40 - padding), (x + w + padding, y + h + 10 + padding), (0, 255, 0), 4)
        
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
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

# import cv2
# import numpy as np
# from keras.models import model_from_json

# # Load the emotion recognition model
# emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# # Load json and create model
# json_file = open('emotion_model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# emotion_model = model_from_json(loaded_model_json)

# # Load weights into new model
# emotion_model.load_weights("emotion_model.h5")
# print("Loaded model from disk")

# # Start the webcam feed or video file
# # cap = cv2.VideoCapture(0)  # For webcam
# cap = cv2.VideoCapture(r"C:\Users\Admin\emotiontrain\WIN_20240630_00_58_04_Pro.mp4")  # For video file

# while True:
#     # Read frame from video
#     ret, frame = cap.read()
#     if not ret:
#         break
#     frame = cv2.resize(frame, (640, 360))  # Resize for display

#     # Convert frame to grayscale for face detection
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#     # Detect faces in the frame
#     num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

#     # Create a copy of the frame for segmentation display
#     segmented_frame = frame.copy()

#     # Process each detected face
#     for (x, y, w, h) in num_faces:
#         padding = 20
#         # Draw rectangle on the original frame
#         cv2.rectangle(frame, (x - padding, y - 40 - padding), (x + w + padding, y + h + 10 + padding), (0, 255, 0), 2)
        
#         roi_gray_frame = gray_frame[y:y + h, x:x + w]
#         cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

#         # Predict emotion
#         emotion_prediction = emotion_model.predict(cropped_img)
#         maxindex = int(np.argmax(emotion_prediction))
#         emotion_label = emotion_dict[maxindex]

#         # Draw emotion label on both frames
#         cv2.putText(frame, emotion_label, (x + 5, y - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(segmented_frame, emotion_label, (x + 5, y - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

#         # Segment the detected face region
#         face_region = segmented_frame[y:y+h, x:x+w]
#         lab_face_region = cv2.cvtColor(face_region, cv2.COLOR_BGR2LAB)
#         pixel_values = lab_face_region.reshape((-1, 3))
#         pixel_values = np.float32(pixel_values)

#         # K-means clustering
#         criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
#         k = 3  # Number of clusters
#         _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
#         centers = np.uint8(centers)
#         segmented_face_region = centers[labels.flatten()]
#         segmented_face_region = segmented_face_region.reshape(lab_face_region.shape)
#         segmented_face_region_bgr = cv2.cvtColor(segmented_face_region, cv2.COLOR_LAB2BGR)

#         # Replace the original face region with the segmented face region
#         segmented_frame[y:y+h, x:x+w] = segmented_face_region_bgr

#     # Display the results in two separate windows
#     cv2.imshow('Original Emotion Detection', frame)
#     cv2.imshow('Segmented Emotion Detection', segmented_frame)

#     # Position the windows next to each other
#     cv2.moveWindow('Original Emotion Detection', 0, 0)
#     cv2.moveWindow('Segmented Emotion Detection', 650, 0)  # Adjust the x-coordinate for positioning

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
