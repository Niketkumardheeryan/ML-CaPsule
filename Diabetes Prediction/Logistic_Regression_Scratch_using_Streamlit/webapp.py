import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import kagglehub
import os


# Load dataset using KaggleHub
path = kagglehub.dataset_download("diabetes_binary_5050split_health_indicators_BRFSS2015.csv")

csv_file = None

for file in os.listdir(path):
    if file.endswith(".csv"):
        csv_file = os.path.join(path, file)
        break

if csv_file is None:
    st.error("CSV file not found in dataset")
    st.stop()

data = pd.read_csv(csv_file)


st.title("Diabetes predictor")

nav = st.sidebar.radio("Navigation", ["Home", "Prediction"])


if nav == "Home":

    st.write("Home")
    st.image("diab.jpg", width=800)

    if st.checkbox("Show table"):
        st.table(data.sample(10))
    
    graph = st.selectbox(
        "Would you like to see a graph",
        ["No", "Yes"]
    )

    if graph == "Yes":

        plt.figure(figsize=(10,5))
        plt.scatter(data["BMI"], data["Diabetes_binary"])
        plt.ylim(0)
        plt.xlabel("BMI")
        plt.ylabel("Diabetes")
        plt.tight_layout()

        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


        plt.pcolormesh(data.sample(20), cmap='winter')
        plt.title('2-D Heat Map')
        plt.show()

        st.pyplot()


def sigmoid(z):
    '''Compute sigmoid function'''
    sig = 1/(1+np.exp(-z))
    
    return sig



def predict(w,b,x_test):

    m = x_test.shape[1]

    y_prediction = np.zeros((1,m))

    w = w.reshape(x_test.shape[0],1)

    A = sigmoid(np.dot(w.T,x_test)+b)


    for i in range(A.shape[1]):

        if A[0,i] >= 0.75:
            y_prediction[0,i] = 1

        else:
            y_prediction[0,i] = 0
   
    return y_prediction



f1 = open("model_parameters.txt","r")

para = f1.read()

parameters = eval(para)

w = parameters["w"]

b = parameters["b"]



if nav == "Prediction":

    st.subheader("Predict")


    HighBP = st.selectbox(
        "Do you have high BP?",
        ["Yes","No"]
    )

    HighBP = 1 if HighBP=="Yes" else 0



    HighChol = st.selectbox(
        "Do you have high cholestrol",
        ["Yes","No"]
    )

    HighChol = 1 if HighChol=="Yes" else 0



    Cholcheck = st.selectbox(
        "Have you had a cholestrol check in the last five years",
        ['Yes','No']
    )

    Cholcheck = 1 if Cholcheck=="Yes" else 0



    BMI = st.number_input(
        "Enter your BMI",
        0,
       50
    )


    smoke = st.selectbox(
        "Do you smoke",
        ["Yes",'No']
    )

    smoke = 1 if smoke=="Yes" else 0



    stroke = st.selectbox(
        "Ever had a stroke",
        ['Yes',"No"]
    )

    stroke = 1 if stroke=="Yes" else 0



    HrDis = st.selectbox(
        "Had a heart attack or suffer from heart conditions",
        ["Yes",'No']
    )

    HrDis = 1 if HrDis=="Yes" else 0



    Physact = st.selectbox(
        "Do you get regular exercise in the last 30 days",
        ['Yes','No']
    )

    Physact = 1 if Physact=="Yes" else 0



    Fruits = st.selectbox(
        "Do you have one or more fruits in a day",
        ['Yes','No']
    )

    Fruits = 1 if Fruits=="Yes" else 0



    Veggies = st.selectbox(
        "Do you have one or more vegetables in a day",
        ['Yes','No']
    )

    Veggies = 1 if Veggies=="Yes" else 0



    Alc = st.selectbox(
        "Do you consume more than 14 drinks in a week (for men) and 7 drinks a week(for women)",
        ["Yes","No"]
    )

    Alc = 1 if Alc=="Yes" else 0



    AnyHealthcare = st.selectbox(
        "Do you have health care access",
        ['Yes',"No"]
    )

    AnyHealthcare = 1 if AnyHealthcare=="Yes" else 0



    NoDoc = st.selectbox(
        "Was there a time in the past 12 months you could not see a doctor due to the costs",
        ["Yes","No"]
    )

    NoDoc = 1 if NoDoc=="Yes" else 0



    Genhealth = st.number_input(
        "How is your general health? (1- excellent....5-poor)",
        1,
       5
    )


    MentalHealth = st.number_input(
        "How many bad mental health days in the last 30 days",
        0,
       30
    )


    PhysHlth = st.number_input(
        "How many times have you had a physical injury in the last 30 days",
        0,
       30
    )



    diffstairs = st.selectbox(
        "Do you have serious difficulty in climbing stairs",
        ['Yes','No']
    )

    diffstairs = 1 if diffstairs=="Yes" else 0



    pred_data = np.array([
        HighBP,
        HighChol,
        Cholcheck,
        BMI,
        smoke,
        stroke,
        HrDis,
        Physact,
        Fruits,
        Veggies,
        Alc,
        AnyHealthcare,
        NoDoc,
        Genhealth,
        MentalHealth,
        PhysHlth,
        diffstairs
    ])


    pred_data = (
        pred_data - np.mean(pred_data)
    ) / np.std(pred_data)


    pred_data = pred_data.reshape(
        pred_data.shape[0],
        1
    )


    y_prediction = predict(
        w,
        b,
        pred_data
    )


    diabetes = {
        1:"Chances of having diabetes is high",
        0:"You have low chances having diabetes"
    }


    if st.button("Predict"):

        st.success(
            diabetes[y_prediction[0][0]]
        )