import time
import subprocess
from thema2 import _integer, partitions


def partitionen_vergleich(n):
    _integer(n)

    if n < 0:
        raise ValueError("Die Zahl muss nichtnegativ sein.")

  
    start = time.perf_counter()
    ergebnis_eigen = partitions(n)
    zeit_eigen = time.perf_counter() - start

  
    gap_code = f"Print(Partitions({n}));"

    start = time.perf_counter()

    ergebnis_gap = subprocess.run(
        ["gap", "-q"],
        input=gap_code,
        capture_output=True,
        text=True,
        check=True
    )

    zeit_gap = time.perf_counter() - start

    return (
        f"Partitionsvergleich für n = {n}\n\n"
        f"Kompilierzeit unser Befehl: {zeit_eigen:.6f} Sekunden\n"
        f"Kompilierzeit GAP.partitions: {zeit_gap:.6f} Sekunden"
    )
