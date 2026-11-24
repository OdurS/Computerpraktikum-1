import sys
## Aus der GAP-Stdlib
def GPartitions(n):
    """
    Returns a list of all integer partitions of n,
    sorted lexicographically.

    Requires n >= 1.
    """
    if n < 1:
        raise ValueError("n must be a natural number >= 1")

    B = [[] for _ in range(n)]

    for k in range(1, n // 2 + 1):

        # Trivial partition with greatest part k
        B[n - k - 1].append([n - k, k])

        for j in range(n - k - 1, k - 1, -1):

            # Partitions of n-j-k with greatest part k
            for p in B[j + k - 1]:

                # Construct a new partition
                l = [j] + p.copy()

                # Replace the second entry by k
                l[1] = k

                B[j - 1].append(l)

    # Add the partition [n]
    B[n - 1].insert(0, [n])

    # Concatenate all lists
    return [p for sublist in B for p in sublist]


n = int(sys.argv[1])

# print(len(GPartitions(n)))
k = 0
for partition in GPartitions(n):
#    print(partition)
    k+= 1
print(k)
