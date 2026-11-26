# Partitionen und Tableaux – Benutzung

Dieses Projekt enthält:

- einen Generator für ganzzahlige Partitionen,
- eine Implementierung von Standard- und Skew-Tableaux,
- Zeileneinfügung (Row Insertion), Tableau-Produkte und Jeu de Taquin,
- Robinson–Schensted,
- Vergleichsfunktionen für Partitionen,
- eine kleine grafische Oberfläche mit Tkinter (Details am Ende).

---

## 1. Voraussetzungen

- Python 3
- für die grafische Oberfläche: `tkinter`

`tkinter` ist bei den meisten Python-Installationen dabei. Unter Debian/Ubuntu
lässt es sich bei Bedarf nachinstallieren mit:

```sh
sudo apt install python3-tk
```

Alle Befehle in dieser Anleitung werden aus dem Projektordner ausgeführt, also
aus dem Ordner, in dem `main.py` liegt.

Unter manchen Systemen heißt der Python-Befehl `python3` statt `python`. Die
Beispiele funktionieren entsprechend auch mit `python3`.

---

## 2. Schnellstart

| Befehl | Wirkung |
|---|---|
| `python main.py` | zeigt die kurze Anleitung im Terminal |
| `python main.py examples` | führt die Beispielsammlung aus |
| `python -i main.py` | startet die Anleitung und danach eine interaktive Python-Konsole |
| `python main.py gui` | startet die grafische Oberfläche (siehe Abschnitt 14) |

Die Terminalausgaben von `main()` und `examples()` sind farbig. Wenn die Ausgabe
umgeleitet wird oder die Umgebungsvariable `NO_COLOR` gesetzt ist, werden keine
Farbcodes verwendet:

```sh
python main.py examples | less
NO_COLOR=1 python main.py examples
```

---

## 3. Die Beispiele: `examples()`

Die Funktion `examples()` zeigt typische Aufrufe für alle wichtigen Teile des
Programms. Sie ist der schnellste Weg, um zu sehen, was das Programm kann:

```sh
python main.py examples
```

Dabei werden unter anderem ausgegeben:

- alle Partitionen einer kleinen Zahl,
- Standardtableaux mit einer bestimmten Anzahl von Kästchen,
- Standardtableaux einer festen Form,
- eine Zeileneinfügung,
- das Tableau-Produkt auf zwei verschiedene Arten,
- ein schiefes Tableau mit inneren Ecken, einem Slide und seiner Rektifikation,
- das Ergebnis von Robinson–Schensted,
- ein kurzer Laufzeitvergleich der Partitionsfunktionen.

### Eingaben der Beispiele ändern

Die Eingaben stehen am Anfang der Funktion `examples()` in `main.py`:

```python
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
```

Diese Werte können direkt geändert werden. Für eigene Experimente ist aber die
interaktive Konsole oft angenehmer. Die Eingaben werden beim Ausführen geprüft;
eine Übersicht steht in Abschnitt 11.

---

## 4. Interaktive Konsole

Mit

```sh
python -i main.py
```

wird zuerst die Anleitung angezeigt und danach eine Python-Konsole geöffnet.
Die Funktionen und importierten Namen aus `main.py` stehen dort bereits zur
Verfügung. Ein erneutes `import main` ist **nicht** nötig.

```python
examples()                 # Beispielsammlung starten
gui()                      # grafische Oberfläche starten
main()                     # Anleitung erneut anzeigen
```

Außerdem sind unter anderem diese Namen bereits verfügbar:

```python
Tableau     # Klassenwrapper um tableau.py
SkewTableau # Klassenwrapper um tableau.py
t           # src/tableau.py, die unterliegenden Implementationen
part        # src/partitions.py
partitionen_vergleich
gleiche_partitionen
```

Beispiel:

```python
>>> T = Tableau([[1, 3], [2]])
>>> T.rows
[[1, 3], [2]]
>>> T.shape
(2, 1)
>>> T.is_standard()
True
>>> T.row_insert(4).rows
[[1, 3, 4], [2]]
```

---

## 5. Tableaux verwenden

### 5.1 Ein Tableau anlegen

```python
T = Tableau([[1, 3], [2]])
```

Ein gültiges Tableau hat:

- Zeilen mit positiven ganzen Zahlen,
- schwach aufsteigende Einträge innerhalb jeder Zeile,
- streng aufsteigende Einträge innerhalb jeder Spalte,
- Zeilenlängen, die von oben nach unten nicht zunehmen.

Eigenschaften und Prüfungen:

