# Excel2ZugFeRD

Dieses Programm liest die Daten aus einer Excel Datei aus und hängt sie als ZUGFeRD - kompatible XML-Daten an die neu erstellte Rechnungs-PDF an.

Alternativ kann das Programm den ZugFeRD - Anteil an eine von Ihnen erstellte PDF anhängen. Dann wird die PDF als IhrPdfName_ZuGFeRD.pdf ins Verzeichnis Ihrer PDF gestellt.

Die verwendbaren Einheiten in der Spalte 'Typ' sind:
* 'h': Stunden,
* 'min': Minuten,
* 'Tag(e)': Tage,
* 'Monat(e)': Monate,
* 'Jahr(e)': Jahre,
* 'l': Liter,
* 'Liter': Liter,
* 'kg': Kilogramm,
* 't': Tonne,
* 'm': Meter,
* 'm²': Quadratmeter,
* 'm³': Kubikmeter,
* '1': Stück,
* 'Stk.': Stück,
* 'kWh': Kilowattstunden;
* der Default liefert Stück und dokumentiert in der Beschreibung (BT-154): "Die Einheit 'NIX' ist nicht\
 verfügbar und wurde durch 'C62' (Stück) ersetzt."

 ### Für die Automatisierer:

Das Programm kann auch ohne Oberfläche verwendet werden (nach der Einstellung der Stammdaten):

`"C:\Program Files (x86)\Excel2ZUGFeRD\excel2zugferd.exe" -BlattNr Pfad_zur_Exceldatei.xlsx`

oder

`"C:\Program Files (x86)\Excel2ZUGFeRD\excel2zugferd.exe" -BlattNr Pfad_zur_eigenen_PDF.pdf Pfad_zur_Exceldatei.xlsx`
* BlattNr 0..n: 0 ist das erste Tabellenblatt
* alle Parameter sind als Zeichenketten anzugeben.

- Die Anwendung schreibt Meldungen in die Windows Ereignisanzeige unter 'Windows-Protokolle' -> 'Anwendung' mit der Quelle 'Excel2ZUGFeRD'
- Fehler werden dort als 'Fehler' ausgegeben und das Programm mit exit Code -1 beendet; bitte die Details ansehen
- bei fehlerfreiem Durchlauf wird die Erfolgsmeldung als 'Informationen' ausgegeben und das Programm mit exit Code 0 beendet

## Installation

1. Aus dem Release-Verzeichnis in github die neueste Version "setup_excel2zugferd_x6432_VERSION.msi" herunterladen und als Administrator ausführen.
1. Der Defender Smart Screen sagt dann, dass diese Datei nicht ausgeführt werden sollte, was ich aber will und auf "trotzdem ausführen" klicke. Das Programm wird in das Verzeichnis "C:\Program Files (x86)\Excel2ZugFeRD" installiert.
1. Eine Verknüpfung auf die Datei "excel2zugferd.exe" auf dem Desktop wird vom Setup-Programm erstellt.

- Alternativ: In einem Administrator - CMD Fenster `wget excel2zugferd` ausführen.
- Die Freigabe durch freiwillige Helfer bei WingetCreate findet normalerweise ca. 6 - 12 h nach der neuen Release statt.

- Wenn eine neue Version des Setup-Programms herauskommt, meckert der Virenscanner bei der Ausführung, dass das eine Datei sei, die einen Virus enthalten könnte, das ist die am Anfang fehlende Hash-Signatur für das Python Setup. Ich sage dann "Download beibehalten" und lasse das Ganze vom Virenprogramm im Internet Scannen. Nach ca. 14 Tagen hat sich das bisher immer gegeben.

## Updates

- Die Vorgehensweise ist Identisch zur Installation.
- Alternativ: In einem Administrator - CMD Fenster `wget update excel2zugferd` ausführen.

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
![Image der Sonstigen Stammdaten](/assets/Sonstige.png)
![Image der Excel Steuerung](/assets/Excelsteuerung.png)
![Image der Excel Positionen](/assets/Excelpositionen.png)

### Excel-Datei
Die Struktur der Excel Datei ist vorgegeben und kann nicht verändert werden, ohne die Funktion zu verlieren.
Als Vorlage benutzen Sie bitte die Datei "TestRechnung.xlsx".

