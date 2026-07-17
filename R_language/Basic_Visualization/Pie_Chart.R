# Pie Chart

# Making a data for pie chart
> df <- data.frame (
+ group = c("Male","Female","Child"),
+ value = c(25,25,50)
+ )

# printing the data
> df

# Output of the above code :

#    group value
# 1   Male    25
# 2 Female    25
# 3  Child    50

> pie(df$value,labels= df$group, radius=1)

# Refer the output of this plot in the plots folder.
