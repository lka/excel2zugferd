"""
Modul Konto
"""
from src.constants import KONTO_ERROR
import src


class Konto(object):
    """
    Class for Girokonto
    """
    def __init__(self) -> None:
        self._name = None
        self._iban = None
        self._bic = None

    def __repr__(self) -> str:
        return f"(Kontoinhaber) name: '{self.name}', iban: '{self.iban}',\
 bic: '{self.bic}')"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def iban(self):
        return self._iban

    @iban.setter
    def iban(self, value):
        self._iban = value

    @property
    def bic(self):
        return self._bic

    @bic.setter
    def bic(self, value):
        self._bic = value

    def oneliner(self) -> str:
        """get Konto Information as One Line"""
        return self.name + ', IBAN: ' + self.iban + ', BIC: ' + self.bic

    def multiliner(self) -> str:
        """get Konto Information as Multi Lines"""
        return self.name + '\nIBAN: ' + self.iban + '\nBIC: ' + self.bic

    # def _fill_iban_bic(self, key: str, value: str) -> None:
    #     if len(value) == 0:
    #         raise ValueError(KONTO_ERROR)
    #     if 'IBAN' in key:
    #         self.iban = value
    #     elif 'BIC' in key:
    #         self.bic = value
    #     else:
    #         raise ValueError(KONTO_ERROR)

    # def _search_iban_bic(self, arr: list) -> None:
    #     for elem in arr[1:]:
    #         sub = _normalize(elem.split(' ', 1))
    #         if len(sub) != 2:
    #             raise ValueError(KONTO_ERROR)
    #         else:
    #             self._fill_iban_bic(sub[0], sub[1])

    def _check_konto(self) -> None:
        """raise ValueError on failure"""
        if self.name and self.iban and self.bic:
            return
        raise ValueError(KONTO_ERROR)

    def fill_konto(self, daten: dict = None, keys: list = None) -> None:
        """fills Konto of Lieferant from stammdaten"""
        if daten:
            # print("fill_konto:", daten)
            if "Kontoinhaber" in keys:
                self.name = src._setNoneIfEmpty(daten["Kontoinhaber"])
            if "IBAN" in keys:
                self.iban = src._setNoneIfEmpty(daten["IBAN"])
            if "BIC" in keys:
                self.bic = src._setNoneIfEmpty(daten["BIC"])
            self._check_konto()
        # print(repr(self))