Alternativ können Sie die XY-Positionen im Excel Blatt (Spalten: A...Z, Zeilen: 1...) in den Stammdaten "Excel Steuerung" und "Excel Positionen" angeben.
Damit können die XY-Positionen verändert werden und die Suchfunktion wird abgeschaltet. Durch die Angabe der "Excel Positionen" können Sie auch die Überschriften der Einzelpositionen anpassen z.B: Pos. -> Nr., Typ -> EH usw..

## Versionen

### 0.24.x

- Umstellung auf die fpdf2 Release - Version 2.8.3
- In der PDF wird jetzt unterhalb der Rechnungsnummer `Leistungszeitraum VON - BIS` angezeigt.
Die Kennzeichnung für die Kleinunternehmerregelung ist von dieser Position jetzt hinter die Rechnungssummen verschoben worden.
- Der Abgleich mit `wingetcreate` funktioniert wieder. `winget install excel2zugferd` ist daher wieder auf dem aktuellen Stand.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.23.x

- Erweiterung der Benutzung für 'Automatisierer' um die Möglichkeit, eine eigene PDF Datei anzugeben, an die der ZUGFeRD Anteil angehängt werden soll. Dann wird die PDF als IhrPdfName_ZuGFeRD.pdf ins Verzeichnis Ihrer PDF gestellt.

### 0.22.x

- Umstellung des Installers von InnoSetup auf das WiX Toolset zur Erstellung einer Windows MSI Installer Datei.
- Vereinfachung der Codestruktur der Oberfläche und Umstellung auf ttk für eine modernere Darstellung.
- Für mehr als 20 Tabellenblätter in der Excel-Datei hat das Auswahlfeld jetzt eine Scrollbar.
- Das Speichern der Setup-Daten beendet nicht mehr das Programm und unter Datei -> Excel2ZUGFeRD kann vom Setup in das eigentliche Programm gewechselt werden.
- Fehlermeldungen und Programmausführung werden in der Ereignisanzeige unter Anwendungen protokolliert.
- Die Stammdaten werden mit Defaultwerten gefüllt, wenn sie nicht existieren.

### 0.21.x

- Das Programm kann jetzt auch ohne Oberfläche verwendet werden (gedacht für Automatisierungen).

### 0.20.x

- Für eine Funktionalität wie *"Das Datum der Rechnung entspricht dem Datum der Leistungserbringung, sofern nicht anders angegeben."* wird das Rechnungsdatum in die erste Position (wenn sie leer ist) geschrieben und dann fortgeführt.
- Die Sourcen wurden so verändert, dass sie einer Zyklomatischen Komplexität <= 5 entsprechen.
- Der Workaround für die fehlenden Bestandteile der Bibliothek drafthorse wurde entfernt und die Version 2025.1.0 von drafthorse eingeführt.

### 0.19.x

- Die Stammdaten wurden um 2 Eingabefenster für die Angaben der Koordinaten im Excel Blatt ergänzt, um ein flexibleres Parsing der Rechnungspositionen zu ermöglichen. Werden dort keine Angaben gemacht, bleibt es beim bisherigen Verfahren. Werden jedoch Angaben gemacht, sind diese priorisiert. Die Angaben sind wie im Excel Blatt zu machen: Spalten: A...Z, Zeilen: 1...
- Wenn im Excel Blatt "Rechnungsdatum: dd.mm.YYYY" steht, wird das verwendet, ansonsten das aktuelle Datum.

### 0.18.x

- Die Einheit '10 Min.' gelöscht
- Die Einheiten 'kWh', 'Tag(e)', 'Monat(e)', 'Jahr(e)' und 't' ergänzt
- Bei einer nicht bekannten Einheit wird in der Beschreibung eine Erläuterung eingefügt.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.17.x

- Die verwendbaren Einheiten sind erweitert um:
    'h': Stunden,
    'min': Minuten,
    '10 Min.': zehn Sets,
    'l': Liter,
    'Liter': Liter,
    'kg': Kilogramm,
    'm': Meter,
    'm²': Quadratmeter,
    'm³': Kubikmeter,
    '1': Stück,
    'Stk.': Stück;
    der Default liefert Stück
