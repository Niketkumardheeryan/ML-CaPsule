# Centroid of digits

● At this repo we classify digits using KNN model
algorithm.
● Firstly, we split the MNIST dataset into a test and training dataset
according to (1000,10000) 10000 for training dataset and the
other for tested dataset.
● We divided each digit into 4-grids (2x2) grid.
● Then we got the centroid of each divided grid of each digit.
● We put each centroid(x,y) into a list to train and predict the
model.
● We compared the KNN model with different K-parameter to get
the optimal one :

 -  At K = 3 → Accuracy of KNN model: 0.801
 -  At K = 8 → Accuracy of KNN model: 0.833
 -  At K = 12 → Accuracy of KNN model: 0.832
 -  At K = 100 → Accuracy of KNN model: 0.782
 -  At K = 1000 → Accuracy of KNN model: 0.659
 -  At K = 20 → Accuracy of KNN model: 0.822
 -  At K = 7 → Accuracy of KNN model: 0.824
 -  At K = 9 → Accuracy of KNN model: 0.826

● So the best K-parameter to fit into the model and get highest
accuracy according to the above statistics is at K = 8 with
accuracy 0.833.


## Tools 
> tensorflow  
> numpy   
> keras   
> matplotlib   
> sklearn   

