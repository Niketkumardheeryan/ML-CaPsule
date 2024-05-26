
from collections import defaultdict 

dd = defaultdict(lambda:'none') 

normal_d = {1:'a',2:'b',3:'c'}
	
for i in range(5): 
	dd[i]=i
		

print(dd[1000])
#print(normal_d[10])

