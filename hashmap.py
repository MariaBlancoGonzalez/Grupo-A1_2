"""
HashMap of buckets implementation.\n
Optimized to work with maze solving intelligent system.
"""

class BucketHashMap:
    """BucketHashMap(bucket_width=1)\n
    Store buckets of elements"""

    def __init__(self, bucket_width=1):
        self.width = max(abs(bucket_width), 1)
        self.__keys = []
        self.hmap = {}

    def __len__(self):
        l = 0
        for k in self.hmap:
            l += len(self.hmap[k])
        return l

    def __getitem__(self, i):
        return self.get(i)

    def __iter__(self):
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

    def get_keys(self):
        "Get list of current buckets"
        return list(self.__keys)

    def bucket(self, value):
        "Convert integer value to bucket key"
        s = self.width * (value // self.width)
        return (s, s + self.width)

    def get(self, i):
        "Return data object under given index"
        for k in self.__keys:
            size = len(self.hmap[k])
            if size <= i:
                i -= size
            else:
                return self.hmap[k][i]
        raise IndexError

    def _bisection(self, array, y, start, end):
        "Find position of y using bisection"
        if start == end:
            return end

        x = start + (end - start) // 2
        if array[x] < y:
            x = self._bisection(array, y, x + 1, end)
        else:
            x = self._bisection(array, y, start, x)
        return x

    def push(self, elem):
        "Insert element in ascending order"
        b = self.bucket(int(elem))
        if b not in self.__keys:
            size = len(self.__keys)
            x = self._bisection(self.__keys, b, 0, size)

            self.__keys.append(b)
            if x < size:
                for i in reversed(range(x,len(self.__keys))):
                    self.__keys[i] = self.__keys[i - 1]
                self.__keys[x] = b

            self.hmap[b] = []
        
        size = len(self.hmap[b])
        x = self._bisection(self.hmap[b], elem, 0, size)

        if x >= size:
            self.hmap[b].append(elem)
        else:
            self.hmap[b].append(None)
            for i in reversed(range(x,len(self.hmap[b]))):
                self.hmap[b][i] = self.hmap[b][i-1]
            self.hmap[b][x] = elem

    def pop(self):
        "Remove the first element and return its value"
        if len(self.__keys) < 1:
            raise IndexError
        obj = self.hmap[self.__keys[0]].pop(0)

        # remove empty bucket
        if len(self.hmap[self.__keys[0]]) < 1:
            self.hmap.pop(self.__keys[0])
            self.__keys.pop(0)

        return obj
