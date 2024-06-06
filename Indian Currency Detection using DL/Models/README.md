# Indian Currency Detection and Recognition

## 🎯 Goal
The main purpose of this project is to **classify 7 different indian currencies** from the dataset (mentioned below) using various image detection/recognition models and comparing their accuracy.

## 🧵 Dataset

The link to the dataset is given below :-

**Link :- https://www.kaggle.com/datasets/shobhit18th/indian-currency-notes**

## 🧾 Description

This project involves the comparative analysis of **Five** Keras image detection models, namely **NASNetMobile** , **ResNet50V2** , **InceptionV3** , **DenseNet121** and **Xception**  applied to a specific dataset. The dataset consists of annotated images related to a particular domain, and the objectives include training and evaluating these models to compare their accuracy scores and performance metrics. Additionally, exploratory data analysis (EDA) techniques are employed to understand the dataset's characteristics, explore class distributions, detect imbalances, and identify areas for potential improvement. The methodology encompasses data preparation, model training, evaluation, comparative analysis of accuracy and performance metrics, and visualization of EDA insights. 

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

![alt text](../Images/Xception_predictions/1ee80672-8bf2-4946-a8c4-0c742949ae70.png)</br>

![alt text](../Images/Xception_predictions/5ddb2db6-6493-472e-9fb2-3510b6e214a2.png)</br>

![alt text](../Images/Xception_predictions/85aaddd6-dd79-42ad-b209-33f89cc5ff18.png)



### NASNetMobile

Incorporating the NASNetMobile model into our codebase brings a wealth of advantages to our image processing workflows. By initializing the pre-trained NASNetMobile model with weights from the ImageNet dataset, we tap into its profound understanding of visual data.

**Reasons for selecting NASNetMobile:** Lightweight (22 MB) ,
**Outstanding Accuracy (NASNetMobile demonstrates superior accuracy in various image-related tasks .)** ,
Reduced Parameters (5.3M) ,
Enhanced Inference Speed (CPU - 55.1, GPU - 10.3)

Visualization of Predicted Labels on test set :- </br>
![alt text](../Images/NASNetMobile_predictions/28cea739-a49a-452d-8796-6d3069780991.png)</br>

![alt text](../Images/NASNetMobile_predictions/2e4cba78-0b17-4c85-9ee0-7bdd3522b9d1.png)</br>

![alt text](../Images/NASNetMobile_predictions/df1812d9-3e50-4de0-9024-af9d2f54d16e.png)




### ResNet50V2

Implementing transfer learning with the ResNet50V2 model allows us to benefit from pre-trained weights, significantly reducing the training duration necessary for image classification tasks. This strategy is particularly advantageous when dealing with limited training data, as we can leverage the comprehensive representations learned by the base model from extensive datasets like ImageNet.

**Reasons for opting for ResNet50V2:** Relatively lightweight (98 MB) , High Accuracy (92.1 % Top 5 accuracy), Moderate Parameters (25.6M) , Reasonable Inference Speed on GPU (CPU - 32.1, GPU - 4.7)

Visualization of Predicted Labels on test set :- </br>
![alt text](../Images/Resnet50V2_predictions/7cf8ba06-bb9e-4f23-9e39-c59923f3f300.png)</br>

![alt text](../Images/Resnet50V2_predictions/994bb09c-443a-4f94-a2b2-8457e0875228.png)</br>

![alt text](../Images/Resnet50V2_predictions/ce0ab66b-583d-4966-8848-bbe2032d5060.png)




### InceptionV3
When implementing the InceptionV3 model in code, we leverage its powerful architecture to enhance our image classification tasks. By loading the pre-trained InceptionV3 model with weights from the ImageNet dataset, we benefit from its extensive knowledge. 

**Reason for choosing :-** 
lightweighted (92 MB) , better accuracy , less parameters (23.9M) , less inference speed (CPU - 42.2 , GPU - 6.9)

Visualization of Predicted Labels on test set :- </br>
![alt text](../Images/InceptionV3_predictions/32abcdf1-3a32-4a63-97ae-2500dee9bbb3.png)</br>

![alt text](../Images/InceptionV3_predictions/72d2062d-41f0-4455-9607-f437b4362a51.png)</br>

![alt text](../Images/InceptionV3_predictions/988c3a1f-cd99-4d61-b395-0b2617891bea.png)


### DenseNet121

When implementing the DenseNet121 model in code, we leverage its densely connected architecture to enhance our image classification tasks. By loading the pre-trained DenseNet121 model with weights from the ImageNet dataset, we benefit from its extensive knowledge.

**Reason for choosing:** Lightweight (33 MB)
, High accuracy , Moderate number of parameters (8M) , Efficient inference speed (CPU - ~45 ms, GPU - ~10 ms).

Visualization of Predicted Labels on test set :- </br>

![alt text](../Images/DenseNet121/09ec2435-528f-467a-886c-5a6c563778c0.png)</br>

![alt text](../Images/DenseNet121/1aeba4fe-e49c-4f98-a78c-863e9105a6a8.png)</br>

![alt text](../Images/DenseNet121/43981767-5776-4649-bc6e-bee34ffac39c.png)

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

![alt text](../Images/bar.png)


### Pie Chart :-
A pie chart illustrating the distribution of labels in the training dataset. The percentage value displayed on each segment indicates the relative frequency of each label category.

![alt text](../Images/pie.png)

### Image paths distribution :-
 Visualizes the distribution of top 20 image paths by label, displays unique values in categorical columns.

![alt text](../Images/image_path.png)



## 📈 Performance of the Models based on the Accuracy Scores

| Models      |       Accuracy Scores|
|------------ |------------|
|Xception  |98% ( Validation Accuracy: 0.9831)|
|InceptionV3  | 97% (Validation Accuracy: 0.9661) |
|DenseNet121     | 98% (Validation Accuracy:0.9831) |
|ResNet50V2  | 90% (Validation Accuracy: 0.8983) |
|NASNetMobile       | 53% (Validation Accuracy:  0.5254) |


## 📢 Conclusion

**According to the accuracy scores it can be concluded that  DenseNet121 , Xception and InceptionV3 were able to perform good on this dataset.**

Even though most of  the models implemented above are giving above 90% accuracy which is great when it comes to image recognition.

## ✒️ Your Signature

Full name:- AaradhyaSingh                      
Github Id :- https://github.com/kyra-09  
Email ID :- aaradhyasinghgaur@gmail.com  
LinkdIn :- https://www.linkedin.com/in/aaradhya-singh-0b1927250/ </br>
Participant Role :- Contributor / GSSOC (Girl Script Summer of Code ) - 2024