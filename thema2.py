from bisect import bisect_right


def _integer(n):
    if type(n) is not int:
        raise TypeError("n muss eine ganze Zahl sein.")


def _shape(shape):
    shape = tuple(shape)
    if any(type(x) is not int or x <= 0 for x in shape):
        raise ValueError("Die Form muss eine Partition mit positiven Teilen sein.")
    if any(a < b for a, b in zip(shape, shape[1:])):
        raise ValueError("Die Zeilenlaengen muessen absteigend geordnet sein.")
    return shape


def rec_partitions(n):
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


def _rec_partitions(n):
    _integer(n)
    if n < 0:
        return iter(())
    if n == 0:
        return iter(((),))
    return (tuple(reversed(part)) for part in rec_partitions(n))


def partitions(n):
    return list(_rec_partitions(n))


def count_partitions(n):
    _integer(n)
    if n < 0:
        return 0
    counts = [1] + [0] * n
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]


def is_semistandard(T):
    previous_length = None
    for r, row in enumerate(T):
        if not row or (previous_length is not None and len(row) > previous_length):
            return False
        previous_length = len(row)
        for c, x in enumerate(row):
            if type(x) is not int or x < 1:
                return False
            if c and row[c - 1] > x:
                return False
            if r and T[r - 1][c] >= x:
                return False
    return True


def _check_tableau(T):
    if not is_semistandard(T):
        raise ValueError("Erwartet wird ein semistandard Tableau mit positiven ganzen Eintraegen.")


def outer_corners(shape):
    shape = _shape(shape)
    return [(r, length - 1) for r, length in enumerate(shape)
            if r + 1 == len(shape) or length > shape[r + 1]]


def standard_tableaux_corners(shape):
    shape = _shape(shape)
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


def standard_tableaux(n_or_shape):
    result = []
    for shape in partitions(n_or_shape):
        result.extend(standard_tableaux_corners(shape))
    return result



def _row_insert(T, x):
    for r, row in enumerate(T):
        if x >= row[-1]:
            row.append(x)
            return r, len(row) - 1
        c = 0 if x < row[0] else bisect_right(row, x)
        row[c], x = x, row[c]
    T.append([x])
    return len(T) - 1, 0


def row_insert(T, x):
    _check_tableau(T)
    if type(x) is not int or x < 1:
        raise ValueError("Der neue Eintrag muss eine positive ganze Zahl sein.")
    result = [list(row) for row in T]
    _row_insert(result, x)
    return result


def reading_word(T):
    _check_tableau(T)
    return [x for row in reversed(T) for x in row]


def tableau_product_insertion(T, U):
    _check_tableau(T)
    _check_tableau(U)
    result = [list(row) for row in T]
    for row in reversed(U):
        for x in row:
            _row_insert(result, x)
    return result


def skew_shapes(S):
    lam = list(_shape(len(row) for row in S))
    mu = []
    for r, row in enumerate(S):
        start = 0
        while start < len(row) and row[start] is None:
            start += 1
        if r and start > mu[-1]:
            raise ValueError("Die inneren Zeilenlaengen muessen absteigend sein.")
        mu.append(start)
        for c in range(start, len(row)):
            x = row[c]
            if type(x) is not int or x < 1:
                raise ValueError("None ist nur am Zeilenanfang erlaubt; Eintraege muessen positiv sein.")
            if c > start and row[c - 1] > x:
                raise ValueError("Die Zeilen muessen schwach aufsteigend sein.")
            if r and S[r - 1][c] is not None and S[r - 1][c] >= x:
                raise ValueError("Die Spalten muessen streng aufsteigend sein.")
    while mu and mu[-1] == 0:
        mu.pop()
    return lam, mu


def make_skew(lam, mu, filling):
    lam, mu = _shape(lam), _shape(mu)
    if len(mu) > len(lam) or any(a > b for a, b in zip(mu, lam)):
        raise ValueError("Die innere Form muss in der aeusseren Form liegen.")
    filling = [list(row) for row in filling]
    if len(filling) != len(lam):
        raise ValueError("Die Anzahl der Fuellungszeilen passt nicht zur Form.")
    result = []
    for r, length in enumerate(lam):
        start = mu[r] if r < len(mu) else 0
        if len(filling[r]) != length - start:
            raise ValueError("Die Anzahl der Eintraege passt nicht zur Schiefform.")
        result.append([None] * start + filling[r])
    skew_shapes(result)
    return result


def inner_corners(S):
    _, mu = skew_shapes(S)
    return outer_corners(mu)


def _slide(S, corner):
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
    corner = tuple(corner)
    if (len(corner) != 2 or any(type(x) is not int for x in corner)
            or corner not in inner_corners(S)):
        raise ValueError("Der Startpunkt muss eine entfernbare Ecke der inneren Form sein.")
    result = [list(row) for row in S]
    _slide(result, corner)
    return result


def rectify(S):
    _, mu = skew_shapes(S)
    result = [list(row) for row in S]
    while mu:
        r = len(mu) - 1
        _slide(result, (r, mu[r] - 1))
        mu[r] -= 1
        if mu[r] == 0:
            mu.pop()
    return result


def make_product_skew(T, U):
    _check_tableau(T)
    _check_tableau(U)
    width = len(T[0]) if T else 0
    return [[None] * width + list(row) for row in U] + [list(row) for row in T]


def tableau_product_jdt(T, U):
    S = make_product_skew(T, U)
    return rectify(S)


def robinson_schensted(perm):
    perm = list(perm)
    n = len(perm)
    seen = bytearray(n + 1)
    for x in perm:
        if type(x) is not int or not 1 <= x <= n or seen[x]:
            raise ValueError("Eingabe muss eine Permutation von 1,...,n sein.")
        seen[x] = 1

    P, Q = [], []
    for k, x in enumerate(perm, start=1):
        r, _ = _row_insert(P, x)
        if r == len(Q):
            Q.append([])
        Q[r].append(k)
    return P, Q





if __name__ == "__main__":
    T = [[1, 3], [2]]
    U = [[1, 2]]
    S = make_skew([4, 3, 2], [2, 1], [[2, 4], [1, 3], [2, 4]])

    print("Partitionen von 5:", partitions(5))
    print("Anzahl Partitionen von 75:", count_partitions(75))
    print("Standardtableaux (3,2):", standard_tableaux([3, 2]))
    print("Row Insertion:", row_insert(T, 1))
    print("Produkt durch Einfuegen:", tableau_product_insertion(T, U))
    print("Produkt durch Jeu de taquin:", tableau_product_jdt(T, U))
    print("Rectification:", rectify(S))
    print("Robinson-Schensted (P,Q):", robinson_schensted([3, 1, 4, 2]))
