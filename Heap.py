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
        size = len(self)
        if size == 0:
            self.arr.append(elem)
        else:
            self.arr.append(elem)
            for i in range((size // 2)-1, -1, -1):
                self.heapify(size, i)

    def pop(self):
        "Remove the first element and return its value"
        size = len(self)
            
        self.arr[0], self.arr[size-1] = self.arr[size-1], self.arr[0]

        obj = self.arr.pop(size-1)
        
        for i in range((len(self.arr) // 2)-1, -1, -1):
            self.heapify(len(self.arr), i)

        return obj

    def heapify(self, n, i):
        smallest = i
        leftChild = 2 * i + 1
        rightChild = 2 * i + 2 
        
        if leftChild < n and self.arr[i] > self.arr[leftChild]:
            smallest = leftChild
        
        if rightChild < n and self.arr[smallest] > self.arr[rightChild]:
            smallest = rightChild
        
        if smallest != i:
            self.arr[i], self.arr[smallest] = self.arr[smallest], self.arr[i]
            self.heapify(n, smallest)
