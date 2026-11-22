import sys
import torch
from torchvision import models, transforms
from torch import nn
from PIL import Image

# CHECK INPUT 
if len(sys.argv) < 2:
    print("X Usage: python predict_image.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

# LOAD CLASSES 
with open("models/classes.txt") as f:
    classes = [line.strip() for line in f.readlines()]

# LOAD MODEL 
model = models.mobilenet_v2()
model.classifier[1] = nn.Linear(1280, len(classes))
model.load_state_dict(
    torch.load("models/food_classifier.pth", map_location="cpu")
)
model.eval()

# TRANSFORM 
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# LOAD IMAGE 
img = Image.open(image_path).convert("RGB")
x = transform(img).unsqueeze(0)

#PREDICT
with torch.no_grad():
    outputs = model(x)
    probs = torch.softmax(outputs, dim=1)
    pred_idx = probs.argmax(1).item()
    confidence = probs[0][pred_idx].item() * 100

#OUTPUT 
print(f" Predicted Dish : {classes[pred_idx]}")
print(f" Confidence    : {confidence:.2f}%")
