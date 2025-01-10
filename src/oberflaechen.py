"""
Module Oberflaechen
"""

import tkinter as tk
from tkinter import messagebox, filedialog, Button, ttk
import json
import tempfile
import os
from pathlib import Path
import shutil
from PIL import Image, ImageTk
from src.handle_pdf import Pdf

import src.excel_content
from src.handle_ini_file import IniFile
from src.collect_data import InvoiceCollection
from src.handle_zugferd import ZugFeRD


def format_ioerr(err: IOError) -> str:
    """
    format IOError corresponding to errno and string
    """
    return f"Error ({0}): {1}".format(err.errno, err.strerror)


LABELWIDTH = 22
TEXTWIDTH = 60
PADX = 5
PADY = 5


class Oberflaeche:
    """
    Creates Parts of Oberflaeche
    """

    def __init__(self, window=None) -> None:
        if window:
            # print('Oberflaeche destroying window')
            self.destroy_children(window)

        self.root = tk.Tk() if window is None else window
        # self.myFont = Font(family="Helvetica", size=12)
        self.root.resizable(False, False)
        self.canvas = None
        self.img_area = None
        self.logo_fn = os.path.join(
            os.getenv("APPDATA"), "excel2zugferd", "logo.jpg"  # type: ignore
        )  # type: ignore
        try:
            # windows only (remove the minimize/maximize button)
            self.root.attributes("-toolwindow", True)
        except tk.TclError:
            print("Not supported on your platform")
        return self.root

    def _add_menu_items(self, menu, key, command) -> None:
        if key == "Separator":
            menu.add_separator()
        else:
            menu.add_command(label=key, command=command)

    def _add_items(self, menu_bar: tk.Menu, menu_items: list) -> None:
        # print('\n_add_item\n')
        for item in menu_items:
            # print(f"item: {item}")
            for outerkey in item.keys():
                # print(f"outerkey: {outerkey}")
                menu = tk.Menu(menu_bar, tearoff=0)
                for innerkey in item[outerkey].keys():
                    # print(f"innerkey: {innerkey}")
                    if isinstance(item[outerkey][innerkey], dict):
                        submenu = self.make_sub_menu(menu,
                                                     item[outerkey][innerkey])
                        menu.add_cascade(label=innerkey, menu=submenu)
                    else:
                        self._add_menu_items(menu, innerkey,
                                             item[outerkey][innerkey])
                menu_bar.add_cascade(label=outerkey, menu=menu, underline=0)

    def make_sub_menu(self, menu: tk.Menu, menu_items: dict) -> tk.Menu:
        submenu = tk.Menu(menu, tearoff=0)
        if menu_items is None:
            return
        # print(f"submenuitems: {menu_items}")
        for key in menu_items.keys():
            # print(f"submenuitem: {key}")
            self._add_menu_items(submenu, key,
                                 menu_items[key])
        return submenu

    def make_menu_bar(self, menu_items: list = None):
        """
        MenuBar for each Oberflaeche
        """
        menu_bar = tk.Menu(self.root)
        # print(menuItems)
        if menu_items is None:
            return
        self._add_items(menu_bar, menu_items)
        self.root.config(menu=menu_bar)

    def make_logo(self, fn):
        """
        set logo to position
        """
        if fn is not None and Path(fn).exists():
            img = Image.open(fn)
            img = img.resize((100, 100), Image.BOX)
            image = ImageTk.PhotoImage(img)
            if self.canvas:
                self.img_area = self.canvas.create_image(
                    0, 0, anchor=tk.NW, image=image
                )
                self.canvas.img = image

    def quit_cmd(self):
        """
        Quit window
        """
        confirm = messagebox.askokcancel("Beenden?",
                                         "Möchten Sie wirklich Beenden ?")
        if confirm:
            self.root.destroy()

    def info_cmd(self):
        """
        show Info
        """
        try:
            with open(
                os.path.join("_internal", "version.json"), "r",
                    encoding="utf-16"
            ) as f_in:
                version = json.load(f_in)
                my_msg = f"Copyright © H.Lischka, 2024\n\
        Version {version['version'] if version is not None else 'unbekannt'}"
        except IOError as ex:
            my_msg = f"IOError ({0}): {1}".format(ex.errno, ex.strerror)

        messagebox.showinfo("Info", my_msg)
        self.root.lift()

    def destroy_children(self, parent):
        """
        recursive destroy all children of current window
        """
        for child in parent.winfo_children():
            if child.winfo_children():
                self.destroy_children(child)
            child.destroy()

    def _add_string(self, row: tk.Frame, field: dict, content: any) -> tk.Text:
        lab = tk.Label(
            row, width=LABELWIDTH, text=field["Label"] + ": ",
            anchor="w"
        )
        # ent = Entry(row)
        # ent.insert(0, "")
        ent = tk.Text(row, width=TEXTWIDTH, height=field["Lines"])
        # ent.configure(font=self.myFont)
        ent.insert(
            tk.END,
            content[field["Text"]] if field["Text"] in content else "",
        )
        row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        return ent

    def _add_label(self, row: tk.Frame, field: dict, content: any)\
            -> tk.Message:
        ent = tk.Message(row,
                         text=field["Label"],
                         border=1,
                         width=9*TEXTWIDTH,
                         )
        row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
        return ent

    def _add_boolean(self, row: tk.Frame, field: dict, content: any)\
            -> tk.Checkbutton:
        self.menuvars[field["Variable"]] = tk.StringVar()
        ent = ttk.Checkbutton(
            row, text=field["Label"], variable=self.menuvars[
                                                field["Variable"]]
        )
        self.menuvars[field["Variable"]].set(
            "1"
            if (len(content) > 0)
            and field["Text"] in content
            and (
                (content[field["Text"]] == "Ja")
                or (content[field["Text"]] == "1")
            )
            else "0"
        )
        lab = tk.Label(row, width=LABELWIDTH, text=" ", anchor="w")
        row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        return ent

    def open_stammdaten(self, fields: dict = None, ini_file: str = None):
        """
        Open Stammdaten for editing
        """
        self.root.quit()
        s_oberfl = OberflaecheIniFile(fields, ini_file, self.root)
        s_oberfl.loop()

    def open_steuerung(self, fields: dict = None, ini_file: str = None):
        """
        Open Steuerung for editing
        """
        self.root.quit()
        s_oberfl = OberflaecheSteuerung(fields, ini_file, self.root)
        s_oberfl.loop()

    def _create_iniFile(self, ini_file: IniFile, content: dict = None) -> bool:
        try:
            if ini_file:
                ini_file.create_ini_file(content)
        except IOError as ex:
            mymsg = f"Erstellen der Ini-Datei fehlgeschlagen.\n\
            {format_ioerr(ex)}"
            messagebox.showerror("Fehler:", mymsg)
            return True
        return False

    def _get_text_of_field(self, field: any) -> str:
        if isinstance(field, tk.Message):
            return ''
        return (
                    field.get("1.0", "end-1c")
                    if hasattr(field, "get")
                    else "Ja" if field.instate(["selected"]) else "Nein"
                )

    def get_entries_from_type(self, row: tk.Frame, field: dict, content: dict):
        ent = None
        if field["Type"] == "String":
            ent = self._add_string(row, field, content)
        if field["Type"] == "Boolean":
            ent = self._add_boolean(row, field, content)
        if field["Type"] == "Label":
            ent = self._add_label(row, field, content)
        return ent

    def loop(self):
        """
        run main loop
        """
        self.root.mainloop()


