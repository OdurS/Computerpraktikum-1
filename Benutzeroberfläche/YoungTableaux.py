import tkinter as tk
from .Befehle import befehle_Oberflaeche


def YoungTableaux_erstellen(Fenster, Seiten):

    YoungTableaux = Seiten["Young Tableaux"]

    Befehle = befehle_Oberflaeche()

    YoungTableaux.add_BackButton()
    YoungTableaux.add_HomeButton()

    YoungTableaux.add_Label(
        Name="Titel",
        Text="Young Tableaux",
        Position=(100, 100),
        Groesse=(600, 60),
        Schriftgroesse=28
    )

    YoungTableaux.add_Label(
        Name="Hinweis",
        Text="Partition-Eingabe im Format: (3,2)",
        Position=(100, 180),
        Groesse=(700, 45),
        Schriftgroesse=18
    )

    Eingabe = YoungTableaux.add_Eingabefeld(
        Name="Eingabe",
        Position=(100, 250),
        Groesse=(500, 45)
    )

    Ausgabe = YoungTableaux.add_Textfeld(
        Name="Ausgabe",
        Text="",
        Position=(100, 390),
        Groesse=(850, 350)
    )

    Scrollbar = tk.Scrollbar(
        YoungTableaux.Frame,
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

    def YoungTableaux_ausfuehren():
        Wert = Eingabe.get_Text()

        if not Wert.strip():
            Ausgabe_schreiben("Bitte gib eine Partition ein.")
            return

        try:
            Ergebnis = Befehle.young_tableaux_eingabe(Wert)
            Ausgabe_schreiben(Ergebnis)

        except Exception as Fehler:
            Ausgabe_schreiben(f"Fehler: {Fehler}")

    def Beispiel_1():
        Ergebnis = Befehle.young_tableaux_beispiel_1()
        Ausgabe_schreiben(Ergebnis)

    def Beispiel_2():
        Ergebnis = Befehle.young_tableaux_beispiel_2()
        Ausgabe_schreiben(Ergebnis)

    YoungTableaux.add_Button(
        Name="Ausführen",
        Farbe="#3498DB",
        Befehl=YoungTableaux_ausfuehren,
        Position=(650, 245),
        Groesse=(180, 55)
    )

    YoungTableaux.add_Button(
        Name="Beispiel 1",
        Farbe="#2ECC71",
        Befehl=Beispiel_1,
        Position=(1000, 390),
        Groesse=(180, 55)
    )

    YoungTableaux.add_Button(
        Name="Beispiel 2",
        Farbe="#2ECC71",
        Befehl=Beispiel_2,
        Position=(1000, 460),
        Groesse=(180, 55)
    )

    return YoungTableaux