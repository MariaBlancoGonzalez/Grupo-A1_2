def heapify(arr, n, i):
    largest = i
    leftChild = 2 * i + 1
    rightChild   = 2 * i + 2 
    
    if leftChild < n and arr[i] < arr[leftChild]:
        largest = leftChild
    
    if rightChild < n and arr[largest] < arr[rightChild]:
        largest = rightChild
    
    if largest != i:
        arr[i],arr[largest] = arr[largest],arr[i]
        heapify(arr, n, largest)

def insert(array, newNode):
    size = len(array)
    if size == 0:
        array.append(newNode)
    else:
        array.append(newNode);
        for i in range((size//2)-1, -1, -1):
            heapify(array, size, i)


def deleteNode(array, id):
    size = len(array)
    i = 0
    for i in range(0, size):
        if id == array[i]:
            break
        
    array[i], array[size-1] = array[size-1], array[i]

    array.remove(size-1)
    
    for i in range((len(array)//2)-1, -1, -1):
        heapify(array, len(array), i)
    
arr = []

insert(arr, 3)
insert(arr, 4)
insert(arr, 9)
insert(arr, 5)
insert(arr, 2)

print ("Max-Heap array: " + str(arr))

deleteNode(arr, 4)
print("After deleting an element: " + str(arr))