"""
Modul OberflaecheSteuerung
"""

from src.middleware import Middleware
import src
import src.oberflaeche_base
import src.oberflaeche_excelpositions
import src.oberflaeche_excelsteuerung
import src.oberflaeche_ini


class OberflaecheSteuerung(src.oberflaeche_base.Oberflaeche):
    """
    Oberflaeche for Ini File Inputs; Steuerung (Sonstige) Parts
    """

    def __init__(self, thefields: dict, middleware: Middleware = None,
                 window=None) -> None:
        super().__init__(window=window, wsize="700x380")  # tk.Toplevel())
        self.fields: dict = thefields
        self.middleware: Middleware = middleware
        self.root.title("Stammdateneingabe - Sonstige")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Stammdateneingabe":
                            {
                                "Firmendaten": self.pre_open_stammdaten,
                                "Excel Steuerung":
                                    self.pre_open_excelsteuerung,
                                "Excel Positionen":
                                    self.pre_open_excelpositions,
                            },
                        "Separator": 0,
                        "Excel2ZUGFeRD": self.pre_open_excel2zugferd,
                        "Beenden": self.quit_cmd,
                        }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        self.ents = self.makeform("Steuerung")
        self._add_quit_save_buttons(len(self.ents), self.fetch)
