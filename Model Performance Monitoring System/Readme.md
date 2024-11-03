## Model Performance Monitoring System

### Introduction

The Model Performance Monitoring System is designed to ensure the continuous accuracy and reliability of deployed machine learning models. By monitoring key performance metrics and promptly alerting administrators of any significant changes or degradations in performance, this system helps maintain the quality of service provided by machine learning applications.

### Motivation

The motivation behind this system is rooted in the need to maintain model integrity and effectiveness in production environments. Ensuring that deployed models consistently meet performance standards is critical for providing reliable and accurate services to users.

### Key Components

**1. Model Performance Metrics**

The system monitors the following key performance metrics:

Accuracy
Precision
Recall
F1-score
Area Under the ROC Curve (AUC-ROC)
Root Mean Squared Error (RMSE)
Mean Absolute Error (MAE)

**2. Alerting Mechanism**

Administrators are alerted via email when the performance of a deployed model falls below acceptable thresholds for any of the monitored metrics. This immediate notification enables administrators to take timely actions to address issues and maintain model quality.



### Requirements

To use the Model Performance Monitoring System, the following requirements must be met:
- Python 3.x
- Libraries: pandas, scikit-learn, matplotlib, smtplib
- Installation and Configuration
- Clone the repository to your local machine.
- Install the required Python libraries using `pip install -r requirements.txt`.
Update the email credentials (sender_email, receiver_email, password) in Model_Performance_Monitoring_System.ipynb with your email details.
- Adjust the performance thresholds (threshold) in the code to align with your acceptable performance criteria.

### Usage
- Load your deployed machine learning model and data.
- Periodically run the Model_Performance_Monitoring_System.ipynb script to evaluate model performance and send alerts if necessary.
Example
- **An example dataset and code implementation are provided in the Model_Performance_Monitoring_System.ipynb script for reference. Customize the script according to your specific model and data.**