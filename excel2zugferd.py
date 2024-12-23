"""
Module excel2zugferd
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

from src.handle_ini_file import IniFile
from src.excel_content import ExcelContent


def format_ioerr(err: IOError) -> str:
    """
    format IOError corresponding to errno and string
    """
    return f"Error ({0}): {1}".format(err.errno, err.strerror)


fields = [
    {
        "Text": "Betriebsbezeichnung",
        "Label": "Betriebsbezeichnung",
        "Lines": 1,
        "Type": "String",
    },
    {"Text": "Anschrift", "Label": "Anschrift", "Lines": 5, "Type": "String"},
    {"Text": "Bundesland", "Label": "Bundesland", "Lines": 1,
        "Type": "String"},
    {"Text": "Name", "Label": "Name", "Lines": 1, "Type": "String"},
    {"Text": "Kontakt", "Label": "Kontakt", "Lines": 5, "Type": "String"},
    {"Text": "Umsatzsteuer", "Label": "Umsatzsteuer", "Lines": 2,
        "Type": "String"},
    {"Text": "Konto", "Label": "Konto", "Lines": 3, "Type": "String"},
    {"Text": "Zahlungsziel", "Label": "Zahlungsziel", "Lines": 1,
        "Type": "String"},
    {"Text": "Abspann", "Label": "Abspann", "Lines": 5, "Type": "String"},
    {"Text": "Verzeichnis", "Label": "Verzeichnis", "Lines": 1,
        "Type": "String"},
    {
        "Text": "Kleinunternehmen",
        "Label": "Kleinunternehmen",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "Kleinunternehmen",
    },
    {
        "Text": "ZugFeRD",
        "Label": "ZugFeRD Datensatz erzeugen und anhängen",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "ZugFeRD",
    },
    {
        "Text": "GiroCode",
        "Label": "GiroCode erzeugen und einblenden",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "GiroCode",
    },
    {
        "Text": "BYOPdf",
        "Label": "anderweitig erzeugtes PDF verwenden",
        "Lines": 1,
        "Type": "Boolean",
        "Variable": "BYOPdf",
    }
]

LABELWIDTH = 22
TEXTWIDTH = 40
PADX = 5
PADY = 5


class Oberflaeche:
    """
    Creates Parts of Oberflaeche
    """

    def __init__(self, window=None):
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

    def _add_items(self, menu_bar, menu_items) -> None:
        for item in menu_items:
            outerkeys = item.keys()
            for outerkey in outerkeys:
                # print(outerkey)
                menu = tk.Menu(menu_bar, tearoff=0)
                innerkeys = item[outerkey].keys()
                for innerkey in innerkeys:
                    # print(innerkey)
                    if innerkey == "Separator":
                        menu.add_separator()
                    else:
                        menu.add_command(
                            label=innerkey, command=item[outerkey][innerkey]
                        )
                menu_bar.add_cascade(label=outerkey, menu=menu, underline=0)

    def make_menu_bar(self, menu_items=None):
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

    def loop(self):
        """
        run main loop
        """
        self.root.mainloop()


class OberflaecheIniFile(Oberflaeche):
    """
    Oberflaeche for Ini File Inputs
    """

    def __init__(self, thefields, myini_file=None, window=None):
        if window:
            self.destroy_children(window)

        super().__init__(window=window)  # tk.Toplevel())
        self.fields = thefields
        self.menuvars = {}
        self.ini_file = myini_file
        self.root.title("Stammdateneingabe")
        self.make_menu_bar(
            [
                {"Datei": {"Stammdateneingabe Beenden": self.quit_cmd}},
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

    def destroy_children(self, parent):
        """
        recursive destroy all children of current window
        """
        for child in parent.winfo_children():
            if child.winfo_children():
                self.destroy_children(child)
            child.destroy()

    def _check_content_of_stammdaten(self, content: dict) -> bool:
        """return whether stammdaten have failures"""
        try:
            Pdf(
                None,
                content,
                None,
            )
        except ValueError as e:
            messagebox.showerror("Fehler in den Stammdaten", e)
            return True
        return False

    def _create_iniFile(self, content: dict) -> bool:
        try:
            if self.ini_file:
                self.ini_file.create_ini_file(content)
        except IOError as ex:
            mymsg = f"Erstellen der Ini-Datei fehlgeschlagen.\n\
            {format_ioerr(ex)}"
            messagebox.showerror("Fehler:", mymsg)
            return True
        return False

    def _get_text_of_field(self, field: any) -> str:
        return (
                    field.get("1.0", "end-1c")
                    if hasattr(field, "get")
                    else "Ja" if field.instate(["selected"]) else "Nein"
                )

    def fetch(self):
        """
        get all values for IniFile
        """
        content = {}
        ini_has_failure = False
        if self.ents:
            for key, field in self.ents.items():
                content[key] = self._get_text_of_field(field)
            ini_has_failure = self._check_content_of_stammdaten(content)
            ini_has_failure = ini_has_failure or self._create_iniFile(
                content)
            if ini_has_failure:
                return
        self.root.destroy()

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
            row = tk.Frame(self.root)
            if field["Type"] == "String":
                ent = self._add_string(row, field, content)
            if field["Type"] == "Boolean":
                ent = self._add_boolean(row, field, content)
            entries[field["Text"]] = ent
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
        print(resp)
        if resp is True:
            os.remove(self.logo_fn)
            self.logo_delete.pack_forget()
            self.canvas.delete("all")
        self.root.lift()


class OberflaecheExcel2Zugferd(Oberflaeche):
    """
    Klasse OberflaecheExcel2ZugFerd
    """

    def __init__(self, myfields, myini=None):
        super().__init__()
        self.fields = myfields
        self.ini_file = myini
        self.filename = None
        self.excel_file = None
        self.selected_lb_item = None
        self.double_clicked_flag = False
        self.root.title("Excel2ZugFeRD")
        self.make_menu_bar(
            [
                {
                    "Datei": {
                        "Öffnen...": self.open_file,
                        "Stammdateneingabe": self.open_stammdaten,
                        "Separator": 0,
                        "Beenden": self.quit_cmd,
                    }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        self.makeform()
        # self.root.bind('<Return>', (lambda event,
        # e=self.ents: self.fetch(e)))
        self.quit_button = tk.Button(self.root, text="Beenden",
                                     command=self.quit_cmd)
        self.quit_button.pack(side=tk.LEFT, padx=PADX, pady=PADY)
        self.quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        self.save_button = tk.Button(
            self.root, text="Speichern", command=self.create_pdf
        )
        self.save_button.pack(side=tk.LEFT, padx=PADX, pady=PADY)
        self.save_button.bind("<Return>", (lambda event: self.create_pdf()))

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
            self.pdf.zugferd.add_xml2pdf(file_name, outfile)
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
        if self.pdf.lieferantensteuerung.BYOPdf:
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
            self.pdf.fill_pdf()
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

    def _fill_pdf_only(self, outfile: str) -> None:
        if outfile is not None:
            self.pdf.output(outfile)
            self._success_message(outfile)

    def _fill_pdf(self, directory):
        if self._try_to_fill_pdf():
            return
        fn, outfile = self._get_filenames(directory)
        if self.pdf.lieferantensteuerung.create_xml:
            if self._create_and_add_xml(fn, outfile):
                return
            self._success_message(outfile)
        else:
            self._fill_pdf_only(outfile)

    def _try_to_init_pdf(self, contentini_file: dict) -> bool:
        """returns True if error occurs"""
        try:
            self.pdf = Pdf(
                self.excel_file,
                contentini_file,
                self.logo_fn if Path(self.logo_fn).exists() else None,
            )
        except ValueError as e:
            messagebox.showerror("Fehler in den Stammdaten", e)
            return True
        return False

    def create_pdf(self):
        """
        create the pdf
        """
        # print('entries:', entries)
        if self.selected_lb_item is None:
            mymsg = "Bitte erst ein Excel Tabellenblatt auswählen."
            messagebox.showinfo("Information", mymsg)
            return
        if self.ini_file:
            contentini_file = self.ini_file.read_ini_file()
        if self.excel_file:
            self.excel_file.read_sheet(self.selected_lb_item)
        if self._try_to_init_pdf(contentini_file):
            return
        self._fill_pdf(contentini_file["Verzeichnis"])

    def open_stammdaten(self):
        """
        Open Stammdaten for editing
        """
        self.root.quit()
        s_oberfl = OberflaecheIniFile(self.fields, self.ini_file, self.root)
        s_oberfl.loop()

    def _file_dialog(self, init_dir: str) -> None:
        self.filename = filedialog.askopenfilename(
            title="Bitte die Excel Datei auswählen",
            initialdir=Path(init_dir).resolve(),
            filetypes=(("Excel Datei", "*.xlsx"), ("Alle Dateien", "*.*")),
        )

    def _read_sheet_list(self) -> list:
        self.excel_file = ExcelContent(self.filename, "")
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


if __name__ == "__main__":
    thedir = Path.joinpath(
        Path(os.getenv("APPDATA")).resolve(), Path("excel2zugferd")
    )
    ini = IniFile("config.ini", thedir)
    if not Path.exists(thedir):
        try:
            os.mkdir(thedir)
        except IOError as e:
            msg = f"Ich kann das Verzeichnis {dir} nicht erstellen.\n\
                    {format_ioerr(e)}"
            messagebox.showerror("Fehler", msg)
    oberfl = None
    if ini.exists_ini_file() is None:
        oberfl = OberflaecheIniFile(fields, ini)
    else:
        oberfl = OberflaecheExcel2Zugferd(fields, ini)
    oberfl.loop()
