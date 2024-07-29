# import tensorflow
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import pandas as pd
from tensorflow.keras.applications.vgg16 import preprocess_input 
from keras.applications import ResNet50V2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, BatchNormalization, GlobalAveragePooling2D
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import array
import sys
# Load the pre-trained model

# Define the desired input image size
input_shape = (224, 224)

def classifier(file):

    a = {0: 'beagle', 1: 'bulldog', 2: 'dalmatian', 3: 'german-shepherd', 4: 'husky', 5: 'labrador-retriever', 6: 'poodle', 7: 'rottweiler'}
    model= load_model('../Models/best_mod.keras')
    
    # # Load and preprocess the first image
    img = file
    img = img.resize(input_shape)
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)  


    # # Print the shape of the concatenated array
    img_array=img_array/255


    # # Now you can use the images_array to make predictions with your model
    predictions = model.predict(img_array)

    # # Get the predicted class indices for each image
    predicted_class_indices = np.argmax(np.array(predictions), axis=1)

    return [predicted_class_indices[0],a[predicted_class_indices[0]]]

