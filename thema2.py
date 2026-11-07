from itertools import permutations


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


def is_standard(T):
    shape = [len(row) for row in T]
    if any(length == 0 for length in shape):
        return False
    if any(shape[r] < shape[r + 1] for r in range(len(shape) - 1)):
        return False

    values = [x for row in T for x in row]
    if sorted(values) != list(range(1, len(values) + 1)):
        return False
    for r, row in enumerate(T):
        for c, x in enumerate(row):
            if c > 0 and row[c - 1] >= x:
                return False
            if r > 0 and T[r - 1][c] >= x:
                return False
    return True


def standard_tableaux(shape):
    n = sum(shape)
    result = []
    for perm in permutations(range(1, n + 1)):
        T, pos = [], 0
        for length in shape:
            T.append(list(perm[pos:pos + length]))
            pos += length
        if is_standard(T):
            result.append(T)
    return result

def standard_tableaux_corners(shape):
    remaining = list(shape)
    T = [[0] * length for length in shape]
    result = []
    h = len(shape)

    def fill(k):
        if k == 0:
            result.append([row[:] for row in T])
            return
        for r in range(h):
            below = remaining[r + 1] if r + 1 < h else 0
            if remaining[r] > below:
                c = remaining[r] - 1
                T[r][c] = k
                remaining[r] -= 1
                fill(k - 1)
                remaining[r] += 1
                T[r][c] = 0

    fill(sum(shape))
    return result

def row_insert(T, x):
    result = [list(row) for row in T]
    for row in result:
        for c, y in enumerate(row):
            if y > x:
                row[c], x = x, y
                break
        else:
            row.append(x)
            return result
    result.append([x])
    return result


def reading_word(T):
    return [x for row in reversed(T) for x in row]


def tableau_product_insertion(T, U):
    result = [list(row) for row in T]
    for x in reading_word(U):
        result = row_insert(result, x)
    return result


def skew_shapes(S):
    lam = [len(row) for row in S]
    mu = []
    for row in S:
        count = 0
        for x in row:
            if x is not None:
                break
            count += 1
        mu.append(count)
    while mu and mu[-1] == 0:
        mu.pop()
    return lam, mu


def make_skew(lam, mu, filling):
    S = []
    for r in range(len(lam)):
        start = mu[r] if r < len(mu) else 0
        S.append([None] * start + list(filling[r]))
    return S



def _slide_mut(S, corner):
    r, c = corner
    while True:
        right = S[r][c + 1] if c + 1 < len(S[r]) else None
        down = (S[r + 1][c]
                if r + 1 < len(S) and c < len(S[r + 1]) else None)
        if right is None and down is None:
            S[r].pop()
            if not S[r]:
                S.pop()
            return
        if down is not None and (right is None or down <= right):
            nr, nc = r + 1, c
        else:
            nr, nc = r, c + 1
        S[r][c], S[nr][nc] = S[nr][nc], None
        r, c = nr, nc


def jeu_de_taquin_slide(S, corner):
    result = [list(row) for row in S]
    _slide_mut(result, corner)
    return result


def rectify(S):
    result = [list(row) for row in S]
    lam, mu = skew_shapes(result)
    while mu:
        r = len(mu) - 1
        c = mu[r] - 1
        _slide_mut(result, (r, c))
        mu[r] -= 1
        if mu[r] == 0:
            mu.pop()
    return result


def make_product_skew(T, U):
    width = len(T[0]) if T else 0
    return [[None] * width + list(row) for row in U] + [list(row) for row in T]


def tableau_product_jdt(T, U):
    return rectify(make_product_skew(T, U))


if __name__ == "__main__":
    T = [[1, 3], [2]]
    U = [[1, 2]]
    S = make_skew([4, 3, 2], [2, 1], [[2, 4], [1, 3], [2, 4]])

    print("Partitionen von 75:", partitions(75), len(partitions(75)))
    print("Standardtableaux der Form (3,2):", standard_tableaux_corners([3, 2]))
    print("Row Insertion:", row_insert(T, 1))
    print("Produkt durch Einfuegen:", tableau_product_insertion(T, U))
    print("Produkt durch Jeu de taquin:", tableau_product_jdt(T, U))
    print("Rectification:", rectify(S))
