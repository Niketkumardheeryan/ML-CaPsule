import streamlit as st

st.title("Hindi Letter classification 🕉️")
st.divider()
st.image("https://i.pinimg.com/474x/ce/79/6c/ce796ceb0d16147fd7853f1a3fdd0210.jpg")
st.subheader("Introduction")
st.write('''
The web app is created using streamlit framework. It contains a heading, small introduction and then a image uploader.
          After the user uploads image, the image goes to backend and respected class is predicted by the CNN model and then
          the uploaded image along with prediction is showed. We can play with prediciton time and accuracy by changing batch_size,
          number of epochs and using a different CNN architecture.

''')
st.divider()
uploaded_file = st.file_uploader("Enter image to Predict", type=['png', 'jpg'])
submit = st.button("Submit")
st.write("It may take 2-3 minutes to predict the image")
if submit:
    if uploaded_file is not None:

        import tensorflow as tf
        from keras.preprocessing.image import ImageDataGenerator

        train_datagen = ImageDataGenerator(rescale = 1./255,
                                        shear_range = 0.2,
                                        zoom_range = 0.2,
                                        horizontal_flip = True)
        training_set = train_datagen.flow_from_directory('Dataset/dataset/train',
                                                        target_size = (64, 64),
                                                        batch_size = 30,
                                                        class_mode = 'categorical')
        test_datagen = ImageDataGenerator(rescale = 1./255)
        test_set = test_datagen.flow_from_directory('Dataset/dataset/test',
                                                    target_size = (64, 64),
                                                    batch_size = 30,
                                                    class_mode = 'categorical')
        # LeNet-5 architecture
        lenet = tf.keras.models.Sequential()

        # Layer 1: Convolutional layer with 6 filters, kernel size 5x5, and ReLU activation
        lenet.add(tf.keras.layers.Conv2D(filters=6, kernel_size=5, activation='relu', input_shape=[64, 64, 3]))

        # Layer 2: Average pooling layer with pool size 2x2 and strides 2
        lenet.add(tf.keras.layers.AveragePooling2D(pool_size=2, strides=2))

        # Layer 3: Convolutional layer with 16 filters, kernel size 5x5, and ReLU activation
        lenet.add(tf.keras.layers.Conv2D(filters=16, kernel_size=5, activation='relu'))

        # Layer 4: Average pooling layer with pool size 2x2 and strides 2
        lenet.add(tf.keras.layers.AveragePooling2D(pool_size=2, strides=2))

        # Layer 5: Flatten layer
        lenet.add(tf.keras.layers.Flatten())

        # Layer 6: Fully connected layer with 120 units and ReLU activation
        lenet.add(tf.keras.layers.Dense(units=120, activation='relu'))

        # Layer 7: Fully connected layer with 84 units and ReLU activation
        lenet.add(tf.keras.layers.Dense(units=84, activation='relu'))

        # Layer 8: Output layer with 46 units (assuming it's the number of classes) and softmax activation
        lenet.add(tf.keras.layers.Dense(units=46, activation='softmax'))

        # Compile the model with Adam optimizer and categorical crossentropy loss
        lenet.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        lenet.fit(x = training_set, validation_data = test_set, epochs = 15)

        # Part 4 - Making a single prediction
        print(training_set.class_indices)
        import numpy as np
        from keras.preprocessing import image
        if uploaded_file is not None:
            try:
                test_image = image.load_img('uploaded_file', target_size = (64, 64))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis = 0)
                result = lenet.predict(test_image)
                training_set.class_indices
                prediction = lenet.predict(test_image)
                predicted_class_index = np.argmax(prediction)
                print(predicted_class_index)
                st.write(predicted_class_index)
                print(training_set.class_indices)
                st.write(training_set.class_indices)
            except:
                st.write("There is error in file provided")
                st.subheader("Result : " + prediction)
                st.write("Accuracy for 15 epochs is 74.03%")
        elif uploaded_file is None:
            st.markdown(":red[Please enter a image]")


