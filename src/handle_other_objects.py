"""
Module handles Classes Adresse, Konto, Steuerung and Invoice
"""

import pandas as pd
from datetime import datetime, timedelta

KONTAKT_ERROR = "'Kontakt': mindestens 2, maximal 3 Zeilen\n\
Tel.: 012345-1234\nFax: 012345-1235 (optional)\nE-Mail: xyz@abcdef.de"
ANSCHRIFT_ERROR = "'Anschrift': mindestens 3, maximal 5 Zeilen,\
 keine Leerzeilen\n\
\nFirma\nAdresszeile 2 (optional)\nAdresszeile 3 (optional)\n\
Strasse Hausnummer oder Postfach 12345\n\
PLZ Ortsname"
USTID_ERROR = "'Umsatzsteuer': 1-2 Zeilen\n\
Steuernummer: 12345/12345\nFinanzamt Ortsname\n\noder\n\n\
Umsatzsteuer-ID: DE999999999"
KONTO_ERROR = "'Konto': 3 Zeilen\n\
Kontoinhaber\nIBAN: DE12345678901\nBIC: XYZABCDEF"
BETRIEB_ERROR = "'Betriebsbezeichnung' muss ausgefüllt sein."
NAME_ERROR = "'Name' muss ausgefüllt sein."
ZZIEL_ERROR = "'Zahlungsziel' muss ausgefüllt sein."
STEUERSATZ_ERR_MSG = "'Steuersatz (in %)' darf nur aus Ziffern und\
 '.' bestehen z.B. 7.5 oder 19"


def _normalize(arr_in: list) -> list:
    """remove empty elements of array"""
    return list(filter(None, arr_in))


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

