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
        self.fn: str = filename
        self.dir: str = directory
        self.path: str = os.path.join(self.dir, self.fn)
        self.content: dict = {}

    def exists_ini_file(self):
        """
        test whether iniFile exists;
        returns None if not
        """
        try:
            with open(self.path, encoding="utf-8") as file:
                return file
        except IOError:
            return None

    def merge_content_of_ini_file(self, content: dict = None) -> dict:
        """
        merge the content of the ini_file with new content
        return merged content
        """
        if content:
            self.content = self.content | content
        return self.content

    def create_ini_file(self, content: dict) -> None:
        """
        create IniFile
        """
        self.merge_content_of_ini_file(content)
        with open(self.path, 'w', encoding='utf-8') as f_out:
            json.dump(self.content, f_out, sort_keys=True, ensure_ascii=False,
                      indent=4)

    def read_ini_file(self) -> dict:
        """
        read IniFile
        """
        if not self.content:
            try:
                with open(self.path, 'r', encoding='utf-8') as f_in:
                    self.content = json.load(f_in)
            except IOError:
                return ()
        return self.content
