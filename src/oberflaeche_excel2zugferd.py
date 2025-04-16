"""
Modul OberflaecheExcel2Zugferd
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from src.excel_content import ExcelContent
from src.middleware import Middleware
from src.constants import PADY
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

    def __init__(
        self, myfields: dict, middleware: Middleware = None, window=None
    ) -> None:
        super().__init__(window, wsize="480x440")
        self.fields: dict = myfields
        self.middleware = middleware
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
        self.selected_lb_item = ",".join([self.lb.get(i) for i in selected_indices])
        if self.double_clicked_flag:
            # messagebox.showinfo("Info", "Double-Clicked")
            self.create_pdf()
            self.double_clicked_flag = False

    def myListbox(self) -> tk.Listbox:
        """create listbox with scrollbar"""
        # create frame for listbox and scrollbar
        frame = ttk.Frame(self.content_frame)
        frame.grid(row=1, column=0, columnspan=2, pady=PADY, sticky=tk.W)
        # create listbox for excel sheetnames
        lb = tk.Listbox(
            frame, height=20, width=60, justify="left", selectmode=tk.SINGLE
        )
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lb.bind("<<ListboxSelect>>", self.mouse_click)
        lb.bind("<Double-Button>", self.double_click)
        # Add a scrollbar to the listbox
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=lb.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Configure the listbox to work with the scrollbar
        lb.config(yscrollcommand=scrollbar.set)
        return lb

    def makeform(self):
        """
        create form for input
        overwrites makeform from base class
        """
        self.file_name_button = ttk.Button(
            self.content_frame, text="Excel-Datei...", command=self.open_file
        )
        self.file_name_button.grid(row=0, column=0, pady=PADY)
        self.file_name_label = ttk.Label(
            self.content_frame,
            text="Bitte erst die Excel Datei auswählen\
 (über Datei -> Öffnen...).",
        )
        self.file_name_label.grid(row=0, column=1, pady=PADY)
        self.lb = self.myListbox()
