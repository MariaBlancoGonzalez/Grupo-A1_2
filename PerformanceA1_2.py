import random
import time

from IntelligentSystemsA1_2 import STNode
from vector import SortedVector
from hashmap import BucketHashMap
from linkedlist import LinkedList
from heap import Heap

def performance(tf):
    STNode.IDC = 0
    start = time.time()
    frontier = tf()
    for i in range(20000):
        frontier.push(STNode(random.randint(0,10)))
        if i % 8 == 0:
            frontier.pop()
    end = time.time()
    return end - start

def main():
    test = [('SortedVector', SortedVector), ('BucketHashMap', BucketHashMap), ('LinkedList', LinkedList), ('Heap', Heap)]
    for x in test:
        print("\n{0}:".format(x[0]))
        t = 0.0
        for _ in range(3):
            t += performance(x[1])
            print(t)
        print("Average: {0}".format(t / 3))

if __name__ == "__main__":
    main()
