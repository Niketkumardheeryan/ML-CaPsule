# Aim
Internet is frequently used by criminals for illegal activities, such as financial fraud, phishing, online gambling, fake TV shopping, fraudulent prize-winning, and spam SMS in social networks so detection of malicious URL is a major concern so the main objective of this project is to develop a machine learning model to detect whether the URL is malicious or benign.

# Introduction
Malicious URL detection is of great interest nowadays. There have been several scientific studies showing a number of methods to detect malicious URLs based on machine learning and deep learning techniques. In this project malicious URL detection method using machine learning techniques based on our proposed URL behaviors and attributes. In short, the proposed detection system consists of a new set of URLs features and behaviors, a machine learning algorithm. The experimental results show that the proposed URL attributes and behavior can help improve the ability to detect malicious URL significantly. This is suggested that the proposed system may be considered as an optimized and friendly used solution for malicious URL detection.
The malicious URLs can be detected using the lexical features along with tokenization of the URL strings. In this project, I have built a basic binary classifier that would help classify the URLs as malicious or benign.

# Experimentation 
Steps followed in building the machine learning classifier
- Data Preprocessing / Feature Engineering
- Data Visualization
- Building Machine Learning Models using Lexical Features.

# Required Libraries 
- Numpy - NumPy is a Python library used for working with arrays.
- Pandas - Pandas is a Python library for data analysis.
- Matplotlib - Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
- Seaborn - Seaborn is a data visualization library built on top of matplotlib and closely integrated with pandas data structures in Python.
- OS - The OS module in Python provides functions for creating and removing a directory (folder).

# Dataset 
![image](https://user-images.githubusercontent.com/69976168/169657483-34c40ac4-df81-4e9c-a135-da6f5427eb2f.png)

# Result 
I have used  two models for my classification.
- Decision Trees
- Random Forest
- Decision tree is the most powerful and popular tool for classification and prediction. A Decision tree is a flowchart-like tree structure, where each internal node denotes a test on an attribute, each branch represents an outcome of the test, and each leaf node (terminal node) holds a class label.
Random Forest is a classifier that contains a number of decision trees on various subsets of the given dataset and takes the average to improve the predictive accuracy of that dataset.

![image](https://user-images.githubusercontent.com/69976168/169657540-ffbfdd9c-dd33-4252-9676-6f67b9972f3b.png)

