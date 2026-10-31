
class Tableau_standard:
    def __init__(self, *parts):
        self.parts = parts
        self.n = sum(parts)

        # Tableau mit Zahlen füllen
        self.entries = []
        number = 1

        for length in parts:
            row = list(range(number, number + length))
            self.entries.append(row)
            number += length

    def __str__(self):
        return "\n".join(
            " ".join(map(str, row))
            for row in self.entries
        )



#t = Tableau(3, 1)

