import tkinter as tk
from ast import literal_eval
from itertools import islice

from tableau import (
    Tableau,
    count_partitions,
    inner_corners,
    partitions_list,
    jeu_de_taquin_slide,
    rectify,
    robinson_schensted,
    skew_shapes,
)

HINTERGRUND = "#20243C"
TEXTFARBE = "#FFFFFF"
VORSCHAU = 100


class FarbButton(tk.Canvas):
    """Ein Button mit selbst gezeichneter Beschriftung und fester Farbe."""

    def __init__(self, parent, text, farbe, befehl, breite=190):
        super().__init__(
            parent, width=breite, height=42, bg=farbe, bd=0,
            highlightthickness=2, highlightbackground=farbe,
            highlightcolor=TEXTFARBE, takefocus=True, cursor="hand2",
        )
        beschriftung = self.create_text(
            0, 0, text=text, fill=TEXTFARBE, font=("Arial", 13, "bold")
        )
        self.bind(
            "<Configure>",
            lambda event: self.coords(
                beschriftung, event.width / 2, event.height / 2
            ),
        )
        self.bind("<ButtonPress-1>", lambda event: self.focus_set())

        def klick(event):
            if 0 <= event.x < self.winfo_width() and 0 <= event.y < self.winfo_height():
                befehl()

        self.bind("<ButtonRelease-1>", klick)
        self.bind("<Return>", lambda event: befehl())
        self.bind("<space>", lambda event: befehl())


def folge(wert):
    if not isinstance(wert, (list, tuple)):
        raise ValueError("Erwartet wird eine Liste oder ein Tupel.")
    return wert


def zeilen(wert):
    return [folge(zeile) for zeile in folge(wert)]


def partitionen_anzeigen(n):
    if type(n) is not int or n < 0:
        raise ValueError("n muss eine nichtnegative ganze Zahl sein.")

    anzahl = count_partitions(n)
    kopf = f"Partitionen von {n} · {anzahl:,} insgesamt".replace(",", ".")
    if anzahl > VORSCHAU:
        kopf += f" · erste {VORSCHAU}"
    vorschau = "\n".join(map(str, islice(partitions_list(n), VORSCHAU)))
    return f"{kopf}\n\n{vorschau}"


def standardtableaux_anzeigen(eingabe):
    if type(eingabe) is int:
        if eingabe < 0:
            raise ValueError("n muss nichtnegativ sein.")
        tableaus = Tableau.iter_standard_tableaux(eingabe)
    else:
        tableaus = Tableau.iter_standard_tableaux_corners(folge(eingabe))

    vorschau = list(islice(tableaus, VORSCHAU + 1))
    text = "\n\n".join(map(str, vorschau[:VORSCHAU]))
    if len(vorschau) > VORSCHAU:
        return f"Erste {VORSCHAU} Standardtableaux\n\n{text}"
    return f"{len(vorschau)} Standardtableaux\n\n{text}"


def robinson_schensted_anzeigen(perm):
    P, Q = robinson_schensted(folge(perm))
    return f"Einfügungstableau P\n{P}\n\nAufzeichnungstableau Q\n{Q}"


def schiefe_zeilen_anzeigen(S):
    return "\n".join(
        " ".join("·" if x is None else str(x) for x in zeile)
        for zeile in S
    ) or "∅"


def slide_anzeigen(S, ecke):
    S = zeilen(S)
    ecken = inner_corners(S)
    if tuple(folge(ecke)) not in ecken:
        raise ValueError(f"Mögliche Startpunkte sind {ecken}.")
    ergebnis = jeu_de_taquin_slide(S, ecke)
    return f"Nach einem Slide ab {tuple(ecke)}\n{schiefe_zeilen_anzeigen(ergebnis)}"


def rektifikation_anzeigen(S):
    S = zeilen(S)
    return f"Rektifiziertes Tableau\n{rectify(S)}"


def formen_anzeigen(S):
    S = zeilen(S)
    lam, mu = skew_shapes(S)
    return (
        f"Äußere Form  λ = {tuple(lam)}\n"
        f"Innere Form  μ = {tuple(mu)}\n"
        f"Innere Ecken (ab 0)  {inner_corners(S)}\n\n"
        f"{schiefe_zeilen_anzeigen(S)}"
    )


def produkt_anzeigen(T, U, methode):
    return str(methode(Tableau(zeilen(T)), Tableau(zeilen(U))))


