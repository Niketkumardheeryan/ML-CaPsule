## for testing the model

import pandas as pd
import pickle
from sklearn.metrics import confusion_matrix

file = pd.read_csv('datasets\Testing.csv')

model = pickle.load(open('model','rb'))
x_test= file.drop('prognosis',axis=1).values 
y_test= file.iloc[:, 132].values 

y_pred = model.predict(x_test)
print(y_pred)

print("Y Pred == Y Test : \n",y_test==y_pred)

print("Confusion Matrix : ",confusion_matrix(y_test,y_pred))