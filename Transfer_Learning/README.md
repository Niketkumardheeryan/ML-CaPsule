# Tranfer Learning

Transfer learning is a machine learning method where we reuse a pre-trained model as the starting point for a model on a new task. To put it simply—a model trained on one task is repurposed on a second, related task as an optimization that allows rapid progress when modeling the second task.<br> It can be done in two methods: <br>

### Feature Extraction<br>

You simply add a new classifier, which will be trained from scratch, on top of the pretrained model so that you can repurpose the feature maps learned previously for the dataset.<br>

### Fine-Tuning<br>

Unfreeze a few of the top layers of a frozen model base and jointly train both the newly-added classifier layers and the last layers of the base model for the task in hand.<br>

## Model Training

The code for training can be found in src/classication.py. The architectures available are Resnet, AlexNet, DenseNet, VGG, InceptionV3 and Squeezenet. Currently uses ResNet-18 in demo classification. In order to change architectures, change **model_name** in the below section of **\_setup_model()**.

```
model, input_size = initialize_model(model_name, num_classes, feature_extract, use_pretrained=True)
```

Put **feature_extract= False** to perform fine tuning and set to **True** for feature extraction. <br> For training InceptionV3, set **is_inception=True** in the below function.

```
train_model(model, dataloaders, criterion, optimizer, num_epochs=25, is_inception=False)
```

## How to use:

- Clone repository to local machine and open directory src.<br>

```
 streamlit run app.py
```

## To Do:

- Release it as a functional api
