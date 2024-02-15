# Excel2ZugFeRD

Dieses Programm liest die Daten aus einer Excel Datei aus und hängt sie als ZugFeRD - kompatible XML-Daten an die erstellte PDF an.

# Entwicklung

Erstellt eine Virtual-Env Umgebung: `Ctrl+Shift+P -> Python: Create Environment -> Venv`

Zum aktivieren der Umgebung: `.\.venv\scripts\activate` aufrufen.

## Tests

Die tkinter Umgebung zur Ein- / Ausgabe kann nicht mit Unittests getestet werden. (Todo: mit Selenium testen?)

Alle anderen Klassen werden mit Unittests versehen und getestet.

## Implementation

Die Klasse IniFile behandelt die Vorgaben für das Programm in Form von einem JSON Konstrukt.

Die Klasse ExcelContent liest eine Excel-Datei und liefert deren Inhalt als DataFrame.

Die Klasse ZugFeRD erstellt die XML Rechnungsdaten nach ZugFeRD 2.2 Spezifikation mit Hilfe der Bibliothek drafthorse.

## Programmablauf

Nach dem Start des Programms:

* Wenn keine Ini-Datei vorhanden ist, erstelle sie mit Hilfe der Oberfläche.
    * Sie enthält die Stammdaten des Rechnungserstellers
* Wenn eine Ini-Datei vorhanden ist, lies sie ein.
* Lasse eine Excel-Datei auswählen und lies die darin vorhandenen Sheet-Namen aus.
* Stelle die Sheet-Namen als Liste dar und lasse ein Sheet daraus auswählen.
* Lies das ausgewählte Sheet ein und erstelle daraus ein PDF.
* Hänge an das PDF das ZugFeRD Konstrukt im XML-Format an.
* Speichere die Datei als Rechnung_Rechnungsnummer.pdf in einem ausgewählten Verzeichnis.

## Benutzter Font

### Free Font Pack
For your convenience, the author of the original PyFPDF has collected 96 TTF files in an optional "[Free Unicode TrueType Font Pack for FPDF](https://github.com/reingart/pyfpdf/releases/download/binary/fpdf_unicode_font_pack.zip)", with useful fonts commonly distributed with GNU/Linux operating systems. Note that this collection is from 2015, so it will not contain any newer fonts or possible updates.

Ich habe daraus den Font `DejaVuSansCondensed` gewählt und in allen Ausprägungenen eingebettet.
