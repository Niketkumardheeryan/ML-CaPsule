# Car Price Prediction
# Algorithm Used- Simple Linear Regression 


## Explanation of the code

### 1. Importing the Libraries

  In this section, we import the necessary libraries for further working on the dataset.
  We have included 3 libraries namely **NumPy**, **pandas** and **matplotlib**</span>. Now we can see that we have used the syntax “import pandas as pd”. The **“as”** keyword is used for **aliasing**. This is   basically the abbreviation or a short form of the library name. Now, why do we need it? It is used to reduce redundancy. If we don’t use an alias then we would have to use the       whole library name every time we use any function of the library. So we use a short form that indicates that whenever we refer to that, we basically call the library imported. For   example here when we use pd, we are basically calling the pandas library.

  Now let’s understand what is the use of each library that we import them.
  #### i) numpy- 
  This library is used for handling different operations involving arrays. In Python, we have lists that resemble arrays in other programming languages. But we cannot use                lists because they are very slow and various operations on lists take a lot of time in the process. So it makes our code slow. This is the reason we use numpy for                    handling array operations which is approx 50 times faster than traditional Python lists.

  #### ii) pandas- 
  This library is used for handling data. Whenever we work on data science or machine learning models we involve a huge amount of data and datasets. So going through the               whole data and drawing a conclusion is difficult for humans. So we use pandas which are used to manipulate data in various ways and help us draw statistical conclusions                based on the data which we further use.

  #### iii) matplotlib- 
  This library is used for data visualization. We use this module to analyze a huge dataset by converting it into visuals like bar graphs, pie charts, line graphs                      etc. We have imported a submodule of matplotlib which is pyplot. Whenever we use library name followed by “.” another name, it means we are importing a submodule                      from that entire library to use. Pyplot is the most widely used module in matplotlib used for data visualization.



### 2. Importing dataset into the Colab Notebook

In this section, we import the dataset or the file in which our data is stored into the code so that we can work upon that file and perform manipulations and analyse it. So the library pandas can be used to read that file. The file format is mostly in **CSV( Comma Separated Values)** which is easily readable by pandas using the function **read_csv**. Now if you have an excel file with the .xlsx extension in which your data set is stored. You can use the function **read_xlsx** to read that file into your code. Inside the parenthesis, we provide the path or directory in which your file with the data is stored. We store the whole data in that file in a variable named ‘dataset’. To check if the file is fetched correctly we print the data stored in the variable.



### 3. Segregating data in X and Y where X= Engine Size and Y= Car Price

In this code section, we are aiming to separate the data available in the dataset variable into two variables X and Y. As we know to build a machine learning model which predicts data based on some input we have to have two variables, predictor variable and the target variable. So here we are separating the data into two variables X which contains the engine size and is the predictor variable. The variable Y contains Car price which is our target variable.
Now let’s understand how the code works. 
So we first create a variable X and in that variable, we need to assign the engine size column. Now we have an inbuilt function in pandas that is used to retrieve a particular column and row from the whole data frame( data frame is a 2-D array). That inbuilt function is **“iloc”**. So we mention the variable in which data is stored, in our case its dataset. Now we call the iloc function and in the square brackets of the iloc we mention the row and columns to be included. We can clearly see we need all the rows but only the 1st column in our X variable. SO we write “:” as the first argument which means we provide no restriction to the rows and all rows should be included. In the second argument of the bracket, we write “:-1”. This means that the number written after the colon will not be included and except that every column will be included in the variable. Now we all know that indexing in Python can be done in a forwarding direction starting from 0 and also in the backward direction starting from -1. So the -1 represents the Car price column in our data and it is not stored in the X variable. Then we have successfully stored engine size in our X variable. 
Similarly, we use the iloc function. We again put no restriction to the rows and then we write “-1” as the second argument. This means only the -1 column will be included in the Y variable and Car price is stored in the Y variable.


### 4. Visualizing the Data

Now we have successfully separated the data into two variables. So we can visualize the data using the pyplot module. So in the code, we first assign the labels of the X-Axis and the Y-axis using the xlabel and ylabel functions. In the graph, you can see that Engine Size is shown in the X-Axis and CarPrice is shown in the Y-Axis. We can also provide a title to the graph using the title function. I have used the title of “engine Size vs price”. Then to plot the graph we have used the scatter function which comes with pyplot. It is used to plot data points that can be visualized individually on the graph and it is used when we have a 2D array of any length. We have given X and Y as the arguments to be plotted on the graph. We can also customize the colour of the graph using color function. Here I have used green colour and used “*” as the marker which is basically the points in the dataset.



