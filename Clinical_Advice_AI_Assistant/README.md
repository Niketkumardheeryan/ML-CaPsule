Clinical Advice AI Assistant

Problem Statement:
Sometimes, patients are not able to get clinical advice (regarding diagnosis, required medical tests, medicine) on time due to doctor's unavailability.

Solution:
A Clinical Advice AI Assistant that gives diagnosis and advice to patients based on their symptoms, medical test results, medical history, and lifestyle factors. It also asks the patient to consult medical professional if needed. This would provide clinical advice to patients on their fingertips.

Tech Stack:
Pandas: For Obtaining Dataframes of Training Dataset
Scikit-learn: For Machine learning (model training and disease prediction)
Langextract: For Extracting Information From User Medical Query Prompts and then Create Corresponding Test Dataset
Google-genai: For Generating Text Response Containing Medical Advice For User

Approach:
1. Train ML Model (Random Forest Classifier) for Learning on Disease Dataset
2. Input User Medical Query 
3. Extract Key Information from User Query using Langextract
4. Create Corresponding Test Dataset by Adding Extracted Information into a Dataframe
5. Predict Possible Disease through Trained ML Model
6. Generate Medical Response for User using Gemini API

File Description:
Clinical Advice Model.ipynb: Jupyter Notebook containing code for this feature
User Prompt Parameters.csv: CSV file containing training data for understanding user’s medical condition
Model Response Parameters.csv: CSV file containing training data on diagnosis, cause, and treatment of disease

Hope you find this feature interesting.
Looking forward to feedback from mentors and maintainers for GSSoC’26!
