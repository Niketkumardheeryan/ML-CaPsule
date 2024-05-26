
def printAllSubstrings(str):
 
    # consider all substrings starting from i
    for i in range(len(str)):
 
        # consider all substrings ending at `j`
        for j in range(i, len(str)):
            print(str[i: j + 1], end=' ')
 
str = "python"
printAllSubstrings(str)