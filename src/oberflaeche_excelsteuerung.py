"""
Module OberflaecheExcelSteuerung
"""

from src.middleware import Middleware
import src
import src.oberflaeche_base
import src.oberflaeche_excelpositions
import src.oberflaeche_ini
import src.oberflaeche_steuerung


class OberflaecheExcelSteuerung(src.oberflaeche_base.Oberflaeche):
    """
    Oberflaeche for Ini File Inputs; Steuerung (Excel) Parts
    """

    def __init__(
        self, thefields: dict, middleware: Middleware = None, window=None
    ) -> None:
        super().__init__(window=window, wsize="700x600")  # tk.Toplevel())
        self.fields: dict = thefields
        self.middleware: Middleware = middleware
        self.root.title("Stammdateneingabe - Excel Steuerung")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Stammdateneingabe": {
                            "Firmendaten": self.pre_open_stammdaten,
                            "Steuerung": self.pre_open_steuerung,
                            "Excel Positionen": self.pre_open_excelpositions,
                        },
                        "Separator1": 0,
                        "Excel2ZUGFeRD": self.pre_open_excel2zugferd,
                        "Separator2": 0,
                        "Beenden": self.quit_cmd,
                    }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )

        self.ents = self.makeform("Excel")
        self._add_quit_save_buttons(len(self.ents), self.fetch)
