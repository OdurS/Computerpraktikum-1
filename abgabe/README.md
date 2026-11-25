# Thema 2 · Partitionen und Tableaux

Entpacke das ZIP an deinem gewünschten Ort. Der vollständige Pfad darf Leerzeichen enthalten. Öffne in VS Code über **Datei → Ordner öffnen** den entpackten Ordner `Computerpraktikum-1`. Öffne `main.py` und drücke **▶ oben rechts**. Die Ausgaben erscheinen unten im integrierten Terminal. Der Button gehört zur VS-Code-Erweiterung **Python** von Microsoft.

Zeigt der ▶-Button für einen Pfad mit Leerzeichen `[Errno 2]` und doppelte Anführungszeichen innerhalb einfacher Anführungszeichen, kann der bekannte VS-Code-Fehler vorliegen. Deaktiviere in **Erweiterungen** über das Zahnrad bei **Python Environments** die Erweiterung für diesen Arbeitsbereich und starte VS Code neu. Die Erweiterung **Python** bleibt aktiviert. [VS-Code-Fehlerbericht](https://github.com/microsoft/vscode-python/issues/26274)

Im Terminal des Projektordners kannst du das Programm auch direkt starten.

```sh
python3 main.py
```

Oben in `main()` kannst du `T`, `U`, `n`, `n_standard`, `shape`, `x` und `perm` ändern. Alle Beispiele verwenden Python 3 mit der Standardbibliothek. GAP wird ausschließlich im letzten Abschnitt für den Partitionsvergleich aufgerufen.

## Dateien

| Datei | Wofür du sie öffnest |
|---|---|
| `main.py` | Hier stehen die Eingaben und die Aufrufe für alle Ausgaben. |
| `tableau.py` | Hier stehen die Klasse `Tableau`, Davids Partitionsgenerator, die Eckrekursion, die Zeileneinfügung, die Slides und Robinson–Schensted. |
| `partitionen_vergleich.py` | Hier startet Python GAP und liest dessen Antwort ein. |

## Befehle für deine Beispiele

| Aufruf | Ergebnis |
|---|---|
| `partitions(5)` | Liste aller sieben Partitionen von 5 |
| `count_partitions(75)` | Anzahl 8.118.264 |
| `iter_partitions(n)` | Liefert die Partitionen einzeln. Bei mehr als zehn Ergebnissen zeigt `main.py` die ersten zehn. |
| `T = Tableau([[1, 3], [2]])` | Ein gerades Tableau. `T.rows` enthält die Zeilen, `T.shape` ergibt `(2, 1)`. |
| `T.is_tableau()`, `T.is_semistandard()`, `T.is_standard()` | Die ersten beiden prüfen die Semistandard-Eigenschaft. Der dritte prüft zusätzlich, ob jede Zahl von 1 bis zur Größe genau einmal vorkommt. |
| `Tableau.standard_tableaux(3)` | Alle vier Standardtableaux mit drei Kästchen |
| `Tableau.standard_tableaux_corners((3, 2))` | Die fünf Standardtableaux dieser Form |
| `T.row_insert(1)` | Neues Tableau nach Einfügen der 1 |
| `U.reading_word()`, `T.tableau_product_insertion(U)` | Lesewort von `U` und Produkt durch Einfügen dieses Worts in `T` |
| `T.make_product_skew(U)`, `T.tableau_product_jdt(U)`, `T * U` | Schiefe Ausgangsform und ihr rektifiziertes Produkt. `T * U` verwendet Jeu de taquin. |
| `make_skew(lam, mu, filling)`, `skew_shapes(S)` | Erstellt die schiefen Zeilen bzw. liest daraus äußere und innere Form. Führende `None` markieren die ausgesparten Kästchen. |
| `T.outer_corners()`, `inner_corners(S)` | Ecken als Paare (Zeile, Spalte), beginnend bei null |
| `jeu_de_taquin_slide(S, ecke)`, `rectify(S)` | Ein Slide liefert schiefe Zeilen. Die vollständige Rektifikation liefert ein gerades `Tableau`. |
| `P, Q = robinson_schensted([3, 1, 4, 2])` | Einfügungs- und Aufzeichnungstableau |
| `partitionen_vergleich(30, listen=True)` | Beide Programme erzeugen die vollständige Liste. |
| `partitionen_vergleich(75)` | Beide Programme berechnen die Anzahl. |
| `gleiche_partitionen(5)` | Vergleicht für ein kleines Beispiel auch die einzelnen Partitionen einschließlich ihrer Vielfachheiten. |

Für einen **Listenvergleich bei 75** ändere in `main.py` die Zeile auf `n_listenvergleich = 75`. Dann erzeugt jedes Programm 8.118.264 Partitionen. Beide messen die eigene Berechnung. GAP überträgt für die Zeitmessung nur Anzahl und Dauer. Prozessstart, Übertragung und Drucken liegen außerhalb der gemessenen Laufzeit.
