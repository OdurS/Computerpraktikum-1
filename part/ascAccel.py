import sys

## Aus https://arxiv.org/pdf/0909.2331
def accel_asc(n):
    k = 2
    a = [0] * (n + 2)
    a[1] = 0
    y = n - 1

    while k != 1:
        k -= 1
        x = a[k] + 1

        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1

        l = k + 1

        while x <= y:
            a[k] = x
            a[l] = y

            yield tuple(a[1:l + 1])

            x += 1
            y -= 1

        y = y + x - 1
        a[k] = y + 1

        yield tuple(a[1:k + 1])


# n = 65
n = int(sys.argv[1])
k = 0
for partition in accel_asc(n):
#    print(partition)
    k+= 1

print(k)
