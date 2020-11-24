#!/usr/bin/python
import random
import time

from IntelligentSystemsA1_2 import STNode
from vector import SortedVector
from hashmap import BucketHashMap
from linkedlist import LinkedList
from heap import Heap

def performance(tf, nodes=50000, value=1000, pop=8):
    """
    Performance test of a data structure.

    Arguments:
    - tf -- a data structure class
    - nodes -- amount of nodes to push
    - value -- maximum possible value of a node
    - pop -- every n-th iteration pop an element
    """
    STNode.IDC = 0
    start = time.time()
    frontier = tf()
    for i in range(nodes):
        frontier.push(STNode(1, 1, (0,0), 0, 'N', 0, random.randint(0,value)))
        if i % pop == 0:
            frontier.pop()
    end = time.time()
    return end - start

def main():
    test = [Heap, SortedVector, BucketHashMap, LinkedList]
    print("Running performance test...")
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
