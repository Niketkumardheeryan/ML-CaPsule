# Defective Captcha Image Recognition

## 🎯 Goal
The main purpose of this project is to **identify capcha digits from 1-9 even when they're noisy and defected** from the dataset (mentioned below) using various image detection/recognition models and comparing their accuracy.

## 🧵 Dataset

The link to the dataset is given below :-

**Link :- https://www.kaggle.com/datasets/kadenm/noisy-digitbased-captcha-images**

## 🧾 Description

This project involves the comparative analysis of **Five** Keras image detection models, namely **EfficientNetB1** , **ResNet50V2** , **InceptionV3** , **DenseNet121** and **Xception**  applied to a specific dataset. The dataset consists of annotated images related to a particular domain, and the objectives include training and evaluating these models to compare their accuracy scores and performance metrics. Additionally, exploratory data analysis (EDA) techniques are employed to understand the dataset's characteristics, explore class distributions, detect imbalances, and identify areas for potential improvement. The methodology encompasses data preparation, model training, evaluation, comparative analysis of accuracy and performance metrics, and visualization of EDA insights. 

## 🧮 What I had done!

### 1. Data Loading and Preparation:
    Loaded the dataset containing image paths and corresponding labels into a pandas DataFrame for easy manipulation and analysis.

### 2. Exploratory Data Analysis (EDA):
    Bar Chart for Label Distribution: Created a bar chart to visualize the frequency distribution of different labels in the dataset.

    Pie Chart for Label Distribution: Generated a pie chart to represent the proportion of each label in the dataset.

### 3. Data Analysis:
    Counted the number of unique image paths to ensure data uniqueness and quality.
        Analyzed the distribution of image paths by label for the top 20 most frequent paths.
        Displayed the number of unique values for each categorical column to understand data variety.
        Visualized missing values in the dataset using a heatmap to identify and address potential data quality issues.
        Summarized and printed the counts of each label.

### 4. Image Preprocessing and Model Training:
    Loaded and preprocessed the test images, ensuring normalization of pixel values for consistency.
        Iterated through multiple models (VGG16, ResNet50 , Xception) saved in a directory and made predictions on the test dataset.
        Saved the predictions to CSV files for further analysis and comparison.

### 5. Model Prediction Visualization:
    Loaded models and visualized their predictions on a sample set of test images to qualitatively assess model performance.
        Adjusted image preprocessing for models requiring specific input sizes (e.g., 299x299 for Xception).

## 🚀 Models Implemented

Trained the dataset on various models , each of their summary is as follows :-

### Xception

When implementing the Xception model in code, we leverage its sophisticated architecture to bolster our image classification tasks. By loading the pre-trained Xception model with weights from the ImageNet dataset, we harness its comprehensive knowledge.

**Reasons for choosing Xception:** :  Lightweight (88 MB) , 
**Excellent Accuracy** (Xception achieves high accuracy in image classification tasks .) , 
Reduced Parameters (22.9M) ,
Faster Inference Speed (CPU - 39.4, GPU - 5.2)

Visualization of Predicted Labels on test set :- </br>
![alt text](Images/Xception_predictions/10169ba4-59c7-4a8d-bc3b-6c874085b3f5.png)</br>

![alt text](Images/Xception_predictions/9897dbb4-b870-4efa-b927-8c966741cb1e.png)</br>

![alt text](Images/Xception_predictions/b849f400-11db-456e-bfae-d6eea992561d.png)</br>

![alt text](Images/Xception_predictions/f1bda14c-5c5d-40fa-a382-81ab3114a830.png)


### EfficientNetB1
Incorporating the EfficientNetB1 model into our codebase brings a wealth of advantages to our image processing workflows. By initializing the pre-trained EfficientNetB1 model with weights from the ImageNet dataset, we tap into its profound understanding of visual data.

**Reasons for selecting EfficientNetB1:**
- Balanced Performance (EfficientNetB1 offers a balanced trade-off between accuracy and model size.)
- High Accuracy (EfficientNetB1 demonstrates superior accuracy in various image-related tasks.)
- Optimized Parameters (7.8M)
- Enhanced Efficiency (CPU - 60, GPU - 12)

Visualization of Predicted Labels on test set :- </br>

![alt text](Images/EfficientNetB1_predictions/110c0489-de74-4a4a-b156-2e3d0e5d1dcd.png)</br>

![alt text](Images/EfficientNetB1_predictions/351e8e1c-65d4-4459-bbdd-d25640feecd6.png)</br>

![alt text](Images/EfficientNetB1_predictions/57fabd9e-4a15-4f9b-84aa-f6fcdad06f2f.png)</br>

![alt text](Images/EfficientNetB1_predictions/db3e72d8-9787-49c5-ac29-0f883714fbe8-1.png)


### ResNet50V2

Implementing transfer learning with the ResNet50V2 model allows us to benefit from pre-trained weights, significantly reducing the training duration necessary for image classification tasks. This strategy is particularly advantageous when dealing with limited training data, as we can leverage the comprehensive representations learned by the base model from extensive datasets like ImageNet.

