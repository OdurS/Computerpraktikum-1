import thema2 as t
class Tabelaux:
    """Tabellaux Objektorientiert
    """

    def __init__(self, rows):
        self.rows = [list(row) for row in rows]

    def __str__(self):
        return "\n".join(
            " ".join(map(str, row))
            for row in self.rows
        )

    def __repr__(self):
        return f"Tabelle({self.rows})"

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

    def __mul__(self, other):

        if not isinstance(other, Tabelaux):
            return NotImplemented

        result = t.tableau_product_jdt(
            self.rows,
            other.rows
        )

        return Tabelaux(result)


def multiply_tableaux(T, U):

    if not isinstance(T, Tabelaux):
        raise TypeError("T muss ein Tabelle-Objekt sein.")

    if not isinstance(U, Tabelaux):
        raise TypeError("U muss ein Tabelle-Objekt sein.")

    return T * U


def standard_tableaux(partition):#erzeugt alle Standard-Young-Tableaux der gegebenen Form (Partition)

    n = sum(partition)
    tableaux = []

    def generate(rows, remaining):

        if not remaining:
            tableaux.append(Tabelaux([row[:] for row in rows]))
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
T1 = Tabelle([
    [1, 2],
    [3]
])

# Erzeugt ein Tableau mit zwei Zeilen und drei Einträgen.

T2 = Tabelle([
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

alle = standard_tableaux([3, 1])

# Erzeugt alle Standard-Young-Tableaux der Form (3,1).

for T in alle:
    print(T)
    print()

# Gibt alle erzeugten Standard-Young-Tableaux aus.
"""