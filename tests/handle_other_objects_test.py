"""
Module for test of handle_other_objects
"""

import unittest
# import pandas as pd
import numpy as np
from src.handle_other_objects import Adresse, Konto, Steuerung, Invoice


class TestAdresse(unittest.TestCase):
    """
    Test Class for Class Adresse
    """
    def test_forNoneOnInit(self):
        """
        Tests that all elements are initialized to None
        after creation of Object
        """
        adresse = Adresse()
        MSG = 'should be None on init'
        self.assertIsNone(adresse.betriebsbezeichnung, MSG)
        self.assertIsNone(adresse.name, MSG)
        self.assertIsNone(adresse.anschrift_line1, MSG)
        self.assertIsNone(adresse.adresszusatz, MSG)
        self.assertIsNone(adresse.strasse, MSG)
        self.assertIsNone(adresse.hausnummer, MSG)
        self.assertIsNone(adresse.plz, MSG)
        self.assertIsNone(adresse.ort, MSG)
        self.assertIsNone(adresse.telefon, MSG)
        self.assertIsNone(adresse.fax, MSG)
        self.assertIsNone(adresse.email, MSG)
        self.assertIsNone(adresse.steuernr, MSG)
        self.assertIsNone(adresse.finanzamt, MSG)
        self.assertIsNone(adresse.zahlungsziel, MSG)
        self.assertIsNone(adresse.steuersatz, MSG)

    def test_forPopulation(self):
        """
        Tests that elements of Class are populatable
        and gives back correct element (getter and setter)
        """
        adr = Adresse()
        MSG = 'should be filled'
        BEZ = "Software AG"
        NAME = 'Max Mustermann'
        AN1 = 'Maximilian Mustermann'
        AN2 = 'Softwareentwicklung'
        ORT = 'Musterstadt'
        PLZ = '12345'
        STR = 'Musterstrasse'
        HNR = '17a'
        TEL = '01234 5678 456'
        FAX = '01234 5678 457'
        MAIL = 'mustermann@telekom.de'
        COUNTY = 'Baden Württemberg'
        AMT = 'Finanzamt Musterstadt'
        USTNR = '12345/12345'
        ZZIEL = '14'
        SSATZ = '19'
        adr.betriebsbezeichnung = BEZ
        self.assertEqual(adr.betriebsbezeichnung, BEZ, MSG)
        adr.name = NAME
        self.assertEqual(adr.name, NAME, MSG)
        adr.anschrift_line1 = AN1
        self.assertEqual(adr.anschrift_line1, AN1, MSG)
        adr.anschrift_line2 = AN2
        self.assertEqual(adr.anschrift_line2, AN2, MSG)
        adr.ort = ORT
        self.assertEqual(adr.ort, ORT, MSG)
        adr.plz = PLZ
        self.assertEqual(adr.plz, PLZ, MSG)
        adr.strasse = STR
        self.assertEqual(adr.strasse, STR, MSG)
        adr.hausnummer = HNR
        self.assertEqual(adr.hausnummer, HNR, MSG)
        adr.telefon = TEL
        self.assertEqual(adr.telefon, TEL, MSG)
        adr.fax = FAX
        self.assertEqual(adr.fax, FAX, MSG)
        adr.email = MAIL
        self.assertEqual(adr.email, MAIL, MSG)
        adr.bundesland = COUNTY
        self.assertEqual(adr.bundesland, COUNTY, MSG)
        adr.steuernr = USTNR
        self.assertEqual(adr.steuernr, USTNR, MSG)
        adr.finanzamt = AMT
        self.assertEqual(adr.finanzamt, AMT, MSG)
        adr.zahlungsziel = ZZIEL
        self.assertEqual(adr.zahlungsziel, ZZIEL, MSG)
        adr.steuersatz = SSATZ
        self.assertEqual(adr.steuersatz, SSATZ, MSG)

    def test_get_anschrift(self):
        """Tests get_anschrift"""
        adr = Adresse()
        MSG = 'should be filled'
        BEZ = "Software AG"
        NAME = 'Max Mustermann'
        AN1 = 'Maximilian Mustermann'
        ZUS = 'z.H. Herrn Müller'
        ORT = 'Musterstadt'
        PLZ = '12345'
        STR = 'Musterstrasse'
        HNR = '17a'
        TEL = '01234 5678 456'
        FAX = '01234 5678 457'
        MAIL = 'mustermann@telekom.de'
        COUNTY = 'Baden Württemberg'
        adr.betriebsbezeichnung = BEZ
        adr.name = NAME
        adr.anschrift_line1 = AN1
        adr.ort = ORT
        adr.plz = PLZ
        adr.strasse = STR
        adr.hausnummer = HNR
        adr.email = MAIL
        adr.telefon = TEL
        adr.fax = FAX
        adr.bundesland = COUNTY
        self.assertEqual(adr.anschrift,
                         f"{AN1}\n{STR} {HNR}\n{PLZ} {ORT}", MSG)
        adr.adresszusatz = ZUS
        self.assertEqual(adr.anschrift,
                         f"{AN1}\n{ZUS}\n{STR} {HNR}\n{PLZ} {ORT}", MSG)

    def test_get_kontakt(self):
        """Tests get_kontakt"""
        adr = Adresse()
        TEL = '01234 5678 456'
        FAX = '01234 5678 457'
        MAIL = 'mustermann@telekom.de'
        adr.telefon = TEL
        adr.email = MAIL
        self.assertEqual(adr.kontakt,
                         f"Tel.: {TEL}\nE-Mail: {MAIL}")
        adr.fax = FAX
        self.assertEqual(adr.kontakt,
                         f"Tel.: {TEL}\nFax: {FAX}\nE-Mail: {MAIL}")

    def test_get_umsatzsteuer(self):
        """Tests get_umsatzsteuer"""
        adr = Adresse()
        AMT = 'Finanzamt Musterstadt'
        USTNR = '12345/12345'
        adr.steuernr = USTNR
        adr.finanzamt = AMT
        self.assertEqual(adr.umsatzsteuer,
                         f"Steuernummer: {USTNR}\n{AMT}")

    def test_get_umsatzsteuer_ID(self):
        """Tests get_umsatzsteuer with Umsatzsteuer-ID"""
        adr = Adresse()
        USTNR = 'DE123456789'
        adr.steuerid = USTNR
        self.assertEqual(adr.umsatzsteuer,
                         f"Umsatzsteuer-ID: {USTNR}")

    def test__fill_umsatzsteuer(self):
        """Tests _fill_umsatzsteuer with Steuernummer"""
        MSG = "should be equal"
        adr = Adresse()
        AMT = 'Finanzamt Musterstadt'
        USTNR = '12345/12345'
        adr._fill_umsatzsteuer({'Umsatzsteuer':
                                f"Steuernummer: {USTNR}\n{AMT}"})
        self.assertEqual(adr.steuernr, USTNR, MSG)
        self.assertEqual(adr.finanzamt, AMT, MSG)
        self.assertIsNone(adr.steuerid)

    def test__fill_umsatzsteuer_ID_withoutAMT(self):
        """Tests _fill_umsatzsteuer with Umsatzsteuer-ID"""
        MSG = "should be equal"
        adr = Adresse()
        USTNR = 'DE123456789'
        adr._fill_umsatzsteuer({'Umsatzsteuer':
                                f"Umsatzsteuer-ID: {USTNR}"})
        self.assertEqual(adr.steuerid, USTNR, MSG)
        self.assertIsNone(adr.finanzamt)
        self.assertIsNone(adr.steuernr)

    def test__fill_umsatzsteuer_ID(self):
        """Tests _fill_umsatzsteuer with Umsatzsteuer-ID"""
        MSG = "should be equal"
        adr = Adresse()
        AMT = 'Finanzamt Musterstadt'
        USTNR = 'DE123456789'
        adr._fill_umsatzsteuer({'Umsatzsteuer':
                                f"Umsatzsteuer-ID: {USTNR}\n{AMT}"})
        self.assertEqual(adr.steuerid, USTNR, MSG)
        self.assertIsNone(adr.finanzamt)
        self.assertIsNone(adr.steuernr)

    def test__fill_steuersatz(self):
        """Test _fill_steuersatz with correct value"""
        MSG = "should be equal"
        adr = Adresse()
        daten = {
            'Steuersatz': '19'
        }
        EXPECTED = "19.00"
        adr._fill_steuersatz(daten)
        self.assertEqual(adr.steuersatz, EXPECTED, MSG)

    def test_fill_lieferant(self):
        """
        Tests that procedure fill_lieferant works
        """
        MSG = 'Should be equal'
        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                    "Steuersatz": "7.5",
                }
        lieferant = Adresse()
        lieferant.fill_lieferant(daten)
        self.assertEqual(lieferant.anschrift_line1, "Max Mustermann", MSG)
        self.assertEqual(lieferant.adresszusatz, "Software", MSG)
        self.assertEqual(lieferant.betriebsbezeichnung,
                         "Max Mustermann - Software", MSG)
        self.assertEqual(lieferant.bundesland, "Baden-Württemberg", MSG)
        self.assertEqual(lieferant.email, "max@mustermann.de", MSG)
        self.assertIsNone(lieferant.fax, MSG)
        self.assertEqual(lieferant.finanzamt, "Finanzamt Musterstadt", MSG)
        self.assertEqual(lieferant.hausnummer, "17a", MSG)
        self.assertEqual(lieferant.name, "Max Mustermann", MSG)
        self.assertEqual(lieferant.ort, "Musterstadt", MSG)
        self.assertEqual(lieferant.plz, "12345", MSG)
        self.assertEqual(lieferant.steuernr, "12345/12345", MSG)
        self.assertEqual(lieferant.strasse, "Musterstr.", MSG)
        self.assertEqual(lieferant.telefon, "01234-1234567", MSG)
        self.assertEqual(lieferant.zahlungsziel, "14", MSG)
        self.assertEqual(lieferant.steuersatz, "7.50", MSG)

    def test_fill_lieferant_throws_cond1(self):
        """
        Tests that wrong Anschrift in Stammdaten throws ValueError
        """
        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                    "Steuersatz": "19",
                }
        lieferant = Adresse()
        daten["Anschrift"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Anschrift"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Anschrift"] = "Max\nMusterstr.\nMusterstadt"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Anschrift"] = "Max\nMusterstr. 17a\nMusterstadt"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Anschrift"] = "Musterstr. 17a\n12345 Musterstadt"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Anschrift"] = "\n\nMusterstr. 17a\n12345 Musterstadt"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Anschrift"] = "Max\nMusterstr. 17a\n12345 Musterstadt"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        daten["Anschrift"] = "Software AG\nMax\n\
Musterstr. 17a\n12345 Musterstadt"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        daten["Anschrift"] = "Software AG\nAbtlg. EDV\n\
Herr Maier\nMusterstr. 17a\n12345 Musterstadt"
        daten["Steuersatz"] = "Hallo"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Steuersatz"] = "19"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond2(self):
        """
        Tests that wrong Betriebsbezeichnung in Stammdaten throws ValueError
        """
        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                    "Steuersatz": None,
                }
        lieferant = Adresse()
        daten["Betriebsbezeichnung"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Betriebsbezeichnung"] = "Max Mustermann\nSoftware"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Betriebsbezeichnung"] = "Max Mustermann - Software"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond3(self):
        """
        Tests that wrong Kontakt in Stammdaten throws ValueError
        """
        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                    "Steuersatz": None,
                }
        lieferant = Adresse()
        daten["Kontakt"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Kontakt"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Kontakt"] = "Tel.: 01234-1234567"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Kontakt"] = "Tel.: \nEmail: max@mustermann.de"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Kontakt"] = "Tel.: 01234-1234567\nE-Mail: max@mustermann.de"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        daten["Kontakt"] = "Tel.: 01234-1234567\nEmail: max@mustermann.de\n"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond4(self):
        """
        Tests that wrong Name in Stammdaten throws ValueError
        """
        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                    "Steuersatz": None,
                }
        lieferant = Adresse()
        daten["Name"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Name"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Name"] = "Max\nMustermann"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Name"] = "Max Mustermann"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond5(self):
        """
        Tests that wrong Umsatzsteuer in Stammdaten throws ValueError
        """
        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                    "Steuersatz": None,
                }
        lieferant = Adresse()
        daten["Umsatzsteuer"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Umsatzsteuer"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Umsatzsteuer"] = "\n"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Umsatzsteuer"] = "12345/12345\nFinanzamt"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Umsatzsteuer"] = "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond6(self):
        """
        Tests that wrong Zahlungsziel in Stammdaten throws ValueError
        """
        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                    "Steuersatz": None,
                }
        lieferant = Adresse()
        daten["Zahlungsziel"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Zahlungsziel"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Zahlungsziel"] = "\n"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Zahlungsziel"] = "14"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")


