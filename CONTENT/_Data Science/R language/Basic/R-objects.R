''' The variables are assigned with R-Objects
 The data type of the R-object becomes the data type of the variable'''
 
 '''
R-Objeccts are following:
Vectors
Lists
Matrices
Arrays
Factors
Data Frames
'''

# c() function which means to combine the elements

# Create a vector
> color <- c('red','green',"yellow",'blue')

# Create a list
> lt <- list(c(2,5,1),10.3)

# Create a matrix
> M = matrix( c('a','b','c','d','e','f'), nrow = 3, ncol = 2, byrow = TRUE)

# Create an array
> a <- array(c('green','yellow'),dim = c(3,3,2))

> color <- c('red','green',"yellow",'blue','red','green')
# Create a factor object
> factor_color <- factor(color)
# It stores the vector along with the distinct values of the elements in the vector as labels

# Create the data frame.
> BMI <- 	data.frame(
   gender = c("Male", "Male","Female"), 
   height = c(152, 171.5, 165), 
   weight = c(81,93, 78),
   Age = c(42,38,26)
)


