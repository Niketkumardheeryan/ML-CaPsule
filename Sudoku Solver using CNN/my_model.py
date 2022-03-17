import keras
from keras.layers import Activation
from keras.layers import Conv2D, BatchNormalization, Dense, Flatten, Reshape

def get_my_model():

    my_model = keras.models.Sequential()

    my_model.add(Conv2D(64, kernel_size=(3,3), activation='relu', padding='same', input_shape=(9,9,1)))
    my_model.add(BatchNormalization())
    my_model.add(Conv2D(64, kernel_size=(3,3), activation='relu', padding='same'))
    my_model.add(BatchNormalization())
    my_model.add(Conv2D(128, kernel_size=(1,1), activation='relu', padding='same'))

    my_model.add(Flatten())
    my_model.add(Dense(81*9))
    my_model.add(Reshape((-1, 9)))
    my_model.add(Activation('softmax'))
    
    return my_model
 