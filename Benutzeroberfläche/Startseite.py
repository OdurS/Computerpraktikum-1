def Startseite_erstellen(Fenster, Seiten):

    Startseite = Seiten["Startseite"]

    Startseite.add_Button(
        Name="Partitions",
        Farbe="#3498DB",
        Befehl=lambda: Fenster.zeige(Seiten["Partitions"]),
        Position=(150, 220),
        Groesse=(300, 70)
    )

    Startseite.add_Button(
        Name="Young Tableaux",
        Farbe="#2ECC71",
        Befehl=lambda: Fenster.zeige(Seiten["Young Tableaux"]),
        Position=(150, 320),
        Groesse=(300, 70)
    )

    Startseite.add_Button(
        Name="Multiplikation",
        Farbe="#9B59B6",
        Befehl=lambda: Fenster.zeige(Seiten["Multiplikation"]),
        Position=(150, 420),
        Groesse=(300, 70)
    )

    Startseite.add_Button(
        Name="Vergleich",
        Farbe="#E67E22",
        Befehl=lambda: Fenster.zeige(Seiten["Vergleich"]),
        Position=(550, 220),
        Groesse=(300, 70)
    )

    Startseite.add_Button(
        Name="Robinson-Schensted",
        Farbe="#16A085",
        Befehl=lambda: Fenster.zeige(Seiten["Robinson_Schensted"]),
        Position=(550, 320),
        Groesse=(300, 70)
    )

    Startseite.add_Button(
        Name="Info",
        Farbe="#7F8C8D",
        Befehl=lambda: Fenster.zeige(Seiten["Info"]),
        Position=(550, 420),
        Groesse=(300, 70)
    )

    return Startseite