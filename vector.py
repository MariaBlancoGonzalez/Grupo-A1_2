"""
Vector implementation.\n
Optimized to work with maze solving intelligent system.
"""

class SortedVector:
    """SortedVector()\n
    Store elements in a sorted list"""
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
        x = 0
        while x < size and self.vector[x] < elem:
            x += 1

        if x >= size:
            self.vector.append(elem)
        else:
            self.vector.append(None)
            for i in reversed(range(x,len(self.vector))):
                self.vector[i] = self.vector[i-1]
            self.vector[x] = elem

    def pop(self):
        "Remove the first element and return its value"
        return self.vector.pop(0)
