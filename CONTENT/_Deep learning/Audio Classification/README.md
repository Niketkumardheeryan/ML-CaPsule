
## Audio Classification

### Librabries you need to install :

 - python_speech_features library
 - mfcc function
 - scipy.io.wavfile function
 - numpy library
 - os module
 - pickle module
 - tempfile library
 - random module
 - operator module
 - math library

### what algorithim i have used ?

- KNN 
- Nearest Neighbours is an efficient algorithm, in terms of calculation time and predictive power, for classification. 

## steps to implement
We can easily implement a KNN using the following steps:

 1. Load the dataset
 2. Initialize the value of a
 3. Iterate from 1 to the total number of data training points:

		 i. Calculate the distance between the test data and each row of the training data.
		 ii. after doing the first step, Sort the distances in ascending order.
		 iii. later, Get the top a rows from the sorted list.
		 iv. after completing first three steps, Get the most frequent class of these a rows.
		 v. last but not least, Return the predicted class.