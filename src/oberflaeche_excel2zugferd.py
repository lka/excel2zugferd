"""
Modul OberflaecheExcel2Zugferd
"""

import tkinter as tk
from tkinter import messagebox, filedialog, Button
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


class OberflaecheExcel2Zugferd(src.oberflaeche_base.Oberflaeche):
    """
    Klasse OberflaecheExcel2ZugFerd
    """

    def __init__(self, myfields: dict, middleware: Middleware = None,
                 args: list = None) -> None:
        super().__init__()
        self.fields: dict = myfields
        self.middleware: Middleware = middleware
        self.filename: str = None
        self.selected_lb_item = None
        self.double_clicked_flag = False
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

        self.quit_button = tk.Button(self.root, text="Beenden",
                                     command=self.quit_cmd)
        self.quit_button.pack(side=tk.LEFT, padx=PADX, pady=PADY)
        self.quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        self.save_button = tk.Button(
            self.root, text="Speichern", command=self.create_pdf
        )
        self.save_button.pack(side=tk.LEFT, padx=PADX, pady=PADY)
        self.save_button.bind("<Return>", (lambda event: self.create_pdf()))
        self.middleware.setStammdatenToInvoiceCollection()
        self.check_args(args)

    def check_args(self, args: list) -> None:
        """check arguments from main call"""
        # messagebox.showinfo("Information", f"Args: {args}")
        if len(args) > 1:
            self.filename = args[-1]
            if len(self.filename) > 0 and Path(self.filename).exists():
                self._read_sheet_list()

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
        if self.middleware\
                .setExcelDatenToInvoiceCollection(self.selected_lb_item):
            return
        if self.middleware.try_to_init_pdf(self.logo_fn):
            return
        self.middleware.fill_pdf(self.selected_lb_item)

    def pre_open_stammdaten(self):
        self.open_stammdaten(self.fields, self.middleware)

    def pre_open_steuerung(self):
        self.open_steuerung(self.fields, self.middleware)

    def pre_open_excelsteuerung(self):
        self.open_excelsteuerung(self.fields, self.middleware)

    def open_stammdaten(self, fields: dict = None,
                        middleware: Middleware = None):
        """
        Open Stammdaten for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_ini.OberflaecheIniFile(fields, middleware,
                                                          self.root)
        s_oberfl.loop()

    def open_steuerung(self, fields: dict = None,
                       middleware: Middleware = None):
        """
        Open Steuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_steuerung.OberflaecheSteuerung(fields,
                                                                  middleware,
                                                                  self.root)
        s_oberfl.loop()

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
        # self.fetch_values_from_entries()
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

    def _read_sheet_list(self) -> list:
        """creates ExcelContent from filename, reads sheet list"""
        self.middleware.excel_file = ExcelContent(self.filename, "")
        self.file_name_label.config(text=self.filename)
        self.lb.delete(0, "end")
        items = self.middleware.excel_file.read_sheet_list()
        for item in items:
            self.lb.insert("end", item)

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
            messagebox.showerror("IO-Fehler",
                                 f"Ini-File \
kann nicht beschrieben werden.\n{ex}")

    def open_file(self):
        """
        Open File
        """
        self._file_dialog(self.middleware.get_working_directory())
        if len(self.filename) > 0 and Path(self.filename).exists():
            self._read_sheet_list()
            self._try_to_save_Verzeichnis()

    def mouse_click(self, event):  # pylint: disable=unused-argument
        """
        reaction to clicking of the selected item in listbox
        """
        self.lb.after(300, self.mouse_action, event)

    def double_click(self, event):  # pylint: disable=unused-argument
        """
        reaction to double-clicking of the selected item in listbox
        """
        self.double_clicked_flag = True

    def mouse_action(self, event):  # pylint: disable=unused-argument
        """
        reaction to clicking or double-clicking of the selected item in listbox
        """
        # get selected indices
        selected_indices = self.lb.curselection()
        # get selected items
        self.selected_lb_item = ",".join([self.lb.get(i)
                                         for i in selected_indices])
        if self.double_clicked_flag:
            # messagebox.showinfo("Info", "Double-Clicked")
            self.create_pdf()
            self.double_clicked_flag = False

    #        else:
    #            messagebox.showinfo("Info", "Single-Clicked")

    def makeform(self):
        """
        create form for input
        """
        self.file_name_button = Button(
            self.root, text="Excel-Datei...", command=self.open_file
        )
        self.file_name_button.pack(anchor="nw")
        self.file_name_label = tk.Label(
            self.root,
            text="Bitte erst die Excel Datei auswählen\
 (über Datei -> Öffnen...).",
        )
        self.file_name_label.pack()
        self.lb = tk.Listbox(self.root, height=20)
        self.lb.bind("<<ListboxSelect>>", self.mouse_click)  # type: ignore
        self.lb.bind("<Double-Button>", self.double_click)
        self.lb.pack(expand=True, fill=tk.BOTH)
