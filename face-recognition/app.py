from deepface import DeepFace
detector_backends = [ 'opencv', 'retinaface',
        'mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8', 'centerface'] # or 'skip' (default is opencv).
#Faces Detection
faces=DeepFace.extract_faces(img_path="img.jpg", #select the image [it can have multiple faces]
                             detector_backend = 'mtcnn', #[select the backend among mtcnn, opencv, ssd, dlib]
                             enforce_detection = False, #pass this argument to disable multiple face detection
                             align = True, #pass this argument to align faces
                             margin = 10) #add margin for face extraction
print(faces)

#Facial Recognition
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
  "GhostFaceNet",
]
#You can adjust the threshold according to your use case. Print the result and see the distance values. Then, you can decide the optimal threshold for your project.
#you can use any of the these models for verify and find methods for recognition
fr_result = DeepFace.verify(
  img1_path = "img1.jpg",
  img2_path = "img2.jpg",
)
print(fr_result)

dfs = DeepFace.find(
  img_path = "img1.jpg",
  db_path = "PATH_TO_YOUR_DB"
)
print(dfs) #you can print the result to see the distance values

#Facial Analysis
objs = DeepFace.analyze(
  img_path = "img1.jpg", 
  actions = ['age', 'gender', 'race', 'emotion'],
)
print(objs)

#Facial Embeddings
embedding_objs = DeepFace.represent(
  img_path = "img1.jpg",
  model_name = models[2],
)
#These can be used for clustering, finding similarity between faces, vector operations, by storing in a vector database for faster retrieval, etc.