"""
Module Oberflaechen
"""

import tkinter as tk
from tkinter import messagebox, filedialog, Button
import tempfile
import os
from pathlib import Path
import shutil
from src.handle_pdf import Pdf

import src.excel_content
from src.handle_ini_file import IniFile
from src.collect_data import InvoiceCollection
from src.handle_zugferd import ZugFeRD
# from src.oberflaeche_base import Oberflaeche
# from src.oberflaeche_excelsteuerung import OberflaecheExcelSteuerung
# from src.oberflaeche_ini import OberflaecheIniFile
# from src.oberflaeche_steuerung import OberflaecheSteuerung
# from src.oberflaeche_excelpositions import OberflaecheExcelPositions, \
#     Oberflaeche, OberflaecheIniFile, OberflaecheSteuerung
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

    def __init__(self, myfields: dict, myini: IniFile = None,
                 args: list = None) -> None:
        super().__init__()
        self.fields = myfields
        self.ini_file = myini
        self.filename = None
        self.excel_file = None
        self.selected_lb_item = None
        self.invoiceCollection = InvoiceCollection()
        self.zugferd = None
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
        self._getStammdatenToInvoiceCollection()
        self.check_args(args)

    def check_args(self, args: list) -> None:
        """check arguments from main call"""
        # messagebox.showinfo("Information", f"Args: {args}")
        if len(args) > 1:
            self.filename = args[-1]
            if len(self.filename) > 0 and Path(self.filename).exists():
                self._read_sheet_list()

    def _get_own_pdf(self):
        fn = filedialog.askopenfilename(
            title="Bitte die anderweitig erstellte PDF auswählen",
            # initialdir=Path(init_dir).resolve(),
            filetypes=(("PDF Datei", "*.pdf"), ("Alle Dateien", "*.*")),
        )
        return fn

    def _add_xml(self, file_name: str, outfile: str) -> bool:
        """returns true if failure"""
        try:
            self.zugferd.add_xml2pdf(file_name, outfile)
        except IOError as ex:
            mymsg = f"Konnte {outfile} aus {file_name} \
                        nicht erstellen, \
                        da ein Problem aufgetreten ist.\n\
                        {src.format_ioerr(ex)}"
            messagebox.showerror("Fehler:", mymsg)
            return True
        # msg = f"Die Datei {fileName} wurde erstellt"
        # messagebox.showinfo("Debug-Information", msg)
        return False

    def _populate_temp_file(self, file_name: str) -> str | None:
        """returns own pdf filename with path"""
        if self.invoiceCollection.management.BYOPdf:
            theFile = self._get_own_pdf()
            shutil.copyfile(theFile, file_name)
            return theFile
        else:
            self.pdf.output(file_name)
            return None

    def _add_xml_with_perhaps_modify_outfile(self, file_name: str,
                                             outfile: str) -> bool:
        modifiedFn = self._populate_temp_file(file_name)
        if modifiedFn is not None:
            outfile = self.pdf.uniquify(modifiedFn, '_ZugFeRD')
        if self._add_xml(file_name, outfile):
            return True
        if modifiedFn is not None:
            self._success_message(outfile)
            return True  # just to permit success_message
                         #  with wrong filename # noqa 116
        return False

    def _create_and_add_xml(self, fn: str, outfile: str) -> bool:
        """returns True if caught 'has_error'"""
        if self.create_ZugFeRD():
            return True
        if fn is None or outfile is None:
            return True
        try:
            # tmp = tempfile.gettempdir()
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True)\
                 as tmp:
                file_name = os.path.join(
                    Path(tmp), fn
                )  # doesn't matter, cannot exist twice
                return self._add_xml_with_perhaps_modify_outfile(file_name,
                                                                 outfile)
        except IOError as ex:
            mymsg = f"Konnte {file_name} nicht erstellen, \
                da ein Problem aufgetreten ist.\n{src.format_ioerr(ex)}"
            messagebox.showerror("Fehler:", mymsg)
            return True
        return False

    def _try_to_fill_pdf(self) -> bool:
        """returns True if Daten have failures"""
        try:
            self.pdf.fill_pdf(self.invoiceCollection)
        except ValueError as e:
            messagebox.showerror("Fehler in den Daten", e)
            return True
        return False

    def _get_filenames(self, directory) -> list:
        outfile = None
        fn = None
        if self.selected_lb_item:
            fn = self.selected_lb_item + ".pdf"
            # print(contentini_file["Verzeichnis"], fn)
            tmpfn = os.path.join(Path(directory)
                                 .absolute(), fn)
            outfile = self.pdf.uniquify(tmpfn)
        #        msg = f"Die Datei {outfile} wurde vorgesehen"
        #        messagebox.showinfo("Debug-Information", msg)
        return [fn, outfile]

    def _success_message(self, outfile: str) -> None:
        mymsg = f"Die Datei {outfile} wurde erstellt."
        messagebox.showinfo("Information", mymsg)

    def _create_pdf_file_only(self, outfile: str) -> None:
        if outfile is not None:
            self.pdf.output(outfile)
            self._success_message(outfile)

    def _fill_pdf(self):
        if self._try_to_fill_pdf():
            return
        fn, outfile = self._get_filenames(self.invoiceCollection
                                          .management.directory)
        if self.invoiceCollection.management.create_xml:
            if self._create_and_add_xml(fn, outfile):
                return
            self._success_message(outfile)
        else:
            self._create_pdf_file_only(outfile)

    def _try_to_init_pdf(self) -> bool:
        """returns True if error occurs"""
        try:
            self.pdf = Pdf(
                self.logo_fn if Path(self.logo_fn).exists() else None
            )
        except ValueError as e:
            messagebox.showerror("Fehler in den Stammdaten", e)
            return True
        return False

    def try_to_fill_stammdaten(self, invoiceCollection: InvoiceCollection,
                               stammdaten: dict) -> bool:
        """returns True if error in stammdaten occurs"""
        try:
            invoiceCollection.set_stammdaten(stammdaten)
        except ValueError as e:
            messagebox.showerror("Fehler in den Stammdaten", e)
            return True
        return False

    def try_to_fill_daten(self, invoiceCollection: InvoiceCollection,
                          daten: src.excel_content.ExcelContent) -> bool:
        """returns True if error in stammdaten occurs"""
        try:
            invoiceCollection.set_daten(daten)
        except ValueError as e:
            messagebox.showerror("Fehler in den Excel-Daten", e)
            return True
        # print('excel2zugferd:567: ', repr(invoiceCollection))
        return False

    def create_ZugFeRD(self) -> bool:
        """returns True on Failure"""
        self.zugferd = ZugFeRD()
        # print('create_ZugFeRD:572', repr(self.invoiceCollection))
        self.zugferd.fill_xml(self.invoiceCollection)
        return False

    def _getStammdatenToInvoiceCollection(self) -> bool:
        """return True on failure"""
        if self.ini_file:
            contentini_file = self.ini_file.read_ini_file()
            # print("_getStammdatenToInvoiceCollection:\n", contentini_file)
            return self.try_to_fill_stammdaten(self.invoiceCollection,
                                               contentini_file)
        return False

    def _getExcelDatenToInvoiceCollection(self) -> bool:
        """return True on failure"""
        if self.excel_file:
            self.excel_file.read_sheet(self.selected_lb_item)
            return self.try_to_fill_daten(self.invoiceCollection,
                                          self.excel_file)
        return False

    def _check_tabellenblatt(self) -> bool:
        """return True on failure"""
        if self.selected_lb_item is None:
            mymsg = "Bitte erst ein Excel Tabellenblatt auswählen."
            messagebox.showinfo("Information", mymsg)
            return True
        return False

    def create_pdf(self):
        """
        create the pdf
        """
        if self._check_tabellenblatt():
            return
        # if self._getStammdatenToInvoiceCollection():
        #     return
        # do it only once on initialization, Lka, 03.01.2025
        if self._getExcelDatenToInvoiceCollection():
            return
        if self._try_to_init_pdf():
            return
        self._fill_pdf()

    def pre_open_stammdaten(self):
        self.open_stammdaten(self.fields, self.ini_file)

    def pre_open_steuerung(self):
        self.open_steuerung(self.fields, self.ini_file)

    def pre_open_excelsteuerung(self):
        self.open_excelsteuerung(self.fields, self.ini_file)

    def open_stammdaten(self, fields: dict = None, ini_file: str = None):
        """
        Open Stammdaten for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_ini.OberflaecheIniFile(fields, ini_file,
                                                          self.root)
        s_oberfl.loop()

    def open_steuerung(self, fields: dict = None, ini_file: str = None):
        """
        Open Steuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_steuerung.OberflaecheSteuerung(fields,
                                                                  ini_file,
                                                                  self.root)
        s_oberfl.loop()

    def open_excelsteuerung(self, fields: dict = None, ini_file: str = None):
        """
        Open ExcelSteuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_excelsteuerung\
            .OberflaecheExcelSteuerung(fields, ini_file, self.root)
        s_oberfl.loop()

    def pre_open_excelpositions(self):
        # self.fetch_values_from_entries()
        self.open_excelpositions(self.fields, self.ini_file)

    def open_excelpositions(self, fields: dict = None, ini_file: str = None):
        """
        Open Steuerung for editing
        """
        self.root.quit()
        s_oberfl = src.oberflaeche_excelpositions\
            .OberflaecheExcelPositions(fields, ini_file, self.root)
        s_oberfl.loop()

    def _file_dialog(self, init_dir: str) -> None:
        self.filename = filedialog.askopenfilename(
            title="Bitte die Excel Datei auswählen",
            initialdir=Path(init_dir).resolve(),
            filetypes=(("Excel Datei", "*.xlsx"), ("Alle Dateien", "*.*")),
        )

    def _read_sheet_list(self) -> list:
        self.excel_file = src.excel_content.ExcelContent(self.filename, "")
        self.file_name_label.config(text=self.filename)
        self.lb.delete(0, "end")
        items = self.excel_file.read_sheet_list()
        for item in items:
            self.lb.insert("end", item)

    def _try_to_save_Verzeichnis(self, contentini_file: dict) -> None:
        """save Verzeichnis in INI-File"""
        mydir = os.path.dirname(self.filename)
        try:
            if self.ini_file:
                self.ini_file.create_ini_file(
                    {**contentini_file, "Verzeichnis": mydir}
                )
        except IOError as ex:
            mymsg = f"Ini-File kann nicht beschrieben werden.\n\
                {src.format_ioerr(ex)}"
            messagebox.showerror("Fehler", mymsg)

    def _open_file(self, init_dir, contentini_file):
        # print(init_dir, "Verzeichnis" in contentini_file, contentini_file)
        self._file_dialog(init_dir)
        if len(self.filename) > 0 and Path(self.filename).exists():
            self._read_sheet_list()
            self._try_to_save_Verzeichnis(contentini_file)

    def _get_documents_directory(self):
        doc_dir = Path.home()
        if Path(Path.joinpath(doc_dir, "Documents")).is_dir():
            doc_dir = Path.joinpath(doc_dir, "Documents")
        return doc_dir

    def open_file(self):
        """
        Open File
        """
        if self.ini_file:
            contentini_file = self.ini_file.read_ini_file()
        doc_dir = self._get_documents_directory()
        init_dir = (
            contentini_file["Verzeichnis"]
            if contentini_file
            and "Verzeichnis" in contentini_file
            and len(contentini_file["Verzeichnis"]) > 0
            else doc_dir
        )

        self._open_file(init_dir, contentini_file)

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
