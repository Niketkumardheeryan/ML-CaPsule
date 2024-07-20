# Box Plot

# Data Set Used : mtcars (inbuilt)

> mtcars <- transform(mtcars,cyl=factor(cyl))

> class(mtcars$cyl)

# Output of the above code :
# [1] "factor"

> boxplot(mpg~cyl,mtcars,xlab='Number of Cylinders',ylab='miles per gallon',
+ main='miles per gallon for varied cylinders in automobiles', cex.main=1.2)

# Refer the output of this plot in the plots folder.
