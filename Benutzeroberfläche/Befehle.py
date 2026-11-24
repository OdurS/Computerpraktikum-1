#Hier werden die Befehle für die Benutzeroberfläche definiert.
import partitionen_vergleich
import thema2
import ast #damit rechnbarer wert

class befehle_Oberflaeche:
    #Partipitions
    def partitionen_eingabe(self, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise TypeError("Die Eingabe muss eine ganze Zahl sein.")

        if n < 0:
            raise ValueError("Die Zahl muss mindestens 0 sein.")

        return thema2.partitions(n)

    def partitionen_4(self):# Partipitions Beispiel 1 
        return thema2.partitions(4)

    def partitionen_75(self): #Partipitions Beispiel 2
        return thema2.partitions(75)
    
    
    #Multiplikation
    
    def tableaux_multiplikation(self, Wert1, Wert2):
        try:
            T = ast.literal_eval(Wert1)
            U = ast.literal_eval(Wert2)
        except Exception:
            raise ValueError("Erwartet werden zwei Tableaux, z. B. [[[1, 3], [2]], [[1, 2]]].")

        return thema2.tableau_product_insertion(T, U)

    def tableaux_beispiel_1(self):  #Multiplikation Beispiel 1
        T = [[1, 3], [2]]
        U = [[1, 2]]

        return thema2.tableau_product_insertion(T, U)

    def tableaux_beispiel_2(self):  #Multiplikation Beispiel 2
        T = [[1, 2], [3]]
        U = [[1, 2]]

        return thema2.tableau_product_jdt(T, U)
    
    #YoungTableaux
    
    def young_tableaux_eingabe(self, Wert):
        try:
            partition = ast.literal_eval(Wert)
        except Exception:
            raise ValueError("Bitte gib eine Partition der Form (3, 2) ein.")

        if not isinstance(partition, (list, tuple)):
            raise TypeError("Die Eingabe muss eine Liste oder ein Tupel sein.")

        return thema2.standard_tableaux_corners(partition)

    def young_tableaux_beispiel_1(self):    ##YoungTableaux Beispiel 1
        return thema2.standard_tableaux_corners((3, 2))

    def young_tableaux_beispiel_2(self):    #YoungTableaux Beispiel 2
        return thema2.standard_tableaux_corners((4, 2, 1))
    
    #Vergleich
    def partitionen_vergleich(self, n):
        return partitionen_vergleich.partitionen_vergleich(n)
    
    #Robinson_Schensted
    def robinson_schensted_eingabe(self, Wert):
        try:
            perm = ast.literal_eval(Wert)
        except Exception:
            raise ValueError("Bitte gib eine gültige Permutation ein, z. B. [3, 1, 4, 2].")

        if not isinstance(perm, (list, tuple)):
            raise TypeError("Die Eingabe muss eine Liste oder ein Tupel sein.")

        return thema2.robinson_schensted(perm)

    def robinson_schensted_beispiel_1(self):#Robinson_Schensted Beispiel 1
        return thema2.robinson_schensted([3, 1, 4, 2])

    def robinson_schensted_beispiel_2(self):#Robinson_Schensted Beispiel 2
        return thema2.robinson_schensted([5, 2, 4, 1, 3])
            
