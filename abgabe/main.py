from itertools import islice

from partitionen_vergleich import gleiche_partitionen, partitionen_vergleich
# from src.Tableau import (
#     Tableau, count_partitions, inner_corners, partitions, jeu_de_taquin_slide,
#     make_skew, partitions_list, rectify, robinson_schensted, skew_shapes,
# )
from src import Tableau as tabby
import src.partitions as part


def main():
    T = tabby.Tableau([[1, 3], [2]])
    U = tabby.Tableau([[1, 2]])
    x = 1
    n = 5
    n_standard = 3
    shape = (3, 2)
    perm = [3, 1, 4, 2]
    S = tabby.SkewTableau.Skew_Shape((4, 3, 2), (2, 1), [[2, 4], [1, 3], [2, 4]])
    n_listenvergleich = 30
    n_zaehlvergleich = 75

    anzahl = part.count_partitions(n)
    print(f"Partitionen von {n} ({anzahl} insgesamt)")
    if anzahl <= 10:
        print(part.partitions_list(n))
    else:
        print("Die ersten zehn:", list(islice(part.partitions(n), 10)))

    alle = tabby.Tableau.Standard_Tableaux(n_standard)
    print(f"\nStandardtableaux mit {n_standard} Kästchen ({len(alle)} insgesamt)")
    for tableau in alle:
        print(" ", tableau.rows)

    feste_form = tabby.Tableau.Standard_Tableaux_Corners(shape)
    print(f"\nStandardtableaux der Form {shape} ({len(feste_form)} insgesamt)")
    for tableau in feste_form:
        print(" ", tableau.rows)

    print(f"\nRow Insertion von {x} in T = {T.rows}")
    print(T.row_insert(x))

    print(f"\nTableau-Produkt mit U = {U.rows}, Lesewort {U.reading_word()}")
    produkt = T.tableau_product_insertion(U)
    print("Durch Row Insertion")
    print(produkt)
    print("Durch Jeu de taquin")
    produkt_jdt = T * U
    print(produkt_jdt)
    print("Beide Produkte sind gleich:", produkt == produkt_jdt)

    print("\nSchiefe Form")
    print("S =", S)
    print("Äußere und innere Form:", S.shape)
    ecken = S.inner_corners()
    print("Innere Ecken:", ecken)
    if ecken:
        print("Ein Slide ab", ecken[-1], "ergibt", S.jeu_de_taquin(ecken[-1]))
    print("Rektifikation")
    print(S.rectify())

    print("\nRobinson–Schensted für", perm)
    P, Q = tabby.Tableau.Robinson_schensted(perm)
    print("Einfügungstableau P")
    print(P)
    print("Aufzeichnungstableau Q")
    print(Q)

    print("\nLaufzeitvergleich mit GAP (Ported nach Python)")
    print(partitionen_vergleich(n_listenvergleich, listen=True))
    print(partitionen_vergleich(n_zaehlvergleich, listen=False))
    print("Inhaltsvergleich für n = 5:", gleiche_partitionen(5))


def gui():
    """Startet die grafische Oberfläche aus src/interface.py."""
    from src.interface import main as interface_main

    interface_main()


if __name__ == "__main__":
    import sys

    if sys.argv[1:] == ["gui"]:
        gui()
    else:
        main()
