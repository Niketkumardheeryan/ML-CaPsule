# 🧠 Brain Tumor Detection using Deep Learning

## 📝 Abstract

Brain tumors are a serious medical condition affecting both children and adults, constituting 85 to 90 percent of all primary Central Nervous System (CNS) tumors. Annually, around 11,700 people receive a brain tumor diagnosis, with a 5-year survival rate of approximately 34 percent for men and 36 percent for women. Proper treatment, planning, and accurate diagnostics are crucial to improving patient life expectancy.

This project focuses on automated classification techniques using Deep Learning Algorithms such as Convolutional Neural Network (CNN), Transfer Learning (TL), and Artificial Neural Network (ANN). These techniques offer higher accuracy than manual classification, aiding doctors worldwide in efficient detection and classification of brain tumors.

## 🌐 Context

Brain tumors present complexities in size and location, requiring expertise for accurate analysis. Developing countries often face challenges due to a shortage of skilled doctors and insufficient knowledge about tumors. An automated system on the cloud can address these issues, providing a faster and more accessible solution.

## Methodology

### Project Overview
The Brain Tumor Detection project aims to develop a deep learning model to classify brain tumor images into different categories. Three different models, a Convolutional Neural Network (CNN), a Multilayer Perceptron (MLP) based on TensorFlow, and a VGG16 transfer learning model, are explored for this task.

### Project Directory Structure
```
Brain Tumor Detection
|- Dataset
  |- Training Folder
  |- Testing Folder
  |- README.md
|- Images
  |- EDA README.md
|- Model
  |- brain_tumor.ipynb
  |- README.md
|- Web App
  |- app.py
  |- templates
  |- demo.mp4
  |- best_model.h5
  |- README.md
|- requirements.txt
```

### Methodology
1. **Importing Libraries:**  
   - Libraries such as NumPy, Pandas, TensorFlow, and others are imported for data manipulation, visualization, and model building.

2. **Loading the Dataset:**
   - The training and testing datasets are loaded into dataframes. File paths and labels are extracted for each image in the dataset.

3. **Data Preprocessing:**
   - Data balance is checked to ensure an even distribution of classes.
   - The testing dataset is split into validation and test sets.
   - ImageDataGenerator is used to convert dataframes to numpy arrays for model training.

4. **Model Structure:**
   - Three models are explored: 
     - CNN: A CNN model is created using Keras Sequential API with convolutional and pooling layers followed by dense layers for classification.
     - MLP: An MLP model is created with Flatten, Dense, and Dropout layers.
     - VGG16: A VGG16 transfer learning model is used with a custom dense layer for classification.

5. **Training the Models:**
   - Each model is compiled using the Adamax optimizer and categorical cross-entropy loss.
   - Models are trained on the training dataset for a specified number of epochs, with validation data for evaluation.

6. **Model Performance:**
   - Training and validation loss and accuracy are plotted over epochs to visualize the model's performance.
   - The best epoch based on validation loss and accuracy is noted for each model.

### Model Performance
#### Convolutional Neural Network (CNN)
- **Structure**  
   ![CNN Structure](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-1.png)

- **Loss vs. Epochs and Accuracy vs. Epochs**  
   ![Loss vs. Epochs and Accuracy vs. Epochs](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-2.png)

- **Performance Metrics**  
   ![Performance Metrics](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image.png)

- **Confusion Matrix**  
   ![Confusion Matrix](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-10.png)

- **Classification Report**  
   ```
               precision    recall  f1-score   support

      glioma       0.79      0.93      0.85       151
  meningioma       0.91      0.76      0.83       164
     notumor       0.97      0.97      0.97       192
   pituitary       0.99      0.98      0.99       149

    accuracy                           0.91       656
   macro avg       0.92      0.91      0.91       656
   weighted avg    0.92      0.91      0.91       656
   ```

#### Multilayer Perceptron (MLP) Based on TensorFlow
- **Structure**  
   ![MLP Structure](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-7.png)

- **Loss vs. Epochs and Accuracy vs. Epochs**  
   ![Loss vs. Epochs and Accuracy vs. Epochs](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-3.png)

