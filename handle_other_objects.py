"""
Module handles Classes Adresse and Konto
"""
KONTAKT_ERROR = ValueError("'Kontakt': mindestens 1, maximal 3 Zeilen\n\
Tel.: 012345-1234\nFax: 012345-1235 (optional)\nEmail: xyz@abcdef.de")
ANSCHRIFT_ERROR = ValueError("'Anschrift': mindestens 3, maximal 4 Zeilen\n\
Adresszeile 1\nAdresszeile 2 (optional)\nStrasse Hausnummer\nPLZ Ortsname")
USTID_ERROR = ValueError("'Umsatzsteuer': 2 Zeilen\n\
Steuernummer: 12345/12345\nFinanzamt Ortsname")
KONTO_ERROR = ValueError("'Konto': 3 Zeilen\n\
Kontoinhaber\nIBAN: DE12345678901\nBIC: XYZABCDEF")
BETRIEB_ERROR = ValueError("'Betriebsbezeichnung' muss ausgefüllt sein.")
NAME_ERROR = ValueError("'Name' muss ausgefüllt sein.")
ZZIEL_ERROR = ValueError("'Zahlungsziel' muss ausgefüllt sein.")


class Adresse(object):
    """Class Adresse"""
    def __init__(self) -> None:
        self._betriebsbezeichnung = None
        self._name = None
        self._anschrift_line1 = None
        self._anschrift_line2 = None
        self._strasse = None
        self._hausnummer = None
        self._plz = None
        self._ort = None
        self._bundesland = None
        self._telefon = None
        self._fax = None
        self._email = None
        self._steuernr = None
        self._finanzamt = None
        self._zahlungsziel = None

    def __repr__(self) -> str:
        return f"Adresse(betriebsbezeichnung: '{self.betriebsbezeichnung}',\
 name: '{self.name}', anschrift_line1: '{self.anschrift_line1}',\
 anschrift_line2: '{self.anschrift_line2}',\
 strasse: '{self.strasse}', hausnummer: '{self.hausnummer}',\
 plz: '{self.plz}', ort: {self.ort}',\
 bundesland: '{self.bundesland}', telefon: '{self.telefon}',\
 fax: '{self.fax}', email: '{self.email}', steuernr: '{self.steuernr}',\
 finanzamt: '{self.finanzamt}', zahlungsziel: '{self.zahlungsziel}')"

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
    def anschrift_line2(self):
        return self._anschrift_line2

    @anschrift_line2.setter
    def anschrift_line2(self, value):
        self._anschrift_line2 = value

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
    def zahlungsziel(self):
        return self._zahlungsziel

    @zahlungsziel.setter
    def zahlungsziel(self, value):
        self._zahlungsziel = value

    def get_anschrift(self) -> str:
        return '\n'.join(
            filter(None,
                   [
                            self.anschrift_line1,
                            self.anschrift_line2,
                            ' '.join([self.strasse, self.hausnummer]),
                            ' '.join([self.plz, self.ort]),
                    ]
                   )
            )

    def get_kontakt(self) -> str:
        return '\n'.join(
            filter(None,
                   [
                        'Tel.: ' + self.telefon if self.telefon else None,
                        'Fax: ' + self.fax if self.fax else None,
                        'Email: ' + self.email if self.email else None,
                   ])
        )

    def get_umsatzsteuer(self) -> str:
        return '\n'.join(
            filter(None,
                   [
                       'Steuernummer: ' +
                       self.steuernr if self.steuernr else None,
                       self.finanzamt,
                   ])
        )

    def _fill_str_hnr_plz_ort(self, strasse, ort):
        sub = strasse.split(' ', -1)
        self.strasse = sub[0]
        if len(sub) > 1:
            self.hausnummer = sub[1]
        sub = ort.split(' ', 1)
        self.plz = sub[0]
        if len(sub) > 1:
            self.ort = sub[1]
        else:
            raise ANSCHRIFT_ERROR

    def _fill_anschrift(self, daten):
        if daten["Anschrift"] is None:
            raise ANSCHRIFT_ERROR
        arr = daten["Anschrift"].split('\n')
        if len(arr) < 3 or len(arr) > 4:
            raise ANSCHRIFT_ERROR
        self.anschrift_line1 = arr[0]
        if len(arr) > 3:
            self.anschrift_line2 = arr[1]
            self._fill_str_hnr_plz_ort(arr[2], arr[3])
        else:
            self._fill_str_hnr_plz_ort(arr[1], arr[2])

    def _fill_tel_fax_email(self, elem, value):
        if len(value) == 0:
            raise KONTAKT_ERROR
        if 'Tel' in elem:
            self.telefon = value
        elif 'Fax' in elem:
            self.fax = value
        elif 'Email' in elem:
            self.email = value
        else:
            raise KONTAKT_ERROR

    def _fill_kontakt(self, daten):
        if daten["Kontakt"] is None:
            raise ANSCHRIFT_ERROR
        arr = daten["Kontakt"].split('\n')
        if len(arr) < 2 or len(arr) > 3:
            raise KONTAKT_ERROR
        for elem in arr:
            sub = elem.split()
            if len(sub) != 2:
                raise KONTAKT_ERROR
            else:
                self._fill_tel_fax_email(elem, sub[1])

    def _fill_umsatzsteuer(self, daten):
        if daten["Umsatzsteuer"] is None:
            raise USTID_ERROR
        arr = daten["Umsatzsteuer"].split('\n')
        if len(arr) != 2:
            raise USTID_ERROR
        sub = arr[0].split()
        if len(sub) != 2:
            raise USTID_ERROR
        self.steuernr = sub[1]
        self.finanzamt = arr[1]

    def fill_lieferant(self, daten=None) -> None:
        """fills Adresse of Lieferant from stammdaten"""
        if daten:
            betrieb = daten['Betriebsbezeichnung']
            if (betrieb is not None) and (len(betrieb) > 0) and\
                    ('\n' not in betrieb):
                self.betriebsbezeichnung = betrieb
            else:
                raise BETRIEB_ERROR
            name = daten['Name']
            if name is not None and len(name) > 0 and\
                    '\n' not in name:
                self.name = name
            else:
                raise NAME_ERROR
            self._fill_anschrift(daten)
            self.bundesland = daten["Bundesland"]
            self._fill_kontakt(daten)
            self._fill_umsatzsteuer(daten)
            ziel = daten["Zahlungsziel"]
            if ziel is not None and len(ziel) > 0 and\
                '\n' not in ziel:
                self.zahlungsziel = ziel
            else:
                raise ZZIEL_ERROR
            # print(repr(self))


