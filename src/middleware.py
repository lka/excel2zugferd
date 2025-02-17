"""
Modul Middleware
"""
from tkinter import messagebox, filedialog
from pathlib import Path
import logging
import shutil
import tempfile
import os
import sys
from src.handle_ini_file import IniFile
from src.invoice_collection import InvoiceCollection
from src.excel_content import ExcelContent
from src.handle_pdf import Pdf
from src.handle_zugferd import ZugFeRD
from src.windowseventlog import WindowsEventLogHandler
import src


class Middleware():
    """
    holds class containers, data containers and functions to handle them
    """
    def __init__(self):
        self.ini_file: IniFile = None
        self.invoiceCollection: InvoiceCollection = InvoiceCollection()
        self.excel_file: ExcelContent = None
        self.zugferd: ZugFeRD = None
        self.quiet: bool = False
        self.logger: logging.Logger = None
        self.pdf_filename: str = None
        self.initLogger()

    def initLogger(self) -> None:
        myAppName = 'Excel2ZUGFeRD'
        self.logger = logging.getLogger(myAppName)
        self.logger.setLevel(logging.DEBUG)

        event_log_handler = WindowsEventLogHandler(appname=myAppName)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \
- %(message)s')
        event_log_handler.setFormatter(formatter)
        self.logger.addHandler(event_log_handler)

    def _error_msg(self, header: str, msg: str) -> None:
        """
        bei Benutzung ohne Oberfläche wird die Fehlermeldung
        ausgegeben und das Programm mit exit(-1) beendet
        """
        self.logger.error(msg=f"{header}\n{msg}")
        if self.quiet:
            # sys.stderr.write(header + "\n" + msg)
            sys.exit(-1)
        else:
            messagebox.showerror(header, msg)

    def _usage(self) -> None:
        msg = (
            "Benutzung:\nexcel2zugferd.exe"
            " -BlattNr Pfad_zur_Exceldatei.xlsx\noder\n"
            "excel2zugferd.exe"
            " -BlattNr Pfad_zur_eigenen_PDF.pdf Pfad_zur_Exceldatei.xlsx\n\n"
            "BlattNr 0..n, 0 ist das erste Tabellenblatt\n"
            "alle Parameter sind als Zeichenketten anzugeben."
        )
        # sys.stdout.write(msg)
        self.logger.info(msg)

    def _check_existance(self, fn) -> str | None:
        """check existance of file

        Args:
            fn (function): filename with path

        Returns:
            str | None: None if File does not exist
        """
        print(fn)
        if fn and len(fn) > 0 and Path(fn).exists():
            return fn
        return None

    def _is_pdf(self, fn: str) -> str | None:
        """check whether fn is a pdf file

        Args:
            fn (str): filename

        Returns:
            str | None: None if File has no pdf extension
        """
        parts = os.path.splitext(fn)
        if parts[1].lower() == '.pdf':
            return fn
        return None

    def _check_with_pdf(self, args: list) -> str | None:
        """check wether pdf and excel file exist

        Args:
            args (list): arguments from program start

        Returns:
            str | None: excel filename;
            pdf filename is written to self.pdf_filename
        """
        pdf_filename = self._is_pdf(args[2])
        if self._check_existance(pdf_filename):
            self.pdf_filename = pdf_filename
            filename = args[3]
            if len(filename) > 0 and Path(filename).exists():
                return filename
        return None

    def check_filenames(self, args: list) -> str | None:
        """check filenames and existance of the files

        Args:
            args (list): arguments from program start

        Returns:
            str: None if failure occurs, filename of excelfile if all is OK
        """
        length = len(args)
        if length == 3:
            filename = args[2]
            if self._is_pdf(filename):
                return None
            return self._check_existance(filename)
        elif length == 4:
            return self._check_with_pdf(args)
        return None

    def _isNumber(self, num: str) -> bool:
        """checks whether num is number

        Args:
            num (str): string to be checked

        Returns:
            bool: True if number
        """
        try:
            abs(int(num))
        except ValueError:
            return False
        return True

    def check_args(self, args: list) -> bool:
        """check arguments from main call\n
           return True if called without arguments
        """
        length = len(args)
        if length == 1:
            self.set_iniFile()
            return False
        self.quiet = True
        self.set_iniFile()
        if self._isNumber(args[1]) and length in [3, 4]:
            sheetnr = args[1]
            filename = self.check_filenames(args)
            if filename:
                self.quiet_workflow(filename, abs(int(sheetnr)),
                                    self.pdf_filename)
                return True
        self._usage()
        return True

    def _success_message(self, outfile: str) -> None:
        mymsg = f"Die Datei {outfile} wurde erstellt."
        self.logger.info("Information: \n" + mymsg)
        if not self.quiet:
            messagebox.showinfo("Information", mymsg)

    def set_iniFile(self) -> None:
        """
        wenn das Verzeichnis für die Init-Datei nicht erzeugt werden kann
        wird der Fehler ausgegeben und das Programm mit exit(-1) beendet
        """
        try:
            self.ini_file = IniFile()  # dir=Path('Z:/data'))
        except ValueError as e:
            self.logger.critical("Schwerer Fehler:\n" + e.args[0])
            if not self.quiet:
                self._error_msg("Schwerer Fehler:", e.args[0])
            sys.exit(-1)

    def get_filenames(self, infile: str = None) -> list:
        """
        returns list with ('infile.pdf', 'workingdirectory/infile [(1..)].pdf')
        """
        outfile = None
        fn = None
        if infile:
            fn = infile + ".pdf"
            # print(contentini_file["Verzeichnis"], fn)
            tmpfn = os.path.join(Path(self.invoiceCollection
                                      .management.directory)
                                 .absolute(), fn)
            outfile = self.pdf.uniquify(tmpfn)
        #        msg = f"Die Datei {outfile} wurde vorgesehen"
        #        messagebox.showinfo("Debug-Information", msg)
        return (fn, outfile)

    def setStammdatenToInvoiceCollection(self) -> bool:
        """return True on failure"""
        contentini_file = self.ini_file.read_ini_file()
        # print("_getStammdatenToInvoiceCollection:\n", contentini_file)
        return self._try_to_fill_stammdaten(self.invoiceCollection,
                                            contentini_file)

    def _try_to_fill_stammdaten(self, invoiceCollection: InvoiceCollection,
                                stammdaten: dict) -> bool:
        """returns True if error in stammdaten occurs"""
        try:
            invoiceCollection.set_stammdaten(stammdaten)
        except ValueError as ex:
            self._error_msg("Fehler in den Stammdaten:", ex.args[0])
            return True
        return False

    def setExcelDatenToInvoiceCollection(self, sheet_name: str | int) -> bool:
        """return True on failure"""
        if self.excel_file is not None:
            self.excel_file.read_sheet(sheet_name)
            return self._try_to_fill_excel_daten(self.invoiceCollection,
                                                 self.excel_file)
        return False

    def _try_to_fill_excel_daten(self, invoiceCollection: InvoiceCollection,
                                 daten: ExcelContent) -> bool:
        """returns True if error in stammdaten occurs"""
        try:
            invoiceCollection.set_daten(daten)
        except ValueError as ex:
            self._error_msg("Fehler in den Excel-Daten:", ex.args[0])
            return True
        # print('excel2zugferd:223: ', repr(invoiceCollection))
        return False

    def try_to_init_pdf(self, logo_fn: str) -> bool:
        """returns True if error occurs"""
        try:
            self.pdf = Pdf(logo_fn if Path(logo_fn).exists() else None)
        except ValueError as ex:
            self._error_msg("Fehler in den Stammdaten (PDF):",
                            ex.args[0])
            return True
        return False

    def try_to_fill_pdf(self) -> bool:
        """returns True if Daten have failures"""
        try:
            self.pdf.fill_pdf(self.invoiceCollection)
        except ValueError as ex:
            self._error_msg("Fehler in den Daten:", ex.args[0])
            return True
        return False

    def create_ZugFeRD(self) -> bool:
        """returns True on Failure"""
        try:
            self.zugferd = ZugFeRD(self.invoiceCollection)
        except Exception as ex:
            self._error_msg("ZUGFeRD kann nicht erstellt werden:",
                            ', '.join(ex.args))
            return True
        # print('create_ZugFeRD:235', repr(self.invoiceCollection))
        return False

    def create_pdf_file_only(self, outfile: str) -> None:
        if outfile is not None:
            self.pdf.output(outfile)
            self._success_message(outfile)

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
        except OSError as ex:
            self._error_msg("IO-Fehler:", f"Konnte {outfile} aus \
{file_name} nicht erstellen, da ein Problem aufgetreten ist.\n{ex}")
            return True
        # msg = f"Die Datei {fileName} wurde erstellt"
        # messagebox.showinfo("Debug-Information", msg)
        return False

    def _populate_temp_file(self, file_name: str) -> str:
        """returns own pdf filename with path"""
        if self.invoiceCollection.management.BYOPdf:
            theFile = self.invoiceCollection.management.pdf_filename
            if theFile is None:
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
        except OSError as ex:
            self._error_msg("IO-Fehler:", f"Konnte {file_name} nicht \
erstellen, da ein Problem aufgetreten ist.\n{ex}")
            return True
        return False

    def fill_pdf(self, filename: str = None) -> None:
        if self.try_to_fill_pdf():
            return
        fn, outfile = self.get_filenames(filename)
        if self.invoiceCollection.management.create_xml:
            if self._create_and_add_xml(fn, outfile):
                return
            self._success_message(outfile)
        else:
            self.create_pdf_file_only(outfile)

    def get_working_directory(self) -> Path:
        return self.ini_file.get_working_directory()

    def save_working_directory(self, filename: str) -> None:
        self.ini_file.save_working_directory(filename)
        self.invoiceCollection.management.directory = os.path.dirname(filename)
        # self.setStammdatenToInvoiceCollection()

    def quiet_workflow(self, filename: str, sheetnr: int,
                       pdf_filename: str = None) -> None:
        if self.ini_file.exists_ini_file() is None:
            self.ini_file.create_ini_file(self.ini_file.set_default_content())
        self.setStammdatenToInvoiceCollection()
        self.save_working_directory(filename)
        self.excel_file = ExcelContent(filename, "")
        if pdf_filename is not None:
            self.invoiceCollection.management.pdf_filename = pdf_filename
            self.invoiceCollection.management.BYOPdf = True
        else:
            self.invoiceCollection.management.BYOPdf = False
        self.setExcelDatenToInvoiceCollection(sheetnr)
        self.try_to_init_pdf(src.logo_fn())
        arr = self.excel_file.read_sheet_list()
        outfile = arr[sheetnr]
        self.fill_pdf(outfile)
