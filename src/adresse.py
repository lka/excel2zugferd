"""
Modul Adresse
"""

from src.constants import ANSCHRIFT_ERROR, KONTAKT_ERROR, USTID_ERROR


class Adresse(object):
    """Class Adresse"""
    def __init__(self) -> None:
        self._betriebsbezeichnung = None
        self._name = None
        self._anschrift_line1 = None
        self._anschrift_line3 = None
        self._postfach = None
        self._strasse = None
        self._hausnummer = None
        self._adresszusatz = None
        self._plz = None
        self._ort = None
        self._bundesland = None
        self._landeskennz = None
        self._telefon = None
        self._fax = None
        self._email = None
        self._steuernr = None
        self._steuerid = None
        self._finanzamt = None
        self._zahlungsziel = None
        self._steuersatz = None

    def __repr__(self) -> str:
        return f"Adresse(betriebsbezeichnung: '{self.betriebsbezeichnung}',\
 name: '{self.name}', anschrift_line1: '{self.anschrift_line1}',\
 adresszusatz: '{self.adresszusatz}',\
 anschrift_line3: '{self.anschrift_line3}',\
 strasse: '{self.strasse}', hausnummer: '{self.hausnummer}',\
 postfach: '{self.postfach}',\
 plz: '{self.plz}', ort: {self.ort}',\
 landeskennz: '{self.landeskennz}'\
 bundesland: '{self.bundesland}', telefon: '{self.telefon}',\
 fax: '{self.fax}', email: '{self.email}', steuernr: '{self.steuernr}',\
 finanzamt: '{self.finanzamt}', steuerid: '{self.steuerid}',\
 zahlungsziel: '{self.zahlungsziel}',\
 steuersatz: '{self.steuersatz}')"

    @property
    def betriebsbezeichnung(self):
        return self._betriebsbezeichnung

    @betriebsbezeichnung.setter
    def betriebsbezeichnung(self, value):
        self._betriebsbezeichnung = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def anschrift_line1(self):
        return self._anschrift_line1

    @anschrift_line1.setter
    def anschrift_line1(self, value):
        self._anschrift_line1 = value

    @property
    def anschrift_line3(self):
        return self._anschrift_line3

    @anschrift_line3.setter
    def anschrift_line3(self, value):
        self._anschrift_line3 = value

    @property
    def postfach(self):
        return self._postfach

    @postfach.setter
    def postfach(self, value):
        self._postfach = value

    @property
    def strasse(self):
        return self._strasse

    @strasse.setter
    def strasse(self, value):
        self._strasse = value

    @property
    def hausnummer(self):
        return self._hausnummer

    @hausnummer.setter
    def hausnummer(self, value):
        self._hausnummer = value

    @property
    def adresszusatz(self):
        return self._adresszusatz

    @adresszusatz.setter
    def adresszusatz(self, value):
        self._adresszusatz = value

    @property
    def plz(self):
        return self._plz

    @plz.setter
    def plz(self, value):
        self._plz = value

    @property
    def ort(self):
        return self._ort

    @ort.setter
    def ort(self, value):
        self._ort = value

    @property
    def landeskennz(self):
        return self._landeskennz

    @landeskennz.setter
    def landeskennz(self, value):
        self._landeskennz = value

    @property
    def bundesland(self):
        return self._bundesland

    @bundesland.setter
    def bundesland(self, value):
        self._bundesland = value

    @property
    def telefon(self):
        return self._telefon

    @telefon.setter
    def telefon(self, value):
        self._telefon = value

    @property
    def fax(self):
        return self._fax

    @fax.setter
    def fax(self, value):
        self._fax = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def steuernr(self):
        return self._steuernr

    @steuernr.setter
    def steuernr(self, value):
        self._steuernr = value

    @property
    def finanzamt(self):
        return self._finanzamt

    @finanzamt.setter
    def finanzamt(self, value):
        self._finanzamt = value

    @property
    def steuerid(self):
        return self._steuerid

    @steuerid.setter
    def steuerid(self, value):
        self._steuerid = value

    @property
    def zahlungsziel(self):
        return self._zahlungsziel

    @zahlungsziel.setter
    def zahlungsziel(self, value):
        self._zahlungsziel = value

    @property
    def steuersatz(self):
        return self._steuersatz

    @steuersatz.setter
    def steuersatz(self, value):
        self._steuersatz = value

# --------------- used for Kunde and Lieferant ---------------------------
    @property
    def anschrift(self) -> str:
        return '\n'.join(
            filter(None,
                   [
                        self.betriebsbezeichnung,
                        self.adresszusatz,
                        self.name,
                        ' '.join(['Postfach:', self.postfach])
                        if self.postfach else None,
                        self.strasse if self.strasse and not self.hausnummer
                        else ' '.join([self.strasse, self.hausnummer])
                        if not self.postfach else None,
                        ' '.join([self.plz, self.ort]),
                    ]
                   )
            )

    def _check_plz_ort(self) -> None:
        """raise ValueError on failure"""
        if (self.plz is not None
                and self.ort is not None):
            return
        raise ValueError(ANSCHRIFT_ERROR)

    def _check_kontakt(self) -> None:
        """raise ValueError on failure"""
        if self.telefon is not None:
            return
        if self.email is not None:
            return
        raise ValueError(KONTAKT_ERROR)

    def _check_umsatzsteuer(self) -> None:
        """raise ValueError on failure"""
        if (self.steuernr is not None
                and self.finanzamt is not None):
            return
        if self.steuerid is not None:
            return
        raise ValueError(USTID_ERROR)

    def _check_anschrift(self) -> None:
        """raise ValueError on failure"""
        self._check_plz_ort()
        if (self.betriebsbezeichnung is not None
                and self.postfach is not None):
            return
        elif (self.betriebsbezeichnung is not None
                and self.strasse is not None):
            return
        else:
            raise ValueError(ANSCHRIFT_ERROR)