# -------------- H E L P E R S ------------------------------------------

    @property
    def anschrift(self) -> str:
        return '\n'.join(
            filter(None,
                   [
                        self.anschrift_line1,
                        self.adresszusatz,
                        self.anschrift_line3,
                        ' '.join(['Postfach:', self.postfach])
                        if self.postfach else None,
                        ' '.join([self.strasse, self.hausnummer])
                        if not self.postfach else None,
                        ' '.join([self.plz, self.ort]),
                    ]
                   )
            )

    @anschrift.setter
    def anschrift(self, arr: list) -> None:
        # print(arr)
        if len(arr) < 3 or len(arr) > 5:
            raise ValueError(ANSCHRIFT_ERROR)
        self._fill_adresszeile1(arr[0])
        if len(arr) == 5:
            self.anschrift_line3 = arr[2]
        if len(arr) > 3:
            self.adresszusatz = arr[1]
        self._fill_str_hnr(arr[-2])
        self._fill_plz_ort(arr[-1])

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

    @kontakt.setter
    def kontakt(self, arr: list) -> None:
        for elem in arr:
            sub = _normalize(elem.split())
            if len(sub) != 2:
                raise ValueError(KONTAKT_ERROR)
            else:
                self._fill_tel_fax_email(elem, sub[1])

    @property
    def umsatzsteuer(self) -> str:
        return '\n'.join(
            filter(None,
                   [
                       ('Steuernummer: ' + self.steuernr)
                       if self.steuernr else None,
                       self.finanzamt if self.steuernr else None,
                       ('Umsatzsteuer-ID: ' + self.steuerid)
                       if self.steuerid else None,
                   ])
        )

    @umsatzsteuer.setter
    def umsatzsteuer(self, arr: list) -> None:
        if len(arr) > 2:
            raise ValueError(USTID_ERROR)
        sub = _normalize(arr[0].split())
        if len(sub) != 2:
            raise ValueError(USTID_ERROR)
        self._fill_umsatzsteuer_or_id(arr, sub)

    def _fill_adresszeile1(self, zeile1: str) -> None:
        if len(zeile1) == 0:
            raise ValueError(ANSCHRIFT_ERROR)
        self.anschrift_line1 = zeile1

    def _fill_postfach(self, postfach):
        sub = _normalize(postfach.split(' ', -1))
        if len(sub) == 2:
            self.postfach = sub[1]
        else:
            raise ANSCHRIFT_ERROR

    def _fill_str_hnr(self, strasse):
        if 'Postfach' in strasse:
            self._fill_postfach(strasse)
        else:
            sub = _normalize(strasse.split(' ', -1))
            self.strasse = sub[0]
            if len(sub) == 2:
                self.hausnummer = sub[1]

    def _fill_plz_ort(self, ort):
        sub = _normalize(ort.split(' ', 1))
        self.plz = sub[0]
        if len(sub) == 2:
            self.ort = sub[1]
        else:
            raise ValueError(ANSCHRIFT_ERROR)

    def _fill_anschrift(self, daten):
        if daten["Anschrift"] is None:
            raise ValueError(ANSCHRIFT_ERROR)
        arr = _normalize(daten["Anschrift"].split('\n'))
        self.anschrift = arr

    def _switch_tel_fax_email(self, elem, value):
        if 'Tel' in elem:
            self.telefon = value
        elif 'Fax' in elem:
            self.fax = value
        elif 'Email' in elem or 'E-Mail' in elem:
            self.email = value
        else:
            raise KONTAKT_ERROR

    def _fill_tel_fax_email(self, elem, value):
        if len(value) == 0:
            raise ValueError(KONTAKT_ERROR)
        self._switch_tel_fax_email(elem, value)

    def _fill_kontakt(self, daten: list) -> None:
        if daten["Kontakt"] is None:
            raise ValueError(ANSCHRIFT_ERROR)
        arr = _normalize(daten["Kontakt"].split('\n'))
        if len(arr) < 2 or len(arr) > 3:
            raise ValueError(KONTAKT_ERROR)
        self.kontakt = arr

    def _fill_umsatzsteuerid(self, sub: list) -> None:
        if len(sub) != 2:
            raise ValueError(USTID_ERROR)
        self.steuerid = sub[1]
        self.finanzamt = None

    def _fill_steuernummer(self, arr: list, sub: list) -> None:
        if len(sub) != 2:
            raise ValueError(USTID_ERROR)
        self.steuernr = sub[1]
        self.finanzamt = arr[1]

    def _fill_umsatzsteuer_or_id(self, arr: list, sub: list) -> None:
        if len(arr) >= 1 and 'Umsatzsteuer-ID' in sub[0]:
            self._fill_umsatzsteuerid(sub)
        else:
            if len(arr) != 2:
                raise USTID_ERROR
            self._fill_steuernummer(arr, sub)

    def _fill_umsatzsteuer(self, daten: list) -> None:
        if daten["Umsatzsteuer"] is None:
            raise ValueError(USTID_ERROR)
        arr = _normalize(daten["Umsatzsteuer"].split('\n'))
        if len(arr) == 0:
            raise ValueError(USTID_ERROR)
        self.umsatzsteuer = arr

    def _fill_steuersatz(self, daten: list) -> None:
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
        betrieb = daten['Betriebsbezeichnung']
        if (betrieb is not None) and (len(betrieb) > 0) and\
                ('\n' not in betrieb):
            self.betriebsbezeichnung = betrieb
        else:
            raise ValueError(BETRIEB_ERROR)

    def _fill_name(self, daten):
        name = daten['Name']
        if name is not None and len(name) > 0 and\
                '\n' not in name:
            self.name = name
        else:
            raise ValueError(NAME_ERROR)

    def _fill_zahlungsziel(self, daten):
        ziel = daten["Zahlungsziel"]
        if ziel is not None and len(ziel) > 0 and\
                '\n' not in ziel:
            self.zahlungsziel = ziel
        else:
            raise ValueError(ZZIEL_ERROR)

    def fill_lieferant(self, daten=None) -> None:
        """fills Adresse of Lieferant from stammdaten"""
        if daten:
            self._fill_betrieb(daten)
            self._fill_name(daten)
            self._fill_anschrift(daten)
            self.bundesland = daten["Bundesland"]
            self._fill_kontakt(daten)
            self._fill_umsatzsteuer(daten)
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

    def _fill_iban_bic(self, key: str, value: str) -> None:
        if len(value) == 0:
            raise ValueError(KONTO_ERROR)
        if 'IBAN' in key:
            self.iban = value
        elif 'BIC' in key:
            self.bic = value
        else:
            raise ValueError(KONTO_ERROR)

    def _search_iban_bic(self, arr: list) -> None:
        for elem in arr[1:]:
            sub = _normalize(elem.split(' ', 1))
            if len(sub) != 2:
                raise ValueError(KONTO_ERROR)
            else:
                self._fill_iban_bic(sub[0], sub[1])

    def fill_konto(self, daten: list = None) -> None:
        """fills Konto of Lieferant from stammdaten"""
        if daten:
            if daten["Konto"] is None:
                raise ValueError(KONTAKT_ERROR)
            arr = _normalize(daten['Konto'].split('\n'))
            if len(arr) != 3:
                raise ValueError(KONTO_ERROR)
            self.name = arr[0]
            self._search_iban_bic(arr)
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
        self._customer: Adresse = None
        self._supplier: Adresse = None
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
    def customer(self) -> Adresse:
        return self._customer

    @customer.setter
    def customer(self, value: Adresse) -> None:
        self._customer = value

    @property
    def supplier(self) -> Adresse:
        return self._supplier

    @supplier.setter
    def supplier(self, value: Adresse) -> None:
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
