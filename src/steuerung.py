"""
Module Invoice
"""


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
