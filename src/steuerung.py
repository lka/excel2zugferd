"""
Module Invoice
"""

from src.constants import (
    ANSCHRIFT_POS_ERROR,
    RECHNUNG_POS_ERROR,
    RECHNUNGSDATUM_POS_ERROR,
    NETTOSUMME_POS_ERROR,
    MWSTSUMME_POS_ERROR,
    BRUTTOSUMME_POS_ERROR,
    EINZELPOSITIONEN_POS_ERR,
)


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
        self._pdf_filename = None
        self._directory = None
        self._anschrift_spalte = None
        self._anschrift_zeile = None
        self._rechnung_spalte = None
        self._rechnung_zeile = None
        self._nettosumme_spalte = None
        self._nettosumme_zeile = None
        self._mwstsumme_spalte = None
        self._mwstsumme_zeile = None
        self._bruttosumme_spalte = None
        self._bruttosumme_zeile = None
        self._positionen_zeile = None
        self._pos_spalte = None
        self._dat_spalte = None
        self._desc_spalte = None
        self._anz_spalte = None
        self._typ_spalte = None
        self._preis_spalte = None
        self._sum_spalte = None

    def __repr__(self) -> str:
        return f"Steuerung(create_xml: '{self.create_xml}', \
 create_girocode: '{self.create_girocode}',\
 is_kleinunternehmen: '{self.is_kleinunternehmen}', abspann: '{self.abspann}',\
 BYOPdf: '{self.BYOPdf}',\
 pdf_filename: '{self.pdf_filename}',\
 directory: '{self.directory}',\
 anschrift_spalte: '{self.anschrift_spalte}',\
 anschrift_zeile: '{self.anschrift_zeile}'\
 rechnung_spalte: '{self.rechnung_spalte}',\
 rechnung_zeile: '{self.rechnung_zeile}'\
 nettosumme_spalte: '{self.nettosumme_spalte}',\
 nettosumme_zeile: '{self.nettosumme_zeile}'\
 mwstsumme_spalte: '{self.mwstsumme_spalte}',\
 mwstsumme_zeile: '{self.mwstsumme_zeile}'\
 positionen_zeile: '{self.positionen_zeile}'\
 pos_spalte: '{self.pos_spalte}'\
 dat_spalte: '{self.dat_spalte}'\
 desc_spalte: '{self.desc_spalte}'\
 anz_spalte: '{self.anz_spalte}'\
 typ_spalte: '{self.typ_spalte}'\
 preis_spalte: '{self.preis_spalte}'\
 sum_spalte: '{self.sum_spalte}'\
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
    def pdf_filename(self):
        return self._pdf_filename

    @pdf_filename.setter
    def pdf_filename(self, value):
        self._pdf_filename = value

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        self._directory = value

    @property
    def anschrift_spalte(self):
        return self._anschrift_spalte

    @anschrift_spalte.setter
    def anschrift_spalte(self, value):
        self._anschrift_spalte = value

    @property
    def anschrift_zeile(self):
        return self._anschrift_zeile

    @anschrift_zeile.setter
    def anschrift_zeile(self, value):
        self._anschrift_zeile = value

    @property
    def rechnung_spalte(self):
        return self._rechnung_spalte

    @rechnung_spalte.setter
    def rechnung_spalte(self, value):
        self._rechnung_spalte = value

    @property
    def rechnung_zeile(self):
        return self._rechnung_zeile

    @rechnung_zeile.setter
    def rechnung_zeile(self, value):
        self._rechnung_zeile = value

    @property
    def nettosumme_spalte(self):
        return self._nettosumme_spalte

    @nettosumme_spalte.setter
    def nettosumme_spalte(self, value):
        self._nettosumme_spalte = value

    @property
    def nettosumme_zeile(self):
        return self._nettosumme_zeile

    @nettosumme_zeile.setter
    def nettosumme_zeile(self, value):
        self._nettosumme_zeile = value

    @property
    def mwstsumme_spalte(self):
        return self._mwstsumme_spalte

    @mwstsumme_spalte.setter
    def mwstsumme_spalte(self, value):
        self._mwstsumme_spalte = value

    @property
    def mwstsumme_zeile(self):
        return self._mwstsumme_zeile

    @mwstsumme_zeile.setter
    def mwstsumme_zeile(self, value):
        self._mwstsumme_zeile = value

    @property
    def positionen_zeile(self):
        return self._positionen_zeile

    @positionen_zeile.setter
    def positionen_zeile(self, value):
        self._positionen_zeile = value

    @property
    def pos_spalte(self):
        return self._pos_spalte

    @pos_spalte.setter
    def pos_spalte(self, value):
        self._pos_spalte = value

    @property
    def dat_spalte(self):
        return self._dat_spalte

    @dat_spalte.setter
    def dat_spalte(self, value):
        self._dat_spalte = value

    @property
    def desc_spalte(self):
        return self._desc_spalte

    @desc_spalte.setter
    def desc_spalte(self, value):
        self._desc_spalte = value

    @property
    def anz_spalte(self):
        return self._anz_spalte

    @anz_spalte.setter
    def anz_spalte(self, value):
        self._anz_spalte = value

    @property
    def typ_spalte(self):
        return self._typ_spalte

    @typ_spalte.setter
    def typ_spalte(self, value):
        self._typ_spalte = value

    @property
    def preis_spalte(self):
        return self._preis_spalte

    @preis_spalte.setter
    def preis_spalte(self, value):
        self._preis_spalte = value

    @property
    def sum_spalte(self):
        return self._sum_spalte

    @sum_spalte.setter
    def sum_spalte(self, value):
        self._sum_spalte = value

    def _check_TrueFalse(self, thekeys: list, daten: dict, name: str) -> bool:
        return (
            (daten[name] == "Ja")
            if name in thekeys and daten[name] is not None
            else False
        )

    def _fill_bools(self, thekeys: list, daten: dict) -> None:
        self.create_girocode = self._check_TrueFalse(thekeys, daten, "GiroCode")
        self.create_xml = self._check_TrueFalse(thekeys, daten, "ZugFeRD")
        self.is_kleinunternehmen = self._check_TrueFalse(
            thekeys, daten, "Kleinunternehmen"
        )
        self.BYOPdf = self._check_TrueFalse(thekeys, daten, "BYOPdf")

    def _check_is_integer(self, thekeys: list, daten: dict, name: str) -> str | None:
        """
        Check whether content of name is int, if yes return str else None
        """
        if name not in thekeys:
            return None
        if not daten[name].strip().isdigit():
            if not daten[name] == "":
                raise ValueError(f"{name} muss ein Integer sein.")
            return None
        return daten[name]

    def _check_is_upper(self, thekeys: list, daten: dict, name: str) -> str | None:
        """
        Check whether content of name is UpperCase character,
        if yes return str[0] else None
        """
        if name not in thekeys:
            return None
        if not daten[name].strip().isupper():
            if not daten[name] == "":
                raise ValueError(f"{name} muss ein Grossbuchstabe sein sein.")
            return None
        return daten[name][0]

    def _check_anschrift_position(self) -> None:
        """raise ValueError on Failure"""
        if (self.anschrift_zeile is not None and self.anschrift_spalte is None) or (
            self.anschrift_zeile is None and self.anschrift_spalte is not None
        ):
            raise ValueError(ANSCHRIFT_POS_ERROR)

    def _fill_and_check_anschrift(self, theKeys: list, daten: dict) -> None:
        self.anschrift_zeile = self._check_is_integer(theKeys, daten, "AnschriftZeile")
        self.anschrift_spalte = self._check_is_upper(theKeys, daten, "AnschriftSpalte")
        self._check_anschrift_position()

    def _check_rechnungsdatum_position(self) -> None:
        """raise ValueError on Failure"""
        if (self.datum_zeile is not None and self.datum_spalte is None) or (
            self.datum_zeile is None and self.datum_spalte is not None
        ):
            raise ValueError(RECHNUNGSDATUM_POS_ERROR)

    def _fill_and_check_rechnungsdatum(self, theKeys: list, daten: dict) -> None:
        self.datum_zeile = self._check_is_integer(theKeys, daten, "RGDatumZeile")
        self.datum_spalte = self._check_is_upper(theKeys, daten, "RGDatumSpalte")
        self._check_rechnungsdatum_position()

    def _check_rechnung_position(self) -> None:
        """raise ValueError on Failure"""
        if (self.rechnung_zeile is not None and self.rechnung_spalte is None) or (
            self.rechnung_zeile is None and self.rechnung_spalte is not None
        ):
            raise ValueError(RECHNUNG_POS_ERROR)

    def _fill_and_check_rechnungsnummer(self, theKeys: list, daten: dict) -> None:
        self.rechnung_zeile = self._check_is_integer(theKeys, daten, "RechnungZeile")
        self.rechnung_spalte = self._check_is_upper(theKeys, daten, "RechnungSpalte")
        self._check_rechnung_position()

    def _check_nettosumme_position(self) -> None:
        """raise ValueError on Failure"""
        if (self.nettosumme_zeile is not None and self.nettosumme_spalte is None) or (
            self.nettosumme_zeile is None and self.nettosumme_spalte is not None
        ):
            raise ValueError(NETTOSUMME_POS_ERROR)

    def _fill_and_check_nettosumme(self, theKeys: list, daten: dict) -> None:
        self.nettosumme_zeile = self._check_is_integer(
            theKeys, daten, "NettosummeZeile"
        )
        self.nettosumme_spalte = self._check_is_upper(
            theKeys, daten, "NettosummeSpalte"
        )
        self._check_nettosumme_position()

    def _check_mwstsumme_position(self) -> None:
        """raise ValueError on Failure"""
        if (self.mwstsumme_zeile is not None and self.mwstsumme_spalte is None) or (
            self.mwstsumme_zeile is None and self.mwstsumme_spalte is not None
        ):
            raise ValueError(MWSTSUMME_POS_ERROR)

    def _fill_and_check_mwstsumme(self, theKeys: list, daten: dict) -> None:
        self.mwstsumme_zeile = self._check_is_integer(theKeys, daten, "MWStsummeZeile")
        self.mwstsumme_spalte = self._check_is_upper(theKeys, daten, "MWStsummeSpalte")
        self._check_mwstsumme_position()

    def _check_bruttosumme_position(self) -> None:
        """raise ValueError on Failure"""
        if (self.bruttosumme_zeile is not None and self.bruttosumme_spalte is None) or (
            self.bruttosumme_zeile is None and self.bruttosumme_spalte is not None
        ):
            raise ValueError(BRUTTOSUMME_POS_ERROR)

    def _fill_and_check_bruttosumme(self, theKeys: list, daten: dict) -> None:
        self.bruttosumme_zeile = self._check_is_integer(
            theKeys, daten, "BruttosummeZeile"
        )
        self.bruttosumme_spalte = self._check_is_upper(
            theKeys, daten, "BruttosummeSpalte"
        )
        self._check_bruttosumme_position()

    def _get_einzelpositionen_values(self) -> list:
        return [
            self.positionen_zeile,
            self.pos_spalte,
            self.dat_spalte,
            self.desc_spalte,
            self.anz_spalte,
            self.typ_spalte,
            self.preis_spalte,
            self.sum_spalte,
        ]

    def _check_fields(self) -> list:
        allAreNone = True
        allAreNotNone = True
        for field in self._get_einzelpositionen_values():
            allAreNone = allAreNone and field is None
            allAreNotNone = allAreNotNone and field is not None
            # print("field, all, some\n", field, allAreNone, allAreNotNone)
        return [allAreNone, allAreNotNone]

    def _check_einzelpositionen(self) -> None:
        """raise ValueError on Failure"""
        allAreNone, allAreNotNone = self._check_fields()
        if not (allAreNone or allAreNotNone):
            raise ValueError(EINZELPOSITIONEN_POS_ERR)

    def _fill_and_check_einzelpositionen(self, thekeys: list, daten: dict) -> None:
        self.positionen_zeile = self._check_is_integer(
            thekeys, daten, "PositionenZeile"
        )
        self.pos_spalte = self._check_is_upper(thekeys, daten, "PosSpalte")
        self.dat_spalte = self._check_is_upper(thekeys, daten, "DatSpalte")
        self.desc_spalte = self._check_is_upper(thekeys, daten, "DescSpalte")
        self.anz_spalte = self._check_is_upper(thekeys, daten, "AnzSpalte")
        self.typ_spalte = self._check_is_upper(thekeys, daten, "TypSpalte")
        self.preis_spalte = self._check_is_upper(thekeys, daten, "PreisSpalte")
        self.sum_spalte = self._check_is_upper(thekeys, daten, "SumSpalte")
        self._check_einzelpositionen()

    def _fill_positions_for_excel(self, theKeys: list, daten: dict) -> None:
        self._fill_and_check_anschrift(theKeys, daten)
        self._fill_and_check_rechnungsnummer(theKeys, daten)
        self._fill_and_check_rechnungsdatum(theKeys, daten)
        self._fill_and_check_nettosumme(theKeys, daten)
        self._fill_and_check_mwstsumme(theKeys, daten)
        self._fill_and_check_bruttosumme(theKeys, daten)
        self._fill_and_check_einzelpositionen(theKeys, daten)

    def fill_steuerung(self, daten: dict = None) -> None:
        """fills Steuerung of Lieferant from stammdaten"""
        if daten:
            thekeys = daten.keys()
            self.abspann = daten["Abspann"] if "Abspann" in thekeys else None
            self._fill_bools(thekeys, daten)
            self._fill_positions_for_excel(thekeys, daten)
            self.directory = daten["Verzeichnis"] if "Verzeichnis" in thekeys else None
            # print(repr(self))
