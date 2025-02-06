STAMMDATEN = [
    {
        "Text": "Betriebsbezeichnung",
        "Label": "Betriebsbezeichnung",
        "Lines": 1,
        "Type": "String",
        "Dest": "Stammdaten"
    },
    # {"Text": "Anschrift", "Label": "Anschrift", "Lines": 5, "Type": "String",
    #     "Dest": "Stammdaten"},
    {"Text": "Abteilung", "Label": "Abteilung (optional)", "Lines": 1,
        "Type": "String",  "Dest": "Stammdaten"},
    {"Text": "Ansprechpartner", "Label": "Ansprechpartner", "Lines": 1,
        "Type": "String",  "Dest": "Stammdaten"},
    {"Text": "Strasse", "Label": "Strasse", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "Hausnummer", "Label": "Hausnummer", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "Postfach",
        "Label": "Postfach (alternativ zu\nStrasse und Hausnr.)",
        "Lines": 1, "Type": "String", "Dest": "Stammdaten"},
    {"Text": "PLZ", "Label": "PLZ", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "Ort", "Label": "Ort", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "Bundesland", "Label": "Bundesland", "Lines": 1,
        "Type": "String",
        "Dest": "Stammdaten"},
    # {"Text": "Name", "Label": "Name", "Lines": 1, "Type": "String",
    #     "Dest": "Stammdaten"},
    # {"Text": "Kontakt", "Label": "Kontakt", "Lines": 5, "Type": "String",
    #     "Dest": "Stammdaten"},
    {"Text": "Telefon", "Label": "Telefon", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "Fax", "Label": "Fax", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "Email", "Label": "E-Mail", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    # {"Text": "Umsatzsteuer", "Label": "Umsatzsteuer", "Lines": 2,
    #     "Type": "String",
    #     "Dest": "Stammdaten"},
    {"Text": "Steuernummer", "Label": "Steuernummer", "Lines": 1,
        "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "Finanzamt", "Label": "Finanzamt", "Lines": 1,
        "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "UmsatzsteuerID",
        "Label": "Umsatzsteuer-ID (alternativ\nzu Steuernr. und Finanzamt)",
        "Lines": 1, "Type": "String", "Dest": "Stammdaten"},
    # {"Text": "Konto", "Label": "Konto", "Lines": 3, "Type": "String",
    #     "Dest": "Stammdaten"},
    {"Text": "Kontoinhaber", "Label": "Kontoinhaber", "Lines": 1,
        "Type": "String",  "Dest": "Stammdaten"},
    {"Text": "IBAN", "Label": "IBAN", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    {"Text": "BIC", "Label": "BIC", "Lines": 1, "Type": "String",
        "Dest": "Stammdaten"},
    {
        "Text": "Kleinunternehmen",
        "Label": "Kleinunternehmen",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "Kleinunternehmen",
        "Dest": "Stammdaten"
    },
    {"Text": "Zahlungsziel",
        "Label": "Zahlungsziel (in Tagen)\n(default 14 Tage)",
        "Lines": 1,
        "Type": "String",
        "Dest": "Steuerung"},
    {"Text": "Abspann", "Label": "Abspann", "Lines": 5, "Type": "String",
        "Dest": "Steuerung"},
    {"Text": "Steuersatz", "Label": "Steuersatz (in %)\n(default 19%)",
        "Lines": 1,
        "Type": "String",
        "Dest": "Steuerung"},
    {
        "Text": "ZugFeRD",
        "Label": "ZugFeRD Datensatz erzeugen und anhängen",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "ZugFeRD",
        "Dest": "Steuerung"
    },
    {
        "Text": "GiroCode",
        "Label": "GiroCode erzeugen und einblenden",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "GiroCode",
        "Dest": "Steuerung"
    },
    {
        "Text": "BYOPdf",
        "Label": "anderweitig erzeugtes PDF verwenden",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "BYOPdf",
        "Dest": "Steuerung"
    },
    {
        "Text": "Verzeichnis", "Label": "Verzeichnis", "Lines": 1,
        "Type": "Label",
        "Dest": "Steuerung",
    },
    {
        "Text": "AnschriftSpalte",
        "Label": "Anschrift Spalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "AnschriftSpalte",
        "Dest": "Excel"
    },
    {
        "Text": "AnschriftZeile",
        "Label": "Anschrift Zeile (1...)",
        "Lines": 1,
        "Type": "String",
        "Variable": "AnschriftZeile",
        "Dest": "Excel"
    },
    {
        "Text": "RechnungSpalte",
        "Label": "Rechnungsnummer\nSpalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "RechnungSpalte",
        "Dest": "Excel"
    },
    {
        "Text": "RechnungZeile",
        "Label": "Rechnungsnummer\nZeile (1...)",
        "Lines": 1,
        "Type": "String",
        "Variable": "RechnungZeile",
        "Dest": "Excel"
    },
    {
        "Text": "RGDatumSpalte",
        "Label": "Rechnungsdatum\nSpalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "RGDatumSpalte",
        "Dest": "Excel"
    },
    {
        "Text": "RGDatumZeile",
        "Label": "Rechnungsdatum\nZeile (1...)",
        "Lines": 1,
        "Type": "String",
        "Variable": "RGDatumZeile",
        "Dest": "Excel"
    },
    {
        "Text": "NettosummeSpalte",
        "Label": "Nettosumme\nSpalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "NettosummeSpalte",
        "Dest": "Excel"
    },
    {
        "Text": "NettosummeZeile",
        "Label": "Nettosumme\nZeile (1...)",
        "Lines": 1,
        "Type": "String",
        "Variable": "NettosummeZeile",
        "Dest": "Excel"
    },
    {
        "Text": "MWStsummeSpalte",
        "Label": "Umsatzsteuersumme\nSpalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "MWStsummeSpalte",
        "Dest": "Excel"
    },
    {
        "Text": "MWStsummeZeile",
        "Label": "Umsatzsteuersumme\nZeile (1...)",
        "Lines": 1,
        "Type": "String",
        "Variable": "MWStsummeZeile",
        "Dest": "Excel"
    },
    {
        "Text": "BruttosummeSpalte",
        "Label": "Bruttosumme\nSpalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "BruttosummeSpalte",
        "Dest": "Excel"
    },
    {
        "Text": "BruttosummeZeile",
        "Label": "Bruttosumme\nZeile (1...)",
        "Lines": 1,
        "Type": "String",
        "Variable": "BruttosummeZeile",
        "Dest": "Excel"
    },
    {
        "Text": "Label1",
        "Label": "↓-- Einzelpositionen im Excel Blatt:\
 Spalten A..Z --↓\n Zeilen 1... ",
        "Lines": 2,
        "Type": "Label",
        "Variable": "Label1",
        "Dest": "ExcelPos"
    },
    {
        "Text": "PositionenZeile",
        "Label": "Einzelpositionen:\nÜberschrift in Zeile (1...)",
        "Lines": 1,
        "Type": "String",
        "Variable": "PositionenZeile",
        "Dest": "ExcelPos"
    },
    {
        "Text": "PosSpalte",
        "Label": "Position:\nin Spalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "PosSpalte",
        "Dest": "ExcelPos"
    },
    {
        "Text": "DatSpalte",
        "Label": "Datum:\nin Spalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "DatSpalte",
        "Dest": "ExcelPos"
    },
    {
        "Text": "DescSpalte",
        "Label": "Beschreibung:\nin Spalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "DescSpalte",
        "Dest": "ExcelPos"
    },
    {
        "Text": "AnzSpalte",
        "Label": "Menge:\nin Spalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "AnzSpalte",
        "Dest": "ExcelPos"
    },
    {
        "Text": "TypSpalte",
        "Label": "Einheit:\nin Spalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "TypSpalte",
        "Dest": "ExcelPos"
    },
    {
        "Text": "PreisSpalte",
        "Label": "Einzelpreis:\nin Spalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "PreisSpalte",
        "Dest": "ExcelPos"
    },
    {
        "Text": "SumSpalte",
        "Label": "Summe:\nin Spalte (A...Z)",
        "Lines": 1,
        "Type": "String",
        "Variable": "SumSpalte",
        "Dest": "ExcelPos"
    },
]
