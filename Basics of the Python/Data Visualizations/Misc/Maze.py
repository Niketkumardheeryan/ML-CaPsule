count=0

def maze(i,j,n,m,osf):
    global count 
    if i == n-1 and j == m-1:
        print(osf)
        count+=1
        return 
    
    if i>=n or j>=m:
        return 
    
    maze(i,j+1,n,m,osf+'R')
    maze(i+1,j,n,m,osf+'D')
       
maze(0,0,3,3,'')
print(count)
