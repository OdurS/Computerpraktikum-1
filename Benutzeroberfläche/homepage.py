import tkinter as tk


# ============================================================
# 1. EINSTELLUNGEN
# ============================================================

HINTERGRUND = "#202B3C"
BUTTON_FARBE = "#3498DB"
BUTTON_HOVER = "#2980B9"
TEXT_FARBE = "#FFFFFF"
ZURUECK_FARBE = "#E67E22"
START_FARBE = "#16A085"

SCHRIFTART = "Arial"
SCHRIFTGROESSE = 16


# ============================================================
# 2. HAUPTFENSTER ERSTELLEN
# ============================================================

fenster = tk.Tk()

fenster.title("Mein Matheprojekt")

# Vollbild aktivieren
fenster.attributes("-fullscreen", True)

# Hintergrundfarbe
fenster.configure(bg=HINTERGRUND)

# Bildschirmgröße ermitteln
fenster.update_idletasks()

BREITE = fenster.winfo_screenwidth()
HOEHE = fenster.winfo_screenheight()

# Escape beendet das Programm
fenster.bind("<Escape>", lambda event: fenster.destroy())


# ============================================================
# 3. SEITENVERWALTUNG
# ============================================================

# Hier werden alle Seiten gespeichert
seiten = {}

# Hier wird der Verlauf der besuchten Seiten gespeichert
seiten_verlauf = []


def seite_erstellen(name):
    """
    Erstellt eine neue Seite im Hauptfenster.
    Jede Seite wird nur einmal erstellt.
    """

    seite = tk.Frame(
        fenster,
        bg=HINTERGRUND
    )

    # Die Seite füllt das gesamte Fenster aus
    seite.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    # Seite speichern
    seiten[name] = seite

    return seite


def seite_anzeigen(name):
    """
    Zeigt eine Seite an und speichert den Seitenverlauf.
    """

    if name not in seiten:
        print(f"Fehler: Die Seite '{name}' existiert nicht.")
        return

    # Aktuelle Seite nicht doppelt in den Verlauf schreiben
    if not seiten_verlauf or seiten_verlauf[-1] != name:
        seiten_verlauf.append(name)

    # Seite in den Vordergrund holen
    seiten[name].tkraise()


def zurueck():
    """
    Kehrt zur vorherigen Seite zurück.
    """

    if len(seiten_verlauf) > 1:

        # Aktuelle Seite aus dem Verlauf entfernen
        seiten_verlauf.pop()

        # Vorherige Seite anzeigen
        vorherige_seite = seiten_verlauf[-1]
        seiten[vorherige_seite].tkraise()

    else:
        # Wenn keine vorherige Seite existiert,
        # zur Startseite wechseln
        seiten["start"].tkraise()

        # Verlauf auf die Startseite zurücksetzen
        seiten_verlauf.clear()
        seiten_verlauf.append("start")


def zur_startseite():
    """
    Kehrt unabhängig vom Verlauf direkt zum Hauptmenü zurück.
    """

    seiten_verlauf.clear()
    seiten_verlauf.append("start")

    seiten["start"].tkraise()


# ============================================================
# 4. BUTTON-FUNKTION
# ============================================================

def button_erstellen(
    seite,
    text,
    x,
    y,
    breite,
    hoehe,
    aktion,
    farbe=BUTTON_FARBE
):
    """
    Erstellt einen Button.

    seite   = Auf welcher Seite soll er erscheinen?
    text    = Beschriftung des Buttons
    x       = Position von links
    y       = Position von oben
    breite  = Breite des Buttons
    hoehe   = Höhe des Buttons
    aktion  = Funktion beim Anklicken
    farbe   = Hintergrundfarbe
    """

    button = tk.Button(
        seite,
        text=text,
        command=aktion,

        bg=farbe,
        fg=TEXT_FARBE,

        activebackground=BUTTON_HOVER,
        activeforeground=TEXT_FARBE,

        font=(SCHRIFTART, SCHRIFTGROESSE, "bold"),

        relief="flat",
        cursor="hand2",
        bd=0
    )

    # Position und Größe festlegen
    button.place(
        x=x,
        y=y,
        width=breite,
        height=hoehe
    )

    return button


