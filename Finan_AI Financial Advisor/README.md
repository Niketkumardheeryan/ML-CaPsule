Problem Statement:
In India, living in metropolitan cities, big dreams, even FOMO or lack of financial literacy– there can be so many reasons because of which people suffer in managing their finances and then end up in financial crisis like debt trap, bankruptcy etc, leading to compromised financial security in future, or even hand-to-mouth situation.

Solution:

Finan – AI Financial Advisor
An AI-Powered Financial Advisor that informs user about their current financial status (based on monthly income, expenditure and debt status). It also advices user on how to enhance their finance management skills and upgrade their financial status.

X-factor: Model would be trained according to Indian economic landscape. Financial status prediction and financial advice would be useful for Indian users.

Tech Stack:
Pandas: For converting finance dataset into Dataframe
Scikit-learn: For ML Model training and predictions
Langextract: For extracting info from user financial query
Google-genai: For providing financial guidance to user using Gemini API

Approach:
1. Train SVC Model to predict Financial State Category, Current Monthly Income Sufficiency and Worth of Current Expenditure
2. Train Random Forest Regressor Model to predict Suggested Monthly Budget
3. Extract info from User Query using Langextract
4. Predict Financial State Category, Current Monthly Income Sufficiency, Worth of Current Expenditure and Suggested Monthly Budget
5. Provide all info to Gemini APi Client to generate text response containing financial advice for user.

File Description:
Finan_AI Financial Advisor.ipynb: Jupyter Notebook containing code
indian_finance_ml_dataset_balanced_final (1).csv: Finance Dataset CSV File
README.md: Contains Feature Description

Hope you find this interesting!
Looking forward to your valuable feedback!