from tensorflow.keras import layers, models


def build_model(input_shape=(224, 224, 3), num_classes=3):
    inputs = layers.Input(shape=input_shape)

    x = layers.Conv2D(32, 3, activation='relu', padding='same')(inputs)
    x = layers.MaxPool2D(2)(x)

    x = layers.Conv2D(64, 3, activation='relu', padding='same')(x)
    x = layers.MaxPool2D(2)(x)

    x = layers.Conv2D(128, 3, activation='relu', padding='same')(x)
    x = layers.MaxPool2D(2)(x)

    # After three 2x pools the spatial dims are reduced by factor 8
    h = input_shape[0] // 8
    w = input_shape[1] // 8

    x = layers.Reshape((h * w, 128))(x)

    x = layers.Bidirectional(layers.LSTM(128, return_sequences=False))(x)
    x = layers.Dense(128, activation='relu')(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs, outputs)
    return model


if __name__ == '__main__':
    m = build_model()
    m.summary()
