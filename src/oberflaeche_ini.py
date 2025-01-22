"""
Module Oberflaechen
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import os
from pathlib import Path
import shutil

from src.handle_ini_file import IniFile
from src.collect_data import InvoiceCollection
# from src.oberflaeche_base import Oberflaeche
# from src.oberflaeche_excelsteuerung import OberflaecheExcelSteuerung
# from src.oberflaeche_steuerung import OberflaecheSteuerung
# from src. oberflaeche_excelpositions import OberflaecheExcelPositions
from src.constants import PADX, PADY
import src
import src.oberflaeche_base
import src.oberflaeche_excelpositions
import src.oberflaeche_excelsteuerung
import src.oberflaeche_steuerung


class OberflaecheIniFile(src.oberflaeche_base.Oberflaeche):
    """
    Oberflaeche for Ini File Inputs
    """

    def __init__(self, thefields: dict, myini_file: IniFile = None,
                 window=None) -> None:
        super().__init__(window=window)  # tk.Toplevel())
        self.fields: dict = thefields
        self.menuvars = {}
        self.ini_file: IniFile = myini_file
        self.root.title("Stammdateneingabe - Firmendaten")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Stammdateneingabe":
                            {
                                "Sonstige": self.pre_open_steuerung,
                                "Excel Steuerung":
                                    self.pre_open_excelsteuerung,
                                "Excel Positionen":
                                    self.pre_open_excelsteuerung,
                            },
                        "Separator": 0,
                        "Beenden": self.quit_cmd
                        }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        row = tk.Frame(self.root)
        row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        self.logo_button = tk.Button(
            row, text="Logo auswählen...", anchor="w",
            command=self.handle_file_button
        )
        self.logo_button.pack(side=tk.LEFT, padx=PADX)
        self.logo_button.bind("<Return>",
                              (lambda event: self.handle_file_button))
        self.logo_delete = tk.Button(
            row, text="Logo löschen", command=self.handle_logo_delete_button
        )
        self.logo_delete.bind(
            "<Return>", (lambda event: self.handle_logo_delete_button)
        )
        if Path(self.logo_fn).exists():
            self.logo_delete.pack(side=tk.LEFT, padx=PADX)

        self.canvas = tk.Canvas(row, width=100, height=100, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=38, anchor="w", expand=True)

        self.make_logo(self.logo_fn)

        self.ents = self.makeform()
        # self.root.bind('<Return>', (lambda event,
        # e=self.ents: self.fetch(e)))
        self.quit_button = tk.Button(self.root, text="Beenden",
                                     command=self.quit_cmd)
        self.quit_button.pack(side=tk.LEFT, padx=PADX, pady=PADY, expand=False)
        self.quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        self.save_button = tk.Button(self.root, text="Speichern",
                                     command=self.fetch)
        self.save_button.pack(side=tk.LEFT, padx=PADX, pady=PADY, expand=False)
        self.save_button.bind("<Return>", (lambda event: self.fetch()))

    def pre_open_steuerung(self):
        self.fetch_values_from_entries()
        self.open_steuerung(self.fields, self.ini_file)

    def open_steuerung(self, fields: dict = None, ini_file: str = None):
        """
        Open Steuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_steuerung\
            .OberflaecheSteuerung(fields, ini_file, self.root)
        s_oberfl.loop()

    def pre_open_excelsteuerung(self):
        self.fetch_values_from_entries()
        self.open_excelsteuerung(self.fields, self.ini_file)

    def open_excelsteuerung(self, fields: dict = None, ini_file: str = None):
        """
        Open ExcelSteuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_excelsteuerung\
            .OberflaecheExcelSteuerung(fields, ini_file, self.root)
        s_oberfl.loop()

    def pre_open_excelpositions(self):
        self.fetch_values_from_entries()
        self.open_excelpositions(self.fields, self.ini_file)

    def open_excelpositions(self, fields: dict = None, ini_file: str = None):
        """
        Open Steuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_excelpositions\
            .OberflaecheExcelPositions(fields, ini_file, self.root)
        s_oberfl.loop()

    def _check_content_of_stammdaten(self, content: dict) -> bool:
        """return whether stammdaten have failures"""
        try:
            InvoiceCollection(stammdaten=content)
        except ValueError as e:
            messagebox.showerror("Fehler in den Stammdaten", e)
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
                return self.ini_file.merge_content_of_ini_file(content)
        return content

    def fetch(self):
        """
        get all values for IniFile
        """
        content = self.fetch_values_from_entries()
        ini_has_failure = False
        if content:
            ini_has_failure = self._create_iniFile(
                self.ini_file, None)
            ini_has_failure = ini_has_failure or \
                self._check_content_of_stammdaten(content)
            if ini_has_failure:
                return
        self.root.destroy()

    def makeform(self) -> dict:
        """
        create the form of IniFile Oberflaeche
        """
        entries = {}
        content = {}
        if self.ini_file:
            content = self.ini_file.read_ini_file()
        # else:
        #     return entries
        # print(self.ini_file, content)
        # print(fields)
        for field in self.fields:
            if field["Dest"] == "Stammdaten":
                row = tk.Frame(self.root)
                entries[field["Text"]] = self.get_entries_from_type(row,
                                                                    field,
                                                                    content)
        return entries

    def handle_file_button(self):
        """
        get the Path of Users/Pictures
        """
        init_dir = Path.joinpath(Path.home(), "Pictures")

        filename = filedialog.askopenfilename(
            title="Bitte die Datei mit dem Logo auswählen",
            initialdir=Path(init_dir).resolve(),
            filetypes=(("Bilder", "*.jpg; *.jpeg"), ("Alle Dateien", "*.*")),
        )

        if filename is not None and filename:
            shutil.copy(filename, self.logo_fn)
            self.make_logo(self.logo_fn)
            self.logo_delete.pack(side=tk.LEFT, padx=5)
            self.root.lift()

    def handle_logo_delete_button(self):
        """
        ask for deletion with really?
        """
        resp = messagebox.askyesno(
            "Löschen des Logos",
            "Sind Sie sicher, dass Sie das Logolöschen möchten?"
        )
        # print(resp)
        if resp is True:
            os.remove(self.logo_fn)
            self.logo_delete.pack_forget()
            self.canvas.delete("all")
        self.root.lift()
