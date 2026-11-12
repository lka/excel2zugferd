"""
Modul OberflaecheExcel2Zugferd
"""

import re
from tkinter import messagebox, filedialog
import customtkinter as ctk
from pathlib import Path

from src.excel_content import ExcelContent
from src.middleware import Middleware
from src.constants import PADX, PADY
import src
import src.oberflaeche_base
import src.oberflaeche_excelpositions
import src.oberflaeche_excelsteuerung
import src.oberflaeche_ini
import src.oberflaeche_steuerung

FILE_LABEL_WIDTH = 300  # px, longer paths are wrapped


class OberflaecheExcel2Zugferd(src.oberflaeche_base.Oberflaeche):
    """
    Klasse OberflaecheExcel2ZugFerd
    """

    def __init__(
        self, myfields: dict, middleware: Middleware = None, window=None
    ) -> None:
        super().__init__(window, wsize="520x480")
        self.fields: dict = myfields
        self.middleware = middleware
        self.filename: str = None
        self.selected_lb_item = None
        self.sheet_buttons: list = []
        self.root.title("Excel2ZugFeRD")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Öffnen...": self.open_file,
                        "Stammdateneingabe": {
                            "Firmendaten": self.pre_open_stammdaten,
                            "Sonstige": self.pre_open_steuerung,
                            "Excel Steuerung": self.pre_open_excelsteuerung,
                            "Excel Positionen": self.pre_open_excelpositions,
                        },
                        "Separator": 0,
                        "Beenden": self.quit_cmd,
                    }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        self.makeform()
        self._add_quit_save_buttons(2, self.create_pdf)

        self.middleware.setStammdatenToInvoiceCollection()

    def _check_tabellenblatt(self) -> bool:
        """return True on failure"""
        if self.selected_lb_item is None:
            mymsg = "Bitte erst ein Excel Tabellenblatt auswählen."
            messagebox.showinfo("Information", mymsg)
            return True
        return False

    def create_pdf(self) -> None:
        """
        create the pdf
        """
        if self._check_tabellenblatt():
            return
        if self.middleware.setExcelDatenToInvoiceCollection(self.selected_lb_item):
            return
        if self.middleware.try_to_init_pdf(self.logo_fn):
            return
        self.middleware.fill_pdf(self.selected_lb_item)

    def _read_sheet_list(self) -> None:
        """creates ExcelContent from filename, reads sheet list"""
        self.middleware.excel_file = ExcelContent(self.filename, "")
        self.file_name_label.configure(text=self._wrappable(self.filename))
        for button in self.sheet_buttons:
            button.destroy()
        self.sheet_buttons = []
        self.selected_lb_item = None
        for item in self.middleware.excel_file.read_sheet_list():
            self._add_sheet_button(item)

    def _wrappable(self, path: str) -> str:
        """insert line breaks after path separators so that no line is
        wider than FILE_LABEL_WIDTH"""
        font = self.file_name_label.cget("font")
        lines = [""]
        for part in re.findall(r"[^/\\]*[/\\]|[^/\\]+", path):
            if lines[-1] and font.measure(lines[-1] + part) > FILE_LABEL_WIDTH:
                lines.append("")
            lines[-1] += part
        return "\n".join(lines)

    def _add_sheet_button(self, item: str) -> None:
        """add one selectable entry to the sheet list"""
        button = ctk.CTkButton(
            self.lb,
            text=item,
            anchor="w",
            fg_color="transparent",
            text_color=("black", "white"),
            hover_color=("gray80", "gray30"),
            command=lambda: self.select_sheet(item),
        )
        button.bind("<Double-Button-1>", lambda event: self.double_click(item))
        button.pack(fill="x", padx=2, pady=1)
        self.sheet_buttons.append(button)

    def select_sheet(self, item: str) -> None:
        """mark the sheet as selected"""
        self.selected_lb_item = item
        for button in self.sheet_buttons:
            selected = button.cget("text") == item
            button.configure(fg_color=("gray75", "gray25") if selected else "transparent")

    def double_click(self, item: str) -> None:
        """select the sheet and create the pdf"""
        self.select_sheet(item)
        self.create_pdf()

    def _file_dialog(self, init_dir: str) -> None:
        self.filename = filedialog.askopenfilename(
            title="Bitte die Excel Datei auswählen",
            initialdir=Path(init_dir).resolve(),
            filetypes=(("Excel Datei", "*.xlsx"), ("Alle Dateien", "*.*")),
        )

    def _try_to_save_Verzeichnis(self) -> None:
        """save Verzeichnis from Excel-Filename in INI-File"""
        try:
            self.middleware.save_working_directory(self.filename)
        except OSError as ex:
            messagebox.showerror(
                "IO-Fehler",
                f"Ini-File \
kann nicht beschrieben werden.\n{ex}",
            )

    def open_file(self):
        """
        Open File
        """
        self._file_dialog(self.middleware.get_working_directory())
        if len(self.filename) > 0 and Path(self.filename).exists():
            self._read_sheet_list()
            self._try_to_save_Verzeichnis()

    def myListbox(self) -> ctk.CTkScrollableFrame:
        """create scrollable list of the sheet names"""
        lb = ctk.CTkScrollableFrame(
            self.content_frame,
            width=420,
            height=330,
            border_width=2,
            border_color=("gray60", "gray40"),
            fg_color=("white", "gray17"),
        )
        lb.grid(row=1, column=0, columnspan=2, pady=PADY, sticky="w")
        return lb

    def makeform(self):
        """
        create form for input
        overwrites makeform from base class
        """
        self.file_name_button = ctk.CTkButton(
            self.content_frame, text="Excel-Datei...", command=self.open_file
        )
        self.file_name_button.grid(row=0, column=0, pady=PADY)
        self.file_name_label = ctk.CTkLabel(
            self.content_frame,
            text="Bitte erst eine Excel-Datei auswählen.",
            wraplength=FILE_LABEL_WIDTH,
            justify="left",
            anchor="w",
        )
        self.file_name_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="w")
        self.lb = self.myListbox()