class OberflaecheIniFile(Oberflaeche):
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
            ini_has_failure = self._check_content_of_stammdaten(content)
            ini_has_failure = ini_has_failure or self._create_iniFile(
                self.ini_file, None)
            if ini_has_failure:
                return
        self.root.destroy()

    def makeform(self) -> dict:
        """
        create the form of IniFile Oberflaeche
        """
        entries = {}
        if self.ini_file:
            content = self.ini_file.read_ini_file()
        else:
            return entries
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


class OberflaecheSteuerung(Oberflaeche):
    """
    Oberflaeche for Ini File Inputs; Steuerung (Sonstige) Parts
    """

    def __init__(self, thefields: dict, myini_file: IniFile = None,
                 window=None) -> None:
        super().__init__(window=window)  # tk.Toplevel())
        self.fields: dict = thefields
        self.menuvars = {}
        self.ini_file: IniFile = myini_file
        self.root.title("Stammdateneingabe - Sonstige")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Stammdateneingabe":
                            {
                                "Firmendaten": self.pre_open_stammdaten,
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
        self.open_stammdaten(self.fields, self.ini_file)

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
            ini_has_failure = self._check_content_of_stammdaten(content)
            ini_has_failure = ini_has_failure or self._create_iniFile(
                self.ini_file, None)
            if ini_has_failure:
                return
        self.root.destroy()

    def makeform(self) -> dict:
        """
        create the form of Steuerung (Sonstige) Oberflaeche
        """
        entries = {}
        if self.ini_file:
            content = self.ini_file.read_ini_file()
        else:
            return entries
        for field in self.fields:
            if (field["Dest"] == "Steuerung"):
                row = tk.Frame(self.root)
                entries[field["Text"]] = self.get_entries_from_type(row,
                                                                    field,
                                                                    content)
        return entries


class OberflaecheExcel2Zugferd(Oberflaeche):
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
                        {format_ioerr(ex)}"
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
                da ein Problem aufgetreten ist.\n{format_ioerr(ex)}"
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
                {format_ioerr(ex)}"
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
