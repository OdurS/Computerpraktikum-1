from time import perf_counter_ns

# from src.tableau import _integer, count_partitions, partitions
import src.partitions as part


def _pruefe_n(n):
    part._integer(n)
    if n < 0:
        raise ValueError("Für den Vergleich muss n mindestens null sein.")

def partitionen_vergleich(n, listen=False):
    _pruefe_n(n)
    if type(listen) is not bool:
        raise TypeError("listen muss True oder False sein.")

    if listen:
        funktion_python = part.partitions_list
        funktion_gap = part.GPartitions
        modus = "vollständige Liste"
    else:
        funktion_python = part.count_partitions
        funktion_gap = part.NrPartitions
        modus = "Anzahl berechnen"

    start = perf_counter_ns()
    antwort = funktion_gap(n)
    zeit_gap = perf_counter_ns() - start
    anzahl_gap = len(antwort) if listen else antwort

    start = perf_counter_ns()
    antwort = funktion_python(n)
    zeit_python = perf_counter_ns() - start
    anzahl_python = len(antwort) if listen else antwort

    if anzahl_python != anzahl_gap:
        raise RuntimeError(f"Verschiedene Anzahlen für n = {n}: Python {anzahl_python}, GAP {anzahl_gap}.")
    anzahl = f"{anzahl_python:,}".replace(",", ".")
    return (
        f"n = {n} · {modus} · p({n}) = {anzahl}\n"
        f"  Python  {zeit_python / 1_000_000:.3f} ms\n"
        f"  GAP     {zeit_gap / 1_000_000:.3f} ms"
    )


def gleiche_partitionen(n):
    _pruefe_n(n)
    return sorted(part.partitions_list(n)) == sorted(tuple(part) for part in part.GPartitions(n))
