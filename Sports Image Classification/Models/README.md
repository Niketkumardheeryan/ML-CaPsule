# Sports Image Classification

## 🎯 Goal
The main purpose of this project is to **classify 100 different sports images** from the dataset (mentioned below) using various image detection/recognition models and comparing their accuracy.

## 🧵 Dataset

The link to the dataset is given below :-

**Link :- https://www.kaggle.com/datasets/gpiosenka/sports-classification**

## 🧾 Description

This project involves the comparative analysis of **Five** Keras image detection models, namely **MobileNetV2** , **ResNet50** , **InceptionV3** , **EfficientNetB0** and **Xception**  applied to a specific dataset. The dataset consists of annotated images related to a particular domain, and the objectives include training and evaluating these models to compare their accuracy scores and performance metrics. Additionally, exploratory data analysis (EDA) techniques are employed to understand the dataset's characteristics, explore class distributions, detect imbalances, and identify areas for potential improvement. The methodology encompasses data preparation, model training, evaluation, comparative analysis of accuracy and performance metrics, and visualization of EDA insights. 

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


![alt text](../images/Xception_predictions/162c7eb0-4671-4991-9f75-5345cc1854f6.png)</br>

![alt text](../images/Xception_predictions/1e3161aa-d016-4e9a-900e-3cc5f11be2ee.png)</br>

![alt text](../images/Xception_predictions/3f6d756f-917b-45a8-ba53-86a96b56bb2d.png)</br>

![alt text](../images/Xception_predictions/49a7b8a8-b8f1-481d-9094-0edce1ac8932.png)</br>

![alt text](../images/Xception_predictions/8132406e-b77e-4497-83a8-7b10d1aacd27.png)</br>

![alt text](../images/Xception_predictions/a6e78b79-83a2-4c28-bd2c-dcefbd858f97.png)



### MobileNetV2
Utilizing transfer learning with the MobileNetV2 model allows us to leverage pre-trained weights, drastically reducing the training time needed for image classification tasks. This strategy is especially beneficial when working with limited training data, as we can capitalize on the comprehensive representations learned by the base model from a vast dataset such as ImageNet.

**Reason for choosing :-** 
 Very lightweighted (14 MB) , better accuracy, very less parameters (3.5M) , less inference speed when using GPU (CPU - 25.9, GPU - 3.8)

Visualization of Predicted Labels on test set :- </br>

![alt text](../images/MobieNetV2_predictions/2e6ecbbe-9f01-476d-af15-c578354d8260.png)</br>
![alt text](../images/MobieNetV2_predictions/318512f5-a8d1-4e6b-bb4b-4aa52a7c5378.png)</br>
![alt text](../images/MobieNetV2_predictions/63b4f459-bcba-47c0-ab6d-e046dca169da.png)</br>
![alt text](../images/MobieNetV2_predictions/3fdb3807-57fe-4b71-81d8-55dcc7b0fe9f.png)</br>

![alt text](../images/MobieNetV2_predictions/7d36752a-3c3b-4cbb-b5c1-6c662f4a8723.png)</br>

![alt text](../images/MobieNetV2_predictions/ec836a26-e5f3-4e07-81ca-9cedb60bdee8.png)






### ResNet50
Employing transfer learning with the ResNet50 model enables us to exploit pre-trained weights, significantly reducing the training time required for image classification tasks. This approach is particularly advantageous when dealing with limited training data, as we can leverage the rich representations learned by the base model from a vast dataset like ImageNet.

**Reason for choosing :-** 
 Relatively lightweight (98 MB) , High Accuracy (92.1 % Top 5 accuracy), Moderate Parameters (25.6M) , Reasonable Inference Speed on GPU (CPU - 32.1, GPU - 4.7)

Visualization of Predicted Labels on test set :- </br>
![alt text](../images/Resnet50_predictions/322db5d3-7d52-4f54-8268-bea5d55feaf8.png)</br>
![alt text](../images/Resnet50_predictions/3aa5211a-80d4-45f7-9f93-7fa4f32c1a71.png)</br>
![alt text](../images/Resnet50_predictions/592f11ba-fb41-44e6-bd5e-b26f4ee3b34a.png)</br>
![alt text](../images/Resnet50_predictions/62cf99c4-c8a4-4331-a4ad-607adc532d87.png)</br>

