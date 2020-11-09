class Heap(object):

    def heapify(self,arr, size, i):  #Method to heapify the tree
        #set i as largest
        largest = i;
        #leftChild = 2i +1
        leftChild = 2*i +1
        #rightChild = 2i +2
        rightChild = 2*i  +2
        
        if leftChild < size and arr[i] < arr[leftChild]:
            #set leftChildIndex as largest
            largest = leftChild
        if rightChild < size and arr[i] < arr[rightChild]:
            #set rightChildIndex as largest
            largest = rightChild

       #swap array[i] and array[largest] 
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, size, largest)

    def insertNode(self,arr, newNode):
        size = len(arr)
        #If there is no node,
        if size == 0:
            #dabuti metes el nodo
            arr.append(newNode)
        #else si ya hay algo dentro
        else:
            #insert el newNode al final 
            for i in range((size//2)-1,-1,-1):
                heapify(arr,size,i)

    def deleteNode(self,arr, idNode):
        size = len(arr)
        i = 0
        #if nodetoDelete is the leafNode
        for i in range (0, size):
            if idNode == arr[i]:
                break
         #swap nodetoDelete with the lastLeafNode   
        arr[i], arr[size-1] = arr[size-1], arr[i]
        arr.remove(size-1) #remove the nodeTodelete
        for i in range((len(arr)//2)-1,-1,-1):
            heapify(arr, len(arr),i) 