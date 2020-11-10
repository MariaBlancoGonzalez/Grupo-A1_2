"""
Heap sorted queue implementation.
"""

class Heap:
    """Heap(sort_by=(lambda x: x))\n
    Store elements in a heap list"""
    def __init__(self, sort_by=(lambda x: x)):
        self.sort_by = sort_by
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

    def insert(self, elem):
        """Insert element in ascending order of the value returned by sort_by"""
        size = len(self)
        if size == 0:
            self.arr.append(elem)
        else:
            self.arr.append(elem)
            for i in range((size // 2)-1, -1, -1):
                self.heapify(size, i)

    def remove(self, i):
        "Remove element at given index and return its value"
        size = len(self)
            
        self.arr[i], self.arr[size-1] = self.arr[size-1], self.arr[i]

        obj = self.arr.pop(size-1)
        
        for j in range((len(self.arr) // 2)-1, -1, -1):
            self.heapify(len(self.arr), j)

        return obj

    def heapify(self, n, i):
        smallest = i
        leftChild = 2 * i + 1
        rightChild = 2 * i + 2 
        
        if leftChild < n and self.sort_by(self.arr[i]) > self.sort_by(self.arr[leftChild]):
            smallest = leftChild
        
        if rightChild < n and self.sort_by(self.arr[smallest]) > self.sort_by(self.arr[rightChild]):
            smallest = rightChild
        
        if smallest != i:
            self.arr[i], self.arr[smallest] = self.arr[smallest], self.arr[i]
            self.heapify(n, smallest)
