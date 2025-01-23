"""
Module excel2zugferd
"""

from sys import argv
from src.handle_ini_file import IniFile
import src.oberflaeche_ini
import src.oberflaechen
from src.stammdaten import STAMMDATEN
import src


if __name__ == "__main__":
    # print(argv)
    ini = IniFile()
    oberfl = None
    if ini.exists_ini_file() is None:
        oberfl = src.oberflaeche_ini.OberflaecheIniFile(STAMMDATEN, ini)
    else:
        oberfl = src.oberflaechen.OberflaecheExcel2Zugferd(STAMMDATEN, ini,
                                                           argv)
    oberfl.loop()
