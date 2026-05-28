import torch
import torch.nn as nn
from torchvision import models,transforms
from PIL import Image
from torchvision.transforms import v2


# Get device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   

breed_names={1: 'Abyssinian', 2: 'american_bulldog', 
             3: 'american_pit_bull_terrier', 4: 'basset_hound', 
             5: 'beagle', 6: 'Bengal', 7: 'Birman', 8: 'Bombay', 
             9: 'boxer', 10: 'British_Shorthair', 11: 'chihuahua', 
             12: 'Egyptian_Mau', 13: 'english_cocker_spaniel', 14: 'english_setter', 
             15: 'german_shorthaired', 16: 'great_pyrenees', 17: 'havanese', 18: 'japanese_chin', 
             19: 'keeshond', 20: 'leonberger', 21: 'Maine_Coon', 22: 'miniature_pinscher', 23: 'newfoundland', 
             24: 'Persian', 25: 'pomeranian', 26: 'pug', 27: 'Ragdoll', 28: 'Russian_Blue', 29: 'saint_bernard', 
             30: 'samoyed', 31: 'scottish_terrier', 32: 'shiba_inu', 33: 'Siamese', 34: 'Sphynx', 
             35: 'staffordshire_bull_terrier', 36: 'wheaten_terrier', 37: 'yorkshire_terrier'}


def image_transform(image):
  width,height=image.size
  ratio=min(224/width,224/height)
  new_height=int(height*ratio)
  new_width=int(width*ratio)
  img_transform=v2.Compose(
      [
          v2.ToImage(),
          v2.Resize((new_height,new_width)),
          v2.ToDtype(torch.float32, scale=True),
      ]
  )
  transformed_image=img_transform(image)
  pad_height=224-new_height
  pad_width=224-new_width
  top=pad_height//2
  bottom=pad_height-top
  left=pad_width//2
  right=pad_width-left

  pad_transform=v2.Pad(
      padding=(left,top,right,bottom),
      fill=0
  )
  transformed_image=pad_transform(transformed_image)

  normalize_transform=v2.Normalize(
      mean=[0.485,0.456,0.406],
      std=[0.229,0.224,0.225]
  )
  transformed_image=normalize_transform(transformed_image)

  return transformed_image


# load model

model=models.resnet50(weights='IMAGENET1K_V1')
model.fc=nn.Sequential(
  nn.Dropout(0.3),
  nn.Linear(2048, 256),
  nn.ReLU(),
  nn.Linear(256, 37)
)

model.load_state_dict(
  torch.load('pet_model.pth',map_location=device)
)

model.to(device)
model.eval()

print("Model loaded")


def predict(image_path):
  img=Image.open(image_path).convert('RGB')
  tensor=image_transform(img).unsqueeze(0).to(device)

  with torch.no_grad():
    output=model(tensor)
    probs=torch.softmax(output,dim=1)
    top3=probs.topk(3)
  print('Top 3 Predictions:')
  print('-'*50)
  for idx,prob in zip(top3.indices[0],top3.values[0]):
    breed=breed_names[idx.item()+1]
    confidence=prob.item()*100
    print(f'{breed:<30} {confidence:.1f}%')

  print('-'*50)

image_path=input("Enter image path : ")
predict(image_path)