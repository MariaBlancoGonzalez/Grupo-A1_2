"""
Simple binary search implementation.

def bisection(array, value, start, end)
"""

def bisection(array, y, start, end):
    "Find position of y in array using binary search"
    if start == end:
        return end

    x = start + (end - start) // 2

    if array[x] < y:
        x = bisection(array, y, x + 1, end)
    else:
        x = bisection(array, y, start, x)

    return x

