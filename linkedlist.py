"""
Python LinkedList implementation.\n
Optimized to work with maze solving intelligent system.
"""

class Node:
    """Node(obj)\n
    obj - data object\n
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

    def push(self, elem):
        "Insert object in ascending order"
        self.length += 1
        n = self.head
        if n is None:
            self.head = Node(elem)
        elif elem < n.get():
            tail = self.head
            self.head = Node(elem)
            self.head.forward = tail
        else:
            while n.forward is not None and elem > n.forward.get():
                n = n.forward

            tail = n.forward
            n.forward = Node(elem)
            n.forward.forward = tail

    def pop(self):
        "Remove the first element and return its value"
        if self.length < 1:
            raise IndexError
        r = self.head
        self.head = self.head.forward
        self.length -= 1
        return r.get()
