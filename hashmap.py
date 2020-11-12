"""
HashMap of buckets implementation.\n
Optimized to work with maze solving intelligent system.
"""

class BucketHashMap:
    """BucketHashMap(bucket_width=1)\n
    Store buckets of elements"""

    def __init__(self, bucket_width=1):
        self.width = max(abs(bucket_width), 1)
        self.hmap = {}

    def __len__(self):
        l = 0
        for k in self.hmap:
            l += len(self.hmap[k])
        return l

    def __getitem__(self, i):
        return self.get(i)

    def __iter__(self):
        self.__keys = self.keys()
        self.__ckey = 0
        self.__ci = 0
        return self

    def __next__(self):
        if self.__ckey < len(self.__keys):
            bucket = self.hmap[self.__keys[self.__ckey]]
            while self.__ci >= len(bucket):
                self.__ckey += 1
                self.__ci = 0
                if self.__ckey >= len(self.__keys):
                    raise StopIteration
                bucket = self.hmap[self.__keys[self.__ckey]]
            n = bucket[self.__ci]
            self.__ci += 1
            return n
        else:
            raise StopIteration

    def keys(self):
        return sorted(list(self.hmap.keys()))

    def bucket(self, value):
        "Convert integer value to bucket key"
        s = self.width * (value // self.width)
        return (s, s + self.width)

    def get(self, i):
        "Return data object under given index"
        ks = self.keys()
        for k in ks:
            size = len(self.hmap[k])
            if size <= i:
                i -= size
            else:
                return self.hmap[k][i]
        raise IndexError

    def _bisection(self, b, y, start, end):
        "Find position of y using bisection"
        if start == end:
            return end

        x = start + (end - start) // 2
        if self.hmap[b][x] < y:
            x = self._bisection(b, y, x + 1, end)
        else:
            x = self._bisection(b, y, start, x)
        return x

    def push(self, elem):
        "Insert element in ascending order"
        ks = self.keys()
        b = self.bucket(int(elem))
        if b not in ks:
            self.hmap[b] = []
        
        size = len(self.hmap[b])
        x = self._bisection(b, elem, 0, size)

        if x >= size:
            self.hmap[b].append(elem)
        else:
            self.hmap[b].append(None)
            for i in reversed(range(x,len(self.hmap[b]))):
                self.hmap[b][i] = self.hmap[b][i-1]
            self.hmap[b][x] = elem

    def pop(self):
        "Remove the first element and return its value"
        ks = self.keys()
        if len(ks) < 1:
            raise IndexError
        obj = self.hmap[ks[0]].pop(0)

        # remove empty bucket
        if len(self.hmap[ks[0]]) < 1:
            self.hmap.pop(ks[0])

        return obj