**Reasons for opting for ResNet50V2:** Relatively lightweight (98 MB) , High Accuracy (92.1 % Top 5 accuracy), Moderate Parameters (25.6M) , Reasonable Inference Speed on GPU (CPU - 32.1, GPU - 4.7)

Visualization of Predicted Labels on test set :- </br>

![alt text](Images/Resnet50V2_predictions/66ff8a40-eae3-4e85-8754-56c7d315e283.png)</br>

![alt text](Images/Resnet50V2_predictions/73526bcd-3bdb-479a-8d5a-eadf95e39bab.png)</br>

![alt text](Images/Resnet50V2_predictions/8e4ae9ac-48e0-47d6-82ae-1b6cf2513264.png)</br>

![alt text](Images/Resnet50V2_predictions/9dc0755b-8e5c-48fd-9f94-9aaebefa4fa6.png)


### InceptionV3
When implementing the InceptionV3 model in code, we leverage its powerful architecture to enhance our image classification tasks. By loading the pre-trained InceptionV3 model with weights from the ImageNet dataset, we benefit from its extensive knowledge. 

**Reason for choosing :-** 
lightweighted (92 MB) , better accuracy , less parameters (23.9M) , less inference speed (CPU - 42.2 , GPU - 6.9)

Visualization of Predicted Labels on test set :- </br>
![alt text](Images/InceptionV3_predictions/0676b4cc-8572-4478-92e6-c18cf4287d9a.png)</br>

![alt text](Images/InceptionV3_predictions/4b389b70-a176-47d0-bdfd-0930742e88a0.png)</br>

![alt text](Images/InceptionV3_predictions/6ea5b05d-d870-48f7-a546-f4f6db373054.png)</br>

![alt text](Images/InceptionV3_predictions/d00c5e4d-f801-4e56-a7d4-741846506133.png)


### DenseNet121

When implementing the DenseNet121 model in code, we leverage its densely connected architecture to enhance our image classification tasks. By loading the pre-trained DenseNet121 model with weights from the ImageNet dataset, we benefit from its extensive knowledge.

**Reason for choosing:** Lightweight (33 MB)
, High accuracy , Moderate number of parameters (8M) , Efficient inference speed (CPU - ~45 ms, GPU - ~10 ms).

Visualization of Predicted Labels on test set :- </br>
![alt text](Images/DenseNet121/26b65009-f08a-4f95-988c-9cb4472d6262.png)</br>

![alt text](Images/DenseNet121/6a74efbb-237f-4ed1-9b1c-53a85ef79c29.png)</br>

![alt text](Images/DenseNet121/ead96295-c9ce-4363-978c-39a87363dca4.png)</br>

![alt text](Images/DenseNet121/fd5fbe70-f1f5-4d32-9f83-7af7b2b96dad.png)



## 📚 Libraries Needed

1. **NumPy:** Fundamental package for numerical computing.
2. **pandas:** Data analysis and manipulation library.
3. **scikit-learn:** Machine learning library for classification, regression, and clustering.
4.  **Matplotlib:** Plotting library for creating visualizations.
5.  **Keras:** High-level neural networks API, typically used with TensorFlow backend.
6. **tqdm:** Progress bar utility for tracking iterations.
7. **seaborn:** Statistical data visualization library based on Matplotlib.

## 📊 Exploratory Data Analysis Results

### Bar Chart :-
 A bar chart showing the distribution of labels in the training dataset. It visually represents the frequency of each label category, providing an overview of how the labels are distributed across the dataset.


![alt text](Images/bar.png)

### Pie Chart :-
A pie chart illustrating the distribution of labels in the training dataset. The percentage value displayed on each segment indicates the relative frequency of each label category.

![alt text](Images/pie.png)

### Image paths distribution :-
 Visualizes the distribution of top 20 image paths by label, displays unique values in categorical columns.

![alt text](Images/image_path_distribution.png)



## 📈 Performance of the Models based on the Accuracy Scores

| Models      |       Accuracy Scores|
|------------ |------------|
|Xception  |98% ( Validation Accuracy: 0.9765)|
|InceptionV3  | 98% (Validation Accuracy: 0.9799) |
|DenseNet121     | 96% (Validation Accuracy:0.9648) |
|ResNet50V2  | 95% (Validation Accuracy: 0.9564) |
|EfficientNetB1      | 69% (Validation Accuracy:  0.6946) |


## 📢 Conclusion

**According to the accuracy scores it can be concluded that  InceptionV3 , Xception and DenseNet121 were able to perform good on this dataset.**

Even though most of  the models implemented above are giving above 90% accuracy which is great when it comes to image recognition and that too of a defective dataset after modifying the models a litle bit.

## ✒️ Your Signature

Full name:-Aaradhya Singh                      
Github Id :- https://github.com/kyra-09  
Email ID :- aaradhyasinghgaur@gmail.com  
LinkdIn :- https://www.linkedin.com/in/aaradhya-singh-0b1927250/ </br>
Participant Role :- Contributor / GSSOC (Girl Script Summer of Code ) - 2024
