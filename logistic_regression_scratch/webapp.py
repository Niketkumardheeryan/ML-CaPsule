from telnetlib import BM
import streamlit as st
import numpy as np
from numpy import array
from matplotlib import pyplot as plt
import pandas as pd



data = pd.read_csv("diabetes.csv")
st.title("Diabetes predictor")

nav = st.sidebar.radio("Navigation",["Home","Prediction"])

if nav == "Home":
    st.write("Home")
    st.image("diab.jpg",width=800)
    if st.checkbox("Show table"):
        st.table(data.sample(10))
    
    graph = st.selectbox("Would you like to see a graph",["No","Yes"])
    if graph == "Yes":
        plt.figure(figsize=(10,5))
        plt.scatter(data["BMI"],data["Diabetes_binary"])
        plt.ylim(0)
        plt.xlabel("BMI")
        plt.ylabel("Diabetes")
        plt.tight_layout()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

        plt.pcolormesh( data.sample(20) , cmap = 'winter' )
  
        plt.title( '2-D Heat Map' )
        plt.show()  
        st.pyplot()


    if graph == "Interactive":
        pass



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
        if A[0,i]>=0.75:
            y_prediction[0,i]=1
        else:
            y_prediction[0,i]=0
   
    return y_prediction

f1 = open("model_parameters.txt","r")

para = f1.read()
parameters = eval(para)
w =parameters["w"]
b = parameters["b"]

if nav =="Prediction":
    st.subheader("Predict")

    HighBP = st.selectbox("Do you have high BP?",["Yes","No"])
    if HighBP=="Yes":
        HighBP = 1
    else:
        HighBP=0

    HighChol = st.selectbox("Do you have high cholestrol",["Yes","No"])
    if HighChol=="Yes":
        HighChol = 1
    else:
        HighChol=0
    
    Cholcheck = st.selectbox("Have you had a cholestrol check in the last five years",['Yes','No'])
    if Cholcheck=="Yes":
        Cholcheck = 1
    else:
        Cholcheck=0

    BMI = st.number_input("Enter your BMI", 0,50)
    smoke = st.selectbox("Do you smoke",["Yes",'No'])
    if smoke=="Yes":
        smoke = 1
    else:
       smoke=0

    stroke = st.selectbox("Ever had a stroke",['Yes',"No"])
    if stroke=="Yes":
        stroke = 1
    else:
       stroke=0

    HrDis = st.selectbox("Had a heart attack or suffer from heart conditions",["Yes",'No'])
    if HrDis=="Yes":
        HrDis = 1
    else:
       HrDis=0

    Physact = st.selectbox("Do you get regular exercise in the last 30 days",['Yes','No'])
    if Physact=="Yes":
        Physact = 1
    else:
       Physact=0
    
    Fruits = st.selectbox("Do you have one or more fruits in a day",['Yes','No'])
    if Fruits=="Yes":
        Fruits = 1
    else:
       Fruits=0
    
    Veggies = st.selectbox("Do you have one or more vegetables in a day",['Yes','No'])
    if Veggies=="Yes":
        Veggies= 1
    else:
       Veggies=0
    
    Alc = st.selectbox("Do you consume more than 14 drinks in a week (for men) and 7 drinks a week(for women)",["Yes","no"])
    if Alc=="Yes":
        Alc = 1
    else:
       Alc=0

    AnyHealthcare = st.selectbox("Do you have health care access",['Yes',"No"])
    if AnyHealthcare=="Yes":
        AnyHealthcare = 1
    else:
       AnyHealthcare=0
    
    NoDoc = st.selectbox("Was there a time in the past 12 months you could not see a doctor due to the costs",["Yes","No"])
    if NoDoc=="Yes":
        NoDoc = 1
    else:
       NoDoc=0
    
    Genhealth = st.number_input("How is your general health? (1- excellent....5-poor)",1,5)
    MentalHealth = st.number_input("How many bad mental health days in the last 30 days",0,30)
    PhysHlth = st.number_input("How many times have you had a physical injury in the last 30 days",0,30)

    diffstairs = st.selectbox("Do you have serious difficulty in climbing stairs",['Yes','No'])
    if diffstairs=="Yes":
        diffstairs = 1
    else:
       diffstairs=0
    
    
    pred_data = np.array([HighBP,HighChol,Cholcheck, BMI,smoke,stroke,HrDis,Physact,Fruits,Veggies,Alc,AnyHealthcare,NoDoc,Genhealth,MentalHealth,PhysHlth,diffstairs])
    pred_data= (pred_data- np.mean(pred_data)) / np.std(pred_data)
    pred_data = pred_data.reshape(pred_data.shape[0],1)
    
    y_prediction = predict(w,b,pred_data)
    
    diabetes = {1:'Chances of having diabetes is high',0:"You have low chances having diabetes"}

    if st.button("Predict"):
        st.success(diabetes[y_prediction[0][0]])

    
    

