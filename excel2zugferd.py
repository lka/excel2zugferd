"""
Module excel2zugferd
"""

from sys import argv, exit
import src.oberflaeche_ini
import src.oberflaeche_excel2zugferd
from src.stammdaten import STAMMDATEN
from src.middleware import Middleware
import src


if __name__ == "__main__":
    # print(argv)
    middleware: Middleware = Middleware()

    if middleware.check_args(argv):
        exit(0)

    oberfl = None
    if middleware.ini_file.exists_ini_file() is None:
        oberfl = src.oberflaeche_ini.OberflaecheIniFile(STAMMDATEN,
                                                        middleware)
    else:
        oberfl = src.oberflaeche_excel2zugferd\
            .OberflaecheExcel2Zugferd(STAMMDATEN,
                                      middleware)
    oberfl.loop()
