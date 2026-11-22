import torch
from torchvision import models, transforms
from torch import nn
from PIL import Image

# Loading classes names
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

# Changing image path here
image_path = "test_image.jpg"

img = Image.open(image_path).convert("RGB")
x = transform(img).unsqueeze(0)

with torch.no_grad():
    outputs = model(x)
    pred_idx = outputs.argmax(1).item()

print("Predicted dish:", classes[pred_idx])
