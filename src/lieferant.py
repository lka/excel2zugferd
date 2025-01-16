"""
Module Lieferant
"""

from src import _setNoneIfEmpty
from datetime import datetime, timedelta
from src.adresse import Adresse
from src import STEUERSATZ_ERR_MSG, BETRIEB_ERROR, NAME_ERROR


class Lieferant(Adresse):

    def __init__(self):
        super().__init__()

    @property
    def kontakt(self) -> str:
        return '\n'.join(
            filter(None,
                   [
                        'Tel.: ' + self.telefon if self.telefon else None,
                        'Fax: ' + self.fax if self.fax else None,
                        'E-Mail: ' + self.email if self.email else None,
                   ])
        )

    # @kontakt.setter
    # def kontakt(self, arr: list) -> None:
    #     for elem in arr:
    #         sub = _normalize(elem.split())
    #         if len(sub) != 2:
    #             raise ValueError(KONTAKT_ERROR)
    #         else:
    #             self._fill_tel_fax_email(elem, sub[1])

    @property
    def umsatzsteuer(self) -> str:
        return '\n'.join(
            filter(None,
                   [
                       ('Steuernummer: ' + self.steuernr)
                       if self.steuernr else None,
                       ('Finanzamt: ' + self.finanzamt)
                       if self.steuernr and self.finanzamt else None,
                       ('Umsatzsteuer-ID: ' + self.steuerid)
                       if self.steuerid else None,
                   ])
        )

    # @umsatzsteuer.setter
    # def umsatzsteuer(self, arr: list) -> None:
    #     if len(arr) > 2:
    #         raise ValueError(USTID_ERROR)
    #     sub = _normalize(arr[0].split())
    #     if len(sub) != 2:
    #         raise ValueError(USTID_ERROR)
    #     self._fill_umsatzsteuer_or_id(arr, sub)

    def _fill_Betrieb_Abteilung_Ansprechpartner(self, daten: dict, keys: list)\
            -> None:
        """use it for Stammdaten only"""
        if "Betriebsbezeichnung" in keys:
            self.betriebsbezeichnung = _setNoneIfEmpty(
                daten["Betriebsbezeichnung"])
        if "Abteilung" in keys:
            self.adresszusatz = _setNoneIfEmpty(daten["Abteilung"])
        if "Ansprechpartner" in keys:
            self.name = _setNoneIfEmpty(daten["Ansprechpartner"])

    def _fill_Postfach_Strasse_Hausnummer(self, daten: dict, keys: list)\
            -> None:
        """use it for Stammdaten only"""
        if "Postfach" in keys:
            self.postfach = _setNoneIfEmpty(daten["Postfach"])
        if "Strasse" in keys:
            self.strasse = _setNoneIfEmpty(daten["Strasse"])
        if "Hausnummer" in keys:
            self.hausnummer = _setNoneIfEmpty(daten["Hausnummer"])

    def _fill_PLZ_Ort(self, daten: dict, keys: list) -> None:
        """use it for Stammdaten only"""
        if "PLZ" in keys:
            self.plz = _setNoneIfEmpty(daten["PLZ"])
        if "Ort" in keys:
            self.ort = _setNoneIfEmpty(daten["Ort"])

    def _fill_anschrift(self, daten: dict, keys: list = None):
        """use it for Stammdaten only"""
        self._fill_Betrieb_Abteilung_Ansprechpartner(daten, keys)
        self._fill_Postfach_Strasse_Hausnummer(daten, keys)
        self._fill_PLZ_Ort(daten, keys)
        self._check_anschrift()

    def _fill_kontakt(self, daten: list, keys: list) -> None:
        """use it for Stammdaten only"""
        if "Telefon" in keys:
            self.telefon = _setNoneIfEmpty(daten["Telefon"])
        if "Fax" in keys:
            self.fax = _setNoneIfEmpty(daten["Fax"])
        if "Email" in keys:
            self.email = _setNoneIfEmpty(daten["Email"])
            self._check_kontakt()

    def _fill_umsatzsteuer(self, daten: dict, keys: list) -> None:
        """use it for Stammdaten only"""
        if "Steuernummer" in keys:
            self.steuernr = _setNoneIfEmpty(daten["Steuernummer"])
        if "Finanzamt" in keys:
            self.finanzamt = _setNoneIfEmpty(daten["Finanzamt"])
        if "UmsatzsteuerID" in keys:
            self.steuerid = _setNoneIfEmpty(daten["UmsatzsteuerID"])
            if self.steuerid is not None:
                self.finanzamt = None
                self.steuernr = None
        self._check_umsatzsteuer()

    def _fill_steuersatz(self, daten: list) -> None:
        """use it for Stammdaten only"""
        # print(daten)
        if "Steuersatz" not in daten.keys() or daten["Steuersatz"] is None\
                or len(daten["Steuersatz"]) == 0:
            # print('Steuersatz:', hasattr(daten, "Steuersatz"))
            self.steuersatz = "19.00"
        else:
            try:
                value = float(daten["Steuersatz"].strip())
            except Exception as ve:
                raise ValueError(STEUERSATZ_ERR_MSG, ve)
            self.steuersatz = f"{value:.2f}"

    def _fill_betrieb(self, daten):
        """use it for Stammdaten only"""
        self.betriebsbezeichnung = _setNoneIfEmpty(
            daten['Betriebsbezeichnung'])
        if not self.betriebsbezeichnung:
            raise ValueError(BETRIEB_ERROR)

    def _fill_name(self, daten: dict, keys: list) -> None:
        """use it for Stammdaten only"""
        if "Ansprechpartner" in keys:
            self.name = _setNoneIfEmpty(daten["Ansprechpartner"])
        if not self.name:
            raise ValueError(NAME_ERROR)

    def _fill_zahlungsziel(self, daten):
        """use it for Stammdaten only"""
        ziel = daten["Zahlungsziel"]
        if ziel is not None and len(ziel) > 0 and\
                '\n' not in ziel:
            self.zahlungsziel = ziel
        else:
            self.zahlungsziel = "14"

    def fill_lieferant(self, daten: dict = None) -> None:
        """fills Adresse of Lieferant from stammdaten"""
        if daten:
            keys = daten.keys()
            self._fill_betrieb(daten)
            # self._fill_name(daten, keys)
            self._fill_anschrift(daten, keys)
            self.bundesland = daten["Bundesland"]
            self._fill_kontakt(daten, keys)
            self._fill_umsatzsteuer(daten, keys)
            self._fill_zahlungsziel(daten)
            self._fill_steuersatz(daten)
            # print(repr(self))

    def get_ueberweisungsdatum(self) -> datetime:
        return (
            datetime.now()
            + timedelta(
                days=int(
                    self.zahlungsziel
                    if self.zahlungsziel > ""
                    else "0"
                )
            )
        )
