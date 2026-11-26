try:
    from . import tableau as t
    from . import partitions as part
except ImportError:  # direkter Start aus dem src-Ordner
    import tableau as t
    import partitions as part

"""Dünner Wrapper um tableau.py, wo alle Implementationen sind"""


def _nichtnegative_ganzzahl(n):
    if type(n) is not int or n < 0:
        raise ValueError("n muss eine nichtnegative ganze Zahl sein.")


class TableauBase:
    """Gemeinsame Basis für Tableaux: speichert die Zeilen und ihre Darstellung."""

    def __init__(self, rows):
        try:
            self.rows = [list(row) for row in rows]
        except TypeError as fehler:
            raise ValueError("Ein Tableau muss eine Folge von Zeilen sein.") from fehler

    def __str__(self):
        if not self.rows:
            return "∅"

        def zelle(x):
            return "·" if x is None else str(x)

        width = max((len(zelle(x)) for row in self.rows for x in row), default=1)
        lines = []
        for row in self.rows:
            lines.append(" ".join(zelle(x).rjust(width) for x in row))
        return "\n".join(lines)

    def __repr__(self):
        return f"{type(self).__name__}({self.rows!r})"


class Tableau(TableauBase):
    """Standard-Tableau."""

    def __init__(self, rows):
        try:
            rows = [list(row) for row in rows]
        except TypeError as fehler:
            raise ValueError("Ein Tableau muss eine Folge von Zeilen sein.") from fehler
        t._check_tableau(rows)
        self.rows = rows

    def __eq__(self, other):
        if not isinstance(other, Tableau):
            return NotImplemented
        return self.rows == other.rows

    @property
    def shape(self):
        return tuple(len(row) for row in self.rows)

    def is_tableau(self):
        if not self.rows:
            return True
        prev = self.shape[0]
        for cur in self.shape:
            if prev < cur:
                return False
            prev = cur
        return True

    def is_semistandard(self):
        return t.is_semistandard(self.rows)

    def is_standard(self):
        if not self.is_semistandard():
            return False
        n = sum(self.shape)
        seen = bytearray(n + 1)
        for row in self.rows:
            for x in row:
                if x > n or seen[x]:
                    return False
                seen[x] = 1
        return True

    @classmethod
    def Robinson_schensted(cls, perm):
        P, Q = t.robinson_schensted(perm)
        return cls(P), cls(Q)

    @classmethod
    def Standard_Tableaux(cls, n):
        _nichtnegative_ganzzahl(n)
        return list(cls.Iter_Standard_Tableaux(n))

    @classmethod
    def Iter_Standard_Tableaux(cls, n):
        _nichtnegative_ganzzahl(n)
        for shape in part.partitions(n):
            yield from cls.Iter_Standard_Tableaux_Corners(shape)

    @classmethod
    def Standard_Tableaux_Corners(cls, shape):
        return list(cls.Iter_Standard_Tableaux_Corners(shape))

    @classmethod
    def Iter_Standard_Tableaux_Corners(cls, shape):
        shape = t._shape(shape)
        remaining = list(shape)
        rows = [[0] * length for length in shape]
        h = len(shape)

        def fill(k):
            if k == 0:
                yield cls(rows)
                return
            for r in range(h):
                below = remaining[r + 1] if r + 1 < h else 0
                if remaining[r] > below:
                    c = remaining[r] - 1
                    rows[r][c] = k
                    remaining[r] -= 1
                    yield from fill(k - 1)
                    remaining[r] += 1

        yield from fill(sum(shape))

    def outer_corners(self):
        return t.outer_corners(self.shape)

    def row_insert(self, x):
        return Tableau(t.row_insert(self.rows, x))

    def reading_word(self):
        return [x for row in reversed(self.rows) for x in row]

    def tableau_product_insertion(self, U):
        if not isinstance(U, Tableau):
            raise TypeError("U muss ein Tableau-Objekt sein.")
        return Tableau(t.tableau_product_insertion(self.rows, U.rows))

    def tableau_product_jdt(self, U):
        if not isinstance(U, Tableau):
            raise TypeError("U muss ein Tableau-Objekt sein.")
        return Tableau(t.tableau_product_jdt(self.rows, U.rows))


    def __mul__(self, other):
        if not isinstance(other, Tableau):
            return NotImplemented

        return (self + other).rectify()

    def __add__(self, other):
        if not isinstance(other, Tableau):
            return NotImplemented

        return SkewTableau.Skew_Tableaux(self, other)