# ============================================================
# 5. STANDARD-BUTTONS FÜR UNTERSEITEN
# ============================================================

def navigationsbuttons_erstellen(seite):
    """
    Erstellt auf einer Unterseite zwei Buttons:
    - Zurück zur vorherigen Seite
    - Direkt zur Startseite
    """

    button_erstellen(
        seite=seite,
        text="← Zurück",
        x=30,
        y=30,
        breite=180,
        hoehe=55,
        aktion=zurueck,
        farbe=ZURUECK_FARBE
    )

    button_erstellen(
        seite=seite,
        text="⌂ Startseite",
        x=230,
        y=30,
        breite=200,
        hoehe=55,
        aktion=zur_startseite,
        farbe=START_FARBE
    )


# ============================================================
# 6. STARTSEITE ERSTELLEN
# ============================================================

startseite = seite_erstellen("start")


# Überschrift
tk.Label(
    startseite,
    text="MEIN MATHEPROJEKT",
    font=("Arial", 34, "bold"),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    y=70,
    anchor="n"
)


# Untertitel
tk.Label(
    startseite,
    text="Wähle ein Thema aus",
    font=("Arial", 18),
    bg=HINTERGRUND,
    fg="#BDC3C7"
).place(
    relx=0.5,
    y=130,
    anchor="n"
)


# ------------------------------------------------------------
# BUTTON 1: GRUNDRECHENARTEN
# ------------------------------------------------------------

button_erstellen(
    seite=startseite,
    text="Grundrechenarten",
    x=100,
    y=220,
    breite=300,
    hoehe=75,
    aktion=lambda: seite_anzeigen("rechnen"),
    farbe="#3498DB"
)


# ------------------------------------------------------------
# BUTTON 2: GEOMETRIE
# ------------------------------------------------------------

button_erstellen(
    seite=startseite,
    text="Geometrie",
    x=100,
    y=320,
    breite=300,
    hoehe=75,
    aktion=lambda: seite_anzeigen("geometrie"),
    farbe="#27AE60"
)


# ------------------------------------------------------------
# BUTTON 3: FORMELSAMMLUNG
# ------------------------------------------------------------

button_erstellen(
    seite=startseite,
    text="Formelsammlung",
    x=100,
    y=420,
    breite=300,
    hoehe=75,
    aktion=lambda: seite_anzeigen("formeln"),
    farbe="#8E44AD"
)


# ------------------------------------------------------------
# BUTTON 4: BEISPIEL FÜR EINE WEITERE SEITE
# ------------------------------------------------------------

button_erstellen(
    seite=startseite,
    text="Wahrscheinlichkeit",
    x=450,
    y=220,
    breite=300,
    hoehe=75,
    aktion=lambda: seite_anzeigen("wahrscheinlichkeit"),
    farbe="#D35400"
)


# ------------------------------------------------------------
# BUTTON 5: PROGRAMM BEENDEN
# ------------------------------------------------------------

button_erstellen(
    seite=startseite,
    text="Programm beenden",
    x=100,
    y=550,
    breite=300,
    hoehe=65,
    aktion=fenster.destroy,
    farbe="#C0392B"
)


# ============================================================
# 7. BEISPIELSEITE: GRUNDRECHENARTEN
# ============================================================

rechnenseite = seite_erstellen("rechnen")

navigationsbuttons_erstellen(rechnenseite)


# Überschrift
tk.Label(
    rechnenseite,
    text="Grundrechenarten",
    font=("Arial", 30, "bold"),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    y=130,
    anchor="n"
)


# Beispielinhalt
tk.Label(
    rechnenseite,
    text="Hier kannst du deine Rechenaufgaben einfügen.",
    font=("Arial", 20),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    rely=0.4,
    anchor="center"
)


# Beispiel: zusätzlicher Button auf dieser Seite
button_erstellen(
    seite=rechnenseite,
    text="Beispiel berechnen",
    x=BREITE // 2 - 150,
    y=HOEHE // 2 + 60,
    breite=300,
    hoehe=65,
    aktion=lambda: tk.messagebox.showinfo(
        "Beispiel",
        "Hier kannst du später eine Berechnung programmieren."
    ),
    farbe="#2980B9"
)


