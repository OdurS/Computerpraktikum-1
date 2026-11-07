# from itertools import permutations
import sys


def rec_partitions(rest, max_part, current, result):
    if rest == 0:
        result.append(tuple(current))
        return
    for k in range(min(rest, max_part), 0, -1):
        current.append(k)
        rec_partitions(rest - k, k, current, result)
        current.pop()


def partitions(n):
    result = []
    rec_partitions(n, n, [], result)
    return result




# n = 65
n = int(sys.argv[1])

for partition in partitions(n):
    print(partition)
