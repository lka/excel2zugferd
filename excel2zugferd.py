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
    },
    {"Text": "Anschrift", "Label": "Anschrift", "Lines": 5, "Type": "String"},
    {"Text": "Bundesland", "Label": "Bundesland", "Lines": 1,
        "Type": "String"},
    {"Text": "Name", "Label": "Name", "Lines": 1, "Type": "String"},
    {"Text": "Kontakt", "Label": "Kontakt", "Lines": 5, "Type": "String"},
    {"Text": "Umsatzsteuer", "Label": "Umsatzsteuer", "Lines": 2,
        "Type": "String"},
    {"Text": "Konto", "Label": "Konto", "Lines": 3, "Type": "String"},
    {"Text": "Zahlungsziel", "Label": "Zahlungsziel (in Tagen)", "Lines": 1,
        "Type": "String"},
    {"Text": "Abspann", "Label": "Abspann", "Lines": 5, "Type": "String"},
    {"Text": "Verzeichnis", "Label": "Verzeichnis", "Lines": 1,
        "Type": "String"},
    {"Text": "Steuersatz", "Label": "Steuersatz (in %)", "Lines": 1,
        "Type": "String"},
    {
        "Text": "Kleinunternehmen",
        "Label": "Kleinunternehmen",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "Kleinunternehmen",
    },
    {
        "Text": "ZugFeRD",
        "Label": "ZugFeRD Datensatz erzeugen und anhängen",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "ZugFeRD",
    },
    {
        "Text": "GiroCode",
        "Label": "GiroCode erzeugen und einblenden",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "GiroCode",
    },
    {
        "Text": "BYOPdf",
        "Label": "anderweitig erzeugtes PDF verwenden",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "BYOPdf",
    }
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
        oberfl = src.oberflaechen.OberflaecheIniFile(STAMMDATEN)
    else:
        oberfl = src.oberflaechen.OberflaecheExcel2Zugferd(STAMMDATEN, ini,
                                                           argv)
    oberfl.loop()
