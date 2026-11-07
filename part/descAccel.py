import sys
def accel_desc(n):
    # assert n >= 1

    k = 1
    q = 1

    # Initialize d_2, ..., d_n
    d = [0] * (n + 1)
    for i in range(2, n + 1):
        d[i] = 1

    d[1] = n

    # Visit the first partition
    yield tuple(d[1:k + 1])

    while q != 0:

        if d[q] == 2:
            k += 1
            d[q] = 1
            q -= 1

        else:
            m = d[q] - 1
            n_prime = k - q + 1

            d[q] = m

            while n_prime >= m:
                q += 1
                d[q] = m
                n_prime -= m

            if n_prime == 0:
                k = q

            else:
                k = q + 1

                if n_prime > 1:
                    q += 1
                    d[q] = n_prime

        # Visit the current partition
        yield tuple(d[1:k + 1])


# n = 65
n = int(sys.argv[1])

for partition in accel_desc(n):
    print(partition)
