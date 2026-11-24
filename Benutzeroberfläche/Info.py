import tkinter as tk


def Info_erstellen(Fenster, Seiten):

    Info = Seiten["Info"]

    Info.add_BackButton()
    Info.add_HomeButton()

    Info.add_Label(
        Name="Titel",
        Text="Informationen zum Mathematikprojekt",
        Position=(100, 70),
        Groesse=(1000, 65),
        Schriftgroesse=28
    )

    Info.add_Label(
        Name="Beispiele_Titel",
        Text="BEISPIELE ÄNDERN",
        Position=(100, 155),
        Groesse=(1000, 40),
        Farbe="#E67E22",
        Textfarbe="white",
        Schriftgroesse=20
    )

    Info.add_Textfeld(
        Name="Beispiele_Text",
        Text="Wenn du die Beispiele der einzelnen Seiten verändern möchtest, öffne den Ordner Benutzeroberfläche und dort die Datei Befehle.py. In der Klasse befehle_Oberflaeche findest du die Methoden, die den jeweiligen Buttons zugeordnet sind. Dort kannst du die Beispielberechnungen und die ausgeführten Befehle ändern.",
        Position=(100, 200),
        Groesse=(1050, 110),
        Farbe="#FDEBD0",
        Textfarbe="#784212",
        Schriftgroesse=14
    )

    Inhalt = Info.add_Textfeld(
        Name="Informationen",
        Text="",
        Position=(100, 340),
        Groesse=(1050, 570),
        Farbe="#202B3C",
        Textfarbe="white",
        Schriftgroesse=14
    )

    Scrollbar = tk.Scrollbar(
        Info.Frame,
        command=Inhalt.Widget.yview
    )

    Scrollbar.place(
        x=1155,
        y=340,
        height=570
    )

    Inhalt.Widget.configure(
        yscrollcommand=Scrollbar.set,
        wrap="word"
    )

    Text = """1. PARTITIONS

Zu einer eingegebenen natürlichen Zahl werden alle Partitionen dieser Zahl berechnet und ausgegeben.


2. MULTIPLIKATION

Hier werden zwei eingegebene Young Tableaux miteinander multipliziert.

Die Eingabe erfolgt beispielsweise im Format:
[[1, 3], [2]]


3. LAUFZEITVERGLEICH

Hier wird die Laufzeit der eigenen Partitionsberechnung mit der Laufzeit des GAP-Befehls Partitions verglichen.

Dazu wird eine Zahl eingegeben und die benötigte Rechenzeit beider Verfahren gegenübergestellt.


4. YOUNG TABLEAUX

Zu einer eingegebenen Partition werden alle Standard Young Tableaux dieser Form ausgegeben.

Die Eingabe erfolgt beispielsweise im Format:
(3,2)


5. ROBINSON-SCHENSTED-ALGORITHMUS

Der Robinson-Schensted-Algorithmus ordnet einer Permutation zwei Standard Young Tableaux P und Q gleicher Form zu.

P entsteht durch das sukzessive Einfügen der Elemente der Permutation mittels Row Insertion.

Q dokumentiert die Reihenfolge, in der die einzelnen Elemente eingefügt werden.

Als Eingabe dient beispielsweise:
(3,1,4,2)
"""

    Inhalt.set_Text(Text)

    return Info