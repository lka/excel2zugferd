import tkinter as tk
from tkinter import messagebox, filedialog, Button
import json
from handlePDF import Pdf
import tempfile
import os
from pathlib import Path
from PIL import Image, ImageTk
import shutil

from handleIniFile import IniFile
from excelContent import ExcelContent

fields = [
    {"Text": "Betriebsbezeichnung", "Lines": 1},
    {"Text": "Anschrift", "Lines": 5},
    {"Text": "Name", "Lines": 1},
    {"Text": "Kontakt", "Lines": 5},
    {"Text": "Umsatzsteuer", "Lines": 2},
    {"Text": "Konto", "Lines": 3},
    {"Text": "Zahlungsziel", "Lines": 1},
    {"Text": "Abspann", "Lines": 5},
    {"Text": "ZugFeRD", "Lines": 1},
]


class Oberflaeche:
    def __init__(self, window=None, *args, **kwargs):
        self.root = tk.Tk() if window is None else window
        # self.myFont = Font(family="Helvetica", size=12)
        self.root.resizable(0, 0)
        self.logo_fn = os.path.join(os.getenv("APPDATA"), "excel2zugferd", "logo.jpg")
        try:
            # windows only (remove the minimize/maximize button)
            self.root.attributes("-toolwindow", True)
        except tk.TclError:
            print("Not supported on your platform")

    def makeMenuBar(self, menuItems=None):
        menu_bar = tk.Menu(self.root)
        # print(menuItems)
        if menuItems is None:
            return
        for item in menuItems:
            outerkeys = item.keys()
            for outerkey in outerkeys:
                # print(outerkey)
                menu = tk.Menu(menu_bar, tearoff=0)
                innerkeys = item[outerkey].keys()
                for innerkey in innerkeys:
                    # print(innerkey)
                    if innerkey == "Separator":
                        menu.add_separator
                    else:
                        menu.add_command(
                            label=innerkey, command=item[outerkey][innerkey]
                        )
                menu_bar.add_cascade(label=outerkey, menu=menu, underline=0)
        self.root.config(menu=menu_bar)

    def makeLogo(self, fn):
        if Path(fn).exists():
            img = Image.open(fn)
            img = img.resize((100, 100), Image.BOX)
            image = ImageTk.PhotoImage(img)
            self.imgArea = self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.img = image

    def quit_cmd(self):
        confirm = messagebox.askokcancel("Beenden?", "Möchten Sie wirklich Beenden ?")
        if confirm:
            self.root.destroy()

    def info_cmd(self):
        try:
            with open(r".\\_internal\\version.json", "r", encoding="utf-16") as f_in:
                version = json.load(f_in)
                msg = f"Copyright © H.Lischka, 2024\nVersion {version['version'] if version is not None else 'unbekannt'}"
        except Exception as e:
            msg = f"Error: {e.message if hasattr(e, 'message')  else e}"

        messagebox.showinfo("Info", msg)
        self.root.lift()

    def loop(self):
        self.root.mainloop()


