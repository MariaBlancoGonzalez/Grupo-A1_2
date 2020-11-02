"""
Python LinkedList implementation.\n
Optimized to work with maze solving intelligent system.
"""

class Node:
    """Node(obj)\nobj - data object\n
    Linked list node element"""

    def __init__(self, obj):
        self.obj = obj
        self.forward = None

    def get(self):
        "Retrieve data object"
        return self.obj

class LinkedList:
    """LinkedList()\n
    Linked list implementation for Python"""

    def __init__(self):
        self.length = 0
        self.head = None

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        return self.get(i)

    def __iter__(self):
        self.__current = self.head
        return self

    def __next__(self):
        if self.__current is None:
            raise StopIteration
        n = self.__current
        self.__current = n.forward
        return n.get()

    def get(self, i):
        "Return data object under given index"
        return self.get_node(i).get()

    def get_node(self, i):
        "Return node under given index"
        node = self.head
        while i > 0:
            if node is None:
                break
            i -= 1
            node = node.forward
        if node is None:
            raise IndexError
        return node

    def insert(self, elem, sort_by=(lambda x: x)):
        """Insert object in ascending order of sort_by parameter\n
        Returns index of newly inserted node"""
        self.length += 1
        pos = 0
        n = self.head
        if n is None:
            self.head = Node(elem)
            return pos

        if sort_by(elem) < sort_by(n.get()):
            tail = self.head
            self.head = Node(elem)
            self.head.forward = tail
            return pos

        while n.forward is not None and sort_by(elem) > sort_by(n.forward.get()):
            pos += 1
            n = n.forward

        tail = n.forward
        n.forward = Node(elem)
        n.forward.forward = tail
        return pos + 1

    def remove(self, i):
        "Removes node at given index and returns its data object"
        if self.length < 1:
            raise IndexError
        if i == 0:
            r = self.head
            self.head = self.head.forward
        else:
            n = self.get_node(i-1)
            r = n.forward
            n.forward = r.forward
        self.length -= 1
        return r.get()
