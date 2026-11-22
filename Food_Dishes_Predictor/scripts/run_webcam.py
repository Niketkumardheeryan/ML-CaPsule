import cv2
import torch
from torchvision import models, transforms
from torch import nn
from PIL import Image

# Load class names
with open("models/classes.txt") as f:
    classes = [line.strip() for line in f.readlines()]

# Load model
model = models.mobilenet_v2()
model.classifier[1] = nn.Linear(1280, len(classes))
model.load_state_dict(torch.load("models/food_classifier.pth", map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    x = transform(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(x)
        pred_idx = outputs.argmax(1).item()
        label = classes[pred_idx]

    cv2.putText(
        frame,
        label,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Live Food Classification (Press Q to quit)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
