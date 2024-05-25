# Disease Prediction and Prescription Suggestion

This project focuses on predicting diseases based on user-provided symptoms and suggesting appropriate prescriptions. The core components include a CatBoost classifier for disease prediction and an integration with OpenAI's language model (via LangChain) for generating prescription recommendations.

## Libraries Required

To run this project, ensure you have the following Python libraries installed:

    numpy
    pandas
    scikit-learn
    catboost
    langchain-openai
    langchain

## Algorithms Used

    Disease Prediction:
        Utilized the CatBoost classifier to predict diseases based on input symptoms.
    Prescription Suggestion:
        Integrated OpenAI's language model using LangChain to suggest prescriptions based on the predicted disease.

## About CatBoost

CatBoost is a powerful algorithm for gradient boosting on decision trees, developed by Yandex. It excels in various applications such as search engines, recommendation systems, personal assistants, self-driving cars, and weather prediction. Notably, it is also used by organizations like CERN, Cloudflare, and Careem.
Model Workflow

## The workflow of the model is as follows:

    Input: User provides symptoms.
    Prediction: Symptoms are fed into the CatBoost model to predict the disease.
    Prescription Generation: The predicted disease is passed to an OpenAI model via LangChain to generate prescription suggestions.

## Input

The input consists of 133 different symptoms. Users can input their symptoms to get a disease prediction.
![image](https://github.com/Kyouma45/ML-CaPsule/assets/67496078/0a402010-3ea1-414f-a7c8-e4ef4835d935)


## Target Diseases Type

The model can predict a variety of diseases based on the provided symptoms.
![image](https://github.com/Kyouma45/ML-CaPsule/assets/67496078/48d998cf-f043-4197-91c0-7e6776269a81)


## Results

The model achieved an accuracy score of over 97.6%, demonstrating high reliability in disease prediction.
![image](https://github.com/Kyouma45/ML-CaPsule/assets/67496078/7cac3ae9-171f-4a15-a1a7-699c12a80028)


## Final Output

The final output includes the predicted disease and a list of suggested prescriptions.
![image](https://github.com/Kyouma45/ML-CaPsule/assets/67496078/3a5a0b0b-aabb-43fc-9965-272d685072c3)


## How to Run the Project

### Clone the Repository:

    bash
    git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
    cd ML-CaPsule

### Install Dependencies:

    bash
    pip install -r requirements.txt

### Run the Model:

    jupyter lab ./Diseases_Prediction.ipynb

### Future Work

    Enhance Prediction Accuracy: Explore additional features and algorithms to improve accuracy.
    Expand Disease Coverage: Include more diseases for comprehensive coverage.
    User Interface: Develop a user-friendly interface for easier input and output interpretation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
