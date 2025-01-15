"""
Module for test of handle_other_objects
"""

import unittest
import numpy as np
from src.handle_other_objects import Konto, Steuerung, Invoice
from src.adresse import Adresse

STAMMDATEN = {
                    "Kontoinhaber": "Max Mustermann",
                    "IBAN": "DEXX YYYY ZZZZ AAAA BBBB CC",
                    "BIC": "XYZBCAY",
             }


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
