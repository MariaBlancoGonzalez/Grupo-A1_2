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

    def get(self, k):
        "Return data object under given index"
        # TODO
        return self.hmap[k]

    def insert(self, elem, sort_by=(lambda x: x)):
        """Insert element in ascending order of the value returned by sort_by\n
        Returns index of the new inserted element"""
        return 0

    def remove(self, k):
        "Remove element at given index and return its value"
        return None
