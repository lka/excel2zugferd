"""
Module for test of handle_other_objects
"""

import unittest
from src.konto import Konto
import random
import string

STAMMDATEN = {
    "Kontoinhaber": "Max Mustermann",
    "IBAN": "DEXX YYYY ZZZZ AAAA BBBB CC",
    "BIC": "XYZBCAY",
}


class TestKonto(unittest.TestCase):
    """
    Test Class for Class Konto
    """

    def get_properties(self, obj: object) -> list:
        """
        find all properties of class
        """
        properties = dir(obj)
        filtered = [
            prop
            for prop in properties
            if not prop.startswith("_")
            and prop not in ["fill_konto", "oneliner", "multiliner"]
        ]
        print("properties without __init__:\n", filtered)
        return filtered

    def randomword(self, length: int) -> str:
        """generate random word with length"""
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    def test_forNoneOnInit(self):
        """
        Tests that all elements are initialized to None
        after creation of Object
        """
        obj = Konto()
        MSG = "should be None on init"
        props = self.get_properties(obj)
        for prop in props:
            self.assertIsNone(
                getattr(obj, prop, "Attribute not found"), f"{prop} {MSG}"
            )

    def test_forReprHasAllProperties(self):
        """
        Tests that all properties are in __repr__
        """
        obj = Konto()
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
        obj = Konto()
        MSG = "should be filled"
        props = self.get_properties(obj)
        for prop in props:
            value = self.randomword(30)
            setattr(obj, prop, value)
            self.assertEqual(
                getattr(obj, prop, "Attribute not found"), value, f"{prop} {MSG}"
            )

    def test_fill_konto(self):
        """
        Tests that procedure fill_konto works
        """
        MSG = "Should be equal"
        daten = STAMMDATEN
        konto = Konto()
        konto.fill_konto(daten, daten.keys())
        self.assertEqual(konto.name, "Max Mustermann", MSG)
        self.assertEqual(konto.iban, "DEXX YYYY ZZZZ AAAA BBBB CC", MSG)
        self.assertEqual(konto.bic, "XYZBCAY", MSG)

    def test_fill_konto_raise_cond(self):
        """
        Tests that wrong init values throw ValueErrors
        """
        konto = Konto()
        daten = {
            "Kontoinhaber": "",
            "IBAN": "DEXX YYYY ZZZZ AAAA BBBB CC",
            "BIC": "XYZBCAY",
        }
        daten["Kontoinhaber"] = None
        with self.assertRaises(ValueError):
            konto.fill_konto(daten, daten.keys())
        daten["Kontoinhaber"] = "Max M"
        daten["IBAN"] = ""
        with self.assertRaises(ValueError):
            konto.fill_konto(daten, daten.keys())
        daten["IBAN"] = "xxxxxxxxxxx yyyyy"
        daten["BIC"] = ""
        with self.assertRaises(ValueError):
            konto.fill_konto(daten, daten.keys())
        daten["BIC"] = "Kasse 0815"
        try:
            konto.fill_konto(daten, daten.keys())
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
