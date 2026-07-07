
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

df=pd.read_csv('iris.data')

X=df.iloc[:,:4].values
y=df.iloc[:,4].values

le=LabelEncoder()

y=le.fit_transform(y)
y=to_categorical(y)

from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

model=Sequential()

model.add(Dense(64,activation='relu',input_shape=[4]))
model.add(Dense(64))
model.add(Dense(3,activation='softmax'))

model.compile(optimizer='sgd',loss='categorical_crossentropy',metrics=['acc'])

model.fit(X,y,epochs=200)

from tensorflow import lite
converter=lite.TFLiteConverter.from_keras_model(model)

tfmodel=converter.convert()
open('iris.tflite','wb').write(tfmodel)