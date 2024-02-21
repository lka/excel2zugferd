import os
import json


class IniFile:
    def __init__(self, filename, directory):
        self.fn = filename
        self.dir = directory
        self.path = os.path.join(self.dir, self.fn)
        self.content = None

    def existsIniFile(self):
        try:
            with open(self.path) as file:
                return file
        except Exception as e:
            return None

    def createIniFile(self, content):
        self.content = content
        with open(self.path, 'w', encoding='utf-8') as f_out:
            json.dump(content, f_out, sort_keys=True, ensure_ascii=False, indent=4)

    def readIniFile(self):
        if self.content is None:
            try:
                with open(self.path, 'r', encoding='utf-8') as f_in:
                    self.content = json.load(f_in)
            except:
                return ()
        return self.content