class Programm:
    def __init__(self):
        self.fenster = tk.Tk()
        self.fenster.title("Computerpraktikum · Partitionen und Tableaux")
        self.fenster.geometry("1000x640")
        self.fenster.minsize(780, 480)
        self.fenster.configure(bg=HINTERGRUND)

        self.navigation = tk.Frame(self.fenster, bg=HINTERGRUND)
        self.navigation.pack(side="left", fill="y", padx=(20, 12), pady=24)
        self.inhalt = tk.Frame(self.fenster, bg=HINTERGRUND)
        self.inhalt.pack(side="left", fill="both", expand=True, padx=16, pady=24)

        seiten = (
            ("Partitionen", "#226393", self.partitionen),
            ("Standardtableaux", "#167359", self.standardtableaux),
            ("Zeileneinfügung", "#395186", self.zeileneinfuegung),
            ("Tableau-Produkt", "#704584", self.produkt),
            ("Jeu de taquin", "#8C4C20", self.jeu_de_taquin),
            ("Robinson–Schensted", "#126C75", self.robinson_schensted),
        )
        for text, farbe, seite in seiten:
            FarbButton(self.navigation, text, farbe, seite).pack(pady=(0, 8))

        self.partitionen()

    def seite(self, titel, felder, aktionen):
        for widget in self.inhalt.winfo_children():
            widget.destroy()

        tk.Label(
            self.inhalt, text=titel, bg=HINTERGRUND, fg=TEXTFARBE,
            font=("Arial", 23, "bold"), anchor="w",
        ).pack(fill="x", pady=(0, 14))

        eingaben = []
        for bezeichnung, beispiel in felder:
            tk.Label(
                self.inhalt, text=bezeichnung, bg=HINTERGRUND,
                fg=TEXTFARBE, anchor="w",
            ).pack(fill="x")
            eingabe = tk.Entry(self.inhalt, font=("Arial", 14))
            eingabe.insert(0, beispiel)
            eingabe.pack(fill="x", pady=(2, 9), ipady=4)
            eingaben.append(eingabe)

        leiste = tk.Frame(self.inhalt, bg=HINTERGRUND)
        leiste.pack(fill="x", pady=(2, 12))

        ausgabe = tk.Frame(self.inhalt, bg=HINTERGRUND)
        ausgabe.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(ausgabe)
        ergebnis = tk.Text(
            ausgabe, font="TkFixedFont", bg="#F3F5F9", fg="#20243C",
            wrap="word", height=8, padx=12, pady=9, state="disabled",
            yscrollcommand=scrollbar.set,
        )
        scrollbar.configure(command=ergebnis.yview)
        scrollbar.pack(side="right", fill="y")
        ergebnis.pack(side="left", fill="both", expand=True)

        def ausfuehren(befehl, anzahl):
            try:
                werte = [literal_eval(eingabe.get()) for eingabe in eingaben[:anzahl]]
                text = befehl(*werte)
            except SyntaxError:
                text = "Ungültige Eingabe. Verwende das Format aus dem Beispielfeld."
            except (TypeError, ValueError) as fehler:
                text = f"Ungültige Eingabe. {fehler}"
            except RecursionError:
                text = "Diese Form ist zu groß für den rekursiven Generator."

            ergebnis.configure(state="normal")
            ergebnis.delete("1.0", "end")
            ergebnis.insert("1.0", text)
            ergebnis.configure(state="disabled")

        for text, befehl, anzahl in aktionen:
            FarbButton(
                leiste, text, "#395186",
                lambda befehl=befehl, anzahl=anzahl: ausfuehren(befehl, anzahl),
                breite=160,
            ).pack(side="left", padx=(0, 8))

        _, befehl, anzahl = aktionen[0]
        for eingabe in eingaben:
            eingabe.bind("<Return>", lambda event: ausfuehren(befehl, anzahl))

    def partitionen(self):
        self.seite(
            "Partitionen", (("Ganze Zahl n", "75"),),
            (("Berechnen", partitionen_anzeigen, 1),),
        )

    def standardtableaux(self):
        self.seite(
            "Standardtableaux", (("Form (3, 2) oder Anzahl der Kästchen", "(3, 2)"),),
            (("Erzeugen", standardtableaux_anzeigen, 1),),
        )

    def zeileneinfuegung(self):
        self.seite(
            "Row Insertion", (("Tableau T", "[[1, 3], [2]]"), ("Eintrag x", "1")),
            (("Einfügen", lambda T, x: str(Tableau(zeilen(T)).row_insert(x)), 2),),
        )

    def produkt(self):
        self.seite(
            "Tableau-Produkt T · U",
            (("Tableau T", "[[1, 3], [2]]"), ("Tableau U", "[[1, 2]]")),
            (
                ("Jeu de taquin", lambda T, U: produkt_anzeigen(T, U, Tableau.tableau_product_jdt), 2),
                ("Row Insertion", lambda T, U: produkt_anzeigen(T, U, Tableau.tableau_product_insertion), 2),
            ),
        )

    def jeu_de_taquin(self):
        self.seite(
            "Jeu de taquin",
            (
                ("Schiefes Tableau S mit None als Platzhalter", "[[None, None, 1, 2], [1, 3], [2]]"),
                ("Startpunkt für einen Slide (Zeile, Spalte), ab 0", "(0, 1)"),
            ),
            (
                ("Rektifizieren", rektifikation_anzeigen, 1),
                ("Ein Slide", slide_anzeigen, 2),
                ("Formen und Ecken", formen_anzeigen, 1),
            ),
        )

    def robinson_schensted(self):
        self.seite(
            "Robinson–Schensted",
            (("Folge verschiedener positiver ganzer Zahlen", "[3, 1]"),),
            (("P und Q berechnen", robinson_schensted_anzeigen, 1),),
        )


def main():
    programm = Programm()
    programm.fenster.mainloop()


if __name__ == "__main__":
    main()
