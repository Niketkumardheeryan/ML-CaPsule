from collections import deque 
	
# initializing deque. 
de = deque([1,2,3]) 
print('Intial Deque')
print(de)
	
# using append() to insert element at right end.  
de.append(4) 
print ("The deque after appending at right is : ") 
print (de) 
	
# using appendleft() to insert element at left end.  
de.appendleft(0) 
print ("The deque after appending at left is : ") 
print (de)

de.pop()   
print ("The deque after pop is  : ")  
print (de)  
    
  
# using insert() to insert the value 3 at 5th position.
de.insert(5,4) 
print ("The deque after insering is : ")  
print(de)

# using popleft() to delete element from left end.
de.popleft()    
print ("The deque after deleting from left is : ")  
print (de)


# using extend() to add numbers to right end adds 5,6 to right end.
de.extend([5,6]) 
print ("The deque after extending deque at end is : ") 
print (de) 