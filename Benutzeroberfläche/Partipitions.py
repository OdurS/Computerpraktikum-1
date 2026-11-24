import tkinter as tk
from .Befehle import befehle_Oberflaeche


def Partitions_erstellen(Fenster, Seiten):

    Partitions = Seiten["Partitions"]

    Befehle = befehle_Oberflaeche()

    Partitions.add_BackButton()
    Partitions.add_HomeButton()

    Partitions.add_Label(
        Name="Titel",
        Text="Partitions",
        Position=(100, 100),
        Groesse=(400, 60),
        Schriftgroesse=28
    )

    Eingabe = Partitions.add_Eingabefeld(
        Name="Eingabe",
        Position=(100, 250),
        Groesse=(500, 45)
    )

    Ausgabe = Partitions.add_Textfeld(
        Name="Ausgabe",
        Text="",
        Position=(100, 390),
        Groesse=(850, 350)
    )

    Scrollbar = tk.Scrollbar(
        Partitions.Frame,
        command=Ausgabe.Widget.yview
    )

    Scrollbar.place(x=950, y=390, height=350)

    Ausgabe.Widget.configure(yscrollcommand=Scrollbar.set)

    def Ausgabe_schreiben(Ergebnis):
        Ausgabe.set_Text(str(Ergebnis))

    def partitionen_berechnen():
        Wert = Eingabe.get_Text()
        Ergebnis = Befehle.partitionen_eingabe(Wert)
        Ausgabe_schreiben(Ergebnis)

    def Beispiel_1():
        Ergebnis = Befehle.partitionen_4()
        Ausgabe_schreiben(Ergebnis)

    def Beispiel_2():
        Ergebnis = Befehle.partitionen_75()
        Ausgabe_schreiben(Ergebnis)

    Partitions.add_Button(
        Name="Ausführen",
        Farbe="#3498DB",
        Befehl=partitionen_berechnen,
        Position=(650, 245),
        Groesse=(180, 55)
    )

    Partitions.add_Button(
        Name="Beispiel 1:4",
        Farbe="#2ECC71",
        Befehl=Beispiel_1,
        Position=(1000, 390),
        Groesse=(180, 55)
    )

    Partitions.add_Button(
        Name="Beispiel 2:75",
        Farbe="#2ECC71",
        Befehl=Beispiel_2,
        Position=(1000, 460),
        Groesse=(180, 55)
    )

    return Partitions