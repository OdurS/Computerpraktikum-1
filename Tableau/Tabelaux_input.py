
class Tableau_input:
    def __init__(self, rows):
        self.rows = rows

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



#T1 = Tableau([
 #   [1, 2, 4],
  #  [3]
#])

#T2 = Tableau([
 #   [1, 3, 2],
  #  [4]
#])


