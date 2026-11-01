#NUtzen?
class Tableaux:
    def __init__(self, *parts):
        self.parts = parts

    def __str__(self):
        return "\n".join("□" * n for n in self.parts)



# t = Tableau(3, 1)

