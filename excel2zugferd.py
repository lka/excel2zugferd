"""
Module excel2zugferd
"""

from sys import argv
from src.handle_ini_file import IniFile
from pathlib import Path
import os
import src.oberflaechen
from tkinter import messagebox

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
    {"Text": "Zahlungsziel", "Label": "Zahlungsziel (in Tagen)", "Lines": 1,
        "Type": "String",
        "Dest": "Steuerung"},
    {"Text": "Abspann", "Label": "Abspann", "Lines": 5, "Type": "String",
        "Dest": "Steuerung"},
    {"Text": "Steuersatz", "Label": "Steuersatz (in %)", "Lines": 1,
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
    # {
    #     "Text": "Label1",
    #     "Label": "↓--------------- Wird automatisch befüllt\
    #  ---------------↓",
    #     "Lines": 2,
    #     "Type": "Label",
    #     "Variable": "Label1",
    #     "Dest": "Steuerung"
    # },
    {"Text": "Verzeichnis", "Label": "Verzeichnis", "Lines": 1,
        "Type": "Label",
        "Dest": "Steuerung"},
]

if __name__ == "__main__":
    # print(argv)
    thedir = Path.joinpath(
        Path(os.getenv("APPDATA")).resolve(), Path("excel2zugferd")
    )
    ini = IniFile("config.ini", thedir)
    if not Path.exists(thedir):
        try:
            os.mkdir(thedir)
        except IOError as e:
            msg = f"Ich kann das Verzeichnis {dir} nicht erstellen.\n\
                    {src.oberflaechen.format_ioerr(e)}"
            messagebox.showerror("Fehler", msg)
    oberfl = None
    if ini.exists_ini_file() is None:
        oberfl = src.oberflaechen.OberflaecheIniFile(STAMMDATEN, ini)
    else:
        oberfl = src.oberflaechen.OberflaecheExcel2Zugferd(STAMMDATEN, ini,
                                                           argv)
    oberfl.loop()
