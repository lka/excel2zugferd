"""
Modul OberflaecheSteuerung
"""

import tkinter as tk
from tkinter import messagebox
from src.middleware import Middleware
from src.invoice_collection import InvoiceCollection
# from src.oberflaeche_base import Oberflaeche
# from src.oberflaeche_excelsteuerung import OberflaecheExcelSteuerung
# from src.oberflaeche_ini import OberflaecheIniFile
# from src.oberflaeche_excelpositions import OberflaecheExcelPositions
from src.constants import PADX, PADY
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
        super().__init__(window=window)  # tk.Toplevel())
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
                        "Beenden": self.quit_cmd,
                        }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        row = tk.Frame(self.root)
        row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)

        self.ents = self.makeform()

        self.quit_button = tk.Button(self.root, text="Beenden",
                                     command=self.quit_cmd)
        self.quit_button.pack(side=tk.LEFT, padx=PADX, pady=PADY, expand=False)
        self.quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        self.save_button = tk.Button(self.root, text="Speichern",
                                     command=self.fetch)
        self.save_button.pack(side=tk.LEFT, padx=PADX, pady=PADY, expand=False)
        self.save_button.bind("<Return>", (lambda event: self.fetch()))

    def pre_open_stammdaten(self):
        self.fetch_values_from_entries()
        self.open_stammdaten(self.fields, self.middleware)

    def open_stammdaten(self, fields: dict = None,
                        middleware: Middleware = None):
        """
        Open Stammdaten for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_ini\
            .OberflaecheIniFile(fields, middleware, self.root)
        s_oberfl.loop()

    def pre_open_excelsteuerung(self):
        self.fetch_values_from_entries()
        self.open_excelsteuerung(self.fields, self.middleware)

    def open_excelsteuerung(self, fields: dict = None,
                            middleware: Middleware = None):
        """
        Open ExcelSteuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_excelsteuerung\
            .OberflaecheExcelSteuerung(fields, middleware, self.root)
        s_oberfl.loop()

    def pre_open_excelpositions(self):
        self.fetch_values_from_entries()
        self.open_excelpositions(self.fields, self.middleware)

    def open_excelpositions(self, fields: dict = None,
                            middleware: Middleware = None):
        """
        Open Steuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_excelpositions\
            .OberflaecheExcelPositions(fields, middleware, self.root)
        s_oberfl.loop()

    def _check_content_of_stammdaten(self, content: dict) -> bool:
        """return whether stammdaten have failures"""
        try:
            InvoiceCollection(stammdaten=content)
        except ValueError as e:
            messagebox.showerror("Fehler in den Stammdaten", e.args[0])
            return True
        return False

    def fetch_values_from_entries(self) -> dict:
        """
        get all values from items in Oberfläche
        and merge them to ini_file.content
        """
        content = {}
        if self.ents:
            for key, field in self.ents.items():
                content[key] = self._get_text_of_field(field)
            if content:
                return self.middleware.ini_file\
                    .merge_content_of_ini_file(content)
        return content

    def fetch(self):
        """
        get all values for IniFile
        """
        content = self.fetch_values_from_entries()
        ini_has_failure = False
        if content:
            ini_has_failure = self._create_iniFile(
                self.middleware.ini_file, None)
            ini_has_failure = ini_has_failure or \
                self._check_content_of_stammdaten(content)
            if ini_has_failure:
                return
        self.root.destroy()

    def makeform(self) -> dict:
        """
        create the form of Steuerung (Sonstige) Oberflaeche
        """
        entries = {}
        content = {}
        if self.middleware.ini_file:
            content = self.middleware.ini_file.read_ini_file()
        # else:
        #     return entries
        for field in self.fields:
            if (field["Dest"] == "Steuerung"):
                row = tk.Frame(self.root)
                entries[field["Text"]] = self.get_entries_from_type(row,
                                                                    field,
                                                                    content)
        return entries
