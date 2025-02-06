"""
Module OberflaecheExcelPositions
"""

# import tkinter as tk
from src.middleware import Middleware
import src
import src.oberflaeche_base
import src.oberflaeche_excelsteuerung
import src.oberflaeche_ini
import src.oberflaeche_steuerung


class OberflaecheExcelPositions(src.oberflaeche_base.Oberflaeche):
    """
    Oberflaeche for Ini File Inputs; Steuerung (Excel Positionen) Parts
    """

    def __init__(self, thefields: dict, middleware: Middleware = None,
                 window=None) -> None:
        super().__init__(window=window, wsize="700x480")  # tk.Toplevel())
        self.fields: dict = thefields
        self.middleware = middleware
        self.root.title("Stammdateneingabe - Excel Positionen")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Stammdateneingabe":
                            {
                                "Firmendaten": self.pre_open_stammdaten,
                                "Steuerung": self.pre_open_steuerung,
                                "Excel Steuerung":
                                    self.pre_open_excelsteuerung,
                            },
                        "Separator": 0,
                        "Excel2ZUGFeRD": self.pre_open_excel2zugferd,
                        "Beenden": self.quit_cmd,
                        }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )

        self.ents = self.makeform("ExcelPos")
        self._add_quit_save_buttons(len(self.ents), self.fetch)
