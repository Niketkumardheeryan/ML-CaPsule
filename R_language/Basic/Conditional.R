# if ...else
x <- c(1,2,3,4)

if(5 %in% x) {
   print("5 is in list")
} else if (3 %in% x) {
   print("5 is in list")
} else {
   print("Not found")
}

'''If if statement is true then it will not go deeper if its false then it go for else if same for this also'''

# Switch 

val1 = 6  
val2 = 7
val3 = "s"  
result = switch(  
    val3,  
    "a"= cat("Addition =", val1 + val2),  
    "d"= cat("Subtraction =", val1 - val2),  
    "r"= cat("Division = ", val1 / val2),  
    "s"= cat("Multiplication =", val1 * val2),
    "m"= cat("Modulus =", val1 %% val2),
    "p"= cat("Power =", val1 ^ val2)
)  
