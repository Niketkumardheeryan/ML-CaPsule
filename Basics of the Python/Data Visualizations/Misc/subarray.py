
# Function to print all sublists 
def printallSublists(A):
 
    # consider all sublists starting from i
    for i in range(len(A)):
 
        # consider all sublists ending at `j`
        for j in range(i, len(A)):
 
            print(A[i: j + 1])  ## slicing in python
 
A = [1, 2, 3, 4, 5]
printallSublists(A)