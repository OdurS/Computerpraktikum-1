def _integer(n):
    if type(n) is not int:
        raise TypeError("n muss eine ganze Zahl sein.")


## Aus https://arxiv.org/pdf/0909.2331, mit dem Index umgekehrt um die richtige Reihenfolge zu erhalten.
## Weil die Funktion hier ein Iterator ist, ist nur 'a' abhängig von n.
## Das ist eine Liste mit Speicherkomplexität O(n+2) = O(n)
#
## Das ist eine Liste mit Speicherkomplexität O(n+2) = O(n)
## Die Arbeit pro Partition ist vorallem anhängig von den Kopien bei den yield's. Diese ist gebunden durch n.
## Ingesamt ist die Zeitkomplexität also O(n P(n)), wobei P(n) die Anzahl der Partitionen der Zahl n ist.
def partitions(n):
    _integer(n)
    if n == 0:
        yield ()
        return
    if n < 0:
        return

    k = -(2) - 1
    a = [0] * (n + 2)
    y = n - 1
    while k != -(1)-1:
        k += 1
        x = a[k] + 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k -= 1
        l = k - 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield tuple(a[l:-1])
            x += 1
            y -= 1
        y = y + x - 1
        a[k] = y + 1
        yield tuple(a[k:-1])

def partitions_list(n):
    return list(partitions(n))


## Einfach nur alle Partitionen einmal gezählt
## O(P(n))
def count_partitions(n):
    _integer(n)
    if n < 0:
        return 0
    counts = [1] + [0] * n
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]

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

## Aus der GAP-Stdlib
def NrPartitions(n):
    s = 1
    p = [s]  # p(0) = 1

    for m in range(1, n + 1):
        s = 0
        k = 1
        l = 1

        while 0 <= m - (l + k):
            s -= (-1)**k * (
                p[m - l] + p[m - (l + k)]
            )

            k += 1
            l += 3 * k - 2

        if 0 <= m - l:
            s -= (-1)**k * p[m - l]

        p.append(s)

    return s
