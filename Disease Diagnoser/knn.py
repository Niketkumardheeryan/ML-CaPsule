from sklearn.neighbors import KNeighborsClassifier  
from sklearn.metrics import confusion_matrix  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle



file = pd.read_csv('datasets\Training.csv')
print()
file  = file.dropna()
print("File Shape: ",file.shape)
x= file.drop('prognosis',axis=1).values 
y= file.iloc[:, 132].values

n_neighbours = len(file.prognosis.unique())

classifier = KNeighborsClassifier(n_neighbours, metric='minkowski' )  
classifier.fit(x,y)

print("Accuracy : ",classifier.score(x,y))

pickle.dump(classifier, open('model','wb'))

