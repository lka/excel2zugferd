"""
Module OberflaecheExcelSteuerung
"""

import re

import customtkinter as ctk

from src.constants import PADX, PADY
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
                            "Sonstige": self.pre_open_steuerung,
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
        self._add_quit_save_buttons(len(self.ents) // 2 + 2, self.fetch)

    @staticmethod
    def _display_name(field: dict) -> str:
        """name of the value without the hint for column or row"""
        name = re.split(r"\s*\n|\s+Spalte", field["Label"])[0]
        return name + (" (optional)" if "optional" in field["Label"] else "")

    def makeform(self, type: str, offset: int = 0) -> dict:
        """one line per value: name, column and row side by side"""
        content = {}
        if self.middleware.ini_file:
            content = self.middleware.ini_file.get_active_company_content()
        fields = {f["Text"]: f for f in self.fields if f["Dest"] == type}
        self._make_header(offset)
        entries = {}
        pairs = [(k, fields[k[: -len("Spalte")] + "Zeile"]) for k in fields if k.endswith("Spalte")]
        for row, (key, zeile) in enumerate(pairs, start=offset + 1):
            entries.update(self._make_line(row, fields[key], zeile, content))
        return entries

    def _make_header(self, row: int) -> None:
        """column headings"""
        head = ctk.CTkFont(weight="bold")
        for col, text in enumerate(("", "Spalte (A...Z)", "Zeile (1...)")):
            ctk.CTkLabel(self.content_frame, text=text, font=head).grid(
                row=row, column=col, padx=PADX, pady=PADY, sticky="w"
            )

    def _make_line(self, row: int, spalte: dict, zeile: dict, content: dict) -> dict:
        """name with the inputs for column and row, returns the inputs"""
        ctk.CTkLabel(
            self.content_frame, text=self._display_name(spalte), anchor="w"
        ).grid(row=row, column=0, padx=PADX, pady=PADY, sticky="w")
        entries = {}
        for col, fld in ((1, spalte), (2, zeile)):
            entry = self._create_textbox(self.content_frame, fld, content, 100)
            entry.grid(row=row, column=col, padx=PADX, pady=PADY, sticky="w")
            entries[fld["Text"]] = entry
        return entries
