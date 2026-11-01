
class Tableaux_all:
    """
    Represents all standard tableaux of a given shape (partition).
    """
    def __init__(self, rows):
        self.rows = rows

    def __str__(self):
        return "\n".join(
            " ".join(map(str, row))
            for row in self.rows
        )


def standard_tableaux(partition):
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

            if i > 0 and j >= len(rows[i - 1]):
                continue

            rows[i].append(number)
            generate(rows, remaining[1:])
            rows[i].pop()

    generate([[] for _ in partition], list(range(1, n + 1)))
    return tableaux



#for t in standard_tableaux((3, 1)):
 #   print(t)
  #  print()
