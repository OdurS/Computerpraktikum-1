import tkinter as tk
from .Befehle import befehle_Oberflaeche


def Vergleich_erstellen(Fenster, Seiten):

    Vergleich = Seiten["Vergleich"]

    Befehle = befehle_Oberflaeche()

    Vergleich.add_BackButton()
    Vergleich.add_HomeButton()

    Vergleich.add_Label(
        Name="Titel",
        Text="Laufzeitvergleich",
        Position=(100, 100),
        Groesse=(500, 60),
        Schriftgroesse=28
    )

    Eingabe = Vergleich.add_Eingabefeld(
        Name="Eingabe",
        Position=(100, 250),
        Groesse=(500, 45)
    )

    Ausgabe = Vergleich.add_Textfeld(
        Name="Ausgabe",
        Text="",
        Position=(100, 390),
        Groesse=(850, 350)
    )

    Scrollbar = tk.Scrollbar(
        Vergleich.Frame,
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

    def Laufzeitvergleich():

        Wert = Eingabe.get_Text()

        if not Wert.strip():
            Ausgabe_schreiben("Bitte gib eine Zahl ein.")
            return

        try:
            Wert = int(Wert)

            if Wert < 0:
                Ausgabe_schreiben("Bitte gib eine nichtnegative Zahl ein.")
                return

            Ergebnis = Befehle.partitionen_vergleich(Wert)

            Ausgabe_schreiben(Ergebnis)

        except ValueError:
            Ausgabe_schreiben("Bitte gib eine gültige ganze Zahl ein.")

        except Exception as Fehler:
            Ausgabe_schreiben(f"Fehler: {Fehler}")

    Vergleich.add_Button(
        Name="Vergleich starten",
        Farbe="#3498DB",
        Befehl=Laufzeitvergleich,
        Position=(650, 245),
        Groesse=(220, 55)
    )

    return Vergleich