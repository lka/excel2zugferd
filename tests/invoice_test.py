"""
Module for test Invoice
"""

import unittest
from src.invoice import Invoice
import random
import string


class TestInvoice(unittest.TestCase):
    """TestClass for class Invoice"""

    def get_properties(self, obj: object) -> list:
        """
        find all properties of class
        """
        properties = dir(obj)
        filtered = [prop for prop in properties if not prop.startswith('_')]
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
        obj = Invoice()
        MSG = 'should be None on init'
        props = self.get_properties(obj)
        for prop in props:
            self.assertIsNone(getattr(obj, prop, 'Attribute not found'),
                              f"{prop} {MSG}")

    def test_forReprHasAllProperties(self):
        """
        Tests that all properties are in __repr__
        """
        obj = Invoice()
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
        obj = Invoice()
        MSG = 'should be filled'
        props = self.get_properties(obj)
        for prop in props:
            value = self.randomword(30)
            setattr(obj, prop, value)
            self.assertEqual(getattr(obj, prop, 'Attribute not found'),
                             value, f"{prop} {MSG}")
