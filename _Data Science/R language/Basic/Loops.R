# The Repeat loop executes the same code again and again until a stop condition is met

result <- c("Repeat loop")
i <- 0
  
# test expression 
repeat {
   print(result)
   # update expression 
   i <- i + 1
     
   # Breaking condition
   if(i >3) {
      break
   }
}

# A For loop is a repetition control structure that allows you to efficiently write a loop that needs to execute a specific number of times

x <- c(2,5,3,9,8,11,6)
count <- 0
for (val in x) {
if(val %% 2 == 0)  count = count+1
}
print(count)

# The While loop executes the same code again and again until a stop condition is met

i <- 1
while (i < 6) {
print(i)
i = i+1
}
