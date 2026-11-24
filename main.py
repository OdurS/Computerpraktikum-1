from Benutzeroberfläche.Benutzeroberflaeche_objekt import GUI

from Benutzeroberfläche.Startseite import Startseite_erstellen
from Benutzeroberfläche.Partipitions import Partitions_erstellen
from Benutzeroberfläche.Vergleich import Vergleich_erstellen
from Benutzeroberfläche.Multiplikation import Multiplikation_erstellen
from Benutzeroberfläche.YoungTableaux import YoungTableaux_erstellen
from Benutzeroberfläche.Info import Info_erstellen
from Benutzeroberfläche.Robinson_Schensted import Robinson_Schensted_erstellen

Fenster = GUI(
    Name="Mathematikprojekt",
    Vollbild=True,
    Hintergrund="#202B3C"
)

Seiten = {}

Seiten["Startseite"] = Fenster.add_Seite("Startseite")
Seiten["Partitions"] = Fenster.add_Seite("Partitions")
Seiten["Young Tableaux"] = Fenster.add_Seite("Young Tableaux")
Seiten["Multiplikation"] = Fenster.add_Seite("Multiplikation")
Seiten["Vergleich"] = Fenster.add_Seite("Vergleich")
Seiten["Robinson_Schensted"] = Fenster.add_Seite("Robinson_Schensted")
Seiten["Info"] = Fenster.add_Seite("Info")


Startseite_erstellen(Fenster, Seiten)
Partitions_erstellen(Fenster, Seiten)
Vergleich_erstellen(Fenster, Seiten)
Multiplikation_erstellen(Fenster, Seiten)
YoungTableaux_erstellen(Fenster, Seiten)
Info_erstellen(Fenster, Seiten)
Robinson_Schensted_erstellen(Fenster, Seiten)



if __name__ == "__main__":
    Fenster.zeige(Seiten["Startseite"])
    Fenster.start()