"""
Module for test Invoice
"""

import unittest
import numpy as np
from src.invoice import Invoice
from src.adresse import Adresse
from src.steuerung import Steuerung
from src.konto import Konto


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