```python
T.rows              # Grundlegende Datenstruktur
T.shape             # Zeilenlängen, z. B. (2, 1)
T.is_tableau()      # prüft die Form
T.is_semistandard() # prüft die Tableau-Eigenschaft
T.is_standard()     # prüft zusätzlich, ob 1 ... n genau einmal vorkommt
T.reading_word()    # Lesewort von unten nach oben, links nach rechts
T.outer_corners()   # äußere Ecken als (Zeile, Spalte), ab 0
```

**Validierung:**

- Die Eingabe muss eine Folge von Zeilen sein.
- Geprüft werden positive ganzzahlige Einträge, schwache Zeilen, strenge
  Spalten und nicht zunehmende Zeilenlängen.
- Die Prüfmethoden ändern das Tableau nicht; `T.shape` berechnet nur die Form.

### 5.2 Zeileneinfügung

```python
neu = T.row_insert(4)
print(neu)
print(neu.rows)
```

`row_insert` verändert `T` nicht, sondern gibt ein neues `Tableau` zurück.

**Validierung:**

- Der neue Eintrag muss eine positive ganze Zahl sein.
- Das vorhandene Tableau muss gültig bleiben.
- `T` selbst wird nicht verändert; das Ergebnis ist ein neues `Tableau`.
- Ein ungültiger Eintrag führt zu `ValueError`.

### 5.3 Standardtableaux erzeugen

```python
alle = Tableau.Standard_Tableaux(3)
print([t.rows for t in alle])

form = Tableau.Standard_Tableaux_Corners((3, 2))
print([t.rows for t in form])
```

`Standard_Tableaux(n)` erzeugt alle Standardtableaux mit `n` Kästchen.
`Standard_Tableaux_Corners(shape)` erzeugt alle Standardtableaux einer festen
Form, zum Beispiel `(3, 2)`.

Für große Eingaben gibt es die Generatorvarianten:

```python
for T in Tableau.Iter_Standard_Tableaux(5):
    print(T)

for T in Tableau.Iter_Standard_Tableaux_Corners((4, 3)):
    print(T)
```

**Validierung:**

- `n` muss eine nichtnegative ganze Zahl sein.
- `shape` muss eine gültige Partition sein: positive ganze Zahlen und nicht
  aufsteigende Zeilenlängen.
- Ein ungültiges `n` oder eine ungültige Form führt zu `ValueError`.

### 5.4 Zwei Tableaux multiplizieren

Gegeben:

```python
T = Tableau([[1, 3], [2]])
U = Tableau([[1, 2]])
```

Dann gibt es mehrere äquivalente Schreibweisen:

```python
P1 = T.tableau_product_insertion(U)  # über Zeileneinfügung
P2 = T.tableau_product_jdt(U)        # über Jeu de Taquin
P3 = T * U                           # Operator für das Produkt
```

Alle drei liefern dasselbe Tableau. Zusätzlich erzeugt

```python
S = T + U
```

das Skew-Tableau vor der Rektifikation. `T * U` ist also im Wesentlichen
`(T + U).rectify()`.

**Validierung:**

- `U` muss ein gültiges `Tableau` sein; sonst wird `TypeError` ausgelöst.
- Beide beteiligten Tableaux müssen die Tableau-Eigenschaften erfüllen.

---

## 6. Skew-Tableaux

Ein Skew-Tableau wird mit `SkewTableau` dargestellt. Führende `None`-Werte
markieren Kästchen, die zur inneren Form gehören und nicht gefüllt sind.

```python
S = SkewTableau([
    [None, None, 1, 2],
    [1, 3],
    [2],
])
```

Wichtige Operationen:

```python
S.rows
S.shape                 # (äußere Form, innere Form)
S.is_skew()
S.inner_corners()       # mögliche Startpunkte für Slides
S.jeu_de_taquin((0, 1)) # Jeu de Taquin angewendet auf Ecke (0, 1)
S.rectify()
```

`S.shape` liefert ein Paar `(lambda, mu)`. Bei obigem Beispiel ist das
`([4, 2, 1], [2])`.

`S.jeu_de_taquin(corner)` gibt wieder ein `SkewTableau` zurück.
`S.rectify()` gibt ein normales `Tableau` zurück.

Die Skew-Tableau- und Tableau-Klassen haben also folgende Relation:

```text
                T + U
        -------------------->
Tableau                       Skew-Tableau
        <--------------------
             S.rectify()
```

**Validierung:**

- Die Eingabe muss eine Folge von Zeilen sein; Einträge müssen positive ganze
  Zahlen sein.
- `None` ist nur am Zeilenanfang erlaubt. Die daraus berechneten inneren
  Zeilenlängen müssen absteigend sein.
