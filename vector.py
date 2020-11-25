"""
Vector implementation.\n
Optimized to work with maze solving intelligent system.
"""
from binarysearch import bisection

class SortedVector:
    """SortedVector()\n
    Store elements in a sorted list using bisection"""
    def __init__(self):
        self.vector = []

    def __len__(self):
        return len(self.vector)

    def __getitem__(self, i):
        return self.get(i)

    def __iter__(self):
        return iter(self.vector)

    def get(self, i):
        "Return data object under given index"
        return self.vector[i]

    def push(self, elem):
        "Insert element in ascending order"
        size = len(self.vector)
        x = bisection(self.vector, elem, 0, size)

        if x < size:
            self.vector = self.vector[:x] + [elem] + self.vector[x:]
        else:
            self.vector.append(elem)

    def pop(self):
        "Remove the first element and return its value"
        return self.vector.pop(0)
