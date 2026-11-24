import tkinter as tk
from .Befehle import befehle_Oberflaeche


def Robinson_Schensted_erstellen(Fenster, Seiten):

    Robinson_Schensted = Seiten["Robinson_Schensted"]

    Befehle = befehle_Oberflaeche()

    Robinson_Schensted.add_BackButton()
    Robinson_Schensted.add_HomeButton()

    Robinson_Schensted.add_Label(
        Name="Titel",
        Text="Robinson-Schensted-Algorithmus",
        Position=(100, 100),
        Groesse=(800, 60),
        Schriftgroesse=28
    )

    Robinson_Schensted.add_Label(
        Name="Hinweis",
        Text="Permutation-Eingabe im Format: (3, 1, 4, 2) oder [3, 1, 4, 2]",
        Position=(100, 180),
        Groesse=(700, 45),
        Schriftgroesse=18
    )

    Eingabe = Robinson_Schensted.add_Eingabefeld(
        Name="Eingabe",
        Position=(100, 250),
        Groesse=(500, 45)
    )

    Ausgabe = Robinson_Schensted.add_Textfeld(
        Name="Ausgabe",
        Text="",
        Position=(100, 390),
        Groesse=(850, 350)
    )

    Scrollbar = tk.Scrollbar(
        Robinson_Schensted.Frame,
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

    def Robinson_Schensted_ausfuehren():

        Wert = Eingabe.get_Text()

        if not Wert.strip():
            Ausgabe_schreiben("Bitte gib eine Permutation ein.")
            return

        try:
            Ergebnis = Befehle.robinson_schensted_eingabe(Wert)
            Ausgabe_schreiben(Ergebnis)

        except Exception as Fehler:
            Ausgabe_schreiben(f"Fehler: {Fehler}")

    def Beispiel_1():
        Ergebnis = Befehle.robinson_schensted_beispiel_1()
        Ausgabe_schreiben(Ergebnis)

    def Beispiel_2():
        Ergebnis = Befehle.robinson_schensted_beispiel_2()
        Ausgabe_schreiben(Ergebnis)

    Robinson_Schensted.add_Button(
        Name="Ausführen",
        Farbe="#3498DB",
        Befehl=Robinson_Schensted_ausfuehren,
        Position=(650, 245),
        Groesse=(180, 55)
    )

    Robinson_Schensted.add_Button(
        Name="Beispiel 1",
        Farbe="#2ECC71",
        Befehl=Beispiel_1,
        Position=(1000, 390),
        Groesse=(180, 55)
    )

    Robinson_Schensted.add_Button(
        Name="Beispiel 2",
        Farbe="#2ECC71",
        Befehl=Beispiel_2,
        Position=(1000, 460),
        Groesse=(180, 55)
    )

    return Robinson_Schensted