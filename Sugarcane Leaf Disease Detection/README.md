
# <h1 align = "center"> Sugarcane Leaf Disease Detection</h1>

### 🎯 **Goal**

The main goal of this project is to develop a machine learning model capable of accurately classifying different diseases in sugarcane leaves.

### 🧵 **Dataset**

The dataset used in this project is the Sugarcane Leaf Disease Dataset. It can be found [here](https://www.kaggle.com/datasets/nirmalsankalana/sugarcane-leaf-disease-dataset).

### 🧾 **Description**

This project involves classifying sugarcane leaf diseases using various machine learning models. The dataset comprises images of sugarcane leaves, categorized into different types. The project utilizes image preprocessing, data augmentation, and ensemble learning techniques to enhance model accuracy.

### 🧮 **What I had done!**

1. **Data Loading and Exploration:**
   - Loaded the dataset and explored its structure.
   - Understanding the distribution of the samples in the dataset through visualization.

2. **Data Splitting:**
   - Split the dataset into training, validation, and test sets using a ratio of 60:20:20.

3. **Data Preprocessing:**
   - Resized images to a uniform size.
   - Applied data augmentation techniques like rotation, zoom, and flip to increase the diversity of the training data.

4. **Model Development:**
   - Built and trained a custom convolutional neural network (CNN) model using Keras.
   - Trained 3 pre-trained models such as VGG16, IncepetionV3 and MobileNetV2.
   - To get the best out of the models, I implemented an ensemble learning approach to combine the predictions of multiple models.

5. **Model Evaluation:**
   - Evaluated model performance using accuracy, confusion matrix, and classification report.

### 🚀 **Models Implemented**

### Convolutional Neural Networks (CNN):
  - Selected for their effectiveness in image classification tasks.
  - Chosen because of customization and experimentation flexibility

### VGG16
- **Feature Extraction Power:** VGG16 is known for its deep architecture (16 layers) and strong feature extraction capabilities, suitable for capturing intricate patterns in leaf images.
- **Simplicity and Transfer Learning:** Its straightforward architecture and pretrained weights from ImageNet make it effective for transfer learning on small datasets.

### MobileNetV2
- **Efficiency and Speed:** MobileNetV2's lightweight design and efficient operations are ideal for environments with limited computational resources, offering good performance without compromising speed.
- **Deployment on Mobile Devices:** Optimized for mobile and edge devices, MobileNetV2 is suitable if deployment involves real-time leaf classification applications.

### InceptionV3
- **Multi-scale Feature Extraction:** InceptionV3's use of inception modules with different kernel sizes enables capturing features at multiple scales, beneficial for classifying leaves with varying textures and shapes.
- **Proven Performance:** It has demonstrated robust performance across diverse image classification tasks, making it a reliable choice for accurate leaf classification.

### 📚 **Libraries Needed**

- numpy
- pandas
- matplotlib
- seaborn
- plotly
- keras
- sklearn
- tensorflow
- cv2
- splitfolders
- PIL

### 📊 **Exploratory Data Analysis Results**

**INCLUSION OF IMAGES OF THE VISUALIZATION IS MUST (RESULT OF EDA)**

- Distribution of images across different disease categories.
  
  ![bar_graph_distribution](https://github.com/atharv1707/DL-Simplified/assets/77221646/5be69072-61a1-4660-84d8-0143f5102acf)
  
  ![pie_chart_distribution](https://github.com/atharv1707/DL-Simplified/assets/77221646/83f0c51c-5f96-4655-943d-7c059620a10e)

- Sample images from the dataset with their respective labels.
  ![Screenshot 2024-06-27 125351](https://github.com/atharv1707/DL-Simplified/assets/77221646/fefb53fe-5969-44b1-8973-32e381ba04e0)


### 📈 **Performance of the Models based on the Accuracy Scores**


| Model               | Accuracy |
|---------------------|----------|
| Model 1 CNN Model   | 84%      |
| Model 2 VGG16       | 82%      |
| Model 3 MobileNetV2 | 81%      |
| Model 4 InceptionV3 | 80%      |
| Ensemble Model      | 90.5%    |

### 📢 **Conclusion**

This project successfully developed a model for highly accurately classifying sugarcane leaf diseases. The ensemble learning approach improved the model's performance, achieving the best results among all the developed models. The accuracy scores indicate that the ensemble model is the most reliable for this classification task.

### ✒️ **Your Signature**

Developed by **Atharv Pal**

Connect with me on [LinkedIn](https://www.linkedin.com/in/atharv-pal17/) | [GitHub](https://github.com/atharv1707)

---
