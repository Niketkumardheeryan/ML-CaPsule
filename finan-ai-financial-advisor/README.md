# 🌐 Live Web Application

### **Finan - AI Financial Advisor**

🔗 **[https://finan-ai-financial-advisor.onrender.com](https://finan-ai-financial-advisor.onrender.com)**

---

# Project Real Time Screen Recording

<video src="https://github.com/user-attachments/assets/c948476b-65f3-4bec-b683-51808127392b" width="100%" controls></video>



# 📌 Project Description

Finan - AI Financial Advisor is a full-stack AI-powered web application developed to provide personalized financial insights based on user income, expenditure patterns, debt status, and overall financial condition. The system combines traditional machine learning models with Large Language Model (LLM) capabilities to deliver financial predictions along with contextual explanations and guidance.

The project repository contains two major components:

* 📓 **Jupyter Notebook Version**

  * Contains documented model development and experimentation workflow.
  * Includes data preprocessing, feature engineering, model training, and evaluation.

* 🌐 **Full-Stack Web Application**

  * Integrates trained machine learning models with an interactive web interface.
  * Provides authentication, cloud storage, and AI-generated explanations through Gemini.

---

# 🚀 Features

### 💬 AI-Powered Financial Assistant

* Generates personalized financial advice and explanations.
* Provides context-aware recommendations instead of only displaying predictions.
* Uses Google Gemini to enhance interpretability of model outputs.

### 📊 Financial State Classification

* Predicts the user's overall financial condition using a **Support Vector Classifier (SVC)**.
* Classification is based on features such as:

  * Monthly income
  * Cost of living expenditure
  * Investment expenditure
  * Consumerist spending
  * Crisis-related expenses
  * Debt status

### 💰 Monthly Budget Prediction

* Uses a **Random Forest Regressor** to estimate suitable monthly budget allocations.
* Helps users understand spending patterns and maintain financial balance.

### 🇮🇳 Indian Finance-Oriented Dataset

* Models are trained on an Indian financial dataset representing realistic economic scenarios.
* Captures diverse financial behaviors and spending patterns.

### 🔐 User Authentication

* Secure account registration and login through Firebase Authentication.

### ☁️ Cloud-Based Storage

* Firebase Cloud Storage integration for storing application assets and supporting resources.

### 🌐 Browser-Based Accessibility

* Responsive web interface accessible without local installation.
* Deployed on Render for public access.

---

# 🧠 Machine Learning Components

## 📈 Financial State Prediction Model

### Model Used

* **Support Vector Classifier (SVC)**

### Purpose

Classifies users into financial categories based on their income and expenditure characteristics.

### Input Parameters

* Monthly income
* Essential living expenses
* Investment expenditure
* Consumer expenditure
* Crisis expenditure
* Debt status

### Objective

Provide an understanding of a user's current financial condition and spending behavior.

---

## 💵 Monthly Budget Estimation Model

### Model Used

* **Random Forest Regressor**

### Purpose

Predicts a recommended monthly budget based on user financial attributes.

### Objective

Assist users in planning and managing expenditures more effectively.

---

# 🏗️ Tech Stack

## 🐍 Backend

* Python
* Flask

### Flask Responsibilities

* API handling
* Server-side routing
* Model inference
* Integration with Gemini API
* Authentication workflow support

---

## 🤖 Artificial Intelligence & Machine Learning

* Scikit-learn
* Support Vector Classifier (SVC)
* Random Forest Regressor
* Google Gemini API

---

## 🔥 Firebase Services

### Firebase Authentication

* Email-based authentication
* Secure user identity management

### Firebase Cloud Storage

* Cloud-hosted storage for application resources

---

## 🎨 Frontend

* HTML5
* CSS3
* JavaScript

---

## ☁️ Deployment

* Render Cloud Platform

---

# 📓 Jupyter Notebook Module

The repository includes a notebook-based implementation containing:

### 🧪 Data Preparation

* Data cleaning
* Feature engineering
* Encoding and preprocessing

### 📈 Model Training

* Support Vector Classifier (SVC)
* Random Forest Regressor

### 📊 Model Evaluation

* Training workflow documentation
* Performance analysis
* Reproducible experimentation pipeline

### 📚 Educational Purpose

* Allows contributors to understand model development and training procedures.
* Provides transparency for experimentation and further improvements.

---

# 🔒 Security Features

## 🛡️ Firebase Authentication Security

* Secure login and registration mechanism.
* Authentication handled through Firebase services.

---

## 🔑 Firebase API Key Restrictions

* Firebase API keys are restricted through **Google Cloud Console**.
* Prevents unauthorized access and misuse.
* Improves production-level security.

---

## 🔐 Secure Gemini API Key Management

* Gemini API credentials are **not hardcoded**.
* Sensitive keys are stored securely using **Render Environment Variables**.
* Keeps secrets separated from the application source code.

---

## 🚫 Secret Isolation

* Configuration and credentials remain external to codebase.
* Reduces risk of accidental exposure during development and deployment.

---

# 🇮🇳 Dataset Characteristics

The machine learning models are trained using an Indian finance dataset designed to represent practical financial situations involving:

* Monthly income levels
* Cost of living expenditure
* Investment expenses
* Consumer spending behavior
* Crisis and emergency expenses
* Debt conditions

The dataset captures multiple financial categories such as:

* 📈 High-Rate Savers
* 💹 Low-Rate Savers
* ⚖️ Balanced Financial States
* 💳 Debt-Driven Financial Conditions
* 📉 Zero-Balance / Deficit Living States

---

# 🎨 User Interface Symbolism

### 🌱 Financial Growth and Stability

The interface design emphasizes gradual financial improvement and responsible money management.

---

### 🤖 AI-Based Financial Guidance

The conversational layout represents an intelligent virtual financial assistant capable of translating machine learning predictions into understandable insights.

---

### ⚖️ Balance Between Spending and Saving

The UI reflects the relationship between:

* Income generation
* Essential expenditure
* Investment habits
* Consumer spending patterns
* Debt management

These factors collectively correspond to the features used by the underlying machine learning models.

---

### 📊 Data-Driven Decision Making

Visual elements are intended to communicate:

* Financial awareness
* Structured budgeting
* Sustainable expenditure patterns
* Long-term financial planning

---

# ⚙️ Architecture Highlights

* 📓 Documented notebook implementation for reproducible model development.
* 🌐 Full-stack Flask-based web application.
* 📈 SVC model for financial state classification.
* 💰 Random Forest Regressor for monthly budget prediction.
* 🤖 Gemini-powered explanation layer.
* 🔥 Firebase Authentication and Cloud Storage integration.
* 🔒 Google Cloud API restrictions for Firebase security.
* ☁️ Secure secret management through Render environment variables.
* 🚀 Public deployment on Render.

---

# 🎯 Project Objective

To develop a secure and accessible AI-assisted financial advisory platform that combines **machine learning, generative AI, and cloud technologies** to help users better understand their financial condition, estimate budgets, and make informed financial decisions based on Indian economic and spending patterns.