class SkewTableau(TableauBase):
    """Skew Tableau: None-Eintraege am Zeilenanfang markieren die innere Form."""

    def __init__(self, rows):
        try:
            rows = [list(row) for row in rows]
        except TypeError as fehler:
            raise ValueError("Ein schiefes Tableau muss eine Folge von Zeilen sein.") from fehler
        t.skew_shapes(rows)
        self.rows = rows

    @classmethod
    def Skew_Tableaux(cls,T, U):
        """Erzeugt das Skew Tableau zum Produkt der Standardtableaux T und U."""
    
        if not isinstance(T, Tableau):
            raise TypeError("T muss ein Tableau-Objekt sein.")
    
        if not isinstance(U, Tableau):
            raise TypeError("U muss ein Tableau-Objekt sein.")

        return SkewTableau(t.make_product_skew(T.rows, U.rows))

    @classmethod
    def Skew_Shape(cls,lam, mu, filling):
        """Erzeugt das Skew-Tableau mit gegebener Form lambda/mu und Einträgen aus Filling"""
        return SkewTableau(t.make_skew(lam, mu, filling))

    def is_skew(self):
        try:
            t.skew_shapes(self.rows)
        except (TypeError, ValueError):
            return False
        return True

    @property
    def shape(self):
        """Gibt die äußere und innere Form als (lambda, mu) zurück."""
        return t.skew_shapes(self.rows)
    
    def inner_corners(self):
        return t.inner_corners(self.rows)

    def __eq__(self, other):
        if not isinstance(other, SkewTableau):
            return NotImplemented
        return self.rows == other.rows

    def jeu_de_taquin(self, x):
        return SkewTableau(t.jeu_de_taquin_slide(self.rows, x))

    def rectify(self):
        """Reduziert das Skew Tableau per Jeu de Taquin zu einem Standardtableau."""
        return Tableau(t.rectify(self.rows))


#Beispiele
"""
T1 = Tableau([
    [1, 2],
    [3]
])

# Erzeugt ein Tableau mit zwei Zeilen und drei Einträgen.

T2 = Tableau([
    [1, 2],
    [3]
])

# Erzeugt ein zweites Tableau.

print(T1.is_tableau())

# Überprüft, ob T1 ein gültiges Young-Tableau ist.

print(T1.is_standard())

# Überprüft, ob T1 ein Standard-Young-Tableau ist.

T3 = multiply_tableaux(T1, T2)

# Multipliziert T1 und T2 mithilfe einer eigenständigen Funktion.

T4 = T1 * T2

# Multipliziert T1 und T2 mithilfe des überladenen Multiplikationsoperators.

print(T3 == T4)

# Überprüft, ob beide Multiplikationen dasselbe Tableau liefern.

alle = standard_tableaux([3, 1])

# Erzeugt alle Standard-Young-Tableaux der Form (3,1).

for T in alle:
    print(T)
    print()

# Gibt alle erzeugten Standard-Young-Tableaux aus.
"""


#Beispiele für Skew-Tableaux

"""
S = SkewTableau([
    [None, 1, 2],
    [None, 3],
    [4]
])

# Erzeugt ein Skew-Tableau der Form (3,2,1)/(1,1).

print(S.is_skew())

# Überprüft, ob S ein gültiges Skew-Tableau ist.

print(S.reduce())

# Reduziert S per Jeu de Taquin zu einem Standard-Young-Tableau.

T1 = Tableau([
    [1, 2],
    [3]
])

T2 = Tableau([
    [1, 2],
    [3]
])

S1 = skew_tableaux(T1, T2)

# Erzeugt das Skew-Tableau zum Produkt von T1 und T2.

S2 = T1 + T2

# Erzeugt dasselbe Skew-Tableau mithilfe des überladenen Additionsoperators.

print(S1 == S2)

# Überprüft, ob beide Konstruktionen dasselbe Skew-Tableau liefern.

print(S1.reduce())

# Reduziert das Skew-Produkt per Jeu de Taquin zu einem geraden Tableau.

print(S.shape())

# Gibt die äußere und innere Form von S als (lambda, mu) zurück.
"""
