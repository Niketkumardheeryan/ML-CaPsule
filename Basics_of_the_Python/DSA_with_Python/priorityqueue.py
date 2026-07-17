# PQ data structure in Python
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i],arr[largest] = arr[largest],arr[i]
        heapify(arr, n, largest)




def insert(array, newNum):
    size = len(array)
    if size == 0:
        array.append(newNum)
    else:
        array.append(newNum)
        for i in range((size//2)-1, -1, -1):
            heapify(array, size, i)




def deleteNode(array, num):

    size = len(array)
    i = 0
    for i in range(0, size):
        if num == array[i]:
            break
    array[i], array[size-1] = array[size-1], array[i]
    array.remove(size-1)

    for i in range((len(array)//2)-1, -1, -1):
        heapify(array, len(array), i)




arr=[]

insert(arr,3)


