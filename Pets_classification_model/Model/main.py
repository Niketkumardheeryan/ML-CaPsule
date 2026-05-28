import kagglehub
kagglehub.login()
hgarg252_pets_classification_dataset_path=kagglehub.dataset_download("hgarg252/pets-classification-dataset")
# import basic lib
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms
import torch 
from torchvision.transforms import v2
from torchvision.transforms.functional import to_pil_image
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
from torchvision import models
import torch.optim as optim

# Functions
def split_data(file):
    names=[]
    with open(file,'r') as f:
        for line in f:
            if line.startswith('#'):
                continue # skip comments
            names.append(line.strip().split()[0])  #only take the name of the pet
    return names

# Dataset path location
dataset_path=kagglehub.dataset_download('hgarg252/pets-classification-dataset')

# Files in the dataset
BASE_ANN=os.path.join(dataset_path,'annotations','annotations')   #Annotations -- Guides us about which image belongs to which class
BASE_IMG=os.path.join(dataset_path,'images','images')   #Actual images 

data=[]
with open (os.path.join(BASE_ANN,'list.txt'),'r') as f:
    for line in f:
        if line.startswith('#'):
            continue

        parts=line.strip().split()
        img_name=parts[0]
        class_id=int(parts[1])
        species='cat' if parts[2]=='1' else 'dog'
        breed=img_name.rsplit('_',1)[0]
        img_path=os.path.join(BASE_IMG,img_name+'.jpg')

        data.append({
            'image_name':img_name,
            'image_path':img_path,
            'breed':breed,
            'species':species,
            'class_id':class_id
        })


df=pd.DataFrame(data)

# separate the train and test data
train_names=split_data(os.path.join(BASE_ANN,'trainval.txt'))
test_names=split_data(os.path.join(BASE_ANN,'test.txt'))

# print(len(test_names))  # debug lines

# Now we will work on training dataset only

# Most important is to make all images of standard size (224x224)

# Add padding, resize and normalisation to all images
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

class PetDataset(Dataset):
    def __init__(self,dataframe,transform=None):
        self.df=dataframe
        self.transform=transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self,index):
        row=self.df.iloc[index]
        image=Image.open(row['image_path']).convert('RGB')
        label=row['class_id']-1
        if self.transform:
            image=self.transform(image)
        return image,label
    

# split the train and test dataset
train_df=df[df['image_name'].isin(train_names)].reset_index(drop=True)
test_df=df[df['image_name'].isin(test_names)].reset_index(drop=True)

train_dataset=PetDataset(train_df,transform=image_transform)
test_dataset=PetDataset(test_df,transform=image_transform)

print(f"Train dataset size : {len(train_dataset)}")
print(f"Test dataset size  : {len(test_dataset)}")

# Create dataloader
train_dataloader=DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=2
)

test_dataloader=DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=2
)

# use the model ResNet50
model=models.resnet50(weights='IMAGENET1K_V1')


for param in model.parameters():
    param.requires_grad=False

in_features=model.fc.in_features
model.fc=nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(in_features,256),
    nn.ReLU(),
    nn.Linear(256,37)
)

# move model to GPU
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

print(f"Using device : {device}")
print("Model ready!")


# make a loss function
criterion=nn.CrossEntropyLoss()

# make an optimizer
optimizer=optim.Adam(model.parameters(),lr=0.001)

# scheduler
scheduler=optim.lr_scheduler.StepLR(optimizer,step_size=5,gamma=0.1)

def train_epoch(model,loader,optimizer,criterion):
    model.train()
    total_loss,correct=0,0

    for images,labels in loader:
        images,labels=images.to(device),labels.to(device)

        optimizer.zero_grad()

        outputs=model(images)
        loss=criterion(outputs,labels)
        loss.backward()
        optimizer.step()

        total_loss+=loss.item()
        correct+=(outputs.argmax(1)==labels).sum().item()
    
    accuracy=correct/len(loader.dataset)
    avg_loss=total_loss/len(loader)
    return avg_loss,accuracy

def eval_epoch(model,loader,criterion):
    model.eval()
    total_loss,correct=0,0

    with torch.no_grad():
        for images,labels in loader:
            images,labels=images.to(device),labels.to(device)

            outputs=model(images)

            total_loss+=criterion(outputs,labels).item()
            correct+=(outputs.argmax(1)==labels).sum().item()
    
    accuracy=correct/len(loader.dataset)
    avg_loss=total_loss/len(loader)
    return avg_loss,accuracy

epochs=10

for epoch in range(epochs):
    train_loss,train_acc=train_epoch(model,train_dataloader,optimizer,criterion)
    val_loss,val_acc=eval_epoch(model,test_dataloader,criterion)
    scheduler.step()

    print(f"Epoch {epoch+1:02d}/{epochs} | "
          f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
          f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")
    

def predict(image_path,model,breed_names):
    img=Image.open(image_path).convert('RGB')
    tensor=image_transform(img).unsqueeze(0).to(device)
    model.eval()

    with torch.no_grad():
        output=model(tensor)
        probs=torch.softmax(output,dim=1)
        top3=probs.topk(3)

    labels=[breed_names[idx.item()+1] for idx in top3.indices[0]]
    scores=[p.item() *100 for p in top3.values[0]]

    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4))

    ax1.imshow(img)
    ax1.axis('off')
    ax1.set_title('Input Image')

    ax2.barh(labels[::-1],scores[::-1],color='steelblue')
    ax2.set_xlabel('Confidence(%)')
    ax2.set_xlim(0,100)
    ax2.set_title('Top 3 Predictions')
    for i,v in enumerate(scores[::-1]):
        ax2.text(v+1,i,f'{v:.1f}%',va='center')

    plt.tight_layout()

    plt.show()

breed_names=(
    df[['class_id','breed']].
    drop_duplicates().
    sort_values('class_id').
    set_index('class_id')['breed'].
    to_dict()
)

samples=test_df.sample(5,random_state=42)
for _,row in samples.iterrows():
    predict(row['image_path'],model,breed_names)
    print(f"Actual Breed : {row['breed']}")
    print('-'*50)


# get overall accuracy :
test_loss, test_accuracy = eval_epoch(model, test_dataloader, criterion)
print(f"Test Accuracy : {test_accuracy * 100:.2f}%")
print(f"Test Loss     : {test_loss:.4f}")

# Save the model
torch.save(model.state_dict(), 'pet_model.pth')
print("Model saved!")