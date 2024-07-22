# R plotting functions provide a candid approach to understand the data. These functions are installed by default in base R and 
# do not require additional visualization package to be installed.

# Bar Chart 

# Data Set Used : BOD (inbuilt)

> data(BOD)

# printing top 6 entry in the data
> head(BOD,6)

# Output of the above code :

#   Time demand
# 1    1    8.3
# 2    2   10.3
# 3    3   19.0
# 4    4   16.0
# 5    5   15.6
# 6    7   19.8

> barplot(height = BOD$demand, names.arg = BOD$Time)

# Refer the output of this plot in the plots folder.
