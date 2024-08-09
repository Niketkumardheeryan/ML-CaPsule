# Pharmaceutical Drugs and Vitamins Images Detection

## 🎯 Goal
The main purpose of this project is to **identify and classify between different pharmaceutical drugs and vitamins** from the dataset (mentioned below) using various image detection/recognition models and comparing their accuracy.

## 🧵 Dataset

The link to the dataset is given below :-

**Link :- https://www.kaggle.com/datasets/vencerlanz09/pharmaceutical-drugs-and-vitamins-dataset-v2**

## 🧾 Description

This project involves the comparative analysis of **Five** Keras image detection models, namely **MobileNet** , **ResNet50V2** , **InceptionV3** , **DenseNet121** and **Xception**  applied to a specific dataset. The dataset consists of annotated images related to a particular domain, and the objectives include training and evaluating these models to compare their accuracy scores and performance metrics. Additionally, exploratory data analysis (EDA) techniques are employed to understand the dataset's characteristics, explore class distributions, detect imbalances, and identify areas for potential improvement. The methodology encompasses data preparation, model training, evaluation, comparative analysis of accuracy and performance metrics, and visualization of EDA insights. 

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

![alt text](../Images/Xception_predictions/1c85d549-30b2-4d7d-b720-85eb84ab1644.png)</br>

![alt text](../Images/Xception_predictions/773ea5a9-7573-4057-968e-4fa8926af4cb.png)</br>

![alt text](../Images/Xception_predictions/976ab080-7145-4f37-aa6a-73713f8a6a9e.png)</br>

![alt text](../Images/Xception_predictions/ed06fe5c-e8a8-42d4-8d38-11da2ac72202.png)



### MobileNet

Incorporating the MobileNet model into our codebase brings a wealth of advantages to our image processing workflows. By initializing the pre-trained MobileNet model with weights from the ImageNet dataset, we tap into its profound understanding of visual data.

**Reasons for selecting MobileNet:**
- Lightweight Architecture (MobileNet's efficient design allows for rapid processing with fewer computational resources.)
- Proven Accuracy (MobileNet consistently performs well in various image recognition benchmarks.)
- Efficient Parameters (4.2M)
- High Efficiency (CPU - 10, GPU - 1.3)

Visualization of Predicted Labels on test set :- </br>

![alt text](../Images/MobileNet_predictions/18b4bf42-2e21-4cd3-afc3-e7c672422e6e.png)</br>

![alt text](../Images/MobileNet_predictions/20fd282c-2edc-48ce-8a52-c7d87a5089cb.png)</br>

![alt text](../Images/MobileNet_predictions/982a84ee-788a-4bb2-89d5-4304a8a56eac.png)</br>

![alt text](../Images/MobileNet_predictions/c35dcb78-6440-4864-98a6-3a2ea4cebb1b.png)





### ResNet50V2

Implementing transfer learning with the ResNet50V2 model allows us to benefit from pre-trained weights, significantly reducing the training duration necessary for image classification tasks. This strategy is particularly advantageous when dealing with limited training data, as we can leverage the comprehensive representations learned by the base model from extensive datasets like ImageNet.

**Reasons for opting for ResNet50V2:** Relatively lightweight (98 MB) , High Accuracy (92.1 % Top 5 accuracy), Moderate Parameters (25.6M) , Reasonable Inference Speed on GPU (CPU - 32.1, GPU - 4.7)

Visualization of Predicted Labels on test set :- </br>

![alt text](../Images/Resnet50V2_predictions/13e67132-466a-472b-877e-0ed951a2809e.png)</br>

![alt text](../Images/Resnet50V2_predictions/2d50be9e-1915-43a9-87ec-486c5d8c8ef5.png)</br>

![alt text](../Images/Resnet50V2_predictions/3581db0f-bd7f-46d5-a93e-d47baced07bd.png)</br>

![alt text](../Images/Resnet50V2_predictions/eb57435f-2201-4f0b-98da-b790e13750a6.png)



### InceptionV3
When implementing the InceptionV3 model in code, we leverage its powerful architecture to enhance our image classification tasks. By loading the pre-trained InceptionV3 model with weights from the ImageNet dataset, we benefit from its extensive knowledge. 

**Reason for choosing :-** 
lightweighted (92 MB) , better accuracy , less parameters (23.9M) , less inference speed (CPU - 42.2 , GPU - 6.9)

Visualization of Predicted Labels on test set :- </br>
![alt text](../Images/InceptionV3_predictions/02509165-66d3-4164-8f0d-1c6a8b57536a.png)</br>

![alt text](../Images/InceptionV3_predictions/385088f1-0165-4ede-a392-c686b0904e29.png)</br>

![alt text](../Images/InceptionV3_predictions/856f6215-1ccf-421a-be41-bdc7817b1590.png)</br>

![alt text](../Images/InceptionV3_predictions/dd0bc14e-65d1-4726-979e-e89d2386a6eb.png)





### DenseNet121

When implementing the DenseNet121 model in code, we leverage its densely connected architecture to enhance our image classification tasks. By loading the pre-trained DenseNet121 model with weights from the ImageNet dataset, we benefit from its extensive knowledge.

**Reason for choosing:** Lightweight (33 MB)
, High accuracy , Moderate number of parameters (8M) , Efficient inference speed (CPU - ~45 ms, GPU - ~10 ms).

Visualization of Predicted Labels on test set :- </br>
![alt text](../Images/DenseNet121/87918c94-5dc8-410e-94f0-fd1f8d08ebff.png)</br>

![alt text](../Images/DenseNet121/992a7274-9ea6-4757-ad0a-7c4e41805fae.png)</br>

![alt text](../Images/DenseNet121/dfb74364-4379-4131-ae23-73e3c5e80d06.png)</br>

![alt text](../Images/DenseNet121/f508171e-a64c-4b62-b1ed-9ce1fddb74c6.png)

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


![alt text](../Images/bar.png)</br>

### Pie Chart :-
A pie chart illustrating the distribution of labels in the training dataset. The percentage value displayed on each segment indicates the relative frequency of each label category.

![alt text](../Images/pie_chart.png)</br>

### Image paths distribution :-
 Visualizes the distribution of top 20 image paths by label, displays unique values in categorical columns.

![alt text](../Images/image_path_distribution.png)</br>


## 📈 Performance of the Models based on the Accuracy Scores

| Models      |       Accuracy Scores|
|------------ |------------|
|Xception  |97% ( Validation Accuracy:0.9750)|
|InceptionV3  | 97% (Validation Accuracy: 0.9690) |
|DenseNet121     | 98% (Validation Accuracy:0.9840) |
|ResNet50V2  | 95% (Validation Accuracy:0.9510) |
|MobileNet    | 94% (Validation Accuracy: 0.9480) |


## 📢 Conclusion

**According to the accuracy scores it can be concluded that DenseNet121 and Xception were able to perform good on this dataset.**

Even though I haven't trained the models on entire dataset because of computational restraints . I only trained the models on 25% of the dataset. 

## ✒️ Your Signature

Full name:-Aaradhya Singh                      
Github Id :- https://github.com/kyra-09  
Email ID :- aaradhyasinghgaur@gmail.com  
LinkdIn :- https://www.linkedin.com/in/aaradhya-singh-0b1927250/ </br>
Participant Role :- Contributor / GSSOC (Girl Script Summer of Code ) - 2024