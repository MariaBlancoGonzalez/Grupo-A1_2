"""
Heap sorted queue implementation.
"""

class Heap:
    """Heap()\n
    Store elements in a heap list"""
    def __init__(self):
        self.arr = []

    def __len__(self):
        return len(self.arr)

    def __getitem__(self, i):
        return self.get(i)

    def __iter__(self):
        return iter(self.arr)

    def get(self, i):
        "Return data object under given index"
        return self.arr[i]

    def push(self, elem):
        """Insert element in ascending order"""
        size = len(self.arr)
        if size < 1:
            self.arr.append(elem)
        else:
            self.arr.append(elem)
            for i in range((size // 2)-1, -1, -1):
                self.heapify(size, i)

    def pop(self):
        "Remove the first element and return its value"
        size = len(self.arr)
            
        # remove element at 0
        self.arr[0], self.arr[size-1] = self.arr[size-1], self.arr[0]
        obj = self.arr.pop(size-1)
        
        for i in range((size // 2)-1, -1, -1):
            self.heapify(size, i)

        return obj

    #For Min-Heap, both leftChild and rightChild must be smaller than the parent for all nodes.
    def heapify(self, n, i):
        largest = i
        leftChild = 2 * i + 1
        rightChild = 2 * i + 2 
        
        if leftChild < n and self.arr[i] < self.arr[leftChild]:
            largest = leftChild
        
        if rightChild < n and self.arr[largest] < self.arr[rightChild]:
            largest = rightChild
        
        if largest != i:
            self.arr[i],self.arr[largest] = self.arr[largest],self.arr[i]
            self.heapify(n, largest)
