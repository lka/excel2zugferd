# Excel2ZugFeRD

Dieses Programm liest die Daten aus einer Excel Datei aus und hängt sie als ZugFeRD - kompatible XML-Daten an die erstellte PDF an.

# Entwicklung

Erstellt eine Virtual-Env Umgebung: `Ctrl+Shift+P -> Python: Create Environment -> Venv` (einmalig zur Initialisierung des Projektes)

Zum aktivieren der Umgebung: `.\.venv\scripts\activate` aufrufen. (jedes mal)

## Using commit messages

In case you are not familiar with conventional commits (as mentioned above), here is a short summary. Basically, you should prefix your commit messages with one of the following keywords:

- `chore` – used for maintenance, does not result in a new version
- `fix` – used for bug fixes, results in a new patch version (e.g. from `1.2.3` to `1.2.4`)
- `feat` – used for introducing new features, results in a new minor version (e.g. from `1.2.3` to `1.3.0`)
- `feat!` – used for breaking changes, results in a new major version (e.g. from `1.2.3` to `2.0.0`)

Some examples for commit messages are shown below:

- `chore: Initial commit`
- `fix: Correct typo`
- `feat: Add support for Node.js 18`
- `feat!: Change API from v1 to v2`

Please note that `!` indicates breaking changes, and will always result in a new major version, independent of the type of change.

`..\get-next-version-windows-amd64.exe -p 'v' --target json > .\_internal\version.json` schreibt die nächste Versionnummer nach _internal\version.json, wenn das Programm von https://github.com/thenativeweb/get-next-version installiert ist.

## Tests

Die tkinter Umgebung zur Ein- / Ausgabe kann nicht mit Unittests getestet werden. (Todo: mit Selenium testen?)

Alle anderen Klassen werden mit Unittests versehen und getestet.

### Test-Status

[![Python application](https://github.com/lka/excel2zugferd/actions/workflows/python-app.yml/badge.svg)](https://github.com/lka/excel2zugferd/actions/workflows/python-app.yml)

## Implementation

* Die Klasse IniFile behandelt die Vorgaben für das Programm in Form von einem JSON Konstrukt.
* Die Klasse ExcelContent liest eine Excel-Datei und liefert deren Inhalt als DataFrame.
* Die Klasse Pdf (in handlePDF.py) erstellt die PDF-Datei.
* Die Klasse ZugFeRD erstellt die XML Rechnungsdaten nach ZugFeRD 2.2 Spezifikation mit Hilfe der Bibliothek drafthorse.

## Programmablauf

Nach dem Start des Programms:

* Wenn keine Ini-Datei vorhanden ist, erstelle sie mit Hilfe der Oberfläche.
    * Sie enthält die Stammdaten des Rechnungserstellers
* Wenn eine Ini-Datei vorhanden ist, lies sie ein.
* Lasse eine Excel-Datei auswählen und lies Namen der darin vorhandenen Tabellenblätter aus.
* Stelle die Tabellenblätter-Namen als Liste dar und lasse ein Tabellenblatt daraus auswählen.
* Lies die Daten des ausgewählten Tabellenblattes ein und erstelle daraus ein PDF.
* Hänge an das PDF das ZugFeRD Konstrukt im XML-Format an.
* Speichere die Datei als Tabellenblatt-Name.pdf in dem ausgewählten Verzeichnis der Excel-Datei.

## Benutzter Font

### Free Font Pack
For your convenience, the author of the original PyFPDF has collected 96 TTF files in an optional "[Free Unicode TrueType Font Pack for FPDF](https://github.com/reingart/pyfpdf/releases/download/binary/fpdf_unicode_font_pack.zip)", with useful fonts commonly distributed with GNU/Linux operating systems. Note that this collection is from 2015, so it will not contain any newer fonts or possible updates.

Ich habe daraus den Font `DejaVuSansCondensed` gewählt und in allen Ausprägungenen eingebettet.

## Erstellen einer Windows exe

`pyinstaller .\excel2zugferd.py --noconsole --add-data _internal/Fonts:Fonts --add-data ./.venv/Lib/site-packages/drafthorse/schema:drafthorse/schema --noconfirm`

## Copyright and License

Copyright [2024] [Herbert Lischka]
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

### Credits and License

#### pandas

pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

#### fpdf2

It is a fork and the successor of PyFPDF 

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

#### Drafthorse 
Maintainer: Raphael Michel <michel@rami.io>

License of the Python code: Apache License 2.0

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

The PDF handling (drafthorse/pdf.py) is based on the code of factur-x, Copyright 2016-2018, Alexis de Lattre <alexis.delattre@akretion.com>, released under a BSD license.

The packages includes schemas and samples of the ZUGFeRD specification (.xsd and .xml files) which are owned by the Forum für elektronische Rechnungen bei der AWV e.V („FeRD“) and are released under a proprietary license that allows bundling them together with other software for free.