import sys

## Normales Recursiver Algorithmus iterativ gemacht
def accel_asc(n):
    s = [0]*(n+1)
    max = [n]*(n+1)
    rem = [n]*(n+1)
    i = 0
    while i >= 0:
        j = s[i]
        m = max[i]
        r = rem[i]
        if r == 0:
            yield(s[:i])
            i -= 1
            continue
        if j < m and j < r:
            s[i] = j+1
            max[i+1] = min(m, j+1)
            rem[i+1] = rem[i] - (j+1)
            s[i+1] = 0
            i += 1
        else:
            i -= 1


n = int(sys.argv[1])
k = 0
for partition in accel_asc(n):
    # print("Part:", partition)
    k+= 1

print(k)
