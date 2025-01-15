"""
Module handles Classes Adresse, Konto, Steuerung and Invoice
"""

import pandas as pd
from src.lieferant import Lieferant
from src.kunde import Kunde
from src import _setNoneIfEmpty, KONTO_ERROR


class Konto(object):
    """
    Class for Girokonto
    """
    def __init__(self) -> None:
        self._name = None
        self._iban = None
        self._bic = None

    def __repr__(self) -> str:
        return f"Kontoinhaber: '{self.name}', iban: '{self.iban}',\
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
                self.name = _setNoneIfEmpty(daten["Kontoinhaber"])
            if "IBAN" in keys:
                self.iban = _setNoneIfEmpty(daten["IBAN"])
            if "BIC" in keys:
                self.bic = _setNoneIfEmpty(daten["BIC"])
            self._check_konto()
        # print(repr(self))


class Steuerung(object):
    """
    Steuerung der PDF Erzeugung durch die Stammdaten
    """
    def __init__(self) -> None:
        self._create_xml = None
        self._create_girocode = None
        self._is_kleinunternehmen = None
        self._abspann = None
        self._BYOPdf = None
        self._directory = None

    def __repr__(self) -> str:
        return f"Steuerung(create_xml: '{self.create_xml}', \
 create_girocode: '{self.create_girocode}',\
 is_kleinunternehmen: '{self.is_kleinunternehmen}', abspann: '{self.abspann}',\
 BYOPdf: '{self.BYOPdf}'\
 directory: '{self.directory}'\
)"

    @property
    def create_xml(self):
        return self._create_xml

    @create_xml.setter
    def create_xml(self, value):
        self._create_xml = value

    @property
    def create_girocode(self):
        return self._create_girocode

    @create_girocode.setter
    def create_girocode(self, value):
        self._create_girocode = value

    @property
    def is_kleinunternehmen(self):
        return self._is_kleinunternehmen

    @is_kleinunternehmen.setter
    def is_kleinunternehmen(self, value):
        self._is_kleinunternehmen = value

    @property
    def abspann(self):
        return self._abspann

    @abspann.setter
    def abspann(self, value):
        self._abspann = value

    @property
    def BYOPdf(self):
        return self._BYOPdf

    @BYOPdf.setter
    def BYOPdf(self, value):
        self._BYOPdf = value

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        self._directory = value

    def _check_TrueFalse(self, thekeys: list, daten: dict, name: str) -> bool:
        return (
            (daten[name] == "Ja")
            if name in thekeys and
            daten[name] is not None else False
        )

    def _fill_bools(self, thekeys: list, daten: dict) -> None:
        self.create_girocode = self._check_TrueFalse(thekeys,
                                                     daten,
                                                     "GiroCode")
        self.create_xml = self._check_TrueFalse(thekeys,
                                                daten,
                                                "ZugFeRD")
        self.is_kleinunternehmen = self._check_TrueFalse(thekeys,
                                                         daten,
                                                         "Kleinunternehmen")
        self.BYOPdf = self._check_TrueFalse(thekeys,
                                            daten,
                                            "BYOPdf")

    def fill_steuerung(self, daten: dict = None) -> None:
        """fills Steuerung of Lieferant from stammdaten"""
        if daten:
            thekeys = daten.keys()
            self.abspann = (
                daten["Abspann"] if "Abspann" in thekeys else None
            )
            self._fill_bools(thekeys, daten)
            self.directory = daten['Verzeichnis']
            # print(repr(self))


class Invoice(object):
    """Class Invoice handles collected data for invoice"""
    def __init__(self) -> None:
        self._customer: Kunde = None
        self._supplier: Lieferant = None
        self._supplier_account: Konto = None
        self._positions: pd.DataFrame = None
        self._invoicenr: dict = None
        self._sums: list = None
        self._management: Steuerung = None

    def __repr__(self) -> str:
        return f"Invoice: customer: '{repr(self.customer)}',\
 supplier: '{repr(self.supplier)}',\
 supplier_account: '{repr(self.supplier_account)}',\
 positions: '{self.positions}',\
 invoicenr: '{self.invoicenr}',\
 sums '{self.sums}'\
 management: '{repr(self.management)}'"

    @property
    def customer(self) -> Kunde:
        return self._customer

    @customer.setter
    def customer(self, value: Kunde) -> None:
        self._customer = value

    @property
    def supplier(self) -> Lieferant:
        return self._supplier

    @supplier.setter
    def supplier(self, value: Lieferant) -> None:
        self._supplier = value

    @property
    def supplier_account(self) -> Konto:
        return self._supplier_account

    @supplier_account.setter
    def supplier_account(self, value: Konto) -> None:
        self._supplier_account = value

    @property
    def positions(self) -> pd.DataFrame:
        return self._positions

    @positions.setter
    def positions(self, value: pd.DataFrame) -> None:
        self._positions = value

    @property
    def invoicenr(self) -> dict:
        return self._invoicenr

    @invoicenr.setter
    def invoicenr(self, value: dict) -> None:
        self._invoicenr = value

    @property
    def sums(self) -> list:
        return self._sums

    @sums.setter
    def sums(self, value: list) -> None:
        self._sums = value

    @property
    def management(self) -> Steuerung:
        return self._management

    @management.setter
    def management(self, value: Steuerung) -> None:
        self._management = value
