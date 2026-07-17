import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.optimizers import Adam


def load_images():
    images = []
    labels = []
    
    categories = [
        ("Alzheimers-ADNI/train/Final AD JPEG", "AD", 171, 0),
        ("Alzheimers-ADNI/train/Final CN JPEG", "CN", 580, 1),
        ("Alzheimers-ADNI/train/Final EMCI JPEG", "EMCI", 240, 2),
        ("Alzheimers-ADNI/train/Final LMCI JPEG", "LMCI", 72, 3),
        ("Alzheimers-ADNI/train/Final MCI JPEG", "MCI", 233, 4),
    ]
    
    for folder, prefix, count, label in categories:
        for i in range(1, count + 1):
            img = cv2.imread(f"{folder}/{prefix} ({i}).jpg")
            if img is None:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = gray / 255.0
            gray = cv2.resize(gray, (240, 240))
            images.append(gray)
            labels.append(label)
    
    return np.array(images), np.array(labels)


def show_samples(images):
    plt.figure(figsize=(15, 15))
    for i in range(20):
        plt.subplot(4, 5, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.axis("off")
    plt.show()


def prepare_data(images, labels):
    images = images.reshape(-1, 240, 240, 1)
    labels = to_categorical(labels)
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.175, random_state=42)
    return X_train, X_test, y_train, y_test


def build_model():
    model = Sequential()
    model.add(Conv2D(75, kernel_size=(3, 3), padding='same', activation='relu', input_shape=(240, 240, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(50, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(500, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(250, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(5, activation='softmax'))
    return model


def train_model(model, X_train, X_test, y_train, y_test):
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=128, epochs=50, shuffle=True)
    return model


if __name__ == "__main__":
    images, labels = load_images()
    show_samples(images)
    X_train, X_test, y_train, y_test = prepare_data(images, labels)
    model = build_model()
    model = train_model(model, X_train, X_test, y_train, y_test)
    model.save("alzheimer_model.h5")