- Zeilen müssen schwach, Spalten streng steigend sein.
- Ein Slide-Startpunkt muss ein Paar ganzer Zahlen sein und in
  `S.inner_corners()` liegen.
- Ungültige Eingaben ergeben `ValueError` oder `TypeError`.

### 6.1 Skew-Tableau aus Formen erzeugen

Wenn die äußere Form `lambda`, die innere Form `mu` und nur die tatsächlich
gefüllten Einträge gegeben sind:

```python
S = SkewTableau.Skew_Shape(
    (4, 3, 2),
    (2, 1),
    [[2, 4], [1, 3], [2, 4]],
)
```

Dabei gilt:

- `lambda` und `mu` sind Partitionen mit positiven Teilen,
- `mu` muss in `lambda` liegen,
- die Füllung enthält genau die Einträge, die nicht durch `None` abgedeckt sind.

**Validierung:**

- `lambda` und `mu` müssen gültige Partitionen mit positiven Teilen sein.
- `mu` muss in `lambda` liegen.
- Die Füllung muss zur Zeilenanzahl und zu den Zeilenlängen passen und darf
  kein `None` enthalten.
- Ungültige Eingaben ergeben `ValueError`.

---

## 7. Robinson–Schensted

```python
P, Q = Tableau.Robinson_schensted([3, 1, 4, 2])
print(P)
print(Q)
```

`P` ist das Einfügungstableau, `Q` das Aufzeichnungstableau.

Die Eingabe muss eine Folge paarweise verschiedener positiver ganzer Zahlen
sein. Für die klassische Permutationsversion verwendet man `1, ..., n` in
beliebiger Reihenfolge.

**Validierung:**

- Die Eingabe muss eine iterierbare Folge sein.
- Jeder Eintrag muss eine positive ganze Zahl sein; doppelte Werte werden
  abgelehnt.
- Werte müssen nicht lückenlos `1 ... n` sein. Die Reihenfolge der Werte bleibt
  erhalten, die Positionen im Aufzeichnungstableau sind `1 ... n`.

---

## 8. Partitionen

Die Partitionsfunktionen liegen in `src/partitions.py` und sind im
interaktiven Modus als `part` verfügbar.

```python
part.partitions_list(5)
```

liefert alle Partitionen von `5` als Liste von Tupeln.

```python
list(part.partitions(5))
```

liefert dieselben Partitionen als Iterator. Das ist bei größeren Zahlen
speicherschonender.

```python
part.count_partitions(75)
```

liefert nur die Anzahl, hier `8118264`.

Wichtige Funktionen:

| Funktion | Ergebnis |
|---|---|
| `part.partitions(n)` | Iterator über alle Partitionen |
| `part.partitions_list(n)` | Liste aller Partitionen |
| `part.count_partitions(n)` | Anzahl der Partitionen |
| `part.GPartitions(n)` | Liste aller Partitionen als Listen (Python-Port aus GAP, `n >= 1`) |
| `part.NrPartitions(n)` | Anzahl der Partitionen (Python-Port aus GAP) |

Für normale Anwendungen reichen `partitions`, `partitions_list` und
`count_partitions`.

**Validierung:**

- `n` muss eine ganze Zahl sein; `bool` wird abgelehnt.
- Für negative `n` liefert `partitions` keine Partitionen und
  `count_partitions` den Wert `0`. Für normale Anwendungen ist `n >= 0`.
- `GPartitions` verlangt `n >= 1`.

---

## 9. Vergleichsfunktionen

In `partitionen_vergleich.py` ist der Vergleich der Partitionsfunktion mit der
Partitionsfunktion aus der GAP-Standardbibliothek (nach Python portiert, um den
Vergleich fairer zu machen):

```python
print(partitionen_vergleich(30, listen=True))
print(partitionen_vergleich(75))
print(gleiche_partitionen(5))
```

- `partitionen_vergleich(n, listen=False)` berechnet die Anzahl und zeigt die
  Laufzeiten.
- `partitionen_vergleich(n, listen=True)` erzeugt zusätzlich die vollständigen
  Listen. Das ist nur für kleinere `n` sinnvoll.
- `gleiche_partitionen(n)` vergleicht die tatsächlichen Partitionen
  einschließlich ihrer Vielfachheiten.

Die Funktionen sind für `n >= 1` gedacht. Für sehr große Listen sollte
`listen=True` vermieden werden.

Die Ausgabe bezeichnet die zweite Implementierung als „GAP“, weil die
Funktionen aus der GAP-Standardbibliothek portiert wurden. Es wird aktuell
kein externes GAP-Programm gestartet.

