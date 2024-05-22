## Sort a list 
lst=[1,33,-2,0,91]
lst.sort() #Try with reverse parameter as well
print("sorted list is :",lst)


## sort a tuple
sol =(9,2021,-2,0)
print("sorted tuple is :" ,tuple(sorted(sol)))


## Sort dict by values and keys 
maps = {'z':1 , "b":3 , "c":0 , "d":5, "a":22}
print("sorted dict is : ")
ansv=sorted(maps.values())
ansk=sorted(maps.keys())
print("by values:" ,ansv)
print("by keys :",ansk)