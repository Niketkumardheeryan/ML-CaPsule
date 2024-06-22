# Predicting Next Sequence Of Numbers Using LSTM

The goal of this project is to predict Next Sequence of Numbers Using LSTM.

The Dataset is Prepared on my own by the basis of taking an example of monthly data of airline passengers from January 1949, with the number of passengers recorded for each month. The dataset includes two columns: "Month" and "Passengers".

---

**MODELS USED**

-  Long Short-Term Memory (LSTM) neural network.
---
**LIBRARIES NEEDED**

- numpy
- pandas
- Pytorch or torch
---
**STEPS BEING FOLLOWED** 

- Load the dataset
- Import libraries
- Data analysis
- Data Pre-Processing
- Splitting data into test and train
- Creating Data Loaders
- Defining LSTM Model
- Training the Model
- Evaluating the Model
- Predicting the Next Sequence

---

**OUTPUT**

  By Long Short-Term Memory (LSTM) neural network 
 ```
 Predicted Next Sequence: [0.3849259614944458, 0.3904801607131958, 0.39612001180648804, 0.3974493741989136, 0.39933568239212036, 0.3995046615600586, 0.3980133533477783, 0.394961953163147, 0.39221280813217163, 0.3911033272743225, 0.3923373222351074, 0.39604806900024414]
 ```

**CONCLUSION**

 The LSTM model is trained to predict the next sequence of numbers based on the provided dataset. The model's performance is evaluated, and it can generate a sequence of numbers that follows the pattern learned from the training data.
