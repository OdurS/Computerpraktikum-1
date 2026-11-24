import thema2 as t


class TableauBase:
    """Gemeinsame Basis fuer Tableaux: speichert die Zeilen und ihre Darstellung."""

    def __init__(self, rows):
        self.rows = [list(row) for row in rows]

    def __str__(self):
        return "\n".join(
            " ".join(map(str, row))
            for row in self.rows
        )

    def __repr__(self):
        return f"{type(self).__name__}({self.rows})"


class Tableau(TableauBase):
    """Standard-Tableau."""

    def is_tableau(self):

        if not self.rows:
            return False

        lengths = [len(row) for row in self.rows]

        if any(length == 0 for length in lengths):
            return False

        if any(lengths[i] < lengths[i+1]
               for i in range(len(lengths)-1)):
            return False

        numbers = [x for row in self.rows for x in row]
        n = len(numbers)

        if sorted(numbers) != list(range(1, n+1)):
            return False

        for row in self.rows:
            if any(row[i] >= row[i+1]
                   for i in range(len(row)-1)):
                return False

        for i in range(len(self.rows)-1):
            for j in range(len(self.rows[i+1])):
                if self.rows[i][j] >= self.rows[i+1][j]:
                    return False

        return True

    def is_standard(self):
        return self.is_tableau()

    def __eq__(self, other):
        if not isinstance(other, Tableau):
            return NotImplemented
        return self.rows == other.rows

    def __mul__(self, other):

        if not isinstance(other, Tableau):
            return NotImplemented

        result = t.tableau_product_jdt(
            self.rows,
            other.rows
        )

        return Tableau(result)

    def __add__(self, other):

        if not isinstance(other, Tableau):
            return NotImplemented

        return skew_tableaux(self, other)


class SkewTableau(TableauBase):
    """Skew Tableau: None-Eintraege am Zeilenanfang markieren die innere Form."""

    def is_skew(self):
        try:
            t.skew_shapes(self.rows)
        except ValueError:
            return False
        return True

    def shape(self):
        """Gibt die äußere und innere Form als (lambda, mu) zurück."""
        return t.skew_shapes(self.rows)

    def __eq__(self, other):
        if not isinstance(other, SkewTableau):
            return NotImplemented
        return self.rows == other.rows

    def reduce(self):
        """Reduziert das Skew Tableau per Jeu de Taquin zu einem Standardtableau."""
        return Tableau(t.rectify(self.rows))


def skew_tableaux(T, U):
    """Erzeugt das Skew Tableau zum Produkt der Standardtableaux T und U."""

    if not isinstance(T, Tableau):
        raise TypeError("T muss ein Tableau-Objekt sein.")

    if not isinstance(U, Tableau):
        raise TypeError("U muss ein Tableau-Objekt sein.")

    return SkewTableau(t.make_product_skew(T.rows, U.rows))


def multiply_tableaux(T, U):

    if not isinstance(T, Tableau):
        raise TypeError("T muss ein Tableau-Objekt sein.")

    if not isinstance(U, Tableau):
        raise TypeError("U muss ein Tableau-Objekt sein.")

    return T * U


def standard_tableaux(partition):#erzeugt alle Standard-Young-Tableaux der gegebenen Form (Partition)

    n = sum(partition)
    tableaux = []

    def generate(rows, remaining):

        if not remaining:
            tableaux.append(Tableau([row[:] for row in rows]))
            return

        number = n - len(remaining) + 1

        for i, length in enumerate(partition):

            if len(rows[i]) >= length:
                continue

            j = len(rows[i])

            if i > 0 and j >= len(rows[i-1]):
                continue

            rows[i].append(number)

            generate(rows, remaining[1:])

            rows[i].pop()

    generate([[] for _ in partition], list(range(1, n+1)))

    return tableaux


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