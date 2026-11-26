import os
import sys
from itertools import islice

from partitionen_vergleich import gleiche_partitionen, partitionen_vergleich
from src.tableau_classes import Tableau, SkewTableau
import src.tableau as t
import src.partitions as part

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

def farbig(text, farbe):
    """Färbt Text im Terminal; bei Umleitung oder NO_COLOR unverändert."""
    if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        return str(text)
    return f"{farbe}{text}{RESET}"


def label(text):
    return farbig(text, YELLOW)


def hinweis(text):
    return farbig(text, DIM)


def examples():
    T = Tableau([[1, 3], [2]])
    U = Tableau([[1, 2]])
    x = 1
    n = 5
    n_standard = 3
    shape = (3, 2)
    perm = [3, 1, 4, 2]
    S = SkewTableau.Skew_Shape((4, 3, 2), (2, 1), [[2, 4], [1, 3], [2, 4]])
    n_listenvergleich = 30
    n_zaehlvergleich = 75

    anzahl = part.count_partitions(n)
    print(farbig(f"Partitionen von {n} ({anzahl} insgesamt)", BOLD + CYAN))
    if anzahl <= 10:
        print(farbig(part.partitions_list(n), GREEN))
    else:
        print(label("Die ersten zehn:"), farbig(list(islice(part.partitions(n), 10)), GREEN))

    alle = Tableau.Standard_Tableaux(n_standard)
    print(farbig(f"\nStandardtableaux mit {n_standard} Kästchen ({len(alle)} insgesamt)", BOLD + CYAN))
    for tableau in alle:
        print(" ", farbig(tableau.rows, GREEN))

    feste_form = Tableau.Standard_Tableaux_Corners(shape)
    print(farbig(f"\nStandardtableaux der Form {shape} ({len(feste_form)} insgesamt)", BOLD + CYAN))
    for tableau in feste_form:
        print(" ", farbig(tableau.rows, GREEN))

    print(farbig(f"\nRow Insertion von {x} in T = {T.rows}", BOLD + CYAN))
    print(farbig(T.row_insert(x), GREEN))

    print(farbig(f"\nTableau-Produkt mit U = {U.rows}, Lesewort {U.reading_word()}", BOLD + CYAN))
    produkt = T.tableau_product_insertion(U)
    print(label("Durch Row Insertion"))
    print(farbig(produkt, GREEN))
    print(label("Durch Jeu de taquin"))
    produkt_jdt = T * U
    print(farbig(produkt_jdt, GREEN))
    gleich = produkt == produkt_jdt
    print(label("Beide Produkte sind gleich:"), farbig(gleich, GREEN if gleich else RED))

    print(farbig("\nSchiefe Form", BOLD + CYAN))
    print(label("S ="), farbig(S, GREEN))
    print(label("Äußere und innere Form:"), farbig(S.shape, GREEN))
    ecken = S.inner_corners()
    print(label("Innere Ecken:"), farbig(ecken, GREEN))
    if ecken:
        print(label("Ein Slide ab"), farbig(ecken[-1], YELLOW),
              label("ergibt"), farbig(S.jeu_de_taquin(ecken[-1]), GREEN))
    print(label("Rektifikation"))
    print(farbig(S.rectify(), GREEN))

    print(farbig(f"\nRobinson–Schensted für {perm}", BOLD + CYAN))
    P, Q = Tableau.Robinson_schensted(perm)
    print(label("Einfügungstableau P"))
    print(farbig(P, GREEN))
    print(label("Aufzeichnungstableau Q"))
    print(farbig(Q, GREEN))

    print(farbig("\nLaufzeitvergleich mit GAP (Ported nach Python)", BOLD + CYAN))
    print(farbig(partitionen_vergleich(n_listenvergleich, listen=True), GREEN))
    print(farbig(partitionen_vergleich(n_zaehlvergleich, listen=False), GREEN))
    inhalt_gleich = gleiche_partitionen(5)
    print(label("Inhaltsvergleich für n = 5:"),
          farbig(inhalt_gleich, GREEN if inhalt_gleich else RED))


def gui():
    """Startet die grafische Oberfläche aus src/interface.py."""
    from src.interface import main as interface_main

    interface_main()


def main():
    """Zeigt eine kurze Anleitung zur Benutzung des Programms."""
    print(farbig("Partitionen und Tableaux", BOLD + CYAN))
    print(farbig("========================", CYAN))
    print()

    print(farbig("Beispiele ausführen:", BOLD + BLUE))
    print("  " + farbig("python main.py examples", GREEN))
    print("  oder interaktiv: " + farbig("python -i main.py", GREEN)
          + "  und dann  " + farbig("examples()", YELLOW))
    print()

    print(farbig("Grafische Oberfläche starten:", BOLD + BLUE))
    print("  " + farbig("python main.py gui", GREEN))
    print("  oder interaktiv: " + farbig("python -i main.py", GREEN)
          + "  und dann  " + farbig("gui()", YELLOW))
    print()

    print(farbig("Diese Anleitung anzeigen:", BOLD + BLUE))
    print("  " + farbig("python main.py", GREEN))
    print("  oder interaktiv: " + farbig("python -i main.py", GREEN)
          + "  und dann  " + farbig("main()", YELLOW))
    print()

    print(hinweis("Bei python -i main.py ist main bereits importiert; "
                  "ein erneutes import main ist nicht nötig."))
    print()

    print(farbig("Kurzer Funktionsüberblick (Details in examples()):", BOLD + BLUE))
    print("  " + farbig("Tableau([[1, 3], [2]])", YELLOW)
          + "                Tableau anlegen")
    print("  " + farbig("T.row_insert(x), T * U", YELLOW)
          + "                 Zeileneinfügung, Produkt")
    print("  " + farbig("Tableau.Standard_Tableaux(n)", YELLOW)
          + "           Standardtableaux")
    print("  " + farbig("Tableau.Standard_Tableaux_Corners(shape)", YELLOW))
    print("  " + farbig("SkewTableau.Skew_Shape(lam, mu, fuellung)", YELLOW))
    print("  " + farbig("S.inner_corners(), S.rectify()", YELLOW)
          + "         Ecken, Rektifikation")
    print("  " + farbig("Tableau.Robinson_schensted(perm)", YELLOW)
          + "       P und Q")
    print("  " + farbig("part.partitions(n), part.count_partitions(n)", YELLOW))
    print("  " + farbig("partitionen_vergleich(n), gleiche_partitionen(n)", YELLOW))
    print()
    print("Die Namen " + farbig("Tableau, SkewTableau, t, part, partitionen_vergleich "
                                "und gleiche_partitionen", YELLOW))
    print("sind im interaktiven Modus bereits verfügbar.")
    print(hinweis("Die Eingaben für die Beispiele stehen oben in examples()."))


if __name__ == "__main__":
    befehl = sys.argv[1:]
    if befehl == ["gui"]:
        gui()
    elif befehl == ["examples"]:
        examples()
    else:
        main()