![alt text](../images/Resnet50_predictions/653173c2-ef01-4fba-bb58-78e740dd71b5.png)</br>

![alt text](../images/Resnet50_predictions/dbde1cae-6337-4236-af24-65f557592867.png)</br>


### InceptionV3
When implementing the InceptionV3 model in code, we leverage its powerful architecture to enhance our image classification tasks. By loading the pre-trained InceptionV3 model with weights from the ImageNet dataset, we benefit from its extensive knowledge. 

**Reason for choosing :-** 
lightweighted (92 MB) , better accuracy , less parameters (23.9M) , less inference speed (CPU - 42.2 , GPU - 6.9)

Visualization of Predicted Labels on test set :- </br>
![alt text](../images/InceptionV3_predictions/014c8af8-227e-4d13-82e8-4d3c016c176a.png)</br>

![alt text](../images/InceptionV3_predictions/3493d4e5-7b47-40fd-b884-b78a89dbe05b.png)</br>
![alt text](../images/InceptionV3_predictions/8e9e4340-411d-46eb-9ad5-ab186f17b33b.png)</br>


![alt text](../images/InceptionV3_predictions/a0278af7-ad0c-49e7-b5c2-c38424b016a6.png)</br>
![alt text](../images/InceptionV3_predictions/d262930f-e7a6-47dd-afa1-6e79326090a2.png)</br>



![alt text](../images/InceptionV3_predictions/dc89f4e9-3240-4dc6-be77-cb9cba0f2a9d.png)</br>





## EfficientNetB0
When implementing the EfficientNetB0 model in code, we leverage its powerful architecture to enhance our image classification tasks. By loading the pre-trained EfficientNetB0 model with weights from the ImageNet dataset, we benefit from its extensive knowledge.

**Reason for choosing :-**
lightweighted (29 MB), better accuracy, less parameters (5.3M), less inference speed (CPU - 32.9 ms, GPU - 7.1 ms)

Visualization of Predicted Labels on test set :- </br>

![alt text](../images/EfficientNetB0_predictions/237b28b0-74e7-44cd-9190-a8e1c74583e6.png) </br>

![alt text](../images/EfficientNetB0_predictions/600e20be-02c2-4e34-afc5-8255fe7ceb0e.png)</br>
![alt text](../images/EfficientNetB0_predictions/e97f3a99-06ab-4091-a4cb-0c52e0f8e266.png)</br>
![alt text](../images/EfficientNetB0_predictions/edd61747-0a67-4e44-8ac8-575db0ed883b.png)</br>
![alt text](../images/EfficientNetB0_predictions/f0b4cc0c-bc35-4aef-b44b-9c83a2cf237c.png)</br>
![alt text](../images/EfficientNetB0_predictions/f932a305-059d-46a9-aa04-6b6df6b8bbe9.png)</br>


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

![alt text](../images/bar.png)


### Pie Chart :-
A pie chart illustrating the distribution of labels in the training dataset. The percentage value displayed on each segment indicates the relative frequency of each label category.

![alt text](../images/pie-chart.png)

### Image paths distribution :-
 Visualizes the distribution of top 20 image paths by label, displays unique values in categorical columns.


![alt text](../images/image_path_distribution.png)


## 📈 Performance of the Models based on the Accuracy Scores

| Models      |       Accuracy Scores|
|------------ |------------|
|Xception  |92% ( Validation Accuracy: 0.9221)|
|InceptionV3  | 88% (Validation Accuracy: 0.8810) |
|EfficienNetB0      | 52% (highest) (Validation Accuracy: 0.5205) |
|ResNet50  | 83% (Validation Accuracy: 0.8353) |
|MobileNetV2       | 89% (Validation Accuracy: 0.8875) |


## 📢 Conclusion

**According to the accuracy scores it can be concluded that Xception and MobileNetV2 were able to perform good on this dataset.**

 Even though on data analysis we found that the distribution of the dataset isn't consistent for all the classes.

## ✒️ Your Signature

Full name:- AaradhyaSingh                      
Github Id :- https://github.com/kyra-09  
Email ID :- aaradhyasinghgaur@gmail.com  
LinkdIn :- https://www.linkedin.com/in/aaradhya-singh-0b1927250/ </br>
Participant Role :- Contributor / GSSOC (Girl Script Summer of Code ) - 2024