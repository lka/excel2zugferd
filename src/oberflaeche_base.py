"""
Module Oberflaechen
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from pathlib import Path
from PIL import Image, ImageTk
import webbrowser
from src.handle_ini_file import IniFile
from src.constants import LABELWIDTH, TEXTWIDTH, PADX, PADY
from src.middleware import Middleware
import src
from src.invoice_collection import InvoiceCollection


class Oberflaeche:
    """
    Creates Parts of Oberflaeche
    """

    def __init__(self, window: tk.Tk = None, wsize: str = "480x420") -> None:
        if window:
            # print('Oberflaeche destroying window')
            self.destroy_children(window)

        self.root = tk.Tk() if window is None else window
        self.root.geometry(wsize)
        self.canvas: tk.Canvas = None
        self.img_area: tk.Image = None
        self.ents: dict = None
        self.menuvars: dict = {}
        self.middleware: Middleware = None
        self.logo_fn: str = src.logo_fn()  # type: ignore
        # make content_frame as grid
        self.icanvas: tk.Canvas = None
        self.content_frame: ttk.Frame = None
        self._add_window_with_scrollbar()

    def _add_window_with_scrollbar(self) -> None:
        # Create a frame to hold the listbox and scrollbar
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        # create inner canvas and scrollbar side by side
        self.icanvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical",
                                 command=self.icanvas.yview)
        self.icanvas.configure(yscrollcommand=scrollbar.set)
        # create frame for scrollable content
        self.content_frame = ttk.Frame(self.icanvas)
        self.content_frame.bind("<Configure>", lambda e:
                                self.icanvas.configure(
                                    scrollregion=self.icanvas
                                    .bbox("all")))
        # Pack Widgets onto the Window
        self.icanvas.create_window((0, 0), window=self.content_frame,
                                   anchor="nw")
        self.icanvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        # create window resizing configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        # bind canvas to mousewheel events
        self.icanvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _add_quit_save_buttons(self, at_row: int, save_cmd: any) -> None:
        quit_button = ttk.Button(self.content_frame, text="Beenden",
                                 command=self.quit_cmd)
        quit_button.grid(row=at_row, column=0, pady=PADY)
        quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        save_button = ttk.Button(
            self.content_frame, text="Speichern", command=save_cmd
        )
        save_button.grid(row=at_row, column=1, padx=PADX, pady=PADY)
        save_button.bind("<Return>", (lambda event: save_cmd()))

    def _on_mousewheel(self, event):
        self.icanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _add_menu_items(self, menu: tk.Menu, key: str,
                        command: callable) -> None:
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

    def make_logo(self, fn: str):
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

    def open_link(self, link: str) -> None:
        webbrowser.open(link)

    def show_custom_messagebox(self, header: str, msg: str, dest: str) -> None:
        custom_box = tk.Toplevel()
        custom_box.title(header)
        ttk.Label(custom_box, text=msg, padding=(20, 10)).pack()
        # padx=20, pady=10).pack()
        link = ttk.Label(custom_box, text=dest,
                         foreground="blue",
                         cursor="hand2",
                         padding=(20, 10))  # padx=20, pady=10)
        link.pack()
        link.bind("<Button-1>", lambda e: self.open_link(dest))
        ttk.Button(custom_box, text="OK", command=custom_box.destroy,
                   padding=(30, 4)).pack(side="right", padx=10, pady=10)
        # padding=(20, 10))
        # padx=10, pady=10)

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
Version {version['version'] if version is not None else 'unbekannt'}\n\n\
Dokumentation: "
        except OSError as ex:
            my_msg = f"OSError: {ex}"
            raise ValueError(my_msg)

#        messagebox.showinfo("Info", my_msg)
        self.show_custom_messagebox("Info", my_msg,
                                    "https://github.com/lka/excel2zugferd")
        self.root.lift()

    def destroy_children(self, parent: tk.Tk) -> None:
        """
        recursive destroy all children of current window
        """
        for child in parent.winfo_children():
            if child.winfo_children():
                self.destroy_children(child)
            child.destroy()

    def _add_string(self, row: tk.Frame, field: dict, content: any,
                    index: int) -> tk.Text:
        lab = ttk.Label(
            row, width=LABELWIDTH, text=field["Label"] + ": ",
            anchor="w"
        )
        ent = tk.Text(row, width=TEXTWIDTH, height=field["Lines"])
        if content:
            ent.insert(
                tk.END,
                content[field["Text"]] if field["Text"] in content else "",
            )
        lab.grid(row=index, column=0, padx=PADX, pady=PADY)
        ent.grid(row=index, column=1, padx=PADX, pady=PADY)
        return ent

    def _add_label(self, row: tk.Frame, field: dict, content: dict,
                   index: int) -> ttk.Label:
        msg = content[field["Text"]] if\
            content and field["Text"] in content else ""
        if msg != "":
            lab = ttk.Label(
                row, width=LABELWIDTH, text=field["Label"] + ": ",
                anchor="w"
            )
        else:
            lab = ttk.Label(
                row, width=LABELWIDTH, text="",
                anchor="w"
            )
            msg = field["Label"]
        ent = ttk.Label(
                row, text=msg, width=TEXTWIDTH, anchor="w"
        )
        lab.grid(row=index, column=0, padx=PADX, pady=PADY)
        ent.grid(row=index, column=1, padx=PADX, pady=PADY, sticky="W")
        return ent

    def _set_value_for_boolean(self, field: dict, content: dict) -> None:
        self.menuvars[field["Variable"]].set(
            "1"
            if content  # and len(content) > 0
            and field["Text"] in content
            and (
                (content[field["Text"]] == "Ja")
                or (content[field["Text"]] == "1")
            )
            else "0"
        )

    def _add_boolean(self, row: tk.Frame, field: dict, content: dict,
                     index: int)\
            -> ttk.Checkbutton:
        self.menuvars[field["Variable"]] = tk.StringVar()
        ent = ttk.Checkbutton(
            row, text=field["Label"], variable=self.menuvars[
                                                field["Variable"]]
        )
        self._set_value_for_boolean(field, content)
        lab = ttk.Label(row, width=LABELWIDTH, text=" ", anchor="w")
        lab.grid(row=index, column=0, padx=PADX, pady=PADY)
        ent.grid(row=index, column=1, padx=PADX, pady=PADY, sticky="W")
        return ent

    def _create_iniFile(self, ini_file: IniFile, content: dict = None) -> bool:
        try:
            if ini_file:
                ini_file.create_ini_file(content)
        except OSError as ex:
            messagebox.showerror("IO-Fehler:",
                                 f"Erstellen der Ini-Datei \
fehlgeschlagen.\n{ex}")
            return True
        return False

    def _get_text_of_field(self, field: any, key: str = None) -> str:
        if isinstance(field, ttk.Label):
            return self.middleware.ini_file.content[key]\
                if self.middleware else ''
        return (
                    field.get("1.0", "end-1c")
                    if hasattr(field, "get")
                    else "Ja" if field.instate(["selected"]) else "Nein"
                )

    def get_entries_from_type(self, row: ttk.Frame, field: dict, content: dict,
                              index: int):
        ent = None
        if field["Type"] == "String":
            ent = self._add_string(row, field, content, index)
        if field["Type"] == "Boolean":
            ent = self._add_boolean(row, field, content, index)
        if field["Type"] == "Label":
            ent = self._add_label(row, field, content, index)
        return ent

    def makeform(self, type: str = None, offset: int = 0) -> dict:
        """
        create the form of Stammdaten Oberflaeche
        """
        entries = {}
        content = {}
        if self.middleware.ini_file:
            content = self.middleware.ini_file.read_ini_file()
        for field in self.fields:
            if (field["Dest"] == type):
                # row = tk.Frame(self.root)
                entries[field["Text"]] = self\
                    .get_entries_from_type(self.content_frame,
                                           field,
                                           content,
                                           len(entries) + offset)
        return entries

    def pre_open_excel2zugferd(self):
        obj = src.oberflaeche_excel2zugferd.OberflaecheExcel2Zugferd
        self.open_new_window(obj)

    def pre_open_stammdaten(self):
        obj = src.oberflaeche_ini.OberflaecheIniFile
        self.open_new_window(obj)

    def pre_open_steuerung(self):
        obj = src.oberflaeche_steuerung.OberflaecheSteuerung
        self.open_new_window(obj)

    def pre_open_excelsteuerung(self):
        obj = src.oberflaeche_excelsteuerung.OberflaecheExcelSteuerung
        self.open_new_window(obj)

    def pre_open_excelpositions(self):
        obj = src.oberflaeche_excelpositions.OberflaecheExcelPositions
        self.open_new_window(obj)

    def open_new_window(self, Obj: object = None):
        """
        Open Object for editing
        """
        self.fetch_values_from_entries()
        self.root.quit()
        s_oberfl = Obj(self.fields, self.middleware, self.root)
        s_oberfl.loop()

    def _check_content_of_stammdaten(self, content: dict) -> bool:
        """return whether stammdaten have failures"""
        try:
            InvoiceCollection(stammdaten=content)
        except ValueError as e:
            messagebox.showerror("Fehler in den Stammdaten", e.args[0])
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
                content[key] = self._get_text_of_field(field, key)
            if content:
                return self.middleware.ini_file\
                    .merge_content_of_ini_file(content)
        return content

    def fetch(self):
        """
        get all values for IniFile
        """
        content = self.fetch_values_from_entries()
        ini_has_failure = False
        if content:
            ini_has_failure = self._create_iniFile(
                self.middleware.ini_file, None)
            ini_has_failure = ini_has_failure or \
                self._check_content_of_stammdaten(content)
            if ini_has_failure:
                messagebox.showinfo("Info",
                                    "Stammdaten mit Fehlern gespeichert.")
                return
            messagebox.showinfo("Info", "Stammdaten gespeichert.")

    def loop(self):
        """
        run main loop
        """
        self.root.mainloop()