- Wenn Sie andere Einheiten benötigen, bitte als Issue melden.
- Die Rundung der aus Excel übernommenen Fliesskommazahlen ist verbessert.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.16.x

- Die Firmendaten sind ab jetzt vereinzelt, um eine bessere Eingabe zu ermöglichen.
Dabei werden die vorhandenen Stammdaten übernommen und umgesetzt. Redundante Informatinen werden gelöscht.
Bitte prüfen, ob die Daten korrekt sind.
Ab Version 1.0.0 werden die Übernahmefunktionen entfernt.

### 0.15.x

- Die Oberfläche der Stammdaten ist ab jetzt in 2 Fenster aufgeteilt: "Firmendaten" und "Sonstige"

### 0.14.x

- In den Stammdaten kann der "normale" Steuersatz gesetzt werden (Default 19%) falls er mal geändert werden sollte.
- Im ZugFeRD BT-134, die Datumsangabe im Positionstext wird durch das Lieferdatum auf Positionsebene ersetzt; BT-135 entfällt, da immer der gleiche Wert wie in BT-134 gesetzt werden müsste.
- Im ZugFeRD wird BT-14, die Rechnungsperiode, wird auf das Minimum bis zum Maximum der Datumseinträge der Positionen gesetzt.
- für erste Tests: Wenn zugferd.exe mit Parametern aufgerufen wird, wird der letzte Parameter als Pfadangabe für die Excel-Datei betrachtet.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.13.x

- Formatierung der Spalte "Anzahl" mit Trennzeichen "Komma" anstatt "Punkt" bei Dezimalwerten (#18)
- Im ZugFeRD BT-73, BT-74, also den Rechnungszeitraum auf Rechnungsebene gesetzt
- Im ZugFeRD BT-134, BT-135, die Datumsangabe im Positionstext wird durch das Lieferdatum auf Positionsebene ersetzt
- Im ZugFeRD wird eine fehlende Datumsangabe bei der Position mit dem Datum der vorherigen Position gesetzt (#19 teilweise)
- Die Formatierung der Tausenderstellen mit '.' ergänzt
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.12.x

- Sie können mit der Option "anderweitig erzeugtes PDF verwenden" ein von Ihnen selbst anderweitig erzeugtes PDF verwenden und daran den ZugFeRD Part anhängen. Z.B. MS Office Professional Plus 2024 erzeugt ein PDF/A-3A Format, das verwendet werden kann. ACHTUNG: Es liegt in Ihrer Verantwortung, die verwendeten Daten zu prüfen; die Inhalte der PDF werden mit den Inhalten der ZugFeRD xml <b>nicht</b> verglichen !!! Ich prüfe den ZugFeRD Anteil mit Hilfe des Ultramarin eRechnung Viewer. Ein GiroCode kann dann nicht erzeugt  werden.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.11.x

- Eingabe einer Umsatzsteuer-ID ermöglicht.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.10.x

- Verwendungszweck im XML Part eingebaut.
- Die Stammdateneingabe bei Fehleingaben um Fehlermeldungen erweitert.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.9.x

- Die Erstellung eines GiroCode's im Dokument kann jetzt in den Stammdaten eingestellt werden.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.8.x

- fix: 0.8.1 Wenn die Stammdaten aus dem Haupt-Fenster heraus aufgerufen werden, wird das Haupt-Fenster durch die Stammdaten ersetzt. Nach Beendigung der Stammdateneingabe wird das gesamte Programm geschlossen. Der erneute Aufruf liest die "neuen" Stammdaten ein.
- Der Verzicht auf die Erhebung der Umsatzsteuer nach § 19 UStG nach der Kleinuntehmerregelung kann in den Stammdaten eingestellt werden und wird in der Rechnung und im XML ausgewiesen. Zusätzlich muss im Excel die Umsatzsteuer 19% auf den Wert 0.00 € gesetzt werden.
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.7.x

- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).
- Die Eingabe vom Bundesland des Rechnungsempfängers ermöglicht.

### 0.6.x

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