- **Performance Metrics**  
   ![Performance Metrics](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-4.png)

- **Confusion Matrix**  
   ![Confusion Matrix](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-9.png)

- **Classification Report**  
   ```
               precision    recall  f1-score   support

      glioma       0.72      0.78      0.75       151
  meningioma       0.66      0.71      0.68       164
     notumor       0.94      0.85      0.89       192
   pituitary       0.93      0.89      0.91       149

    accuracy                           0.81       656
   macro avg       0.81      0.81      0.81       656
   weighted avg    0.82      0.81      0.81       656
   ```

#### VGG16 Transfer Learning Model
- **Structure**  
   ![VGG16 Structure](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-8.png)

- **Loss vs. Epochs and Accuracy vs. Epochs**  
   ![Loss vs. Epochs and Accuracy vs. Epochs](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-5.png)

- **Performance Metrics**  
   ![Performance Metrics](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-6.png)

- **Confusion Matrix**  
   ![Confusion Matrix](https://github.com/TheNaiveSamosa/DL-Simplified/blob/ac7f7edf50bc63c90645157f8f38c3f1b85d83d3/Brain%20Tumor%20Detection/Images/image-11.png)
- **Classification Report:**
   ```
                 precision    recall  f1-score   support

      glioma       0.97      0.95      0.96       151
  meningioma       0.95      0.95      0.95       164
     notumor       0.99      1.00      1.00       192
   pituitary       0.97      0.99      0.98       149

    accuracy                           0.97       656
   macro avg       0.97      0.97      0.97       656
   weighted avg    0.97      0.97      0.97       656
   ```

### Conclusion
The project explores three different models for brain tumor detection. Each model's performance is evaluated based on loss, accuracy, F1-score, and confusion matrix. The best-performing model can be selected for deployment in the Web App directory.
Based on the provided classification reports, the performance ranking from best to worst is as follows:

1. **VGG16 Transfer Learning Model**
   - Accuracy: 0.97
   - F1-score: 0.97
   - Precision and recall scores are also high for all classes.
   - This model performed the best among the three.

2. **Convolutional Neural Network (CNN)**
   - Accuracy: 0.91
   - F1-score: 0.91
   - Precision and recall scores are also relatively high.
   - This model performed well but not as well as VGG16.

3. **Multilayer Perceptron (MLP) Based on TensorFlow**
   - Accuracy: 0.81
   - F1-score: 0.81
   - Precision and recall scores are lower compared to the other two models.
   - This model performed the worst among the three.

- **Approach:** We used three different models for brain tumor detection: VGG16 transfer learning, a custom CNN, and an MLP based on TensorFlow.
- **Performance:** VGG16 showed the best performance, with the highest accuracy, F1-score, precision, and recall across all classes. The custom CNN performed well but slightly lower than VGG16. The MLP had the lowest performance among the three models.
- **Reasons:** VGG16, being a pre-trained model on ImageNet, has learned rich feature representations that are useful for our task. The custom CNN, although designed specifically for this task, might not have been deep enough or trained on enough data compared to VGG16. The MLP, being a simpler model, struggled to learn complex patterns in the data, leading to lower performance.

In conclusion, VGG16 is the most suitable model for this task due to its superior performance, followed by the custom CNN. The MLP, while simpler, is not as effective for this particular problem.

## How to Use
Requirements: Ensure you have the necessary libraries and dependencies installed. You can find the list of required packages in the requirements.txt file.

Download Data: Download the Brain Tumor MRI Dataset from Kaggle mentioned in the dataset section of the project.

Run the Jupyter Notebook: Open the provided Jupyter Notebook file and run each cell sequentially. Make sure to update any file paths or configurations as needed for your environment.

Training and Evaluation: Train the models using the provided data and evaluate their performance using metrics such as accuracy and loss.

Interpret Results: Analyze the model's performance using the visualizations and metrics provided in the notebook.

Feel free to reach out if you encounter any issues or need further assistance with running the notebook.