class TestKonto(unittest.TestCase):
    """
    Test Class for Class Konto
    """
    def test_forNoneOnInit(self):
        """
        Tests that all elements are initialized to None
        after creation of Object
        """
        konto = Konto()
        self.assertIsNone(konto.name,
                          'should be None on init')
        self.assertIsNone(konto.bic,
                          'should be None on init')
        self.assertIsNone(konto.iban,
                          'should be None on init')

    def test_forPopulation(self):
        """
        Tests that elements of Class are populatable
        and gives back correct element (getter and setter)
        """
        konto = Konto()
        MSG = 'should be filled'
        NAME = 'Max Mustermann'
        IBAN = "DE12 3456 7890 1234 5679"
        BIC = "Solades1TBB"
        konto.name = NAME
        self.assertEqual(konto.name, NAME, MSG)
        konto.iban = IBAN
        self.assertEqual(konto.iban, IBAN, MSG)
        konto.bic = BIC
        self.assertEqual(konto.bic, BIC, MSG)

    def test_fill_konto(self):
        """
        Tests that procedure fill_konto works
        """
        MSG = 'Should be equal'
        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "GiroCode": "Nein",
                    "Kleinunternehmen": "Nein",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Konto": "Max Mustermann\
\nIBAN: DEXX YYYY ZZZZ AAAA BBBB CC\nBIC: XYZBCAY",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                    "ZugFeRD": "Ja"
                }
        konto = Konto()
        konto.fill_konto(daten)
        self.assertEqual(konto.name, "Max Mustermann", MSG)
        self.assertEqual(konto.iban, "DEXX YYYY ZZZZ AAAA BBBB CC", MSG)
        self.assertEqual(konto.bic, "XYZBCAY", MSG)

    def test_fill_konto_raise_cond(self):
        """
        Tests that wrong init values throw ValueErrors
        """
        konto = Konto()
        daten = {
            "Konto": "IBAN: DEXX YYYY ZZZZ AAAA BBBB CC\nBIC: XYZBCAY",
        }
        with self.assertRaises(ValueError):
            konto.fill_konto(daten)
        daten["Konto"] = None
        with self.assertRaises(ValueError):
            konto.fill_konto(daten)
        daten["Konto"] = ""
        with self.assertRaises(ValueError):
            konto.fill_konto(daten)
        daten["Konto"] = "\n"
        with self.assertRaises(ValueError):
            konto.fill_konto(daten)
        daten["Konto"] = "\n\n"
        with self.assertRaises(ValueError):
            konto.fill_konto(daten)
        daten["Konto"] = "Max M\n\nBIC: XYZBCAY"
        with self.assertRaises(ValueError):
            konto.fill_konto(daten)
        daten["Konto"] = "Max M\nIBAN: xxxxxxxxxxx yyyyy\nBIC:"
        with self.assertRaises(ValueError):
            konto.fill_konto(daten)
        daten["Konto"] = "Max M\nIBAN: xxxxxxxxxxx yyyyy\nBIC: "
        with self.assertRaises(ValueError):
            konto.fill_konto(daten)
        daten["Konto"] = "Max\nIBAN: DEXX YYYY ZZZZ AAAA BBBB CC\nBIC: XYZBCAY"
        try:
            konto.fill_konto(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")


class TestSteuerung(unittest.TestCase):
    """
    Test Class for Class Steuerung
    """
    def test_forNoneOnInit(self):
        """
        Tests that all elements are initialized to None
        after creation of Object
        """
        MSG = 'should be None on init'
        steuerung = Steuerung()
        self.assertIsNone(steuerung.abspann, MSG)
        self.assertIsNone(steuerung.create_girocode, MSG)
        self.assertIsNone(steuerung.create_xml, MSG)
        self.assertIsNone(steuerung.directory, MSG)

    def test_forPopulation(self):
        """
        Tests that elements of Class are populatable
        and gives back correct element (getter and setter)
        """
        steuerung = Steuerung()
        MSG = 'should be filled'
        ABSPANN = 'Mit freundlichen Grüßen\n Max Mustermann'
        GIROC = True
        XML = True
        VERZ = "C:/Users/Max/Documents"
        steuerung.abspann = ABSPANN
        self.assertEqual(steuerung.abspann, ABSPANN, MSG)
        steuerung.create_girocode = GIROC
        self.assertEqual(steuerung.create_girocode, GIROC, MSG)
        steuerung.create_xml = XML
        self.assertEqual(steuerung.create_xml, XML, MSG)
        steuerung.directory = VERZ
        self.assertEqual(steuerung.directory, VERZ, MSG)

    def test_fill_steuerung(self):
        """
        Tests that procedure fill_steuerung works
        """
        MSG = 'Should be equal'
        daten = {
                    "Abspann": "Mit freundlichen Grüßen\nMax Mustermann",
                    "GiroCode": "Nein",
                    "Kleinunternehmen": "Nein",
                    "ZugFeRD": "Ja",
                    "Verzeichnis": "C:/Users/Max/Documents",
                }
        steuerung = Steuerung()
        steuerung.fill_steuerung(daten)
        self.assertEqual(steuerung.abspann,
                         "Mit freundlichen Grüßen\nMax Mustermann", MSG)
        self.assertEqual(steuerung.create_girocode, False, MSG)
        self.assertEqual(steuerung.create_xml, True, MSG)
        daten["ZugFeRD"] = None
        steuerung.fill_steuerung(daten)
        self.assertFalse(steuerung.create_xml, MSG)
        daten["ZugFeRD"] = ""
        steuerung.fill_steuerung(daten)
        self.assertFalse(steuerung.create_xml, MSG)
        daten["Verzeichnis"] = ""
        steuerung.fill_steuerung(daten)
        self.assertEqual(len(steuerung.directory), 0, MSG)


class TestInvoice(unittest.TestCase):
    """TestClass for class Invoice"""
    def test_forNoneOnInit(self):
        """
        Test that all elements of class are None after creation of object
        """
        MSG = "should be None"
        invoice = Invoice()
        self.assertIsNone(invoice.customer, MSG)
        self.assertIsNone(invoice.supplier, MSG)
        self.assertIsNone(invoice.supplier_account, MSG)
        self.assertIsNone(invoice.positions, MSG)
        self.assertIsNone(invoice.invoicenr, MSG)
        self.assertIsNone(invoice.sums, MSG)
        self.assertIsNone(invoice.management, MSG)

    def test__repr__(self):
        """test that __repr__ contains all elements"""
        MSG = 'representation should contain all elements'
        invoice = Invoice()
        reprStr = repr(invoice)
        self.assertTrue('customer' in reprStr, MSG)
        self.assertTrue('supplier:' in reprStr, MSG)
        self.assertTrue('supplier_account' in reprStr, MSG)
        self.assertTrue('positions' in reprStr, MSG)
        self.assertTrue('invoicenr' in reprStr, MSG)
        self.assertTrue('sums' in reprStr, MSG)
        self.assertTrue('management' in reprStr, MSG)

    def test_forPopulation(self):
        """
        Test the population of elements in object
        """
        MSG = "should be equal"
        invoice = Invoice()
        expected = Adresse()
        invoice.customer = expected
        self.assertEqual(type(invoice.customer), type(expected), MSG)
        invoice.supplier = expected
        self.assertEqual(type(invoice.supplier), type(expected), MSG)
        expected = Konto()
        invoice.supplier_account = expected
        self.assertEqual(type(invoice.supplier_account), type(expected), MSG)
        expected = np.array([['A', 'B', 'C'], [1, 2, 3], [4, 5, 6], [7, 8, 9]])
        invoice.positions = np.r_[[['A', 'B', 'C']], [[1, 2, 3],
                                  [4, 5, 6], [7, 8, 9]]]
        # print(invoice.positions)
        self.assertTrue(np.array_equal(invoice.positions, expected), MSG)
        expected = {'RgNr': 'R2024001'}
        invoice.invoicenr = expected
        self.assertDictEqual(invoice.invoicenr, expected, MSG)
        expected = [{'netto': 1234.80}, {'MwSt': 80.97}, {'Brutto': 2045.98}]
        invoice.sums = expected
        self.assertListEqual(invoice.sums, expected, MSG)
        expected = Steuerung()
        invoice.management = expected
        self.assertEqual(type(invoice.management), type(expected), MSG)
