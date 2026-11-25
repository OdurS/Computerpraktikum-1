from bisect import bisect_right

## Alle Operationen (tuple, any) sind O(n),
## wobei n die Anzahl der Zeilen ist
## Insgesamt also O(n)
def _shape(shape):
    try:
        shape = tuple(shape)
    except TypeError as fehler:
        raise ValueError("Die Form muss eine Folge positiver ganzer Zahlen sein.") from fehler
    if any(type(x) is not int or x <= 0 for x in shape):
        raise ValueError("Die Zeilenlängen müssen positive ganze Zahlen sein.")
    if any(a < b for a, b in zip(shape, shape[1:])):
        raise ValueError("Eine untere Zeile darf nicht länger als die darüber sein.")
    return shape


def outer_corners(shape):
    shape = _shape(shape)
    return [(r, length - 1) for r, length in enumerate(shape)
            if r + 1 == len(shape) or length > shape[r + 1]]


def is_semistandard(T):
    if not isinstance(T, (list, tuple)):
        return False
    for r, row in enumerate(T):
        if not isinstance(row, (list, tuple)):
            return False
        if not row or (r and len(row) > len(T[r - 1])):
            return False
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
        raise ValueError("Erwartet wird ein semistandard Tableau mit positiven ganzen Einträgen.")


## Sei N die Anzahl der Elemente in T und M die Anzahl der Elemente in U
## und L das Produkt der Länge der ersten Zeile und ersten Spalte von
## jeweils T und U.
## Dann ist diese Funktion O(N+M+L)
def make_product_skew(T, U):
    _check_tableau(T)
    _check_tableau(U)
    width = len(T[0]) if T else 0
    return ([[None] * width + list(row) for row in U]
            + [list(row) for row in T])

#TODO: Laufzeit
def tableau_product_jdt(T, U):
    return rectify(make_product_skew(T,U))


## Im besten Fall ist x größer als das letzte Element der ersten Reihe und es wird beim
## append keine Kopie gemacht, wodurch die Funktion O(1) im Bestfall ist.
## Im schlechtesten Fall muss für jede Reihe durch die Reihe gesucht werden und ein append mit Kopie gemacht werden.
## Das hat Zeitkomplexität O(R * (log_2(n) + n_R)) = O(Rn_R) = O(N), wobei der log_2 Term durch das binary search kommt und R
## Die Anzahl der Reihen und n_R die Anzahl der Elemente in Spalte R ist. N ist also die Anzahl der Elemente in T.
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
    """Fügt x in T ein und gibt ein neues Tableau zurück."""
    _check_tableau(T)
    if type(x) is not int or x < 1:
        raise ValueError("Der neue Eintrag muss eine positive ganze Zahl sein.")
    result = [list(row) for row in T]
    _row_insert(result, x)
    return result


## TODO: Zeitkomplexität
def tableau_product_insertion(T, U):
    _check_tableau(T)
    _check_tableau(U)
    result = [list(row) for row in T]
    for row in reversed(U):
        for x in row:
            _row_insert(result, x)
    return result


## Diese Funktion kann grob durch die innere Schleife 'for c in range(...'
## abgeschätz werden. Dessen Innere verläuft in Konstanter Zeit und
## die Schleife iteriert über alle Elemente in einer Reihe
## für jede Reihe und ist somit O(N), wobei N die Anzahl der Elemente in S ist.
## Die Schleife 'while start < len(...' ist auch O(N), da im schlimmsten Fall über
## jeden Eintrag in einer Reihe iteriert wird, für jede Reihe.
## Desweiteren gilt offensichtlich mu <= lam (also mu liegt in mu), hat also weniger
## Elemente. Dadurch folgt, dass die letzte Schleife auch durch O(N) begrenzt ist.
def skew_shapes(S):
    if not isinstance(S, (list, tuple)) or any(
        not isinstance(row, (list, tuple)) for row in S
    ):
        raise ValueError("S muss eine Liste von Zeilen sein.")
    lam = list(_shape(len(row) for row in S))
    mu = []
    for r, row in enumerate(S):
        start = 0
        while start < len(row) and row[start] is None:
            start += 1
        if r and start > mu[-1]:
            raise ValueError("Die inneren Zeilenlängen müssen absteigend geordnet sein.")
        mu.append(start)
        for c in range(start, len(row)):
            x = row[c]
            if type(x) is not int or x < 1:
                raise ValueError("None darf nur am Zeilenanfang stehen. Jeder Eintrag muss eine positive ganze Zahl sein.")
            if c > start and row[c - 1] > x:
                raise ValueError("Die Einträge jeder Zeile müssen schwach steigen.")
            if r and S[r - 1][c] is not None and S[r - 1][c] >= x:
                raise ValueError("Die Einträge jeder Spalte müssen streng steigen.")
    while mu and mu[-1] == 0:
        mu.pop()
    return lam, mu