class Konto(object):
    """
    Class for Girokonto
    """
    def __init__(self) -> None:
        self._name = None
        self._iban = None
        self._bic = None

    def __repr__(self) -> str:
        return f"Konto(name: '{self.name}', iban: '{self.iban}',\
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

    def _fill_iban_bic(self, key, value):
        if len(value) == 0:
            raise KONTO_ERROR
        if 'IBAN' in key:
            self.iban = value
        elif 'BIC' in key:
            self.bic = value
        else:
            raise KONTO_ERROR

    def fill_konto(self, daten=None) -> None:
        """fills Konto of Lieferant from stammdaten"""
        if daten:
            if daten["Konto"] is None:
                raise KONTAKT_ERROR
            arr = daten['Konto'].split('\n')
            if len(arr) != 3:
                raise KONTO_ERROR
            self.name = arr[0]
            for elem in arr[1:]:
                sub = elem.split(' ', 1)
                if len(sub) != 2:
                    raise KONTO_ERROR
                else:
                    self._fill_iban_bic(sub[0], sub[1])
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

    def __repr__(self) -> str:
        return f"Steuerung('create_xml: {self.create_xml}', \
 create_girocode: '{self.create_girocode}',\
 is_kleinunternehmen: '{self.is_kleinunternehmen}', abspann: '{self.abspann}')"

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

    def _fill_bools(self, thekeys, daten) -> None:
        self.create_girocode = (
            (daten["GiroCode"] == "Ja")
            if "GiroCode" in thekeys and
            daten["GiroCode"] is not None else False
        )
        self.create_xml = (
            (daten["ZugFeRD"] == "Ja")
            if (("ZugFeRD" in thekeys) and
                (daten["ZugFeRD"] is not None)) else False
        )
        self.is_kleinunternehmen = (
            (daten["Kleinunternehmen"] == "Ja")
            if "Kleinunternehmen" in thekeys and
            daten["Kleinunternehmen"] is not None else False
        )

    def fill_steuerung(self, daten=None) -> None:
        """fills Steuerung of Lieferant from stammdaten"""
        if daten:
            thekeys = daten.keys()
            self.abspann = (
                daten["Abspann"] if "Abspann" in thekeys else None
            )
            self._fill_bools(thekeys, daten)
            # print(repr(self))
