"""
Heap class wrapping heapq
"""
import heapq

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
        heapq.heappush(self.arr, elem)

    def pop(self):
        "Remove the first element and return its value"
        return heapq.heappop(self.arr)