## Die ersten 6 Zeilen sind jeweils abschätzbar durch die Anzahl der Reihen.
## Hierbei gilt aber insbesonderst, dass lambda die meisten Zeilen hat. Ingesamt
## Sind die ersten 6 Zeilen also durch die Anzahl der Reihen von lambda abschätzbar.
## Die Schleife iteriert über alle Reihen von lambda und der append aufruf kopiert genau length
## Elemente (also die Anzahl der Elemente in einer Reihe von lambda). Damit ist die Schleife
## O(N), wobei N wieder die Anzahl aller Elemente in lambda ist. Zuletzt ist skew_shapes auch O(N)
## Ingesamt ist diese Funktion also O(R + N + N) = O(N), wobei R die Anzahl der Zeilen von lambda ist.
def make_skew(lam, mu, filling):
    lam, mu = _shape(lam), _shape(mu)
    if len(mu) > len(lam) or any(a > b for a, b in zip(mu, lam)):
        raise ValueError("Die innere Form muss in der äußeren Form liegen.")
    try:
        filling = [list(row) for row in filling]
    except TypeError as fehler:
        raise ValueError("Die Füllung muss eine Folge von Zeilen sein.") from fehler
    if len(filling) != len(lam):
        raise ValueError("Die Anzahl der Füllungszeilen passt nicht zur Form.")
    result = []
    for r, length in enumerate(lam):
        start = mu[r] if r < len(mu) else 0
        if len(filling[r]) != length - start or None in filling[r]:
            raise ValueError(f"In Zeile {r} werden genau {length - start} Zahlen erwartet.")
        result.append([None] * start + filling[r])
    skew_shapes(result)
    return result


def inner_corners(S):
    _, mu = skew_shapes(S)
    return outer_corners(mu)


## Im schlimmsten Fall muss die innere Ecke von (0,0) 
## zunächst nach ganz unten (R,0) und danach nach ganz rechts (R,L) ziehen (oder anderstherum)
## Das ist also ingesamt O(R+L) mal ziehen, wobei R die Anzahl der Reihen und
## L die Länge der Spalten ist. Der schlimmste Fall tritt also nur ein, 
## wenn S ein Rechteck ist.
def _slide(S, corner):
    r, c = corner
    while True:
        right = S[r][c + 1] if c + 1 < len(S[r]) else None
        down = S[r + 1][c] if r + 1 < len(S) and c < len(S[r + 1]) else None
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


## Erbt Zeitkomplexität von der Helferfunktion _slide, da
## der tuple aufruf und `result ..` beschränkt ist durch jeweils
## 2 und R, der Anzahl der Reihen von S, wobei offensichtlich R <= R+L gilt.
## Ingesamt ist es also O(R + R+ L) = O(R+L) = O(_shape)
def jeu_de_taquin_slide(S, corner):
    try:
        corner = tuple(corner)
    except TypeError as fehler:
        raise ValueError("Der Startpunkt muss ein Paar (Zeile, Spalte) sein.") from fehler
    if (len(corner) != 2 or any(type(x) is not int for x in corner)
            or corner not in inner_corners(S)):
        raise ValueError("Der Startpunkt muss eine entfernbare Ecke der inneren Form sein.")
    result = [list(row) for row in S]
    _slide(result, corner)
    return result


## rectify muss pro innere Ecke einmal slide ausführen
## Das ist also O(|mu| * (n+m)), wobei mu die Form
## der inneren Ecken ist und |mu| die Summe der entsprechenden Partition
def rectify(S):
    _, mu = skew_shapes(S)
    rows = [list(row) for row in S]
    while mu:
        r = len(mu) - 1
        _slide(rows, (r, mu[r] - 1))
        mu[r] -= 1
        if mu[r] == 0:
            mu.pop()
    return rows


# TODO: Add new test that checks for completeness
## Pro 
## In diesem Fall ist es O(R * log_2(n) * n)
## Wobei der log_2 Term von dem binary Search kommt (schneller als naive Suche)
def robinson_schensted(perm):
    """Fügt eine Folge paarweise verschiedener positiver ganzer Zahlen ein."""
    try:
        perm = list(perm)
    except TypeError as fehler:
        raise ValueError("Die Eingabe muss eine Folge positiver ganzer Zahlen sein.") from fehler
    seen = set()
    for x in perm:
        if type(x) is not int or x < 1:
            raise ValueError("Die Eingabe darf nur positive ganze Zahlen enthalten.")
        if x in seen:
            raise ValueError(f"Die Zahl {x} kommt mehrfach vor.")
        seen.add(x)

    P, Q = [], []
    for k, x in enumerate(perm, start=1):
        r, _ = _row_insert(P, x)
        if r == len(Q):
            Q.append([])
        Q[r].append(k)
    return P, Q
