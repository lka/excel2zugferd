"""
Module handle_ini_file
"""
import os
import json


class IniFile:
    """
    Class IniFile
    """
    def __init__(self, filename, directory):
        self.fn = filename
        self.dir = directory
        self.path = os.path.join(self.dir, self.fn)
        self.content = None

    def exists_ini_file(self):
        """
        test whether iniFile exists
        """
        try:
            with open(self.path, encoding="utf-8") as file:
                return file
        except IOError:
            return None

    def create_ini_file(self, content):
        """
        create IniFile
        """
        self.content = content
        with open(self.path, 'w', encoding='utf-8') as f_out:
            json.dump(content, f_out, sort_keys=True, ensure_ascii=False,
                      indent=4)

    def read_ini_file(self):
        """
        read IniFile
        """
        if self.content is None:
            try:
                with open(self.path, 'r', encoding='utf-8') as f_in:
                    self.content = json.load(f_in)
            except IOError:
                return ()
        return self.content
