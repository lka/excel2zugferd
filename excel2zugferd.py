import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import *

# from tkinter.font import Font
from handlePDF import Pdf

from handleIniFile import IniFile
from excelContent import ExcelContent
import tempfile, os
from pathlib import Path

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
    def __init__(self, *args, **kwargs):
        self.root = tk.Tk()
        # self.myFont = Font(family="Helvetica", size=12)
        self.root.resizable(0, 0)
        try:
            # windows only (remove the minimize/maximize button)
            self.root.attributes("-toolwindow", True)
        except tk.TclError:
            print("Not supported on your platform")

    def makeMenuBar(self, menuItems=None):
        menu_bar = tk.Menu(self.root)
        # print(menuItems)
        if menuItems == None:
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

    def quit_cmd(self):
        confirm = messagebox.askokcancel("Beenden?", "Möchten Sie wirklich Beenden ?")
        if confirm:
            self.root.destroy()

    def info_cmd(self):
        messagebox.showinfo("Info", "Copyright H.Lischka 2024\nVersion 0.1.0")

    def loop(self):
        self.root.mainloop()


class OberflaecheIniFile(Oberflaeche):
    def __init__(self, fields, iniFile=None, *args, **kwargs):
        super(OberflaecheIniFile, self).__init__(*args, **kwargs)
        self.fields = fields
        self.iniFile = iniFile
        self.root.title("Stammdateneingabe")
        self.makeMenuBar(
            [
                {"Datei": {"Stammdateneingabe Beenden": self.quit_cmd}},
                {"Hilfe": {"Info über...": self.info_cmd}},
            ]
        )
        self.ents = self.makeform()
        # self.root.bind('<Return>', (lambda event, e=self.ents: self.fetch(e)))
        self.quit_button = tk.Button(self.root, text="Beenden", command=self.quit_cmd)
        self.quit_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        self.save_button = tk.Button(self.root, text="Speichern", command=self.fetch)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_button.bind("<Return>", (lambda event: self.fetch()))

    def fetch(self):
        # print('entries:', entries)
        content = {}
        for key in self.ents:
            field = key
            text = self.ents[key].get("1.0", "end-1c")
            content[field] = text
            # print('%s: "%s"' % (field, text))
        self.iniFile.createIniFile(content)
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
        self.save_button = tk.Button(self.root, text="Speichern", command=self.createPdf)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_button.bind("<Return>", (lambda event: self.createPdf()))

    def createPdf(self):
        # print('entries:', entries)
        if not hasattr(self, 'selectedItem'):
            msg = f"Bitte erst ein Excel Tabellenblatt auswählen."
            messagebox.showinfo("Information", msg)
            return
        contentIniFile = self.iniFile.readIniFile()
        self.excelFile.readSheet(self.selectedItem)
        createXML = True if contentIniFile["ZugFeRD"].split("\n")[0] == "Ja" else False
        self.pdf = Pdf(self.excelFile, contentIniFile, createXML)
        # msg = f"Ausgewählt wurde das Excel Sheet: {self.selectedItem}"
        # messagebox.showinfo("Information", msg)
        self.pdf.fill_Pdf()
        fn = self.selectedItem + ".pdf"
        # print(contentIniFile["Verzeichnis"], fn)
        tmpfn = Path.joinpath(Path(contentIniFile["Verzeichnis"]).absolute(), fn)
        outfile = self.pdf.uniquify(tmpfn)
        if createXML:
            with tempfile.TemporaryDirectory() as tmp:
                fileName = os.path.join(tmp, fn) # doesn't matter, cannot exist twice
                self.pdf.output(fileName)
                self.pdf.zugferd.add_xml2pdf(fileName, outfile)
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
        if Path(Path.joinpath(docDir, 'Documents')).is_dir():
            docDir = Path.joinpath(docDir, 'Documents')
        initDir = contentIniFile["Verzeichnis"] if len(contentIniFile["Verzeichnis"]) > 0 else docDir

        # print(initDir)
        self.filename = filedialog.askopenfilename(
            title="Bitte die Excel Datei auswählen",
            initialdir=Path(initDir).resolve(),
            filetypes=(("Excel Datei", "*.xlsx"), ("Alle Dateien", "*.*")),
        )
        if len(self.filename) > 0 and Path(self.filename).exists():
            dir = os.path.dirname(self.filename)
            self.iniFile.createIniFile({**contentIniFile, "Verzeichnis": dir})
            self.excelFile = ExcelContent(self.filename, "")
            self.fileNameLabel.config(text=self.filename)
            self.lb.delete(0,'end')
            items = self.excelFile.readSheetList()
            for item in items:
                self.lb.insert("end", item)

    def click_button(self, event):
        # get selected indices
        selected_indices = self.lb.curselection()
        # get selected items
        self.selectedItem = ",".join([self.lb.get(i) for i in selected_indices])

    def makeform(self):
        self.fileNameButton = Button(self.root, text="Excel-Datei...", command=self.openFile)
        self.fileNameButton.pack ( anchor='nw' )
        self.fileNameLabel = tk.Label(
            self.root,
            text="Bitte erst die Excel Datei auswählen (über Datei -> Öffnen...).",
        )
        self.fileNameLabel.pack()
        self.lb = tk.Listbox(self.root, height=20)
        self.lb.bind("<<ListboxSelect>>", self.click_button)
        self.lb.pack(expand=True, fill=tk.BOTH)

if __name__ == "__main__":
    ini = IniFile("Excel2ZugFeRD.ini", ".")
    if ini.existsIniFile() == None:
        oberfl = OberflaecheIniFile(fields, ini)
        oberfl.loop()
    else:
        oberfl = OberflaecheExcel2Zugferd(fields, ini)
        oberfl.loop()
