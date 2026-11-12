"""
Modul OberflaecheIniFile
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
import os
import re
from pathlib import Path
import shutil
from PIL import Image

from src.middleware import Middleware
from src.handle_pdf import LOGO_BOX, logo_placement
from src.constants import (
    PADX,
    PADY,
    LOGO_ALIGN_KEY,
    LOGO_ALIGN_DEFAULT,
    LOGO_ALIGN_CHOICES,
)
import src
import src.oberflaeche_base
import src.oberflaeche_excelpositions
import src.oberflaeche_excelsteuerung
import src.oberflaeche_steuerung

TAB_ACTIVE_COLOR = ("#3B8ED0", "#1F6AA5")
TAB_INACTIVE_COLOR = ("gray75", "gray28")
TAB_HOVER_COLOR = ("gray65", "gray35")
SEPARATOR = "-"  # row type: horizontal line inside a card
TAB_NAMES = ("Anschrift", "Steuer und Bank", "Logo")
CARD_PAGES = (0, 1, 1)  # tab of each entry of CARDS
CARDS = [
    (
        "Anschrift und Kontakt",
        [
            ("Firma", [("Betriebsbezeichnung", 400)]),
            ("Abteilung", [("Abteilung", 400)]),
            ("z. Hd.", [("Ansprechpartner", 400)]),
            ("Straße / Nr.", [("Strasse", 300), (None, "Nr."), ("Hausnummer", 70)]),
            ("PLZ / Ort", [("PLZ", 90), (None, " "), ("Ort", 300)]),
            ("Bundesland", [("Bundesland", 400)]),
            ("Postfach", [("Postfach", 400)]),
            ("Telefon", [("Telefon", 400)]),
            ("Fax", [("Fax", 400)]),
            ("E-Mail", [("Email", 400)]),
        ],
    ),
    (
        "Steuerdaten",
        [
            (
                "Steuernr. / FA",
                [("Steuernummer", 150), (None, "Finanzamt"), ("Finanzamt", 200)],
            ),
            (None, [(None, "oder")]),
            ("USt-IdNr.", [("UmsatzsteuerID", 200)]),
            (SEPARATOR, None),
            ("", [("Kleinunternehmen", 0)]),
        ],
    ),
    (
        "Bankverbindung",
        [
            ("Kontoinhaber", [("Kontoinhaber", 400)]),
            ("IBAN", [("IBAN", 300)]),
            ("BIC", [("BIC", 150)]),
        ],
    ),
]
PREVIEW_WIDTH = 400  # px, corresponds to the width of LOGO_BOX
PREVIEW_HEIGHT = round(PREVIEW_WIDTH * LOGO_BOX[3] / LOGO_BOX[2])


class OberflaecheIniFile(src.oberflaeche_base.Oberflaeche):
    """
    Oberflaeche for Ini File Inputs
    """

    def __init__(
        self, thefields: list, middleware: Middleware = None, window=None
    ) -> None:
        super().__init__(window=window, wsize="720x680")  # tk.Toplevel())
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
        self.company_var = tk.StringVar()
        self.company_row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.company_row.grid(
            row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=tk.W
        )
        ctk.CTkLabel(self.company_row, text="Firma auswählen:").pack(side=tk.LEFT, padx=PADX)
        self.company_combo = ctk.CTkComboBox(
            self.company_row,
            variable=self.company_var,
            state="readonly",
            width=320,
            values=[""],
            command=self.handle_company_change,
        )
        self.company_combo.pack(side=tk.LEFT, padx=PADX)
        self.company_actions = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.company_actions.grid(
            row=1, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=tk.W
        )
        self.company_add_button = ctk.CTkButton(
            self.company_actions, text="Neu", width=110, command=self.handle_company_add
        )
        self.company_add_button.pack(side=tk.LEFT, padx=PADX)
        self.company_delete_button = ctk.CTkButton(
            self.company_actions, text="Löschen", width=110, command=self.handle_company_delete
        )
        self.company_delete_button.pack(side=tk.LEFT, padx=PADX)
        self.company_rename_button = ctk.CTkButton(
            self.company_actions, text="Umbenennen", width=110, command=self.handle_company_rename
        )
        self.company_rename_button.pack(side=tk.LEFT, padx=PADX)
        self.company_export_button = ctk.CTkButton(
            self.company_actions, text="Export", width=110, command=self.handle_company_export
        )
        self.company_export_button.pack(side=tk.LEFT, padx=PADX)
        self.company_import_button = ctk.CTkButton(
            self.company_actions, text="Import", width=110, command=self.handle_company_import
        )
        self.company_import_button.pack(side=tk.LEFT, padx=PADX)
        self.ents = self.makeform("Stammdaten", offset=2)
        self._refresh_company_selector()
        self._add_quit_save_buttons(4, self.fetch)

    def makeform(self, type: str, offset: int = 0) -> dict:
        """create the form on three tabs; related fields are grouped in boxes"""
        content = {}
        if self.middleware.ini_file:
            content = self.middleware.ini_file.get_active_company_content()
        self._make_tab_nav(offset)
        pages = self._make_tab_pages(offset + 1)
        entries = self._make_cards(pages, content)
        entries.update(self._make_remaining_fields(type, pages[1], content, entries))
        self._make_logo_card(pages[2])
        self._show_tab(TAB_NAMES[0])
        return entries

    def _make_tab_nav(self, grid_row: int) -> None:
        """row of buttons to switch between the tabs"""
        self.tab_nav = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tab_nav.grid(
            row=grid_row, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="w"
        )
        self.tab_buttons = {}
        for name in TAB_NAMES:
            button = ctk.CTkButton(
                self.tab_nav,
                text=name,
                width=150,
                command=lambda n=name: self._show_tab(n),
            )
            button.pack(side="left", padx=(0, 4))
            self.tab_buttons[name] = button

    def _make_tab_pages(self, grid_row: int) -> list:
        """one frame per tab, all in the same grid cell"""
        pages = [
            ctk.CTkFrame(self.content_frame, fg_color="transparent")
            for _ in TAB_NAMES
        ]
        self.tab_pages = dict(zip(TAB_NAMES, pages))
        for page in pages:
            page.grid(row=grid_row, column=0, columnspan=2, sticky="nw")
        return pages

    def _make_cards(self, pages: list, content: dict) -> dict:
        """put the boxes of CARDS on their tabs, returns their entries"""
        entries = {}
        by_key = {f["Text"]: f for f in self.fields}
        for page, (title, rows) in zip(CARD_PAGES, CARDS):
            grid_row = len(pages[page].grid_slaves())
            entries.update(
                self._make_card(pages[page], grid_row, title, rows, by_key, content)
            )
        return entries

    def _make_remaining_fields(
        self, type: str, page: ctk.CTkFrame, content: dict, done: dict
    ) -> dict:
        """fields of this form which are not part of a box"""
        entries = {}
        row = len(page.grid_slaves())
        for field in self.fields:
            if field["Dest"] == type and field["Text"] not in done:
                entries[field["Text"]] = self.get_entries_from_type(
                    page, field, content, row
                )
                row += 1
        return entries

    def _show_tab(self, name: str) -> None:
        """show the page of the selected tab, hide the others"""
        for tab, page in self.tab_pages.items():
            selected = tab == name
            if selected:
                page.grid()
            else:
                page.grid_remove()
            self.tab_buttons[tab].configure(
                fg_color=TAB_ACTIVE_COLOR if selected else TAB_INACTIVE_COLOR,
                hover_color=TAB_ACTIVE_COLOR if selected else TAB_HOVER_COLOR,
                text_color=("white", "white") if selected else ("black", "white"),
            )

    def _make_card(
        self,
        parent: ctk.CTkFrame,
        grid_row: int,
        title: str,
        rows: list,
        by_key: dict,
        content: dict,
    ) -> dict:
        """build one framed block, returns its entries"""
        card = ctk.CTkFrame(parent, border_width=1, border_color=("gray60", "gray40"))
        card.grid(
            row=grid_row, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="w"
        )
        ctk.CTkLabel(
            card, text=title, font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=(8, 2), sticky="w")
        entries = {}
        for row, (label, keys_widths) in enumerate(rows, start=1):
            if label == SEPARATOR:
                self._make_separator(card, row)
            else:
                pady = (3, 12) if row == len(rows) else 3
                line = self._make_card_line(card, row, label, pady)
                entries.update(self._make_line_entries(line, keys_widths, by_key, content))
        return entries

    @staticmethod
    def _make_separator(card: ctk.CTkFrame, row: int) -> None:
        """horizontal line inside a card"""
        ctk.CTkFrame(
            card, height=2, corner_radius=0, fg_color=("gray60", "gray45")
        ).grid(row=row, column=0, columnspan=2, sticky="ew", padx=10, pady=6)

    @staticmethod
    def _make_card_line(
        card: ctk.CTkFrame, row: int, label: str, pady: tuple | int
    ) -> ctk.CTkFrame:
        """label and the frame which takes the inputs of one line"""
        ctk.CTkLabel(card, text=label or "", anchor="w", width=110).grid(
            row=row, column=0, padx=(10, 5), pady=pady, sticky="nw"
        )
        line = ctk.CTkFrame(card, fg_color="transparent")
        line.grid(row=row, column=1, padx=(0, 12), pady=pady, sticky="w")
        return line

    def _make_line_entries(
        self, line: ctk.CTkFrame, keys_widths: list, by_key: dict, content: dict
    ) -> dict:
        """inputs (or separator texts) of one line, returns the inputs"""
        entries = {}
        for key, width in keys_widths:
            if key is None:  # separator text
                ctk.CTkLabel(line, text=width).pack(side="left", padx=5)
                continue
            if by_key[key]["Type"] == "Boolean":
                entries[key] = self._create_checkbox(line, by_key[key], content)
            else:
                entries[key] = self._create_textbox(line, by_key[key], content, width)
            entries[key].pack(side="left")
        return entries

    def _make_logo_card(self, parent: ctk.CTkFrame) -> None:
        """framed box with all elements for the logo"""
        card = ctk.CTkFrame(
            parent, border_width=1, border_color=("gray60", "gray40")
        )
        card.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")
        ctk.CTkLabel(
            card, text="Logo", font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=10, pady=(8, 2))
        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(anchor="w", padx=5, pady=3)
        self.logo_button = ctk.CTkButton(
            buttons, text="Logo auswählen...", command=self.handle_file_button
        )
        self.logo_button.pack(side=tk.LEFT, padx=PADX)
        self.logo_button.bind("<Return>", (lambda event: self.handle_file_button))
        self.logo_delete = ctk.CTkButton(
            buttons, text="Logo löschen", command=self.handle_logo_delete_button
        )
        self.logo_delete.bind(
            "<Return>", (lambda event: self.handle_logo_delete_button)
        )
        if Path(self.logo_fn).exists():
            self.logo_delete.pack(side=tk.LEFT, padx=PADX)
        self.canvas = tk.Canvas(
            card,
            width=PREVIEW_WIDTH,
            height=PREVIEW_HEIGHT,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.pack(anchor="w", padx=10, pady=5)
        self._make_logo_align_row(card)
        self._show_logo()

    def _make_logo_align_row(self, parent: ctk.CTkFrame) -> None:
        """input for the horizontal placement of the logo in the pdf"""
        current = LOGO_ALIGN_DEFAULT
        if self.middleware and self.middleware.ini_file:
            current = self.middleware.ini_file.content.get(
                LOGO_ALIGN_KEY, LOGO_ALIGN_DEFAULT
            )
        if current not in LOGO_ALIGN_CHOICES.values():
            current = LOGO_ALIGN_DEFAULT
        self.logo_align_var = tk.StringVar(value=current)
        align_row = ctk.CTkFrame(parent, fg_color="transparent")
        align_row.pack(anchor="w", padx=5, pady=(3, 12))
        ctk.CTkLabel(align_row, text="Logo platzieren:").pack(side=tk.LEFT, padx=PADX)
        for text, value in LOGO_ALIGN_CHOICES.items():
            ctk.CTkRadioButton(
                align_row,
                text=text,
                value=value,
                variable=self.logo_align_var,
                command=self._show_logo,
            ).pack(side=tk.LEFT, padx=PADX)

    def _show_logo(self) -> None:
        """show the logo in the preview where it will be placed in the pdf.
        The preview shows the area LOGO_BOX of the page"""
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0, 0, PREVIEW_WIDTH - 1, PREVIEW_HEIGHT - 1, outline="lightgrey"
        )
        if not Path(self.logo_fn).exists():
            return
        with Image.open(self.logo_fn) as img:
            size = img.size
        box_x, box_y, _, _ = LOGO_BOX
        x, y, w, h = logo_placement(size, self.logo_align_var.get())
        scale = PREVIEW_WIDTH / LOGO_BOX[2]
        self.make_logo(
            self.logo_fn,
            (
                round((x - box_x) * scale),
                round((y - box_y) * scale),
                round(w * scale),
                round(h * scale),
            ),
        )

    def _refresh_company_selector(self) -> None:
        names = []
        if self.middleware:
            names = self.middleware.ini_file.get_company_names()
        self.company_combo.configure(values=names or [""])
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
        # fetch_values_from_entries has reset the selector to the previous company
        self._refresh_company_selector()
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
        name = self.ask_string(
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
        if not self._confirm_company_deletion(selected):
            return

        self.fetch_values_from_entries()
        if not self._delete_company(selected):
            return

        self._refresh_company_selector()
        self._load_active_company_into_form()
        if not self._persist_company_changes():
            return
        self.root.lift()

    def _confirm_company_deletion(self, selected: str) -> bool:
        if not selected:
            messagebox.showinfo("Information", "Es ist keine Firma ausgewählt.")
            return False
        return messagebox.askyesno(
            "Firma löschen",
            f"Soll die Firma '{selected}' wirklich gelöscht werden?",
        )

    def _delete_company(self, selected: str) -> bool:
        try:
            self.middleware.ini_file.delete_company(selected)
        except ValueError as ex:
            messagebox.showerror("Fehler", ex.args[0])
            return False
        return True

    def handle_company_rename(self):
        if not self.middleware:
            return
        selected = self.company_var.get().strip()
        if not selected:
            messagebox.showinfo("Information", "Es ist keine Firma ausgewählt.")
            return

        renamed_name = self._rename_company(selected)
        if renamed_name is None:
            return

        self._refresh_company_selector()
        self.company_var.set(renamed_name)
        self._load_active_company_into_form()
        if not self._persist_company_changes():
            return
        self.root.lift()

    def _rename_company(self, selected: str):
        self.fetch_values_from_entries()
        new_name = self.ask_string(
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
            return None
        return renamed_name

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

        self._export_company_profile(selected)

    def _export_company_profile(self, selected: str):
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
        imported_name = self._import_company_profile(source_file)
        if imported_name is None:
            return

        self._refresh_company_selector()
        self.company_var.set(imported_name)
        self._load_active_company_into_form()
        if not self._persist_company_changes():
            return
        messagebox.showinfo("Information", f"Firmenprofil '{imported_name}' importiert.")
        self.root.lift()

    def _import_company_profile(self, source_file: str):
        try:
            return self.middleware.ini_file.import_company_profile(source_file)
        except (ValueError, OSError, KeyError, TypeError) as ex:
            messagebox.showerror("Fehler", f"Import fehlgeschlagen:\n{ex}")
            return None

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
            self._show_logo()
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
            self._show_logo()
        self.root.lift()

    def fetch_values_from_entries(self):
        content = self._get_current_form_content()
        if content and self.middleware:
            self.middleware.ini_file.save_current_company_content(content)
            self.middleware.ini_file.merge_content_of_ini_file(
                {LOGO_ALIGN_KEY: self.logo_align_var.get()}
            )
            self._refresh_company_selector()
            return self.middleware.ini_file.content
        return content
