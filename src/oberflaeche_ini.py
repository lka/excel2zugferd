"""
Modul OberflaecheIniFile
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
from pathlib import Path
import shutil

from src.middleware import Middleware
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

    def __init__(self, thefields: dict, middleware: Middleware = None,
                 window=None) -> None:
        super().__init__(window=window, wsize="700x800")  # tk.Toplevel())
        self.fields: dict = thefields
        self.middleware: Middleware = middleware
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
                        "Excel2ZUGFeRD": self.pre_open_excel2zugferd,
                        "Beenden": self.quit_cmd
                        }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        row = tk.Frame(self.content_frame)
        row.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY,
                 sticky=tk.W)
        # row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        self.logo_button = ttk.Button(
            row, text="Logo auswählen...",  # anchor="w",
            command=self.handle_file_button
        )
        self.logo_button.pack(side=tk.LEFT, padx=PADX)
        self.logo_button.bind("<Return>",
                              (lambda event: self.handle_file_button))
        self.logo_delete = ttk.Button(
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

        self.ents = self.makeform("Stammdaten", offset=1)
        self._add_quit_save_buttons(len(self.ents)+1, self.fetch)

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
            "Sind Sie sicher, dass Sie das Logo löschen möchten?"
        )
        # print(resp)
        if resp is True:
            os.remove(self.logo_fn)
            self.logo_delete.pack_forget()
            self.canvas.delete("all")
        self.root.lift()
