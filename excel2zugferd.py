"""
Module excel2zugferd
"""

from sys import argv
from src.handle_ini_file import IniFile
from tkinter import messagebox
import src.oberflaeche_ini
import src.oberflaechen
from src.stammdaten import STAMMDATEN
import src


if __name__ == "__main__":
    # print(argv)
    try:
        ini = IniFile()
    except ValueError as e:
        messagebox.showerror("Fehler", e.msg)
        exit(-1)

    oberfl = None
    if ini.exists_ini_file() is None:
        oberfl = src.oberflaeche_ini.OberflaecheIniFile(STAMMDATEN, ini)
    else:
        oberfl = src.oberflaechen.OberflaecheExcel2Zugferd(STAMMDATEN, ini,
                                                           argv)
    oberfl.loop()
