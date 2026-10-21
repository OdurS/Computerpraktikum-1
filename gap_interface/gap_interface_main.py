import ast
import json
import queue
import re
import subprocess
import threading
import uuid
from pathlib import Path


class GAPInterface:
    """Dauerhafte Verbindung zwischen Python und GAP."""

    def __init__(self, gap_command="gap", startup_files=None):
        self.gap_command = gap_command
        self.startup_files = startup_files or []
        self.process = None
        self.output_queue = queue.Queue()
        self.lock = threading.Lock()

    def start(self):
        """Startet GAP und lädt optional eigene GAP-Dateien."""

        if self.process is not None and self.process.poll() is None:
            return

        self.process = subprocess.Popen(
            [self.gap_command, "-q"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )

        threading.Thread(
            target=self._read_output,
            daemon=True,
        ).start()

        for filename in self.startup_files:
            path = str(Path(filename).resolve())
            self.execute(f"Read({json.dumps(path, ensure_ascii=False)});")

    def _read_output(self):
        """Liest die Ausgabe des GAP-Prozesses kontinuierlich."""

        for line in self.process.stdout:
            self.output_queue.put(line)

    def _send(self, code, marker, timeout=30):
        """Sendet Code und wartet auf das zugehörige Endsignal."""

        if self.process is None or self.process.poll() is not None:
            raise RuntimeError("GAP läuft nicht. Rufe start() auf.")

        self.process.stdin.write(code + "\n")
        self.process.stdin.flush()

        lines = []

        while True:
            try:
                line = self.output_queue.get(timeout=timeout)
            except queue.Empty as exc:
                raise TimeoutError(
                    "GAP hat nicht rechtzeitig geantwortet."
                ) from exc

            if marker in line:
                before, _, _ = line.partition(marker)
                if before:
                    lines.append(before)
                return "".join(lines).strip()

            lines.append(line)

    def execute(self, code, timeout=30):
        """
        Führt beliebigen GAP-Code aus.
        Rückgabe: die Textausgabe dieses Codes.
        """

        marker = "__GAP_DONE_" + uuid.uuid4().hex + "__"

        with self.lock:
            return self._send(
                code + f'\nPrint("\\n{marker}\\n");',
                marker,
                timeout,
            )

    @staticmethod
    def _to_gap(value):
        """Konvertiert einfache Python-Daten in GAP-Ausdrücke."""

        if value is None:
            raise TypeError(
                "None hat keine allgemeine GAP-Entsprechung."
            )

        if isinstance(value, bool):
            return "true" if value else "false"

        if isinstance(value, int):
            return str(value)

        if isinstance(value, float):
            if not __import__("math").isfinite(value):
                raise ValueError("NaN und Infinity werden nicht unterstützt.")
            return repr(value)

        if isinstance(value, str):
            return json.dumps(value, ensure_ascii=False)

        if isinstance(value, (list, tuple)):
            return "[" + ", ".join(
                GAPInterface._to_gap(item) for item in value
            ) + "]"

        raise TypeError(
            f"Nicht unterstützter Python-Datentyp: {type(value).__name__}"
        )

    @staticmethod
    def _parse_result(output):
        """Wandelt einfache GAP-Ausgaben in Python-Werte um."""

        output = output.strip()

        try:
            return ast.literal_eval(output)
        except (ValueError, SyntaxError):
            # Komplexere GAP-Objekte bleiben zunächst Text.
            return output

    def call(self, function_name, *args, timeout=30):
        """
        Ruft eine bereits in GAP definierte Funktion auf.

        Beispiel:
            gap.call("MeineFunktion", [[1, 2], [3, 4]])
        """

        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", function_name):
            raise ValueError("Ungültiger GAP-Funktionsname.")

        arguments = ", ".join(self._to_gap(arg) for arg in args)
        expression = f"{function_name}({arguments})"

        request_id = uuid.uuid4().hex
        begin = "__GAP_RESULT_" + request_id + "__"
        end = "__GAP_DONE_" + request_id + "__"

        code = (
            f'Print("\\n{begin}\\n");\n'
            f"Print({expression});\n"
            f'Print("\\n{end}\\n");'
        )

        with self.lock:
            output = self._send(code, end, timeout)

        if begin not in output:
            raise RuntimeError(
                "GAP lieferte keine gültige Ergebnisantwort: "
                + output
            )

        result = output.split(begin, 1)[1]
        return self._parse_result(result)

    def close(self):
        """Beendet den GAP-Prozess."""

        if self.process is not None:
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