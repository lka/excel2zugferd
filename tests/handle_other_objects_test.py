"""
Module for test of handle_other_objects
"""

import unittest
from handle_other_objects import Adresse, Konto, Steuerung


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
        self.assertIsNone(adresse.betriebsbezeichnung,
                          'should be None on init')
        self.assertIsNone(adresse.name,
                          'should be None on init')
        self.assertIsNone(adresse.anschrift_line1,
                          'should be None on init')
        self.assertIsNone(adresse.anschrift_line2,
                          'should be None on init')
        self.assertIsNone(adresse.strasse,
                          'should be None on init')
        self.assertIsNone(adresse.hausnummer,
                          'should be None on init')
        self.assertIsNone(adresse.plz,
                          'should be None on init')
        self.assertIsNone(adresse.ort,
                          'should be None on init')
        self.assertIsNone(adresse.telefon,
                          'should be None on init')
        self.assertIsNone(adresse.fax,
                          'should be None on init')
        self.assertIsNone(adresse.email,
                          'should be None on init')
        self.assertIsNone(adresse.steuernr,
                          'should be None on init')
        self.assertIsNone(adresse.finanzamt,
                          'should be None on init')
        self.assertIsNone(adresse.zahlungsziel,
                          'should be None on init')

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

    def test_get_anschrift(self):
        """Tests get_anschrift"""
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
        self.assertEqual(adr.get_anschrift(),
                         f"{AN1}\n{STR} {HNR}\n{PLZ} {ORT}", MSG)
        adr.anschrift_line2 = AN2
        self.assertEqual(adr.get_anschrift(),
                         f"{AN1}\n{AN2}\n{STR} {HNR}\n{PLZ} {ORT}", MSG)

    def test_get_kontakt(self):
        """Tests get_kontakt"""
        adr = Adresse()
        TEL = '01234 5678 456'
        FAX = '01234 5678 457'
        MAIL = 'mustermann@telekom.de'
        adr.telefon = TEL
        adr.email = MAIL
        self.assertEqual(adr.get_kontakt(),
                         f"Tel.: {TEL}\nEmail: {MAIL}")
        adr.fax = FAX
        self.assertEqual(adr.get_kontakt(),
                         f"Tel.: {TEL}\nFax: {FAX}\nEmail: {MAIL}")

    def test_get_umsatzsteuer(self):
        """Tests get_umsatzsteuer"""
        adr = Adresse()
        AMT = 'Finanzamt Musterstadt'
        USTNR = '12345/12345'
        adr.steuernr = USTNR
        adr.finanzamt = AMT
        self.assertEqual(adr.get_umsatzsteuer(),
                         f"Steuernummer: {USTNR}\n{AMT}")

    def test_fill_lieferant(self):
        """
        Tests that procedure fill_lieferant works
        """
        MSG = 'Should be equal'
        daten = {
                    "Abspann": "Mit freundlichen Grüßen\nMax Mustermann",
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
        lieferant = Adresse()
        lieferant.fill_lieferant(daten)
        self.assertEqual(lieferant.anschrift_line1, "Max Mustermann", MSG)
        self.assertEqual(lieferant.anschrift_line2, "Software", MSG)
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
                    "Abspann": "Mit freundlichen Grüßen\nMax Mustermann",
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


class TestSteuerung(unittest.TestCase):
    """
    Test Class for Class Steuerung
    """
    def test_forNoneOnInit(self):
        """
        Tests that all elements are initialized to None
        after creation of Object
        """
        steuerung = Steuerung()
        self.assertIsNone(steuerung.abspann,
                          'should be None on init')
        self.assertIsNone(steuerung.create_girocode,
                          'should be None on init')
        self.assertIsNone(steuerung.create_xml,
                          'should be None on init')

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
        steuerung.abspann = ABSPANN
        self.assertEqual(steuerung.abspann, ABSPANN, MSG)
        steuerung.create_girocode = GIROC
        self.assertEqual(steuerung.create_girocode, GIROC, MSG)
        steuerung.create_xml = XML
        self.assertEqual(steuerung.create_xml, XML, MSG)

    def test_fill_steuerung(self):
        """
        Tests that procedure fill_steuerung works
        """
        MSG = 'Should be equal'
        daten = {
                    "Abspann": "Mit freundlichen Grüßen\nMax Mustermann",
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
        steuerung = Steuerung()
        steuerung.fill_steuerung(daten)
        self.assertEqual(steuerung.abspann,
                         "Mit freundlichen Grüßen\nMax Mustermann", MSG)
        self.assertEqual(steuerung.create_girocode, False, MSG)
        self.assertEqual(steuerung.create_xml, True, MSG)
