import tkinter as tk
from .Befehle import befehle_Oberflaeche


def Multiplikation_erstellen(Fenster, Seiten):

    Multiplikation = Seiten["Multiplikation"]

    Befehle = befehle_Oberflaeche()

    Multiplikation.add_BackButton()
    Multiplikation.add_HomeButton()

    Multiplikation.add_Label(
        Name="Titel",
        Text="Multiplikation von Tableaux",
        Position=(100, 100),
        Groesse=(600, 60),
        Schriftgroesse=28
    )
    
    Multiplikation.add_Label(
    Name="Beschriftung_1",
    Text="Erstes Tableau:",
    Position=(100, 215),
    Groesse=(300, 30),
    Schriftgroesse=16
    )

    Multiplikation.add_Label(
        Name="Beschriftung_2",
        Text="Zweites Tableau:",
        Position=(100, 285),
        Groesse=(300, 30),
        Schriftgroesse=16
    )

   

    Eingabe_1 = Multiplikation.add_Eingabefeld(
    Name="Tableau_1",
    Position=(100, 250),
    Groesse=(500, 45)
    )

    Eingabe_2 = Multiplikation.add_Eingabefeld(
        Name="Tableau_2",
        Position=(100, 320),
     Groesse=(500, 45)
    )

    Ausgabe = Multiplikation.add_Textfeld(
        Name="Ausgabe",
        Text="",
        Position=(100, 390),
        Groesse=(850, 350)
    )

    Scrollbar = tk.Scrollbar(
        Multiplikation.Frame,
        command=Ausgabe.Widget.yview
    )

    Scrollbar.place(
        x=950,
        y=390,
        height=350
    )

    Ausgabe.Widget.configure(
        yscrollcommand=Scrollbar.set
    )

    def Ausgabe_schreiben(Ergebnis):
        Ausgabe.set_Text(str(Ergebnis))

    def Multiplikation_ausfuehren():

        Wert_1 = Eingabe_1.get_Text()
        Wert_2 = Eingabe_2.get_Text()

        if not Wert_1.strip() or not Wert_2.strip():
            Ausgabe_schreiben("Bitte gib beide Tableaux ein.")
            return

        try:
            Ergebnis = Befehle.tableaux_multiplikation(Wert_1, Wert_2)
            Ausgabe_schreiben(Ergebnis)

        except Exception as Fehler:
            Ausgabe_schreiben(f"Fehler: {Fehler}")

    def Beispiel_1():
        Ergebnis = Befehle.tableaux_beispiel_1()
        Ausgabe_schreiben(Ergebnis)

    def Beispiel_2():
        Ergebnis = Befehle.tableaux_beispiel_2()
        Ausgabe_schreiben(Ergebnis)

    Multiplikation.add_Button(
        Name="Ausführen",
        Farbe="#3498DB",
        Befehl=Multiplikation_ausfuehren,
        Position=(650, 245),
        Groesse=(180, 55)
    )

    Multiplikation.add_Button(
        Name="Beispiel 1",
        Farbe="#2ECC71",
        Befehl=Beispiel_1,
        Position=(1000, 390),
        Groesse=(180, 55)
    )

    Multiplikation.add_Button(
        Name="Beispiel 2",
        Farbe="#2ECC71",
        Befehl=Beispiel_2,
        Position=(1000, 460),
        Groesse=(180, 55)
    )

    return Multiplikation