**Validierung:**

- `n` muss eine ganze Zahl `>= 0` sein.
- `listen` muss exakt `True` oder `False` sein; andere Werte ergeben `TypeError`.
- Für `listen=True` und `gleiche_partitionen` ist praktisch `n >= 1` nötig.
- Wenn die Anzahlen der beiden Implementierungen nicht übereinstimmen, wird
  `RuntimeError` ausgelöst.

---

## 10. Unterliegende Funktionen: `t`

`src/tableau.py` enthält die eigentliche Implementierung. Im interaktiven Modus
ist das Modul als `t` verfügbar. Die meisten Funktionen arbeiten direkt mit
Zeilenlisten und geben Zeilenlisten zurück.

```python
import src.tableau as t

t.row_insert(T.rows, 4)
t.tableau_product_insertion(T.rows, U.rows)
t.tableau_product_jdt(T.rows, U.rows)
t.skew_shapes(S.rows)
t.make_skew((4, 3, 2), (2, 1), [[2, 4], [1, 3], [2, 4]])
t.inner_corners(S.rows)
t.jeu_de_taquin_slide(S.rows, (0, 1))
t.rectify(S.rows)
t.robinson_schensted([3, 1, 4, 2])
```

Die Klassen `Tableau` und `SkewTableau` sind die bequemere, objektorientierte
Schnittstelle. `t` ist nützlich, wenn man mit reinen Zeilenlisten arbeiten
möchte.

**Validierung:**

- Die unterliegenden Funktionen prüfen dieselben Bedingungen wie die Klassen:
  gültige Tableaux, Formen, Füllungen, Startpunkte und Permutationen.
- Die Klassen sind die bequemere Schnittstelle und übernehmen die Prüfungen
  für ihre Objekte.

---

## 11. Eingabeformate und Validierung

Die wichtigsten Formate und ihre Anforderungen:

| Objekt | Format | Erwartet |
|---|---|---|
| Tableau | Liste/Tupel von Zeilenlisten | gültiges Tableau mit positiven Einträgen |
| Tableau-Form | Tupel/Liste positiver ganzer Zahlen | nicht aufsteigende Zeilenlängen |
| Zeileneinfügung `x` | positive ganze Zahl | gültiger neuer Eintrag |
| Tableau-Produkt `U` | `Tableau` | gültiges Tableau |
| schiefes Tableau | Zeilen mit führenden `None` | gültige Skew-Form |
| `lambda`, `mu`, Füllung | Partitionen und Zeilenlisten | `mu` in `lambda`, passende Füllung |
| Slide-Startpunkt | Paar `(Zeile, Spalte)` | innere Ecke |
| Robinson–Schensted-Eingabe | Folge verschiedener positiver `int` | gültige Folge |
| Partition `n` | nichtnegative ganze Zahl | `int >= 0` |
| `listen` | exakt `True` oder `False` | boolescher Wert |
| GUI-Eingabe | Python-Literal | gültiges Literal |

Typische Fehler sind:

- negative oder nicht-ganzzahlige Einträge,
- Zeilen, die nicht schwach steigen,
- Spalten, die nicht streng steigen,
- `None` an einer anderen Stelle als am Zeilenanfang,
- eine innere Form, die nicht in der äußeren Form liegt,
- eine Füllung mit falscher Zeilenlänge,
- ein Slide-Startpunkt, der keine innere Ecke ist,
- ein nicht-boolescher Wert für `listen`.

Solche Fälle führen zu `ValueError` oder `TypeError`. Die GUI fängt diese Fehler
ab und zeigt sie im Ausgabefeld an.

---

## 12. Dateien im Projekt

| Datei | Inhalt |
|---|---|
| `main.py` | Einstiegspunkt, Anleitung, Beispiele und GUI-Start |
| `src/tableau_classes.py` | Klassen `Tableau` und `SkewTableau` |
| `src/tableau.py` | unterliegende Tableau- und Jeu-de-Taquin-Funktionen |
| `src/partitions.py` | Partitionsgenerator und Zählfunktionen |
| `src/interface.py` | tkinter-Oberfläche |
| `partitionen_vergleich.py` | Vergleichs- und Inhaltsfunktionen für Partitionen |

---

## 13. Häufige Probleme

### `ModuleNotFoundError: No module named 'src'`

Dann wurde `main.py` nicht aus dem Projektordner gestartet. Wechsle in den
Ordner, in dem `main.py` liegt, und starte das Programm erneut.

### Farbcodes im Terminal

