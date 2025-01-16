"""
Module Adresse Test
"""

import unittest
from src.adresse import Adresse
from src import _setNoneIfEmpty
import random
import string


class TestAdresse(unittest.TestCase):
    """
    Test Class for Class Adresse
    """

    def get_properties(self, obj: object) -> list:
        """
        find all properties of class
        """
        properties = dir(obj)
        filtered = [prop for prop in properties if not prop.startswith('_')
                    and prop not in ['anschrift']]
        print("properties without __init__:\n", filtered)
        return filtered

    def randomword(self, length: int) -> str:
        """ generate random word with length"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def test_forNoneOnInit(self):
        """
        Tests that all elements are initialized to None
        after creation of Object
        """
        obj = Adresse()
        MSG = 'should be None on init'
        props = self.get_properties(obj)
        for prop in props:
            self.assertIsNone(getattr(obj, prop, 'Attribute not found'),
                              f"{prop} {MSG}")

    def test_forReprHasAllProperties(self):
        """
        Tests that all properties are in __repr__
        """
        obj = Adresse()
        MSG = "should be in __repr__"
        try:
            theRepr = repr(obj)
        except AttributeError:
            self.fail("repr has property that is not in Class")
        props = self.get_properties(obj)
        for prop in props:
            self.assertIn(prop, theRepr, f"{prop} {MSG}")

    def test_forPopulation(self):
        """
        Tests that elements of Class are populatable
        and gives back correct element (getter and setter)
        """
        obj = Adresse()
        MSG = 'should be filled'
        props = self.get_properties(obj)
        for prop in props:
            value = self.randomword(30)
            setattr(obj, prop, value)
            self.assertEqual(getattr(obj, prop, 'Attribute not found'),
                             value, f"{prop} {MSG}")

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
