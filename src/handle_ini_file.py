"""
Module handle_ini_file
"""

import os
import json
from pathlib import Path

from src.stammdaten import COMPANY_PROFILE_KEYS


COMPANY_STORE_KEY = "Firmen"
ACTIVE_COMPANY_KEY = "AktiveFirma"
COMPANY_PROFILE_SCHEMA = "excel2zugferd-company-profile-v1"


class IniFile:
    """
    Class IniFile
        reads ini_file and stores it to self.content()\n
        returns self.content on read_ini_file()\n
        updates self.content on create_ini_file(new_content)\n
        and merge_content_of_ini_file(new_content)
    """

    def __init__(self, path_to_inifile: str = None, dir: Path = None):
        self.fn: str = "config.ini"
        self.dir: Path = (
            dir
            if dir is not None
            else Path.joinpath(
                Path(os.getenv("APPDATA")).resolve(), Path("excel2zugferd")
            )
        )
        self.path: str = path_to_inifile
        self.content: dict = {}
        if self.path is None:
            self._create_inifile_directory()
        if self.exists_ini_file() is not None:
            self.read_ini_file()

    def _create_inifile_directory(self) -> None:
        if not Path.exists(self.dir):
            try:
                os.mkdir(self.dir)
            except OSError as e:
                msg = f"Ich kann das Verzeichnis \
{self.dir} nicht erstellen.\n{e}"
                raise ValueError(msg)
        self.path = os.path.join(self.dir, self.fn)

    def exists_ini_file(self):
        """
        test whether iniFile exists;
        returns None if not
        """
        try:
            with open(self.path, encoding="utf-8") as file:
                return file
        except OSError:
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
        with open(self.path, "w", encoding="utf-8") as f_out:
            json.dump(self.content, f_out, sort_keys=True, ensure_ascii=False, indent=4)

    def set_default_content(self) -> dict:
        return {
            "Ansprechpartner": "Max Mustermann",
            "BIC": "XYZBCAY",
            "Betriebsbezeichnung": "Max Mustermann - Software",
            "Finanzamt": "Musterstadt",
            "Hausnummer": "17a",
            "IBAN": "DEXX YYYY ZZZZ AAAA BBBB CC",
            "Kontoinhaber": "Max Mustermann",
            "Ort": "Musterstadt",
            "PLZ": "12345",
            "Steuernummer": "12345/12345",
            "Strasse": "Musterstr.",
            "Telefon": "01234-5678",
            "ZugFeRD": "Ja",
        }

    def read_ini_file(self) -> dict:
        """
        read IniFile
        """
        if not self.content:
            try:
                with open(self.path, "r", encoding="utf-8") as f_in:
                    self.content = json.load(f_in)
                    self._modify_entries_to_version2()  # noqa E501 should be eliminated in Version 1.0.0
            except OSError:
                return {}
        return self.content

    def _get_documents_directory(self):
        doc_dir = Path.home()
        if Path(Path.joinpath(doc_dir, "Documents")).is_dir():
            doc_dir = Path.joinpath(doc_dir, "Documents")
        return doc_dir

    def get_working_directory(self) -> Path:
        """get the working directory"""
        return (
            Path(self.content["Verzeichnis"])
            if (
                self.content
                and "Verzeichnis" in self.content
                and len(self.content["Verzeichnis"]) > 0
            )
            else self._get_documents_directory()
        )

    def _get_company_store(self) -> dict:
        store = self.content.get(COMPANY_STORE_KEY) if isinstance(self.content, dict) else {}
        return store if isinstance(store, dict) else {}

    def _get_shared_content(self) -> dict:
        return {
            key: value
            for key, value in self.content.items()
            if key not in COMPANY_PROFILE_KEYS
            and key not in [COMPANY_STORE_KEY, ACTIVE_COMPANY_KEY]
        }

    def _sanitize_company_content(self, company_content: dict) -> dict:
        if not isinstance(company_content, dict):
            raise ValueError("Die Firmendaten haben ein ungültiges Format.")
        return {
            key: value
            for key, value in company_content.items()
            if key in COMPANY_PROFILE_KEYS
        }

    def _set_profile_content(self, company_store: dict, active_name: str) -> None:
        self.content = {
            **self._get_shared_content(),
            **company_store[active_name],
            COMPANY_STORE_KEY: company_store,
            ACTIVE_COMPANY_KEY: active_name,
        }

    def get_company_names(self) -> list:
        return list(self._get_company_store().keys())

    def get_active_company_name(self) -> str | None:
        active_name = self.content.get(ACTIVE_COMPANY_KEY)
        if active_name in self._get_company_store():
            return active_name
        names = self.get_company_names()
        return names[0] if names else None

    def _clean_company_name(self, company_name: str) -> str:
        name = (company_name or "").strip()
        if not name:
            raise ValueError("Der Firmenname darf nicht leer sein.")
        return name

    def get_active_company_content(self) -> dict:
        active_name = self.get_active_company_name()
        company_store = self._get_company_store()
        if active_name and active_name in company_store:
            return {
                **self._get_shared_content(),
                **company_store[active_name],
            }
        return {
            key: value
            for key, value in self.content.items()
            if key not in [COMPANY_STORE_KEY, ACTIVE_COMPANY_KEY]
        }

    def set_active_company(self, company_name: str) -> None:
        company_name = self._clean_company_name(company_name)
        company_store = self._get_company_store()
        if company_name not in company_store:
            raise ValueError(f"Die Firma '{company_name}' ist nicht in den Stammdaten vorhanden.")
        self._set_profile_content(company_store, company_name)

    def save_company(self, company_name: str, company_content: dict) -> None:
        company_name = self._clean_company_name(company_name)
        company_content = self._sanitize_company_content(company_content)
        if not company_content.get("Betriebsbezeichnung"):
            company_content["Betriebsbezeichnung"] = company_name
        company_store = self._get_company_store()
        company_store[company_name] = company_content
        active_name = self.get_active_company_name() or company_name
        if active_name not in company_store:
            active_name = company_name
        self._set_profile_content(company_store, active_name)

    def save_current_company_content(self, company_content: dict) -> None:
        company_content = self._sanitize_company_content(company_content)
        company_name = (
            self.get_active_company_name()
            or company_content.get("Betriebsbezeichnung")
            or "Standard"
        )
        company_name = self._clean_company_name(company_name)
        company_store = self._get_company_store()
        company_store[company_name] = company_content
        self._set_profile_content(company_store, company_name)

    def delete_company(self, company_name: str) -> None:
        company_name = self._clean_company_name(company_name)
        company_store = self._get_company_store()
        if company_name not in company_store:
            raise ValueError(f"Die Firma '{company_name}' ist nicht in den Stammdaten vorhanden.")

        del company_store[company_name]

        if not company_store:
            self.content = self._get_shared_content()
            return

        active_name = self.content.get(ACTIVE_COMPANY_KEY)
        if active_name not in company_store:
            active_name = next(iter(company_store.keys()))

        self._set_profile_content(company_store, active_name)

    def rename_company(self, old_name: str, new_name: str) -> str:
        old_name = self._clean_company_name(old_name)
        new_name = self._clean_company_name(new_name)
        company_store = self._get_company_store()

        if old_name not in company_store:
            raise ValueError(f"Die Firma '{old_name}' ist nicht in den Stammdaten vorhanden.")
        if old_name != new_name and new_name in company_store:
            raise ValueError(f"Die Firma '{new_name}' ist bereits vorhanden.")

        company_store[new_name] = company_store.pop(old_name)

        active_name = self.content.get(ACTIVE_COMPANY_KEY)
        if active_name == old_name:
            active_name = new_name
        if active_name not in company_store:
            active_name = new_name

        self._set_profile_content(company_store, active_name)
        return new_name

    def _get_unique_company_name(self, requested_name: str) -> str:
        name = self._clean_company_name(requested_name)
        company_store = self._get_company_store()
        if name not in company_store:
            return name
        idx = 2
        while f"{name} ({idx})" in company_store:
            idx += 1
        return f"{name} ({idx})"

    def export_company_profile(self, company_name: str, file_path: str) -> None:
        company_name = self._clean_company_name(company_name)
        company_store = self._get_company_store()
        if company_name not in company_store:
            raise ValueError(f"Die Firma '{company_name}' ist nicht in den Stammdaten vorhanden.")

        payload = {
            "schema": COMPANY_PROFILE_SCHEMA,
            "company_name": company_name,
            "company_content": self._sanitize_company_content(
                company_store[company_name]
            ),
        }
        with open(file_path, "w", encoding="utf-8") as f_out:
            json.dump(payload, f_out, sort_keys=True, ensure_ascii=False, indent=4)

    def import_company_profile(self, file_path: str, replace_existing: bool = False) -> str:
        with open(file_path, "r", encoding="utf-8") as f_in:
            payload = json.load(f_in)

        if not isinstance(payload, dict):
            raise ValueError("Das Profil hat ein ungültiges Format.")
        if payload.get("schema") != COMPANY_PROFILE_SCHEMA:
            raise ValueError("Das Profilschema wird nicht unterstützt.")

        requested_name = self._clean_company_name(payload.get("company_name", ""))
        company_content = payload.get("company_content")
        company_content = self._sanitize_company_content(company_content)
        if not company_content:
            raise ValueError("Das Profil enthält keine gültigen Firmendaten.")

        target_name = requested_name
        company_store = self._get_company_store()
        if target_name in company_store and not replace_existing:
            target_name = self._get_unique_company_name(target_name)

        self.save_company(target_name, company_content)
        self.set_active_company(target_name)
        return target_name

    def save_working_directory(self, filename: str = None) -> None:
        directory = os.path.dirname(filename)
        self.create_ini_file({**self.content, "Verzeichnis": directory})

    # should be eliminated in Version 1.0.0

    def _normalize(self, arr_in: list) -> list:
        """remove empty elements of array"""
        return list(filter(None, arr_in))

    def _set_tel_fax_email(self, sub: list) -> None:
        if "Tel" in sub[0]:
            self.content["Telefon"] = sub[1]
        elif "Fax" in sub[0]:
            self.content["Fax"] = sub[1]
        elif "Email" in sub[0] or "E-Mail" in sub[0]:
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
        if "Steuernummer" in sub[0]:
            self.content["Steuernummer"] = sub[1]
        if "Finanzamt" in sub[0]:
            self.content["Finanzamt"] = sub[1]
        if "UmsatzsteuerID" in sub[0]:
            self.content["UmsatzsteuerID"] = sub[1]

    def _replace_umsatzsteuer(self, keys: list) -> None:
        if "Umsatzsteuer" not in keys:
            return
        arr = self._normalize(self.content["Umsatzsteuer"].splitlines())
        for elem in arr:
            sub = self._normalize(elem.split(" ", 1))
            self._set_Steuer(sub)
        del self.content["Umsatzsteuer"]

    def _replace_konto(self, keys: list):
        if "Konto" not in keys:
            return
        arr = self._normalize(self.content["Konto"].splitlines())
        self.content["Kontoinhaber"] = arr[0]
        for elem in arr[1:]:
            sub = self._normalize(elem.split(" ", 1))
            if "IBAN" in sub[0]:
                self.content["IBAN"] = sub[1]
            elif "BIC" in sub[0]:
                self.content["BIC"] = sub[1]
        del self.content["Konto"]

    def _fill_str_hnr(self, strasse):
        if "Postfach" in strasse:
            self.content["Postfach"] = strasse
        else:
            sub = self._normalize(strasse.rsplit(" ", 1))
            self.content["Strasse"] = sub[0]
            if len(sub) == 2:
                self.content["Hausnummer"] = sub[1]

    def _fill_plz_ort(self, ort):
        sub = self._normalize(ort.split(" ", 1))
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
