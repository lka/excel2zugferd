## Versionen

### 1.1.0

- Neben Excel-Dateien (.xlsx) können jetzt auch LibreOffice Calc Dateien (.ods) verwendet werden, in der Oberfläche und im Aufruf ohne Oberfläche. Siehe Vorlage "TestRechnung.ods".
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 1.0.0

- Die Oberfläche wurde komplett umgestellt auf ein moderneres Aussehen
- Im Menü "Ansicht" kann zwischen "System" (folgt den Windows-Einstellungen), "Hell" und "Dunkel" umgeschaltet werden. Die Auswahl wird gespeichert.

### 0.28.0

- Das Logo kann jetzt linksbündig, mittig oder rechtsbündig im Bereich zwischen Überschrift, Absender und Adressfeld platziert werden.
- Wenn das Logo kleiner ist als dieser Bereich wird die Größe beibehalten, die Position ist dann oben bündig und entsprechend der Auswahl links, mittig oder rechts.
- Wenn das Logo größer ist, wird es entsprechend skaliert und eingepasst.
- Für die Größenberechnung verwende ich feste 96 DPI.
- Default ist das Verhalten wie vor dieser Änderung.

### 0.27.0

- sowohl Gutschriftanzeige (381), als auch Korrekturrechnung (384) sind jetzt erzeugbar; siehe Vorlage "Gutschriftanzeige", "Gutschriftanzeige negativ" und "Korrekturrechnung" in "TestRechnung.xlsx"
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.26.x

- Unterschiedliche Steuern inklusive Steuersatz 0.00% verfügbar; siehe Vorlage "Rechnung div. Steuern" in "TestRechnung.xlsx"
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

### 0.25.x

- Mehrere Firmenprofile verfügbar, dankenswerterweise beigesteuert von Volker Leitzgen
- Einheit "AW" (Arbeitswerte) mit mapping auf "E48" (service unit)
- Im XML-Part werden die Beträge jetzt mit 2 Nachkommastellen aufgeführt
- Die Validierung des erzeugten ZUGFeRD Dokuments auf https://www.portinvoice.com ist erfolgreich (Ohne Fehler und Warnungen).

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
