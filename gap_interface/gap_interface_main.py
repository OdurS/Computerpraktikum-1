import subprocess
import threading
import queue
import uuid
import json
from pathlib import Path


class GAPInterface:
    """
    Verwaltet einen dauerhaft laufenden GAP-Prozess.

    Das Kommunikationsprotokoll verwendet JSON
    """

    def __init__(self, gap_command="gap"):
        self.gap_command = gap_command
        self.process = None
        self.responses = {}
        self.lock = threading.Lock()
        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()

    def start(self):
        """Startet GAP """

        if self.process is not None:
            if self.process.poll() is None:
                return

        worker = Path(__file__).parent / "gap" / "worker.g"

        self.process = subprocess.Popen(
            [self.gap_command, "-q", str(worker)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1
        )

        threading.Thread(
            target=self._read_stdout,
            daemon=True
        ).start()

        threading.Thread(
            target=self._read_stderr,
            daemon=True
        ).start()

    def _read_stdout(self):
        """Liest Antworten aus GAP."""

        for line in self.process.stdout:
            self.stdout_queue.put(line.rstrip("\n"))

    def _read_stderr(self):
        """Sammelt Diagnosemeldungen."""

        for line in self.process.stderr:
            self.stderr_queue.put(line.rstrip("\n"))

    def execute(self, operation, **arguments):
        """
        Sendet eine Anfrage an GAP und wartet auf die Antwort.

        Beispiel:
            execute("multiply", A=[[1, 2]], B=[[3], [4]])
        """

        if self.process is None or self.process.poll() is not None:
            raise RuntimeError("GAP läuft nicht. Rufe start() auf.")

        request_id = uuid.uuid4().hex

        request = {
            "id": request_id,
            "operation": operation,
            "arguments": arguments
        }

        # Die konkrete GAP-Seite muss dieses JSON-Protokoll
        # implementieren und Antworten mit derselben ID liefern.
        payload = json.dumps(request, separators=(",", ":"))

        with self.lock:
            self.process.stdin.write(payload + "\n")
            self.process.stdin.flush()

            while True:
                try:
                    line = self.stdout_queue.get(timeout=30)
                except queue.Empty as exc:
                    raise TimeoutError(
                        "Keine Antwort von GAP innerhalb von 30 Sekunden."
                    ) from exc

                try:
                    response = json.loads(line)
                except json.JSONDecodeError:
                    # Diagnoseausgaben nicht als Protokollantwort behandeln.
                    continue

                if response.get("id") != request_id:
                    raise RuntimeError(
                        "Unerwartete Antwort-ID von GAP."
                    )

                if response.get("status") != "ok":
                    raise RuntimeError(
                        response.get("error", "Unbekannter GAP-Fehler.")
                    )

                return response.get("result")

    def multiply_matrices(self, A, B):
        """Multipliziert zwei Matrizen über dem gewählten Zahlbereich."""

        return self.execute(
            "multiply",
            A=A,
            B=B
        )

    def determinant(self, A):
        """Berechnet die Determinante einer Matrix."""

        return self.execute(
            "determinant",
            A=A
        )

    def close(self):
        """Beendet den GAP-Prozess."""

        if self.process is None:
            return

        if self.process.poll() is None:
            self.process.terminate()

            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        self.process = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
