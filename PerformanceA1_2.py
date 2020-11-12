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
    for i in range(30000):
        frontier.push(STNode(1, 1, (0,0), 0, 'N', 0, random.randint(0,1000)))
        if i % 8 == 0:
            frontier.pop()
    end = time.time()
    return end - start

def main():
    test = [SortedVector, BucketHashMap, LinkedList]
    for x in test:
        print("\n{0}:".format(str(x)))
        t = 0.0
        for _ in range(3):
            tp = performance(x)
            t += tp
            print(tp)
        print("Average: {0}".format(t / 3))

if __name__ == "__main__":
    main()
