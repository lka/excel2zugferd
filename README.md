# Excel2ZugFeRD

Dieses Programm liest die Daten aus einer Excel Datei aus und hängt sie als ZugFeRD - kompatible XML-Daten an die erstellte PDF an.

Ich benutze das Programm ausschließlich um meine Stundenabrechnungen zu erledigen. Es werden also nur Stunden "h" als Typen erkannt, alle anderen Typen werden als Minuten im ZugFerd-Part dargestellt, auch wenn in der Testrechnung.xlsx beispielsweise "10 Min." stehen.

Die Umsatzsteuer wird ausgewiesen und zwar fix mit 19%.

Das Datum von Position 1 wird als Lieferdatum eingetragen.

## Installation

1. Aus dem Release-Verzeichnis in github die neueste Version "setup_excel2zugferd.zip" herunterladen und entpacken.
    Mein Virenscanner meckert dabei, dass das eine Datei sei, die einen Virus enthalten könnte, was Quatsch ist, das ist die fehlende Signatur für das Python Setup. Ich sage dann "Download beibehalten".
1. Die Datei "setup_excel2zugferd.exe" als Administrator ausführen. Der Defender Smart Screen sagt dann, dass diese Datei nicht ausgeführt werden sollte, was ich aber will und auf "trotzdem ausführen" klicke. Das Programm wird in das Verzeichnis "C:\Program Files (x86)\Excel2ZugFeRD" installiert.
1. Eine Verknüpfung auf die Datei "C:\Program Files (x86)\Excel2ZugFeRD\excel2zugferd.exe" dort erzeugen, von wo aus das Programm gestartet werden können soll. Ich habe das von meinem Desktop aus gemacht.

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
Als Vorgabe benutzen Sie bitte die Datei TestRechnung.xlsx.

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