### 5. Splitting data into train set and test set

As we have learnt already that to build any machine learning model we would need to split the data into two parts named Test set and Train set. The test set is that part of the data that we initially used to make the machine build the logic and how to data is varying based on various inputs in the dataset. And then we use the test set to check that the training has been done properly and how accurate our model is.
Now let’s see how the code works.
So for this data splitting, we use the Scikit Learn library. From the Scikit learn library we use a submodule named model_selection. Any type of regression like linear, logistic regression is all part of the model_selection submodule. So we use that submodule. We import a function in these libraries named “ train_test_split”. This method is used to split the data into two subparts train and test data. Further, this train and test data get divided into X and Y variables. So when we use this function it returns the value in four variables. So we initialise 4 variables named X_train, X_test, Y_train and Y_test.  We use the function and pass X and Y as the Arguments. We can also mention the ratio in which we want the data to be divided. In this case, we mention the test_size as 0.3. This means 30 per cent of the data will be stored as a test set and 70 per cent will be used as the training set. 
When we run the code we can see two values (123,1) and (82,1). Totally there were 205 rows and 2 columns. On the basis of the ratio, we provided the data that got split into two parts train and test data.


### 6. Fitting the trained data in Simple Linear Regression

Now we have completed splitting the data. Now we have to use the train set to train our machine learning model. For that, we will again use the Scikit Learn library and a submodule of this library named “linear_model”. From the submodule, we import the “LinearRegression” function which is the method we will use to train our model. Now let’s see how the code works.
After importing the required function we import that function in a variable which we have named as “model”. So the entire LinearRegression() function is stored in the model variable(Yes we can store a =n entire function into a variable in Python). Now we have to train our model. So we fit the data into the model using our train set. So we are using the  “fit” function and pass the X_train and Y_train values. This makes our model trained and it is now ready to be tested on the test set to calculate the accuracy of the model.





### 7. Predicting the result of the test set

Our model is completely ready for being tested on the test set. Now we declare the variable named Y_pred in which the result of the data which will be predicted by our model when we pass the test set will be stored. So we use the “predict” function and pass the test set which is X_test as the argument. SO we are directing our model to predict the output which is the car price based on the test set containing the engine size. If we print the Y_pred variable you can see an array of values predicted by our model.


### 8. Accuracy of model calculation

In this part, we calculate the accuracy of our model. It can be simply done by using the “score function”. In this function, we pass the X_test and Y_test values to check the accuracy of our model. In the output as you can see it is coming as 0.737. This value is obtained by dividing the accuracy by 100. SO if you want to convey accuracy in percentage then multiply the value you got by 100. So in this case our accuracy is 73%.


### 9. Plotting Regressor Curve

In this section, we visualize the model and how well we have been able to train the model. Now I have divided the code in two parts. The first part is the graph for the training set and the second graph is that for the test data set.
First, we plot the data sets using the scatter function by passing the X_train and Y_train variables. We label the x and y-axis as engine size and car price respectively and give a title to this graph named training set to segregate the two graphs. Now we plot a line to see how best the line fits the data points plotted. So we use the “plot” function and pass the X_train as one argument. The other argument is the predicted value by the model when we pass the X_train values. So what we are doing is we are relying on the model to provide the Y values when we pass the X_train values. This draws a line in blue colour to separate the data points and the line. We can see most of the data points are far away from the blue line which means our model is not that accurate and there is a lot of errors.

Secondly, we plot the data sets using the scatter function and this time we pass X_test and Y_test values. Similarly, as above we plot a line in blue colour in which the x value is given by X_test and the y value is the value our model predicts when we pass the X_test data. We use the “predict” function to get the predicted values.


### 10. Examining model on external Data

In this part, we now check our trained model on any external data. Now we have to store any external data whose output we need to predict as an array. So we use numpy array function to store the data as an array and store that in a variable named test_data. Now we initialise another variable named test_pred in which the predicted value will be stored. So we again use the “predict” function and pass the test_data in that function as an argument. The predicted value is stored in test_pred and we can print it. We get the output in the form of a numpy array.


### 11. Examining model on user-inputted data

This is an extra step to test our model. We are basically taking the data whose output we want to be predicted from the user and predicting the output and showing it to the user. So we take input of the data as in traditional python using input() function. Now we have to convert the data into a numpy array so that we can pass it to the predict function. We then pass the data into predict function and store the output in the variable. Finally, we show the user the predicted output based on their input data.

This completes the whole process of training our Machine Learning model using Linear Regression.

