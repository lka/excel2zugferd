# Excel2ZugFeRD

Dieses Programm liest die Daten aus einer Excel Datei aus und hängt sie als ZUGFeRD - kompatible XML-Daten an die erstellte PDF an.

Ich benutze das Programm ausschließlich um meine Stundenabrechnungen zu erledigen. Es werden also nur Stunden "h" als Typen erkannt, alle anderen Typen werden als Minuten im XML-Part dargestellt, auch wenn in der Testrechnung.xlsx beispielsweise "10 Min." stehen.

Die Umsatzsteuer wird ausgewiesen und zwar fix mit 19%.

## Installation

1. Aus dem Release-Verzeichnis in github die neueste Version "setup_excel2zugferd.zip" herunterladen und entpacken.
1. Die Datei "setup_excel2zugferd.exe" als Administrator ausführen. Der Defender Smart Screen sagt dann, dass diese Datei nicht ausgeführt werden sollte, was ich aber will und auf "trotzdem ausführen" klicke. Das Programm wird in das Verzeichnis "C:\Program Files (x86)\Excel2ZugFeRD" installiert.
1. Eine Verknüpfung auf die Datei "excel2zugferd.exe" auf den Desktop kann vom Setup-Programm erstellt werden.

- Wenn eine neue Version des Setup-Programms herauskommt, meckert der Virenscanner bei der Ausführung, dass das eine Datei sei, die einen Virus enthalten könnte, das ist die am Anfang fehlende Hash-Signatur für das Python Setup. Ich sage dann "Download beibehalten" und lasse das Ganze vom Virenprogramm im Internet Scannen. Nach ca. 14 Tagen hat sich das bisher immer gegeben.

## Updates

- Die Vorgehensweise ist Identisch zur Installation.
- Bei der Ausführung des Setup-Programms keine neue Verknüpfung erstellen lassen.

## Programmablauf

Nach dem Start des Programms:

* Wenn keine Ini-Datei vorhanden ist, erstelle sie mit Hilfe der Oberfläche.
    * Sie enthält die Stammdaten des Rechnungserstellers
    * Die Datei "config.ini" steht im Verzeichnis "C:\Benutzer\BENUTZERNAME\AppData\Roaming\excel2zugferd".
* Wenn die Ini-Datei vorhanden ist, lies sie ein.
* Lasse eine Excel-Datei auswählen und lies die Namen der darin vorhandenen Tabellenblätter aus.
* Stelle die Tabellenblätter-Namen als Liste dar und lasse ein Tabellenblatt daraus auswählen.
* Lies die Daten des ausgewählten Tabellenblattes ein und erstelle daraus ein PDF.
* Hänge an das PDF das ZugFeRD Konstrukt im XML-Format an.
* Speichere die Datei als Tabellenblatt-Name.pdf im Verzeichnis der ausgewählten Excel-Datei.

### Stammdateneingabe
![Image der Stammdaten](/assets/Stammdaten.png)

### Excel-Datei
Die Struktur der Excel Datei ist vorgegeben und kann nicht verändert werden, ohne die Funktion zu verlieren.
Als Vorlage benutzen Sie bitte die Datei TestRechnung.xlsx.

## Versionen

### 0.8.0

- fix: 0.8.1 Wenn die Stammdaten aus dem Haupt-Fenster heraus aufgerufen werden, wird das Haupt-Fenster durch die Stammdaten ersetzt. Nach Beendigung der Stammdateneingabe wird das gesamte Programm geschlossen. Der erneute Aufruf liest die "neuen" Stammdaten ein.
- Der Verzicht auf die Erhebung der Umsatzsteuer nach § 19 UStG nach der Kleinuntehmerregelung kann in den Stammdaten eingestellt werden und wird in der Rechnung und im XML ausgewiesen. Zusätzlich muss im Excel die Umsatzsteuer 19% auf den Wert 0.00 € gesetzt werden.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.7.0

- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).
- Die Eingabe vom Bundesland des Rechnungsempfängers ermöglicht.

### 0.6.0

- Das Datum der ersten Position wird als Lieferdatum eingetragen.
- Alle Datumsangaben der Positionen werden im XML zu den Positionen eingetragen.

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