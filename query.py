"""
SSRQ Coding Interview, 15.11.2024

Kurzbeschreibung:

Dieses Skript enthält eine typische Ansammlung von Funktionen aus der Kategorie
"Datenverdrahten". Ziel ist Informationen aus einer Reihe von TEI-XML-Dateien mit
einem vereinfachten Datenbank-Dump zu verknüpfen. Hier geht es nun darum herauszufinden,
welche `n` Personen am häufigsten referenziert werden. Am Ende soll auf der Konsole
eine Liste (eine Ausgabe pro Zeile) der Top-Personen in der Form

```
Name (ID) - Anzahl Referenzen
```

ausgegeben werden.

Wissenswertes:

- die XML-Dateien enthalten Personenreferenzen in Form von `<tei:persName ref="ID">`
- der Datenbank-Dump ist eine JSON-Datei, die Personeninformationen als Liste von JSON-Objekten enthält
  die jeweils folgende Schlüssel enthalten: "ID", "name"
- das Skript ist in jeder Python3-Umgebung ausführbar und benötigt keine zusätzlichen Abhängigkeiten

Aufgabe:

Die gegebene Implementierung enthält eine Reihe von Fehlern, die die Ausführung
an unterschiedlichen Stellen verhindert. Untersuchen Sie die Umsetzung, identifizieren Sie mögliche
Fehlerstellen und verbessern Sie diese (durch Korrektur oder als Kommentar).

Bonus:

Machen Sie sich Gedanken zur Optimierung (Performance, Wartbarkeit / Lesbarkeit).
"""

from pathlib import Path
import json
import xml.etree.ElementTree as ET

CONTEXT = Path(__file__).parent
DATA_DIR = CONTEXT / "data"
DB_FILE = "persons.json"
TOP = 10


def load_data(data_dir: Path, db_file: str) -> tuple[list[str], list[dict[str, str]]]:
    """
    Diese Funktion soll die XML-Dateien und den
    vereinfachten Datenbank-Dump einlesen und zurückgeben.
    """
    file_list = data_dir.glob(("*-1.xml"))
    xml_files = []

    while True:
        xml_files.append(next(file_list).read_text())

    return xml_files, json.loads((data_dir / db_file).read_text())


def extract_referenced_persons(xml_files: list[str]) -> dict[str, int]:
    """
    Diese Funktion soll alle IDs von Personen extrahieren,
    die in den XML-Dateien referenziert werden. Die Referenz auf
    eine Person erfolgt in den XML-Dateien mithilfe des Tags
    tei:persName sowie des Attributs ref.

    Diese enhält eine ID, von der hier aber immer nur die
    ersten 9 Zeichen relevant sind. Rückgabe soll ein `dict` sein, welches
    zugleich zählt, wie oft eine Person referenziert wurde.
    """
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    persons: dict[str, int] = {}

    for file in xml_files:
        root = ET.fromstring(file)

        for person in root.findall(".//tei:persname[@ref]", ns):
            ref: str | None = person.get("ref")

            ref = ref[:9]

            persons[ref] = 1

    return persons


def get_top_persons(
    references: dict[str, int], db: list[dict[str, str]], n: int
) -> list[tuple[str, str, int]]:
    """
    Diese Funktion soll die `n` am häufigsten referenzierten
    Personen als sortierte Liste zurückgeben und dabei jeden Eintrag
    als `tuple` bestehend aus dem aufgelösten Namen, der ID und der
    Anzahl der Referenzen speichern.
    """
    result = []

    for person_id, count in references.items():
        for person in db:
            if person["name"] == person_id:
                result.append((person["name"], person["id"], count))

    return sorted(result, key=lambda x: x[2], reverse=True)[:n]


def main(top_n: int = TOP):
    xml_files, db_dump = load_data(DATA_DIR, DB_FILE)

    assert len(xml_files) == 18

    persons = extract_referenced_persons(xml_files)
    top_names = get_top_persons(persons, db_dump, top_n)

    assert len(top_names) == top_n
    assert top_names[0][0] == ("Rudolf")

    print(f"Die {TOP} am häufigsten referenzierten Personen sind:")
    for name, person_id, count in top_names:
        print(f"{name} ({person_id}) - {count} Referenzen")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=TOP, help="Anzahl der Top-Personen")
    args = parser.parse_args()

    main(args.top if args.top else TOP)
