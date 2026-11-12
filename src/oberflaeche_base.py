"""
Module Oberflaechen
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
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

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

APPEARANCE_KEY = "Erscheinungsbild"
APPEARANCE_MODES = {"System": "System", "Hell": "Light", "Dunkel": "Dark"}
APPEARANCE_DEFAULT = "System"
MENU_FONT = ("Segoe UI", 14)
MENU_BAR_COLOR = ("gray76", "gray25")
MENU_LINE_COLOR = ("gray50", "gray50")
CTK_ROOT_CALLBACKS = ("update", "check_dpi_scaling")
CHAR_PX = 8  # approximate pixel width of one character
LINE_PX = 20  # approximate pixel height of one text line
LABEL_PX = LABELWIDTH * CHAR_PX
TEXT_PX = TEXTWIDTH * CHAR_PX


class Oberflaeche:
    """
    Creates Parts of Oberflaeche
    """

    def __init__(self, window: ctk.CTk = None, wsize: str = "480x680") -> None:
        if window:
            self.destroy_children(window)

        self.root = ctk.CTk() if window is None else window
        self.wsize = wsize
        self.root.geometry(wsize)
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.canvas: tk.Canvas = None
        self.img_area: int = None
        self.ents: dict = None
        self.menuvars: dict = {}
        self.middleware: Middleware = None
        self.logo_fn: str = src.logo_fn()  # type: ignore
        self.content_frame: ctk.CTkScrollableFrame = None
        self._add_window_with_scrollbar()

    def _add_window_with_scrollbar(self) -> None:
        """adds a scrollable content frame to the window"""
        self.content_frame = ctk.CTkScrollableFrame(self.root)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

    def _add_quit_save_buttons(self, at_row: int, save_cmd: any) -> None:
        """adds quit and save buttons to window

        Args:
            at_row (int): row No. for GUI
            save_cmd (any): call specified command with save button
        """
        quit_button = ctk.CTkButton(
            self.content_frame, text="Beenden", command=self.quit_cmd
        )
        quit_button.grid(row=at_row, column=0, pady=PADY)
        quit_button.bind("<Return>", (lambda event: self.quit_cmd()))
        save_button = ctk.CTkButton(
            self.content_frame, text="Speichern", command=save_cmd
        )
        save_button.grid(row=at_row, column=1, padx=PADX, pady=PADY)
        save_button.bind("<Return>", (lambda event: save_cmd()))

    def _add_menu_items(self, menu: tk.Menu, key: str, command: callable) -> None:
        """adds separator or items to menu

        Args:
            menu (tk.Menu): the menu of the window
            key (str): button for the menu
            command (callable): command called when key is pushed
        """
        if "Separator" in key:
            menu.add_separator()
        else:
            menu.add_command(label=key, command=command)

    def _add_items(self, menu_bar: ctk.CTkFrame, menu_items: list) -> None:
        """add one button with a drop down menu per top level entry

        Args:
            menu_bar (ctk.CTkFrame): the MenuBar
            menu_items (list): list of menu items
        """
        for item in menu_items:
            for outerkey in item.keys():
                menu = tk.Menu(menu_bar, tearoff=0, font=MENU_FONT)
                for innerkey in item[outerkey].keys():
                    if isinstance(item[outerkey][innerkey], dict):
                        submenu = self.make_sub_menu(menu, item[outerkey][innerkey])
                        menu.add_cascade(label=innerkey, menu=submenu)
                    else:
                        self._add_menu_items(menu, innerkey, item[outerkey][innerkey])
                button = ctk.CTkButton(
                    menu_bar,
                    text=outerkey,
                    width=70,
                    corner_radius=4,
                    fg_color="transparent",
                    text_color=("black", "white"),
                    hover_color=("gray64", "gray35"),
                    font=ctk.CTkFont(size=15),
                )
                button.configure(command=lambda b=button, m=menu: self._popup(b, m))
                button.pack(side="left", padx=2, pady=2)

    @staticmethod
    def _popup(button: ctk.CTkButton, menu: tk.Menu) -> None:
        """show drop down menu below the button"""
        try:
            menu.tk_popup(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())
        finally:
            menu.grab_release()

    def make_sub_menu(self, menu: tk.Menu, menu_items: dict) -> tk.Menu:
        """make submenu to menu

        Args:
            menu (tk.Menu): menu where submenu is added to
            menu_items (dict): items in submenu

        Returns:
            tk.Menu: new created submenu
        """
        submenu = tk.Menu(menu, tearoff=0, font=MENU_FONT)
        if menu_items is None:
            return
        for key in menu_items.keys():
            self._add_menu_items(submenu, key, menu_items[key])
        return submenu

    def make_menu_bar(self, menu_items: list = None) -> None:
        """generate MenuBar for each GUI window
        (own bar of CTkButtons with tk.Menu drop downs, larger font)

        Args:
            menu_items (list, optional): the list of menu items to show.
                                         Defaults to None.
        """
        if menu_items is None:
            return
        wrapper = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="ew")
        menu_bar = ctk.CTkFrame(wrapper, corner_radius=0, fg_color=MENU_BAR_COLOR)
        menu_bar.pack(fill="x")
        ctk.CTkFrame(
            wrapper, height=2, corner_radius=0, fg_color=MENU_LINE_COLOR
        ).pack(fill="x")
        self._add_items(menu_bar, menu_items)
        self._add_appearance_menu(menu_bar)

    def _stored_appearance(self) -> str:
        """appearance mode (System, Light, Dark) stored in the ini file"""
        content = self.middleware.ini_file.content if self.middleware else {}
        mode = (content or {}).get(APPEARANCE_KEY, APPEARANCE_DEFAULT)
        return mode if mode in APPEARANCE_MODES.values() else APPEARANCE_DEFAULT

    def _add_appearance_menu(self, menu_bar: ctk.CTkFrame) -> None:
        """menu to switch between System, Hell (light) and Dunkel (dark)"""
        mode = self._stored_appearance()
        if ctk.get_appearance_mode() != mode and mode != APPEARANCE_DEFAULT:
            ctk.set_appearance_mode(mode)
        self.appearance_var = tk.StringVar(value=mode)
        menu = tk.Menu(menu_bar, tearoff=0, font=MENU_FONT)
        for label, value in APPEARANCE_MODES.items():
            menu.add_radiobutton(
                label=label,
                value=value,
                variable=self.appearance_var,
                command=self._change_appearance,
            )
        button = ctk.CTkButton(
            menu_bar,
            text="Ansicht",
            width=70,
            corner_radius=4,
            fg_color="transparent",
            text_color=("black", "white"),
            hover_color=("gray64", "gray35"),
            font=ctk.CTkFont(size=15),
        )
        button.configure(command=lambda: self._popup(button, menu))
        button.pack(side="left", padx=2, pady=2)

    def _change_appearance(self) -> None:
        """apply the selected appearance mode and store it in the ini file"""
        mode = self.appearance_var.get()
        ctk.set_appearance_mode(mode)
        if self.middleware and self.middleware.ini_file:
            self._create_iniFile(self.middleware.ini_file, {APPEARANCE_KEY: mode})

    def make_logo(self, fn: str, rect: tuple = None) -> None:
        """set logo to position

        Args:
            fn (str): filename of logo
            rect (tuple, optional): x, y, w, h in pixel on the canvas.
                Defaults to None: height 100 at the upper left corner,
                aspect ratio is kept.
        """
        if fn is not None and Path(fn).exists():
            img = Image.open(fn)
            if rect is None:
                height = 100
                rect = 0, 0, int(img.width * (height / img.height)), height
            x, y, width, height = rect
            img = img.resize((max(width, 1), max(height, 1)), Image.BOX)
            image = ImageTk.PhotoImage(img)
            if self.canvas:
                self.img_area = self.canvas.create_image(
                    x, y, anchor=tk.NW, image=image
                )
                self.canvas.img = image

    def quit_cmd(self):
        """
        Quit window
        """
        confirm = messagebox.askokcancel("Beenden?", "Möchten Sie wirklich Beenden ?")
        if confirm:
            self.close_window()

    def close_window(self) -> None:
        """destroy the window; the pending after-callbacks of the customtkinter
        window (update, check_dpi_scaling) are cancelled first, otherwise Tk
        reports 'invalid command name' errors after the window is gone"""
        for after_id in self.root.tk.call("after", "info"):
            script = str(self.root.tk.call("after", "info", after_id)[0])
            if script.endswith(CTK_ROOT_CALLBACKS):
                self.root.after_cancel(after_id)
        self.root.destroy()

    def open_link(self, link: str) -> None:
        """open external link in web browser

        Args:
            link (str): external link
        """
        webbrowser.open(link)

    def show_custom_messagebox(self, header: str, msg: str, dest: str) -> None:
        """show message box with external link

        Args:
            header (str): header of the messagebox
            msg (str): message to show
            dest (str): destination (external link)
        """
        custom_box = ctk.CTkToplevel(self.root)
        custom_box.title(header)
        custom_box.after(100, custom_box.focus)
        ctk.CTkLabel(custom_box, text=msg, justify="left").pack(padx=20, pady=10)
        link = ctk.CTkLabel(
            custom_box, text=dest, text_color=("blue", "#6fa8ff"), cursor="hand2"
        )
        link.pack(padx=20, pady=10)
        link.bind("<Button-1>", lambda e: self.open_link(dest))
        ctk.CTkButton(custom_box, text="OK", command=custom_box.destroy).pack(
            side="right", padx=10, pady=10
        )

    def ask_string(
        self, title: str, prompt: str, initialvalue: str = ""
    ) -> str | None:
        """modal input dialog

        Args:
            title (str): title of the dialog
            prompt (str): text above the input field
            initialvalue (str, optional): preset text. Defaults to "".

        Returns:
            str | None: entered text, None if cancelled
        """
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        result: dict = {"value": None}
        ctk.CTkLabel(dialog, text=prompt).pack(padx=20, pady=(15, 5))
        entry = ctk.CTkEntry(dialog, width=300)
        entry.insert(0, initialvalue)
        entry.pack(padx=20, pady=5)

        def accept(_event=None):
            result["value"] = entry.get()
            dialog.destroy()

        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(pady=10)
        ctk.CTkButton(buttons, text="OK", width=90, command=accept).pack(
            side="left", padx=PADX
        )
        ctk.CTkButton(
            buttons, text="Abbrechen", width=90, command=dialog.destroy
        ).pack(side="left", padx=PADX)
        dialog.bind("<Return>", accept)
        dialog.bind("<Escape>", lambda e: dialog.destroy())
        dialog.after(150, entry.focus)
        dialog.after(150, dialog.grab_set)
        self.root.wait_window(dialog)
        return result["value"]

    def info_cmd(self):
        """show Info with Version Number and link to documentation"""
        try:
            with open(
                os.path.join("_internal", "version.json"), "r", encoding="utf-16"
            ) as f_in:
                version = json.load(f_in)
                my_msg = f"Copyright © H.Lischka, 2024\n\
Version {version['version'] if version is not None else 'unbekannt'}\n\n\
Dokumentation: "
        except OSError as ex:
            my_msg = f"OSError: {ex}"
            raise ValueError(my_msg)

        self.show_custom_messagebox(
            "Info", my_msg, "https://github.com/lka/excel2zugferd"
        )
        self.root.lift()

    def destroy_children(self, parent: ctk.CTk) -> None:
        """destroy all children of current window
        (customtkinter widgets destroy their own sub widgets)

        Args:
            parent (ctk.CTk): the root window
        """
        for child in parent.winfo_children():
            child.destroy()

    def _create_textbox(
        self, parent: ctk.CTkBaseClass, field: dict, content: any, width: int = TEXT_PX
    ) -> ctk.CTkTextbox:
        """create a CTkTextbox for a field and fill it with the ini content"""
        ent = ctk.CTkTextbox(
            parent,
            width=width,
            height=field["Lines"] * LINE_PX + 10,
            border_width=1,
            wrap="word",
        )
        if content:
            ent.insert(tk.END, content.get(field["Text"], ""))
        return ent

    def _add_string(
        self, row: ctk.CTkFrame, field: dict, content: any, index: int
    ) -> ctk.CTkTextbox:
        """add CTkTextbox to Frame

        Args:
            row (ctk.CTkFrame): Frame where String with Label will be added
            field (dict): dict with specification
            content (any): content of ini_file
            index (int): row No. where to add Frame

        Returns:
            ctk.CTkTextbox: entity for the GUI
        """
        lab = ctk.CTkLabel(row, width=LABEL_PX, text=field["Label"] + ": ", anchor="w")
        ent = self._create_textbox(row, field, content)
        lab.grid(row=index, column=0, padx=PADX, pady=PADY, sticky="nw")
        ent.grid(row=index, column=1, padx=PADX, pady=PADY)
        return ent

    def _add_label(
        self, row: ctk.CTkFrame, field: dict, content: dict, index: int
    ) -> ctk.CTkLabel:
        """add CTkLabel to Frame

        Args:
            row (ctk.CTkFrame): Frame where Label with Label will be added
            field (dict): dict with specification
            content (any): content of ini_file
            index (int): row No. where to add Frame

        Returns:
            ctk.CTkLabel: entity for the GUI
        """
        msg = content[field["Text"]] if content and field["Text"] in content else ""
        if msg != "":
            lab = ctk.CTkLabel(
                row, width=LABEL_PX, text=field["Label"] + ": ", anchor="w"
            )
        else:
            lab = ctk.CTkLabel(row, width=LABEL_PX, text="", anchor="w")
            msg = field["Label"]
        ent = ctk.CTkLabel(row, text=msg, width=TEXT_PX, anchor="w")
        lab.grid(row=index, column=0, padx=PADX, pady=PADY)
        ent.grid(row=index, column=1, padx=PADX, pady=PADY, sticky="W")
        return ent

    def _set_value_for_boolean(self, field: dict, content: dict) -> None:
        """set correct value for Checkbox

        Args:
            field (dict): dict with specification
            content (dict): content of ini_file
        """
        self.menuvars[field["Variable"]].set(
            "1"
            if content
            and field["Text"] in content
            and ((content[field["Text"]] == "Ja") or (content[field["Text"]] == "1"))
            else "0"
        )

    def _create_checkbox(
        self, parent: ctk.CTkBaseClass, field: dict, content: dict
    ) -> ctk.CTkCheckBox:
        """create a CTkCheckBox for a boolean field"""
        self.menuvars[field["Variable"]] = tk.StringVar()
        ent = ctk.CTkCheckBox(
            parent,
            text=field["Label"],
            variable=self.menuvars[field["Variable"]],
            onvalue="1",
            offvalue="0",
        )
        self._set_value_for_boolean(field, content)
        return ent

    def _add_boolean(
        self, row: ctk.CTkFrame, field: dict, content: dict, index: int
    ) -> ctk.CTkCheckBox:
        """add CTkCheckBox to Frame

        Args:
            row (ctk.CTkFrame): Frame where Checkbox with Label will be added
            field (dict): dict with specification
            content (any): content of ini_file
            index (int): row No. where to add Frame

        Returns:
            ctk.CTkCheckBox: entity for the GUI
        """
        ent = self._create_checkbox(row, field, content)
        lab = ctk.CTkLabel(row, width=LABEL_PX, text=" ", anchor="w")
        lab.grid(row=index, column=0, padx=PADX, pady=PADY)
        ent.grid(row=index, column=1, padx=PADX, pady=PADY, sticky="W")
        return ent

    def _create_iniFile(self, ini_file: IniFile, content: dict = None) -> bool:
        """CReate ini_file if it doesn't exist

        Args:
            ini_file (IniFile): Class IniFile
            content (dict, optional): content for the ini_file.
                                      Defaults to None.

        Returns:
            bool: True if error occurred, False if all is OK
        """
        try:
            if ini_file:
                ini_file.create_ini_file(content)
        except OSError as ex:
            messagebox.showerror(
                "IO-Fehler:",
                f"Erstellen der Ini-Datei \
fehlgeschlagen.\n{ex}",
            )
            return True
        return False

    def _get_Label_content(self, key: str) -> str:
        """get content in ini_file for Label

        Args:
            key (str): key in ini_file.content

        Returns:
            str: value for Label
        """
        content = self.middleware.ini_file.get_active_company_content()
        if key not in content.keys():
            return ""
        return content[key] if self.middleware else ""

    def _get_text_of_field(self, field: any, key: str = None) -> str:
        """get content of field in GUI

        Args:
            field (any): dict with specification
            key (str, optional): key for entity. Defaults to None.

        Returns:
            str: value of field in GUI
        """
        if isinstance(field, ctk.CTkLabel):
            return self._get_Label_content(key)
        if isinstance(field, ctk.CTkCheckBox):
            return "Ja" if str(field.get()) == "1" else "Nein"
        return field.get("1.0", "end-1c")

    def get_entries_from_type(
        self, row: ctk.CTkFrame, field: dict, content: dict, index: int
    ) -> ctk.CTkTextbox | ctk.CTkCheckBox | ctk.CTkLabel | None:
        """create GUI Element of type

        Args:
            row: place it at CTkFrame
            field: use dict with specification for this GUI element
            content: get content of ini_file for this GUI element
            index: used as row No.

        Returns:
            entity: one of type CTkTextbox | CTkCheckBox | CTkLabel | None
        """
        ent = None
        if field["Type"] == "String":
            ent = self._add_string(row, field, content, index)
        elif field["Type"] == "Boolean":
            ent = self._add_boolean(row, field, content, index)
        elif field["Type"] == "Label":
            ent = self._add_label(row, field, content, index)
        return ent

    def makeform(self, type: str, offset: int = 0) -> dict:
        """create the form of Stammdaten Oberflaeche

        Args:
            type (str): separation of the fields for specific GUI.
            offset (int, optional): offset to index of GUI elements
                                    for line No. Defaults to 0.

        Returns:
            dict: entries in specific GUI
        """
        entries = {}
        content = {}
        if self.middleware.ini_file:
            content = self.middleware.ini_file.get_active_company_content()
        for field in self.fields:
            if field["Dest"] == type:
                entries[field["Text"]] = self.get_entries_from_type(
                    self.content_frame, field, content, len(entries) + offset
                )
        return entries

    def load_values_into_entries(self, content: dict) -> None:
        if not self.ents:
            return
        menu_variables = {
            field["Text"]: field.get("Variable")
            for field in self.fields
            if field["Type"] == "Boolean"
        }
        for key, field in self.ents.items():
            value = content.get(key, "") if content else ""
            self._load_value_into_entry(key, field, value, menu_variables)

    def _load_value_into_entry(
        self, key: str, field: any, value: str, menu_variables: dict
    ) -> None:
        """Set the value of one form entry."""
        if isinstance(field, ctk.CTkTextbox):
            field.delete("1.0", "end")
            if value:
                field.insert(tk.END, value)
        elif isinstance(field, ctk.CTkLabel):
            field.configure(text=value)
        elif menu_variables.get(key) in self.menuvars:
            self.menuvars[menu_variables[key]].set(
                "1" if value in ["Ja", "1", True] else "0"
            )

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
        """Open new Window Object for editing

        Args:
            Obj (object, optional): the new window object. Defaults to None.
        """
        self.fetch_values_from_entries()
        self.root.quit()
        s_oberfl = Obj(self.fields, self.middleware, self.root)
        s_oberfl.loop()

    def _check_content_of_stammdaten(self, content: dict) -> bool:
        """return whether stammdaten have failures

        Args:
            content (dict): content of ini_file

        Returns:
            bool: True if Error in Stammdaten, False if OK
        """
        validation_content = self.middleware.ini_file.get_active_company_content()
        try:
            InvoiceCollection(stammdaten=validation_content)
        except ValueError as e:
            messagebox.showerror("Fehler in den Stammdaten", e.args[0])
            return True
        return False

    def fetch_values_from_entries(self) -> dict:
        """get all values from items in Oberfläche
        and merge them to ini_file.content

        Returns:
            dict: merged content of ini_file with changed items from GUI
        """
        content = {}
        if self.ents:
            for key, field in self.ents.items():
                content[key] = self._get_text_of_field(field, key)
            if content:
                return self.middleware.ini_file.merge_content_of_ini_file(content)
        return content

    def fetch(self) -> None:
        """get all values for IniFile"""
        content = self.fetch_values_from_entries()
        ini_has_failure = False
        if content:
            ini_has_failure = self._create_iniFile(self.middleware.ini_file, None)
            ini_has_failure = ini_has_failure or self._check_content_of_stammdaten(
                content
            )
            if ini_has_failure:
                messagebox.showinfo("Info", "Stammdaten mit Fehlern gespeichert.")
                return
            messagebox.showinfo("Info", "Stammdaten gespeichert.")

    def fit_window(self) -> None:
        """enlarge the window so that the content fits; the enlargement is
        limited to the size of the screen, the start size is never undercut"""
        self.root.update_idletasks()
        scaling = self.root._get_window_scaling()  # pylint: disable=protected-access
        start_w, start_h = (int(v) for v in self.wsize.split("+")[0].split("x"))
        # menu bar, title bar and scrollbar around the content
        need_w = self.content_frame.winfo_reqwidth() / scaling + 50
        need_h = self.content_frame.winfo_reqheight() / scaling + 100
        max_w = self.root.winfo_screenwidth() / scaling * 0.95
        max_h = self.root.winfo_screenheight() / scaling * 0.9
        width = int(max(start_w, min(need_w, max_w)))
        height = int(max(start_h, min(need_h, max_h)))
        self.root.geometry(f"{width}x{height}")

    def loop(self):
        """
        run main loop of tk.window
        """
        self.fit_window()
        self.root.mainloop()
