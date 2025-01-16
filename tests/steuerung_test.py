"""
Module for test of handle_other_objects
"""

import unittest
from src.steuerung import Steuerung
import random
import string


class TestSteuerung(unittest.TestCase):
    """
    Test Class for Class Steuerung
    """
    def get_properties(self, obj: object) -> list:
        """
        find all properties of class
        """
        properties = dir(obj)
        filtered = [prop for prop in properties if not prop.startswith('_')
                    and prop not in ['fill_steuerung']]
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
        obj = Steuerung()
        MSG = 'should be None on init'
        props = self.get_properties(obj)
        for prop in props:
            self.assertIsNone(getattr(obj, prop, 'Attribute not found'),
                              f"{prop} {MSG}")

    def test_forReprHasAllProperties(self):
        """
        Tests that all properties are in __repr__
        """
        obj = Steuerung()
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
        obj = Steuerung()
        MSG = 'should be filled'
        props = self.get_properties(obj)
        for prop in props:
            value = self.randomword(30)
            setattr(obj, prop, value)
            self.assertEqual(getattr(obj, prop, 'Attribute not found'),
                             value, f"{prop} {MSG}")

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