class OberflaecheIniFile(Oberflaeche):
    def __init__(self, fields, iniFile=None, *args, **kwargs):
        super(OberflaecheIniFile, self).__init__(window=tk.Toplevel(), *args, **kwargs)

        self.fields = fields
        self.iniFile = iniFile
        self.root.title("Stammdateneingabe")
        self.makeMenuBar(
            [
                {"Datei": {"Stammdateneingabe Beenden": self.quit_cmd}},
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        row = tk.Frame(self.root)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.logo_button = tk.Button(
            row, text="Logo auswählen...", anchor="w", command=self.handleFileButton
        )
        self.logo_button.pack(side=tk.LEFT, padx=5)
        self.logo_button.bind("<Return>", (lambda event: self.handleFileButton))
        self.logo_delete = tk.Button(
            row, text="Logo löschen", command=self.handleLogoDeleteButton
        )
        self.logo_delete.bind("<Return>", (lambda event: self.handleLogoDeleteButton))
        if Path(self.logo_fn).exists():
            self.logo_delete.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(row, width=100, height=100, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=38, anchor="w", expand=True)

        self.makeLogo(self.logo_fn)

        self.ents = self.makeform()
        # self.root.bind('<Return>', (lambda event, e=self.ents: self.fetch(e)))
        self.quit_button = tk.Button(self.root, text="Beenden", command=self.quit_cmd)
        self.quit_button.pack(side=tk.LEFT, padx=5, pady=5, expand=False)
        self.quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        self.save_button = tk.Button(self.root, text="Speichern", command=self.fetch)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5, expand=False)
        self.save_button.bind("<Return>", (lambda event: self.fetch()))

    def fetch(self):
        # print('entries:', entries)
        content = {}
        for key in self.ents:
            field = key
            text = self.ents[key].get("1.0", "end-1c")
            content[field] = text
            # print('%s: "%s"' % (field, text))
        try:
            self.iniFile.createIniFile(content)
        except Exception as e:
            msg = f"Erstellen der Ini-Datei fehlgeschlagen.\n{e.message if hasattr(e, 'message') else e}"
            messagebox.showerror("Fehler:", msg)
        self.root.destroy()

    def makeform(self):
        content = self.iniFile.readIniFile()
        # print(content)
        entries = {}
        # print(fields)
        for field in self.fields:
            row = tk.Frame(self.root)
            lab = tk.Label(row, width=22, text=field["Text"] + ": ", anchor="w")
            # ent = Entry(row)
            # ent.insert(0, "")
            ent = tk.Text(row, width=40, height=field["Lines"])
            # ent.configure(font=self.myFont)
            ent.insert(
                tk.END,
                content[field["Text"]] if field["Text"] in content else "",
            )
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries[field["Text"]] = ent
        return entries

    def handleFileButton(self):
        initDir = Path.joinpath(Path.home(), "Pictures")

        filename = filedialog.askopenfilename(
            title="Bitte die Datei mit dem Logo auswählen",
            initialdir=Path(initDir).resolve(),
            filetypes=(("Bilder", "*.jpg; *.jpeg"), ("Alle Dateien", "*.*")),
        )

        if filename is not None:
            shutil.copy(filename, self.logo_fn)
            self.makeLogo(self.logo_fn)
            self.logo_delete.pack(side=tk.LEFT, padx=5)
            self.root.lift()

    def handleLogoDeleteButton(self):
        resp = messagebox.askyesno(
            "Löschen des Logos", "Sind Sie sicher, dass Sie das Logo löschen möchten?"
        )
        print(resp)
        if resp is True:
            os.remove(self.logo_fn)
            self.logo_delete.pack_forget()
            self.canvas.delete("all")
        self.root.lift()


class OberflaecheExcel2Zugferd(Oberflaeche):
    def __init__(self, fields, ini=None, *args, **kwargs):
        super(OberflaecheExcel2Zugferd, self).__init__(*args, **kwargs)
        self.fields = fields
        self.iniFile = ini
        self.root.title("Excel2ZugFeRD")
        self.makeMenuBar(
            [
                {
                    "Datei": {
                        "Öffnen...": self.openFile,
                        "Stammdateneingabe": self.openStammdaten,
                        "Separator": 0,
                        "Beenden": self.quit_cmd,
                    }
                },
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        self.ents = self.makeform()
        # self.root.bind('<Return>', (lambda event, e=self.ents: self.fetch(e)))
        self.quit_button = tk.Button(self.root, text="Beenden", command=self.quit_cmd)
        self.quit_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        self.save_button = tk.Button(
            self.root, text="Speichern", command=self.createPdf
        )
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_button.bind("<Return>", (lambda event: self.createPdf()))

    def createPdf(self):
        # print('entries:', entries)
        if not hasattr(self, "selectedItem"):
            msg = "Bitte erst ein Excel Tabellenblatt auswählen."
            messagebox.showinfo("Information", msg)
            return
        contentIniFile = self.iniFile.readIniFile()
        self.excelFile.readSheet(self.selectedItem)
        createXML = True if contentIniFile["ZugFeRD"].split("\n")[0] == "Ja" else False

        #        msg = f"Ausgewählt wurde das Excel Sheet: {self.selectedItem}"
        #        messagebox.showinfo("Information", msg)

        self.pdf = Pdf(
            self.excelFile,
            contentIniFile,
            createXML,
            self.logo_fn if Path(self.logo_fn).exists() else None,
        )

        self.pdf.fill_Pdf()
        fn = self.selectedItem + ".pdf"
        # print(contentIniFile["Verzeichnis"], fn)
        tmpfn = Path.joinpath(Path(contentIniFile["Verzeichnis"]).absolute(), fn)
        outfile = self.pdf.uniquify(tmpfn)

        #        msg = f"Die Datei {outfile} wurde vorgesehen"
        #        messagebox.showinfo("Debug-Information", msg)

        if createXML:
            try:
                # tmp = tempfile.gettempdir()
                with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                    fileName = Path.joinpath(
                        Path(tmp), fn
                    )  # doesn't matter, cannot exist twice
                    self.pdf.output(fileName)
                    #                msg = f"Die Datei {fileName} wurde erstellt"
                    #                messagebox.showinfo("Debug-Information", msg)
                    try:
                        self.pdf.zugferd.add_xml2pdf(fileName, outfile)
                    except Exception as e:
                        msg = f"Konnte {outfile} aus {fileName} nicht erstellen, da ein Problem aufgetreten ist.\
                                \n{e.message if hasattr(e, 'message') else e}"
                        messagebox.showerror("Fehler:", msg)
                        return
            except Exception as e:
                msg = f"Konnte {fileName} nicht erstellen, da ein Problem aufgetreten ist.\
                    \n{e.message if hasattr(e, 'message') else e}"
                messagebox.showerror("Fehler:", msg)
                return
        else:
            self.pdf.output(outfile)
        msg = f"Die Datei {outfile} wurde erstellt."
        messagebox.showinfo("Information", msg)

    def openStammdaten(self):
        s_oberfl = OberflaecheIniFile(self.fields, self.iniFile)
        s_oberfl.loop()

    def openFile(self):
        contentIniFile = self.iniFile.readIniFile()
        docDir = Path.home()
        if Path(Path.joinpath(docDir, "Documents")).is_dir():
            docDir = Path.joinpath(docDir, "Documents")
        initDir = (
            contentIniFile["Verzeichnis"]
            if "Verzeichnis" in contentIniFile
            and len(contentIniFile["Verzeichnis"]) > 0
            else docDir
        )

        # print(initDir, "Verzeichnis" in contentIniFile, contentIniFile)
        self.filename = filedialog.askopenfilename(
            title="Bitte die Excel Datei auswählen",
            initialdir=Path(initDir).resolve(),
            filetypes=(("Excel Datei", "*.xlsx"), ("Alle Dateien", "*.*")),
        )
        if len(self.filename) > 0 and Path(self.filename).exists():
            dir = os.path.dirname(self.filename)
            self.excelFile = ExcelContent(self.filename, "")
            self.fileNameLabel.config(text=self.filename)
            self.lb.delete(0, "end")
            items = self.excelFile.readSheetList()
            for item in items:
                self.lb.insert("end", item)
            try:
                self.iniFile.createIniFile({**contentIniFile, "Verzeichnis": dir})
            except Exception as e:
                msg = f"Ini-File kann nicht beschrieben werden.\n{e.message if hasattr(e, 'message') else e}"
                messagebox.showerror("Fehler", msg)

    def click_button(self, event):
        # get selected indices
        selected_indices = self.lb.curselection()
        # get selected items
        self.selectedItem = ",".join([self.lb.get(i) for i in selected_indices])

    def makeform(self):
        self.fileNameButton = Button(
            self.root, text="Excel-Datei...", command=self.openFile
        )
        self.fileNameButton.pack(anchor="nw")
        self.fileNameLabel = tk.Label(
            self.root,
            text="Bitte erst die Excel Datei auswählen (über Datei -> Öffnen...).",
        )
        self.fileNameLabel.pack()
        self.lb = tk.Listbox(self.root, height=20)
        self.lb.bind("<<ListboxSelect>>", self.click_button)
        self.lb.pack(expand=True, fill=tk.BOTH)


if __name__ == "__main__":
    dir = Path.joinpath(Path(os.getenv("APPDATA")), Path("excel2zugferd"))
    ini = IniFile("config.ini", dir)
    if not Path.exists(dir):
        try:
            os.mkdir(dir)
        except Exception as e:
            msg = f"Ich kann das Verzeichnis {dir} nicht erstellen.\n{e.message if hasattr(e, 'message') else e}"
            messagebox.showerror("Fehler", msg)
    if ini.existsIniFile() is None:
        oberfl = OberflaecheIniFile(fields, ini)
        oberfl.loop()
    else:
        oberfl = OberflaecheExcel2Zugferd(fields, ini)
        oberfl.loop()
