"""
Module Oberflaechen
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from pathlib import Path
from PIL import Image, ImageTk
from src.handle_ini_file import IniFile
from src.constants import LABELWIDTH, TEXTWIDTH, PADX, PADY
import src


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
        if content:
            ent.insert(
                tk.END,
                content[field["Text"]] if field["Text"] in content else "",
            )
        row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        return ent

    def _add_label(self, row: tk.Frame, field: dict, content: dict)\
            -> tk.Message:
        msg = content[field["Text"]] if\
            content and field["Text"] in content else ""
        if msg != "":
            lab = tk.Label(
                row, width=LABELWIDTH, text=field["Label"] + ": ",
                anchor="w"
            )
        else:
            lab = tk.Label(
                row, width=LABELWIDTH, text="",
                anchor="w"
            )
            msg = field["Label"]
        ent = tk.Label(
                row, text=msg, width=TEXTWIDTH, anchor="w"
        )
        row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
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

    def _add_boolean(self, row: tk.Frame, field: dict, content: dict)\
            -> tk.Checkbutton:
        self.menuvars[field["Variable"]] = tk.StringVar()
        ent = ttk.Checkbutton(
            row, text=field["Label"], variable=self.menuvars[
                                                field["Variable"]]
        )
        self._set_value_for_boolean(field, content)
        lab = tk.Label(row, width=LABELWIDTH, text=" ", anchor="w")
        row.pack(side=tk.TOP, fill=tk.X, padx=PADX, pady=PADY)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        return ent

    def _create_iniFile(self, ini_file: IniFile, content: dict = None) -> bool:
        try:
            if ini_file:
                ini_file.create_ini_file(content)
        except IOError as ex:
            mymsg = f"Erstellen der Ini-Datei fehlgeschlagen.\n\
            {src.format_ioerr(ex)}"
            messagebox.showerror("Fehler:", mymsg)
            return True
        return False

    def _get_text_of_field(self, field: any) -> str:
        if isinstance(field, tk.Label):
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