Die Farben werden nur ausgegeben, wenn die Ausgabe direkt im Terminal landet.
Bei Umleitungen oder gesetzter `NO_COLOR`-Variable bleibt die Ausgabe normal.

---

## 14. Grafische Oberfläche: `gui()`

Die GUI ist optional. Starten mit:

```sh
python main.py gui
```

oder aus der interaktiven Konsole:

```python
gui()
```

Die Oberfläche hat sechs Seiten:

| Seite | Eingabe | Bedeutung |
|---|---|---|
| Partitionen | `75` | zeigt die Partitionen und ihre Anzahl |
| Standardtableaux | `(3, 2)` oder `5` | Form oder Anzahl der Kästchen |
| Zeileneinfügung | `[[1, 3], [2]]`, `1` | Tableau und neuer Eintrag |
| Tableau-Produkt | `[[1, 3], [2]]`, `[[1, 2]]` | zwei Tableaux |
| Jeu de taquin | `[[None, None, 1, 2], [1, 3], [2]]`, `(0, 1)` | schiefes Tableau und Startpunkt |
| Robinson–Schensted | `[3, 1, 4, 2]` | Folge verschiedener positiver Zahlen |

Die Eingabefelder erwarten **Python-Literale**:

- Zahl: `75`
- Tupel: `(3, 2)`
- Liste: `[3, 1, 4, 2]`
- verschachtelte Liste: `[[1, 3], [2]]`
- leerer Platzhalter in schiefen Tableaux: `None`

Ausdrücke wie `2 + 2` oder Variablennamen wie `n` sind nicht erlaubt.

**Validierung in der GUI:**

- Eingaben müssen gültige Python-Literale sein; Syntaxfehler werden abgefangen.
- Tabellen und Zeilen müssen Listen oder Tupel sein.
- `n` muss eine nichtnegative ganze Zahl sein.
- Formen, Tableaux, Skew-Tableaux und Slide-Startpunkte werden nach denselben
  Regeln wie oben geprüft.
- Fehler werden im Ausgabefeld angezeigt; das Programm stürzt nicht ab.

Auf der Seite „Jeu de taquin“ gibt es drei Aktionen:

- **Rektifizieren**: reduziert das schiefe Tableau vollständig,
- **Ein Slide**: führt einen Slide ab dem angegebenen Startpunkt aus,
- **Formen und Ecken**: zeigt äußere Form, innere Form und innere Ecken.

Der Startpunkt eines Slides ist ein Paar `(Zeile, Spalte)`, beginnend bei `0`.
Mögliche Startpunkte liefert `S.inner_corners()`.

### Probleme mit der GUI

#### `ModuleNotFoundError: No module named 'tkinter'`

`tkinter` fehlt. Installiere es, zum Beispiel unter Debian/Ubuntu mit
`sudo apt install python3-tk`.



## Zeileneinfügung im Interface: lineare Suche

Unter „Zeileneinfügung“ verwendet die Schaltfläche **Lineare Suche**
ausschließlich die lineare Variante. Auch die Eingabetaste führt diese
Variante aus.

Sie untersucht jede Zeile von links nach rechts und ersetzt den ersten
Eintrag, der echt größer als der einzufügende Wert ist. Der verdrängte Wert
wird in der nächsten Zeile eingefügt. Gibt es keinen größeren Wert, wird
angehängt und die Einfügung beendet.

Die lineare Variante akzeptiert auch unsortierte Zeilen und prüft weder
Zeilen-/Spaltenordnung noch eine Young-Form. Alle Zahlen müssen weiterhin
positive ganze Zahlen sein. Eingaben sind Listen oder Tupel von Zeilen;
auch das leere Tableau und leere Zeilen sind erlaubt. Die Eingabe bleibt
unverändert. Das Ergebnis wird als Zeilenliste ausgegeben, da bei beliebigen
Eingaben weder Semistandard-Eigenschaft noch Young-Form garantiert sind.

Beispiel: `T = [[5, 1, 3], [2, 4]]`, `x = 4` liefert
`[[4, 1, 3], [2, 4, 5]]`. Trotz des letzten Wertes 3 wird in der ersten
Zeile nicht sofort angehängt: Der erste größere Wert ist dort die 5.

Direkt über das Modul: `t.row_insert_linear(T, x)` nach `python3 -i main.py`.
Die bestehende Tableau-Klasse sowie Tableau-Produkte und Robinson–Schensted
verwenden weiterhin die binäre Variante für semistandard Tableaux. Die
allgemeine Zeileneinfügung im Interface setzt diese Eigenschaft nicht voraus.
