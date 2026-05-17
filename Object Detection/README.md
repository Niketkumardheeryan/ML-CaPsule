# 🪑 Furniture Image Classification using CNN and TensorFlow

## 📌 Overview

This project implements a Convolutional Neural Network (CNN) using TensorFlow/Keras to classify furniture images into multiple categories. The project covers the complete deep learning workflow including dataset loading, preprocessing, augmentation, model building, training, evaluation, and visualization.

The notebook is beginner-friendly and demonstrates how CNNs can be used for image classification tasks using Google Colab.

---

## 🚀 Features

* Furniture image classification using CNN
* TensorFlow/Keras implementation
* Data preprocessing and augmentation
* Training and validation pipeline
* Accuracy and loss visualization
* Google Colab compatible workflow
* CNN architecture visualization
* Beginner-friendly implementation
* Multi-class classification using Softmax

---

## 🧠 Why CNN?

Convolutional Neural Networks (CNNs) are widely used in Computer Vision tasks because they automatically learn image features such as:

* Edges
* Shapes
* Patterns
* Textures
* Object structures

CNNs help improve image classification accuracy by extracting meaningful spatial information from images.

---

## 📂 Dataset Information

The dataset contains furniture images organized into training and validation directories.

### 📊 Dataset Statistics

| Category          | Count |
| ----------------- | ----- |
| Training Images   | 4024  |
| Validation Images | 423   |
| Number of Classes | 5     |

---

## 📁 Dataset Structure

```bash
furniture-images/
│
├── img/
│   ├── train/
│   ├── val/
│   └── furniture_images.zip
```

---

## ⚙️ Google Drive Setup

Create a shortcut of the dataset inside **My Drive** and mount Google Drive using:

```python
from google.colab import drive
from pathlib import Path

drive.mount('/gdrive', force_remount=True)
```

### Dataset Path

```python
base = Path('/gdrive/My Drive/furniture-images/img/')
```

### Extract Dataset

```python
zip_path = base/'furniture_images.zip'
!cp "{zip_path}" .
!unzip -q furniture_images.zip
!rm furniture_images.zip
```

---

## 🛠️ Installation

### Clone Repository

```bash
git clone <repository-link>
cd <repository-name>
```

### Install Dependencies

```bash
pip install tensorflow numpy matplotlib
```

---

## 📦 Requirements

* TensorFlow
* Keras
* NumPy
* Matplotlib
* Google Colab

---

## 🧾 Technologies Used

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python       | Programming Language       |
| TensorFlow   | Deep Learning Framework    |
| Keras        | Neural Network API         |
| NumPy        | Numerical Computation      |
| Matplotlib   | Data Visualization         |
| Google Colab | Model Training Environment |

---

## 🏗️ Project Workflow

The project follows the following workflow:

1. Load dataset from Google Drive
2. Extract and preprocess images
3. Visualize dataset samples
4. Build CNN architecture
5. Train the model
6. Validate model performance
7. Plot accuracy and loss graphs
8. Analyze results

---

## 🧠 Model Architecture

The CNN architecture contains:

* 3 Convolutional Layers
* MaxPooling Layers
* Flatten Layer
* Fully Connected Dense Layer
* Softmax Output Layer

### Architecture Details

| Layer        | Description                        |
| ------------ | ---------------------------------- |
| Conv2D       | Extracts image features            |
| MaxPooling2D | Reduces spatial dimensions         |
| Flatten      | Converts feature maps into vectors |
| Dense        | Fully connected neural layer       |
| Softmax      | Multi-class classification         |

### Input Configuration

* Input Shape: 150 × 150 × 3
* Number of Classes: 5
* Activation Function: ReLU
* Final Activation: Softmax

---

## 📉 Model Summary

| Layer        | Output Shape |
| ------------ | ------------ |
| Conv2D       | (148,148,16) |
| MaxPooling2D | (74,74,16)   |
| Conv2D       | (72,72,32)   |
| MaxPooling2D | (36,36,32)   |
| Conv2D       | (34,34,64)   |
| MaxPooling2D | (17,17,64)   |
| Flatten      | 18496        |
| Dense        | 512          |
| Output Dense | 5            |

### Total Parameters

* Total Params: 9,496,613
* Trainable Params: 9,496,613

---

## 🔄 Data Augmentation

The project uses ImageDataGenerator for augmentation to improve model generalization.

### Augmentation Techniques Used

* Horizontal Flip
* Zoom Range
* Shear Transformations
* Preprocessing with InceptionV3 preprocessing

### Why Augmentation?

Data augmentation helps:

* Reduce overfitting
* Improve model robustness
* Increase data diversity
* Improve validation performance

---

## ⚡ Hyperparameters

| Parameter     | Value                    |
| ------------- | ------------------------ |
| Epochs        | 5                        |
| Batch Size    | 16                       |
| Optimizer     | Adam                     |
| Loss Function | Categorical Crossentropy |
| Image Width   | 150                      |
| Image Height  | 150                      |

---

## ▶️ Training the Model

### Compile the Model

```python
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

### Train the Model

```python
history = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    epochs=num_epochs,
    verbose=1
)
```

---

## 📈 Results

The CNN model achieved strong classification performance on the furniture dataset.

### Final Performance

| Metric              | Score |
| ------------------- | ----- |
| Training Accuracy   | 90.7% |
| Validation Accuracy | 87.5% |

---

## 📊 Training Progress

| Epoch | Training Accuracy | Validation Accuracy |
| ----- | ----------------- | ------------------- |
| 1     | 69.4%             | 75.9%               |
| 2     | 80.8%             | 80.7%               |
| 3     | 85.8%             | 86.7%               |
| 4     | 88.2%             | 88.2%               |
| 5     | 90.7%             | 87.5%               |

---

## 📷 Visualization

The project includes:

* Sample furniture image visualization
* Accuracy graphs
* Loss graphs
* CNN architecture plot (`model_plot.png`)
* Training performance plots

---

## 📚 Code Snippets

### CNN Layer Example

```python
x = layers.Conv2D(16, 3, activation='relu')(img_input)
x = layers.MaxPooling2D(2)(x)
```

### Data Generator Example

```python
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
```

---

## 🧪 Usage Instructions

### Run the Notebook

1. Open the notebook in Google Colab
2. Mount Google Drive
3. Upload dataset
4. Run all notebook cells sequentially
5. Train and evaluate the model

---

## 📌 Folder Structure

```bash
furniture-classification/
│
├── furniture-images/
├── train/
├── val/
├── model_plot.png
├── notebook.ipynb
└── README.md
```

---

## 🚧 Known Limitations

* Limited to 5 furniture categories
* Small dataset size
* No deployment interface yet
* Possibility of overfitting with extended training

---

## 🔮 Future Improvements

Potential future enhancements:

* Transfer Learning using ResNet/EfficientNet
* Real-time image prediction
* Streamlit/Flask deployment
* More furniture categories
* Hyperparameter optimization
* Improved augmentation techniques
* Mobile application integration

---

## 🤝 Contributions

Contributions, suggestions, and improvements are welcome.

### Steps to Contribute

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Push the branch
6. Submit a Pull Request

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👩‍💻 Author

Developed by Padmini Rai.
