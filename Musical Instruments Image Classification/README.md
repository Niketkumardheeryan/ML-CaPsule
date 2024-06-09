# Musical Instrument Image Classification

## 🎯 Goal
The main purpose of this project is to **classify 30 different musical instruments** from the dataset (mentioned below) using various image detection/recognition models and comparing their accuracy.

## 🧵 Dataset

The link to the dataset is given below :-

**Link :- https://www.kaggle.com/datasets/gpiosenka/musical-instruments-image-classification/data**

## 🧾 Description

This project involves the comparative analysis of **Five** Keras image detection models, namely **MobileNetV2** , **ResNet50** , **InceptionV3** , **DenseNet121** and **Xception**  applied to a specific dataset. The dataset consists of annotated images related to a particular domain, and the objectives include training and evaluating these models to compare their accuracy scores and performance metrics. Additionally, exploratory data analysis (EDA) techniques are employed to understand the dataset's characteristics, explore class distributions, detect imbalances, and identify areas for potential improvement. The methodology encompasses data preparation, model training, evaluation, comparative analysis of accuracy and performance metrics, and visualization of EDA insights. 

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
![alt text](../Images/Xception_predictions/46c54f60-7b66-4832-91bb-f61b5a7d9d35.png)</br>

![alt text](../Images/Xception_predictions/548cbfd4-cfc5-4624-a1fd-56940fe4de42.png)</br>

![alt text](../Images/Xception_predictions/710085b6-de7a-4d6d-a0a8-6aa8bfec79ee.png)</br>

![alt text](../Images/Xception_predictions/908b04ed-6901-4914-9a05-eb1e89b9bd3f.png)


### MobileNetV2
Utilizing transfer learning with the MobileNetV2 model allows us to leverage pre-trained weights, drastically reducing the training time needed for image classification tasks. This strategy is especially beneficial when working with limited training data, as we can capitalize on the comprehensive representations learned by the base model from a vast dataset such as ImageNet.

**Reason for choosing :-** 
 Very lightweighted (14 MB) , better accuracy, very less parameters (3.5M) , less inference speed when using GPU (CPU - 25.9, GPU - 3.8)

Visualization of Predicted Labels on test set :- </br>

![alt text](../Images/MobieNetV2_predictions/28ea1412-a0da-4f29-b523-223265ed705a.png)</br>

![alt text](../Images/MobieNetV2_predictions/9695b7e0-c79e-4ec9-b372-3a91ec298193.png)</br>

![alt text](../Images/MobieNetV2_predictions/b4174a2a-2a10-48dd-8469-fd9c5d4ec262.png)</br>

![alt text](../Images/MobieNetV2_predictions/c7cf489d-52e4-456c-99da-b8a14bce2d89.png)


### ResNet50
Employing transfer learning with the ResNet50 model enables us to exploit pre-trained weights, significantly reducing the training time required for image classification tasks. This approach is particularly advantageous when dealing with limited training data, as we can leverage the rich representations learned by the base model from a vast dataset like ImageNet.

**Reason for choosing :-** 
 Relatively lightweight (98 MB) , High Accuracy (92.1 % Top 5 accuracy), Moderate Parameters (25.6M) , Reasonable Inference Speed on GPU (CPU - 32.1, GPU - 4.7)

Visualization of Predicted Labels on test set :- </br>
![alt text](../Images/Resnet50_predictions/0c0c4726-6f70-42c2-8156-2f5821018649.png)</br>

![alt text](../Images/Resnet50_predictions/47bf42e1-5b24-467c-9126-7f449f2ea3e0.png)</br>

![alt text](../Images/Resnet50_predictions/9dd5c405-dfb9-4be8-9eee-1a84d7fa249f.png)</br>

![alt text](../Images/Resnet50_predictions/a13e7cbc-72f0-40bc-83e2-891b6970bded.png)



### InceptionV3
When implementing the InceptionV3 model in code, we leverage its powerful architecture to enhance our image classification tasks. By loading the pre-trained InceptionV3 model with weights from the ImageNet dataset, we benefit from its extensive knowledge. 

**Reason for choosing :-** 
lightweighted (92 MB) , better accuracy , less parameters (23.9M) , less inference speed (CPU - 42.2 , GPU - 6.9)

Visualization of Predicted Labels on test set :- </br>
![alt text](../Images/InceptionV3_predictions/0715d283-e319-4c0c-9f93-5f2b7eb53ccc.png)</br>

![alt text](../Images/InceptionV3_predictions/9b31cde2-cb09-407f-87e7-4dc298027641.png)</br>

![alt text](../Images/InceptionV3_predictions/b7ad3e1a-70d2-4537-8a96-0b2ac5d8f8f8.png)</br>

![alt text](../Images/InceptionV3_predictions/e9b43bfd-9715-437d-ba47-89e0ba7f7011.png)

### DenseNet121

When implementing the DenseNet121 model in code, we leverage its densely connected architecture to enhance our image classification tasks. By loading the pre-trained DenseNet121 model with weights from the ImageNet dataset, we benefit from its extensive knowledge.

**Reason for choosing:** Lightweight (33 MB)
, High accuracy , Moderate number of parameters (8M) , Efficient inference speed (CPU - ~45 ms, GPU - ~10 ms).

Visualization of Predicted Labels on test set :- </br>
![alt text](../Images/DenseNet121/405a7263-2e26-4e0a-b6e0-d383d74acb08.png)</br>

![alt text](../Images/DenseNet121/48d6a85a-8274-4b0e-b327-65da5424b4b6.png)</br>

![alt text](../Images/DenseNet121/4b0bb137-90bd-4ffc-8c23-496c2c1eb088.png)</br>

![alt text](../Images/DenseNet121/8a11f5b7-4004-49b0-8a51-e552ddd91719.png)


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

![alt text](../Images/pie_chart.png)

### Image paths distribution :-
 Visualizes the distribution of top 20 image paths by label, displays unique values in categorical columns.

![alt text](../Images/path_distribution.png)

## 📈 Performance of the Models based on the Accuracy Scores

| Models      |       Accuracy Scores|
|------------ |------------|
|Xception  |95% ( Validation Accuracy: 0.9475)|
|InceptionV3  | 94% (Validation Accuracy: 0.9374) |
|DenseNet121     | 95% (Validation Accuracy:0.9495) |
|ResNet50  | 91% (Validation Accuracy: 0.9111) |
|MobileNetV2       | 95% (Validation Accuracy:  0.9495) |


## 📢 Conclusion

**According to the accuracy scores it can be concluded that MobileNetV2 , DenseNet121 and Xception were able to perform good on this dataset.**

Even though all the models implemented above are giving above 90% accuracy which is great when it comes to image recognition.

## ✒️ Your Signature

Full name:- AaradhyaSingh                      
Github Id :- https://github.com/kyra-09  
Email ID :- aaradhyasinghgaur@gmail.com  
LinkdIn :- https://www.linkedin.com/in/aaradhya-singh-0b1927250/ </br>
Participant Role :- Contributor / GSSOC (Girl Script Summer of Code ) - 2024