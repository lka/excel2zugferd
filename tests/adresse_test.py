"""
Module Adresse Test
"""

import unittest
from src.adresse import Adresse
from src import _setNoneIfEmpty


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
        self.assertIsNone(adresse.steuerid, MSG)
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

    def test__check_anschrift(self):
        """
        Tests that wrong Anschrift in Adresse throws ValueError
        """
        adresse = Adresse()
        adresse.strasse = _setNoneIfEmpty("Am kleinen Weg")
        adresse.plz = _setNoneIfEmpty("12345")
        adresse.ort = _setNoneIfEmpty("Musterstadt (Ortsteil Klein)")
        adresse.betriebsbezeichnung = None
        with self.assertRaises(ValueError):
            adresse._check_anschrift()
        adresse.betriebsbezeichnung = _setNoneIfEmpty("")
        with self.assertRaises(ValueError):
            adresse._check_anschrift()
        adresse.betriebsbezeichnung = _setNoneIfEmpty("Software AG")
        adresse.strasse = _setNoneIfEmpty("")
        with self.assertRaises(ValueError):
            adresse._check_anschrift()
        adresse.strasse = _setNoneIfEmpty("Am kleinen Weg")
        adresse.plz = _setNoneIfEmpty("12345")
        adresse.ort = _setNoneIfEmpty("Musterstadt (Ortsteil Klein)")
        adresse.hausnummer = None
        try:
            adresse._check_anschrift()
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        adresse.postfach = _setNoneIfEmpty("12345")
        try:
            adresse._check_anschrift()
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        adresse.strasse = _setNoneIfEmpty("An der Musterstrasse")
        adresse.hausnummer = "17a"
        adresse.postfach = None
        adresse.plz = _setNoneIfEmpty("")
        with self.assertRaises(ValueError):
            adresse._check_anschrift()
        adresse.plz = _setNoneIfEmpty("12345")
        adresse.ort = _setNoneIfEmpty("")
        with self.assertRaises(ValueError):
            adresse._check_anschrift()
        adresse.ort = _setNoneIfEmpty("Musterstadt (Ortsteil Klein)")
        try:
            adresse._check_anschrift()
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test__check_umsatzsteuer(self):
        """
        Test that wrong Umsatzsteuer throws ValueError
        """
        adresse = Adresse()
        adresse.steuernr = _setNoneIfEmpty("12345/12345")
        adresse.finanzamt = _setNoneIfEmpty("")
        adresse.steuerid = None
        # print(repr(adresse))
        with self.assertRaises(ValueError):
            adresse._check_umsatzsteuer()
        adresse.finanzamt = _setNoneIfEmpty("Musterstadt")
        adresse.steuernr = _setNoneIfEmpty("")
        with self.assertRaises(ValueError):
            adresse._check_umsatzsteuer()
        adresse.steuernr = _setNoneIfEmpty("12345/12345")
        try:
            adresse._check_umsatzsteuer()
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        adresse.steuerid = _setNoneIfEmpty("DE12345")
        adresse.steuernr = _setNoneIfEmpty("")
        adresse.finanzamt = _setNoneIfEmpty("")
        try:
            adresse._check_umsatzsteuer()
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test__check_kontakt(self):
        """
        Test that wrong kontakt throws ValueError
        """
        adresse = Adresse()
        adresse.telefon = _setNoneIfEmpty("")
        adresse.email = _setNoneIfEmpty("")
        adresse.fax = _setNoneIfEmpty("")
        with self.assertRaises(ValueError):
            adresse._check_kontakt()
        adresse.telefon = _setNoneIfEmpty("0123 4567")
        try:
            adresse._check_kontakt()
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        adresse.telefon = _setNoneIfEmpty("")
        adresse.email = _setNoneIfEmpty("max@mustermann.de")
        try:
            adresse._check_kontakt()
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_get_anschrift_kunde(self):
        """Tests get_anschrift of Adresse"""
        adr = Adresse()
        MSG = 'should be filled'
        BEZ = "Software AG"
        NAME = 'Max Mustermann'
        AN1 = 'Maximilian Mustermann'
        ZUS = 'Berichtswesen'
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
                         f"{BEZ}\n{NAME}\n{STR} {HNR}\n{PLZ} {ORT}", MSG)
        adr.adresszusatz = ZUS
        self.assertEqual(adr.anschrift,
                         f"{BEZ}\n{ZUS}\n{NAME}\n{STR} {HNR}\n{PLZ} {ORT}",
                         MSG)
