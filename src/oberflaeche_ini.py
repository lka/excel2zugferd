"""
Modul OberflaecheIniFile
"""

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import os
import re
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

    def __init__(
        self, thefields: list, middleware: Middleware = None, window=None
    ) -> None:
        super().__init__(window=window, wsize="700x800")  # tk.Toplevel())
        self.fields: list = thefields
        self.middleware: Middleware = middleware
        self.root.title("Stammdateneingabe - Firmendaten")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Stammdateneingabe": {
                            "Sonstige": self.pre_open_steuerung,
                            "Excel Steuerung": self.pre_open_excelsteuerung,
                            "Excel Positionen": self.pre_open_excelsteuerung,
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
        self.company_var = tk.StringVar()
        self.company_row = tk.Frame(self.content_frame)
        self.company_row.grid(
            row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=tk.W
        )
        ttk.Label(self.company_row, text="Firma auswählen:").pack(side=tk.LEFT, padx=PADX)
        self.company_combo = ttk.Combobox(
            self.company_row,
            textvariable=self.company_var,
            state="readonly",
            width=40,
        )
        self.company_combo.pack(side=tk.LEFT, padx=PADX)
        self.company_combo.bind("<<ComboboxSelected>>", self.handle_company_change)
        self.company_actions = tk.Frame(self.content_frame)
        self.company_actions.grid(
            row=1, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=tk.W
        )
        self.company_add_button = ttk.Button(
            self.company_actions, text="Neu", command=self.handle_company_add
        )
        self.company_add_button.pack(side=tk.LEFT, padx=PADX)
        self.company_delete_button = ttk.Button(
            self.company_actions, text="Löschen", command=self.handle_company_delete
        )
        self.company_delete_button.pack(side=tk.LEFT, padx=PADX)
        self.company_rename_button = ttk.Button(
            self.company_actions, text="Umbenennen", command=self.handle_company_rename
        )
        self.company_rename_button.pack(side=tk.LEFT, padx=PADX)
        self.company_export_button = ttk.Button(
            self.company_actions, text="Export", command=self.handle_company_export
        )
        self.company_export_button.pack(side=tk.LEFT, padx=PADX)
        self.company_import_button = ttk.Button(
            self.company_actions, text="Import", command=self.handle_company_import
        )
        self.company_import_button.pack(side=tk.LEFT, padx=PADX)
        row = tk.Frame(self.content_frame)
        row.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=tk.W)
        # row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        self.logo_button = ttk.Button(
            row,
            text="Logo auswählen...",  # anchor="w",
            command=self.handle_file_button,
        )
        self.logo_button.pack(side=tk.LEFT, padx=PADX)
        self.logo_button.bind("<Return>", (lambda event: self.handle_file_button))
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

        self.ents = self.makeform("Stammdaten", offset=3)
        self._refresh_company_selector()
        self._add_quit_save_buttons(len(self.ents) + 3, self.fetch)

    def _refresh_company_selector(self) -> None:
        names = []
        if self.middleware:
            names = self.middleware.ini_file.get_company_names()
        self.company_combo["values"] = names
        active_name = None
        if self.middleware:
            active_name = self.middleware.ini_file.get_active_company_name()
        if active_name:
            self.company_var.set(active_name)
        elif names:
            self.company_var.set(names[0])
        else:
            self.company_var.set("")

    def _load_active_company_into_form(self) -> None:
        content = self.middleware.ini_file.get_active_company_content()
        self.load_values_into_entries(content)

    def _persist_company_changes(self) -> bool:
        return not self._create_iniFile(self.middleware.ini_file, None)

    def handle_company_change(self, event=None):  # pylint: disable=unused-argument
        selected = self.company_var.get()
        if not selected or not self.middleware:
            return
        previous = self.middleware.ini_file.get_active_company_name()
        self.fetch_values_from_entries()
        self.middleware.ini_file.set_active_company(selected)
        self._load_active_company_into_form()
        if not self._persist_company_changes() and previous:
            self.middleware.ini_file.set_active_company(previous)
            self._refresh_company_selector()
            self._load_active_company_into_form()

    def _get_current_form_content(self) -> dict:
        content = {}
        if not self.ents:
            return content
        for key, field in self.ents.items():
            content[key] = self._get_text_of_field(field, key)
        return content

    def handle_company_add(self):
        if not self.middleware:
            return
        self.fetch_values_from_entries()
        name = simpledialog.askstring(
            "Neue Firma", "Name/Betriebsbezeichnung der neuen Firma:"
        )
        if name is None:
            return
        name = name.strip()
        if not name:
            messagebox.showerror("Fehler", "Der Firmenname darf nicht leer sein.")
            return

        self.middleware.ini_file.save_company(
            name,
            {"Betriebsbezeichnung": name},
        )
        self.middleware.ini_file.set_active_company(name)
        self._refresh_company_selector()
        self._load_active_company_into_form()
        if not self._persist_company_changes():
            return
        self.root.lift()

    def handle_company_delete(self):
        if not self.middleware:
            return
        selected = self.company_var.get().strip()
        if not selected:
            messagebox.showinfo("Information", "Es ist keine Firma ausgewählt.")
            return

        confirm = messagebox.askyesno(
            "Firma löschen",
            f"Soll die Firma '{selected}' wirklich gelöscht werden?",
        )
        if not confirm:
            return

        self.fetch_values_from_entries()
        try:
            self.middleware.ini_file.delete_company(selected)
        except ValueError as ex:
            messagebox.showerror("Fehler", ex.args[0])
            return

        self._refresh_company_selector()
        self._load_active_company_into_form()
        if not self._persist_company_changes():
            return
        self.root.lift()

    def handle_company_rename(self):
        if not self.middleware:
            return
        selected = self.company_var.get().strip()
        if not selected:
            messagebox.showinfo("Information", "Es ist keine Firma ausgewählt.")
            return

        self.fetch_values_from_entries()
        new_name = simpledialog.askstring(
            "Firma umbenennen",
            "Neuer Firmenname:",
            initialvalue=selected,
        )
        if new_name is None:
            return
        try:
            renamed_name = self.middleware.ini_file.rename_company(selected, new_name)
        except ValueError as ex:
            messagebox.showerror("Fehler", ex.args[0])
            return

        self._refresh_company_selector()
        self.company_var.set(renamed_name)
        self._load_active_company_into_form()
        if not self._persist_company_changes():
            return
        self.root.lift()

    def _safe_filename_part(self, value: str) -> str:
        sanitized = re.sub(r"[^A-Za-z0-9._-]", "_", value or "firma")
        return sanitized if sanitized else "firma"

    def handle_company_export(self):
        if not self.middleware:
            return
        selected = self.company_var.get().strip()
        if not selected:
            messagebox.showinfo("Information", "Es ist keine Firma ausgewählt.")
            return

        self.fetch_values_from_entries()
        default_name = f"{self._safe_filename_part(selected)}.json"
        target_file = filedialog.asksaveasfilename(
            title="Firmenprofil exportieren",
            initialdir=self.middleware.get_working_directory(),
            initialfile=default_name,
            defaultextension=".json",
            filetypes=(("JSON Datei", "*.json"), ("Alle Dateien", "*.*")),
        )
        if not target_file:
            return
        try:
            self.middleware.ini_file.export_company_profile(selected, target_file)
        except (ValueError, OSError) as ex:
            messagebox.showerror("Fehler", str(ex))
            return
        messagebox.showinfo("Information", f"Firmenprofil exportiert nach:\n{target_file}")

    def handle_company_import(self):
        if not self.middleware:
            return
        source_file = filedialog.askopenfilename(
            title="Firmenprofil importieren",
            initialdir=self.middleware.get_working_directory(),
            filetypes=(("JSON Datei", "*.json"), ("Alle Dateien", "*.*")),
        )
        if not source_file:
            return

        self.fetch_values_from_entries()
        try:
            imported_name = self.middleware.ini_file.import_company_profile(source_file)
        except (ValueError, OSError, KeyError, TypeError) as ex:
            messagebox.showerror("Fehler", f"Import fehlgeschlagen:\n{ex}")
            return

        self._refresh_company_selector()
        self.company_var.set(imported_name)
        self._load_active_company_into_form()
        if not self._persist_company_changes():
            return
        messagebox.showinfo("Information", f"Firmenprofil '{imported_name}' importiert.")
        self.root.lift()

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
            "Löschen des Logos", "Sind Sie sicher, dass Sie das Logo löschen möchten?"
        )
        # print(resp)
        if resp is True:
            os.remove(self.logo_fn)
            self.logo_delete.pack_forget()
            self.canvas.delete("all")
        self.root.lift()

    def fetch_values_from_entries(self):
        content = self._get_current_form_content()
        if content and self.middleware:
            self.middleware.ini_file.save_current_company_content(content)
            self._refresh_company_selector()
            return self.middleware.ini_file.content
        return content
