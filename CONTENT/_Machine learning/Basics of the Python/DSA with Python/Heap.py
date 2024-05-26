# Max-Heap data structure in Python
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


def delete(heap,indx):
        """
        Deletes the value on the specified index node
        :param indx: index whose node is to be removed
        :return: Value of the node deleted from the heap
        """
        heap_size = len(heap)
        if heap_size == 0:
            print("Heap Underflow!!")
            return

        heap[-1], heap[indx] = heap[indx], heap[-1]
        heap_size -= 1

        heapify(indx, heap, heap_size)

        return heap.pop()



arr = []

insert(arr, 3)
insert(arr, 4)
insert(arr,150)
insert(arr, 9)
insert(arr, 5)
insert(arr, 2)

print ("Max-Heap array: " + str(arr))
deleteNode(arr,2)
print("After deleting an element: " + str(arr))
