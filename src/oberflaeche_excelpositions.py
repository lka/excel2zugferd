"""
Module OberflaecheExcelPositions
"""

import customtkinter as ctk

from src.constants import PADX
from src.middleware import Middleware
import src
import src.oberflaeche_base
import src.oberflaeche_excelsteuerung
import src.oberflaeche_ini
import src.oberflaeche_steuerung

HINT = (
    "Geben Sie an, in welcher Zeile die Überschriften der Einzelpositionen\n"
    "stehen und in welcher Spalte (A...Z) die jeweilige Angabe zu finden ist."
)
HEADING_ROW = "PositionenZeile"
LABEL_PX = 130


class OberflaecheExcelPositions(src.oberflaeche_base.Oberflaeche):
    """
    Oberflaeche for Ini File Inputs; Steuerung (Excel Positionen) Parts
    """

    def __init__(
        self, thefields: dict, middleware: Middleware = None, window=None
    ) -> None:
        super().__init__(window=window, wsize="700x500")  # tk.Toplevel())
        self.fields: dict = thefields
        self.middleware = middleware
        self.root.title("Stammdateneingabe - Excel Positionen")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Stammdateneingabe": {
                            "Firmendaten": self.pre_open_stammdaten,
                            "Sonstige": self.pre_open_steuerung,
                            "Excel Steuerung": self.pre_open_excelsteuerung,
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

        self.ents = self.makeform("ExcelPos")
        self._add_quit_save_buttons(2, self.fetch)

    @staticmethod
    def _display_name(field: dict) -> str:
        """name of the value without the hint for the column"""
        return field["Label"].split("\n")[0].rstrip(":")

    def makeform(self, type: str, offset: int = 0) -> dict:
        """one framed box: heading row, then one line per column"""
        content = {}
        if self.middleware.ini_file:
            content = self.middleware.ini_file.get_active_company_content()
        fields = {
            f["Text"]: f for f in self.fields if f["Dest"] == type and f["Type"] == "String"
        }
        card = ctk.CTkFrame(
            self.content_frame, border_width=1, border_color=("gray60", "gray40")
        )
        card.grid(row=offset, column=0, columnspan=2, padx=PADX, pady=PADX, sticky="w")
        self._make_card_head(card)
        entries = self._make_line(card, 2, "Überschriftzeile", fields[HEADING_ROW], content)
        ctk.CTkFrame(card, height=2, corner_radius=0, fg_color=("gray60", "gray45")).grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=6
        )
        ctk.CTkLabel(
            card, text="Spalte (A...Z)", font=ctk.CTkFont(weight="bold")
        ).grid(row=4, column=1, padx=PADX, pady=(2, 0), sticky="w")
        columns = [f for key, f in fields.items() if key != HEADING_ROW]
        for row, field in enumerate(columns, start=5):
            last = row == 4 + len(columns)
            entries.update(
                self._make_line(card, row, self._display_name(field), field, content, last)
            )
        return entries

    @staticmethod
    def _make_card_head(card: ctk.CTkFrame) -> None:
        """title and hint of the box"""
        ctk.CTkLabel(
            card, text="Einzelpositionen", font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=(8, 2), sticky="w")
        ctk.CTkLabel(card, text=HINT, justify="left", anchor="w").grid(
            row=1, column=0, columnspan=2, padx=10, pady=(0, 6), sticky="w"
        )

    def _make_line(
        self, card: ctk.CTkFrame, row: int, name: str, field: dict, content: dict,
        last: bool = False,
    ) -> dict:
        """name and a short input; returns the input"""
        pady = (3, 12) if last else 3
        ctk.CTkLabel(card, text=name, anchor="w", width=LABEL_PX).grid(
            row=row, column=0, padx=(10, 5), pady=pady, sticky="w"
        )
        entry = self._create_textbox(card, field, content, 100)
        entry.grid(row=row, column=1, padx=(PADX, 12), pady=pady, sticky="w")
        return {field["Text"]: entry}
