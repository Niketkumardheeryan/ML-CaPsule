
import heapq 

# initializing list 
li = [5, 7, 9, 1, 3] 
print("intial list li is : ",li)

# using heapify to convert list into heap 
heapq.heapify(li)  
print ("The created heap is : ",end="") 
print (list(li)) 

# using heappush() to push elements into heap  
heapq.heappush(li,4)  
print ("The modified heap after push is : ",end="") 
print (list(li)) 

# using heappop() to pop smallest element 
print ("The popped and smallest element is : ",end="") 
print (heapq.heappop(li)) 
print("The modified heap is : ")
print(list(li))

