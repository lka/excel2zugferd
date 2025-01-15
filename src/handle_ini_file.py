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
                    self._modify_entries_to_version2()
            except IOError:
                return ()
        return self.content

# should be eliminated in Version 1.0.0

    def _normalize(self, arr_in: list) -> list:
        """remove empty elements of array"""
        return list(filter(None, arr_in))

    def _set_tel_fax_email(self, sub: list) -> None:
        if 'Tel' in sub[0]:
            self.content["Telefon"] = sub[1]
        elif 'Fax' in sub[0]:
            self.content["Fax"] = sub[1]
        elif 'Email' in sub[0] or 'E-Mail' in sub[0]:
            self.content["Email"] = sub[1]

    def _replace_kontakt(self, keys: list):
        if "Kontakt" not in keys:
            return
        arr = self._normalize(self.content["Kontakt"].splitlines())
        for elem in arr:
            sub = self._normalize(elem.split())
            self._set_tel_fax_email(sub)
        del self.content["Kontakt"]

    def _set_Steuer(self, sub: list) -> None:
        if 'Steuernummer' in sub[0]:
            self.content["Steuernummer"] = sub[1]
        if 'Finanzamt' in sub[0]:
            self.content["Finanzamt"] = sub[1]
        if 'UmsatzsteuerID' in sub[0]:
            self.content["UmsatzsteuerID"] = sub[1]

    def _replace_umsatzsteuer(self, keys: list) -> None:
        if "Umsatzsteuer" not in keys:
            return
        arr = self._normalize(self.content["Umsatzsteuer"].splitlines())
        for elem in arr:
            sub = self._normalize(elem.split(' ', 1))
            self._set_Steuer(sub)
        del self.content["Umsatzsteuer"]

    def _replace_konto(self, keys: list):
        if "Konto" not in keys:
            return
        arr = self._normalize(self.content["Konto"].splitlines())
        self.content["Kontoinhaber"] = arr[0]
        for elem in arr[1:]:
            sub = self._normalize(elem.split(' ', 1))
            if 'IBAN' in sub[0]:
                self.content["IBAN"] = sub[1]
            elif 'BIC' in sub[0]:
                self.content["BIC"] = sub[1]
        del self.content["Konto"]

    def _fill_str_hnr(self, strasse):
        if 'Postfach' in strasse:
            self.content["Postfach"] = strasse
        else:
            sub = self._normalize(strasse.rsplit(' ', 1))
            self.content["Strasse"] = sub[0]
            if len(sub) == 2:
                self.content["Hausnummer"] = sub[1]

    def _fill_plz_ort(self, ort):
        sub = self._normalize(ort.split(' ', 1))
        self.content["PLZ"] = sub[0]
        if len(sub) == 2:
            self.content["Ort"] = sub[1]

    def _replace_anschrift(self, keys: list) -> None:
        if "Anschrift" not in keys:
            return
        arr = self._normalize(self.content["Anschrift"].splitlines())
        # self.content["Betriebsbezeichnung"] = arr[0]
        if len(arr) == 5:
            self.content["Abteilung"] = arr[2]
            self.content["Ansprechpartner"] = arr[1]
        elif len(arr) == 4:
            self.content["Abteilung"] = arr[1]
        self._fill_str_hnr(arr[-2])
        self._fill_plz_ort(arr[-1])
        del self.content["Anschrift"]

    def _replace_name(self, keys: list):
        if "Name" not in keys:
            return
        self.content["Ansprechpartner"] = self.content["Name"]
        del self.content["Name"]

    def _modify_entries_to_version2(self) -> None:
        """Modify entries from first Version to Version 2"""
        keys = self.content.keys()
        self._replace_kontakt(keys)
        self._replace_umsatzsteuer(keys)
        self._replace_konto(keys)
        self._replace_name(keys)
        self._replace_anschrift(keys)