# ============================================================
# 8. BEISPIELSEITE: GEOMETRIE
# ============================================================

geometrieseite = seite_erstellen("geometrie")

navigationsbuttons_erstellen(geometrieseite)


tk.Label(
    geometrieseite,
    text="Geometrie",
    font=("Arial", 30, "bold"),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    y=130,
    anchor="n"
)


tk.Label(
    geometrieseite,
    text="Flächen, Volumen und geometrische Figuren",
    font=("Arial", 20),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    rely=0.35,
    anchor="center"
)


# ------------------------------------------------------------
# WEITERE UNTERSEITE: FLÄCHENBERECHNUNG
# ------------------------------------------------------------

# Diese Seite wird von der Geometrie-Seite aus geöffnet.
flaechen_seite = seite_erstellen("flaechen")


navigationsbuttons_erstellen(flaechen_seite)


tk.Label(
    flaechen_seite,
    text="Flächenberechnung",
    font=("Arial", 30, "bold"),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    y=130,
    anchor="n"
)


tk.Label(
    flaechen_seite,
    text="Beispiel: Fläche eines Rechtecks",
    font=("Arial", 20),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    rely=0.35,
    anchor="center"
)


# Beispiel für eine Berechnung
def rechteck_berechnen():
    laenge = 8
    breite = 5

    flaeche = laenge * breite

    tk.messagebox.showinfo(
        "Flächenberechnung",
        f"Länge: {laenge}\n"
        f"Breite: {breite}\n\n"
        f"Fläche: {flaeche}"
    )


button_erstellen(
    seite=flaechen_seite,
    text="Rechteck berechnen",
    x=BREITE // 2 - 150,
    y=HOEHE // 2,
    breite=300,
    hoehe=65,
    aktion=rechteck_berechnen,
    farbe="#27AE60"
)


# Button von Geometrie zur Flächenberechnung
button_erstellen(
    seite=geometrieseite,
    text="Flächenberechnung öffnen",
    x=BREITE // 2 - 175,
    y=HOEHE // 2,
    breite=350,
    hoehe=65,
    aktion=lambda: seite_anzeigen("flaechen"),
    farbe="#27AE60"
)


# ============================================================
# 9. BEISPIELSEITE: FORMELSAMMLUNG
# ============================================================

formelseite = seite_erstellen("formeln")

navigationsbuttons_erstellen(formelseite)


tk.Label(
    formelseite,
    text="Formelsammlung",
    font=("Arial", 30, "bold"),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    y=130,
    anchor="n"
)


formeln = (
    "Rechteck: A = a · b\n\n"
    "Dreieck: A = (g · h) / 2\n\n"
    "Kreis: A = π · r²\n\n"
    "Pythagoras: a² + b² = c²"
)


tk.Label(
    formelseite,
    text=formeln,
    font=("Arial", 22),
    bg=HINTERGRUND,
    fg=TEXT_FARBE,
    justify="left"
).place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ============================================================
# 10. BEISPIELSEITE: WAHRSCHEINLICHKEIT
# ============================================================

wahrscheinlichkeit_seite = seite_erstellen("wahrscheinlichkeit")

navigationsbuttons_erstellen(wahrscheinlichkeit_seite)


tk.Label(
    wahrscheinlichkeit_seite,
    text="Wahrscheinlichkeitsrechnung",
    font=("Arial", 30, "bold"),
    bg=HINTERGRUND,
    fg=TEXT_FARBE
).place(
    relx=0.5,
    y=130,
    anchor="n"
)


tk.Label(
    wahrscheinlichkeit_seite,
    text=(
        "Grundformel:\n\n"
        "P(E) = günstige Ergebnisse / mögliche Ergebnisse\n\n"
        "Beispiel: Würfel mit sechs Seiten\n"
        "P(6) = 1/6"
    ),
    font=("Arial", 20),
    bg=HINTERGRUND,
    fg=TEXT_FARBE,
    justify="center"
).place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ============================================================
# 11. PROGRAMM STARTEN
# ============================================================

# Startseite als erste Seite anzeigen
seite_anzeigen("start")

# Ereignisschleife starten
fenster.mainloop()
