"""
Modul excel_content_test
"""

from unittest import TestCase
import os
import numpy as np
import pandas as pd
from src.excel_content import ExcelContent
import decimal
import locale


ADDRESS_EXPECTED = "\n".join(
    [
        "Kunde Hans Mustermann GmbH",
        "Frau Mustermann",
        "Musterstr. 10",
        "12345 Musterstadt",
    ]
)

POSITIONS_EXPECTED = np.array(
    [
        ["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe"],
        [
            "1",
            "01.01.2024",
            "WhatsApp wg. Netzteil für USB-Server",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
        ],
        [
            "2",
            "02.01.2024",
            "Telefonat wg. KVSiServer (steht in der Doku)",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
        ],
        [
            "3",
            "03.01.2024",
            "Telefonat wg. KVSiServer (steht in der Doku)",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
        ],
        [
            "4",
            "03.01.2024",
            "Bewerbungsgespräch mit Frau A und B",
            "2",
            "h",
            "75,00 €",
            "150,00 €",
        ],
        [
            "5",
            "04.01.2024",
            "Email wg. Herrn R Anmeldung im AWS \
(hat versucht sich anzumelden mehr als \
120 Tage vor Beginn der Reha, steht in der Logdatei im W2k19-fs)",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
        ],
        [
            "6",
            "05.01.2024",
            "Anmeldung im AWS von Patienten mit falscher \
MassnahmeID verbessert. Gemäß Email Fr. S.",
            "1",
            "h",
            "75,00 €",
            "75,00 €",
        ],
        [
            "7",
            "11.01.2024",
            "Änderung Rehaziele im AWS und KVS-React gemäß \
Besprechung mit Frau S vom 01.12.2023",
            "7",
            "h",
            "75,00 €",
            "525,00 €",
        ],
        [
            "8",
            "11.01.2024",
            "Email von Hrn F. bezüglich Anpassung Rechnungsnummern: \
An Herrn K verwiesen",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
        ],
        [
            "9",
            "18.01.2024",
            "Prüfung der Anmeldungen im AWS nach Email vom 17.01.2024 \
von Hrn. F",
            "1",
            "h",
            "75,00 €",
            "75,00 €",
        ],
        [
            "10",
            "18.01.2024",
            "Email von Hrn. F bzgl. KVS Downtime und Funktion im Saal. \
(Kein KVS, keine Funktion im Saal)",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
        ],
        [
            "11",
            "",
            "Anfahrt dazu",
            "0,5",
            "h",
            "75,00 €",
            "37,50 €",
        ]
    ]
)


class TestExcelContent(TestCase):
    """TestClass for Excel Content"""

    def setUp(self) -> None:
        self.fn = "TestRechnung.xlsx"
        self.dir = "."
        self.path = os.path.join(self.dir, self.fn)
        self.xlsx = ExcelContent(self.fn, self.dir)
        return super().setUp()

    def test_read_sheet_list(self):
        """
        Teste, ob der Inhalt einer Excel-Datei gelesen werden kann
        """
        expected = ["Tabelle1", "Rechnung2", "Rechnung für Kleinunternehmen"]
        retval = self.xlsx.read_sheet_list()
        # print (retval)
        self.assertEqual(retval, expected,
                         "Excel File should contain expected sheets")

    def test_read_sheet(self):
        """
        Lies ein Sheet aus der Excel Datei als dataFrame
        """
        self.xlsx.read_sheet("Rechnung2")
        # print(retval)
        if self.xlsx and self.xlsx.daten is not None:
            self.assertGreater(len(self.xlsx.daten), 0,
                               "Should contain any content")

    def test_get_invoice_number(self):
        """Lies die Rechnungsnummer aus dem Excel Sheet aus"""
        self.xlsx.read_sheet("Rechnung2")
        expected = 20240001
        retval = self.xlsx.get_invoice_number()
        # print(retval)
        self.assertEqual(retval[list(retval.keys())[0]], expected,
                         "should be equal")

    def test_get_address_of_customer(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        MSG = "should be equal"
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        self.xlsx.get_address_of_customer()
        # print(value)
        self.assertEqual(self.xlsx.customer.anschrift, expected, MSG)

    def test__search_anschrift(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        MSG = "should be equal"
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        self.xlsx._search_anschrift("An:")  # pylint: disable=protected-access
        # print(value)
        self.assertEqual(self.xlsx.customer.anschrift, expected, MSG)

    def test__search_anschrift_object(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet in das Adresse Objekt
        """
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        exp_arr = expected.split('\n')
        MSG = "should be equal"
        self.xlsx._search_anschrift("An:")  # pylint: disable=protected-access
        # print(value)
        self.assertEqual(self.xlsx.customer.anschrift, expected, MSG)
        # print(repr(kunde))
        self.assertEqual(self.xlsx.customer.anschrift_line1, exp_arr[0], MSG)
        self.assertEqual(self.xlsx.customer.adresszusatz, exp_arr[1], MSG)
        self.assertEqual(self.xlsx.customer.strasse, exp_arr[2].split(' ')[0],
                         MSG)
        self.assertEqual(self.xlsx.customer.hausnummer,
                         exp_arr[2].split(' ')[1], MSG)
        self.assertEqual(self.xlsx.customer.plz, exp_arr[3].split(' ')[0], MSG)
        self.assertEqual(self.xlsx.customer.ort, exp_arr[3].split(' ')[1], MSG)
        self.assertEqual(self.xlsx.customer.landeskennz, 'DE', MSG)

    def test__get_index_of_nan(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        if self.xlsx.daten is not None:
            an = self.xlsx.daten["An:"]
            nan_idx = self.xlsx\
                ._get_index_of_nan(  # pylint: disable=protected-access
                    an
                )
            value = "\n".join(an[0:nan_idx])
            # print(value)
            self.assertEqual(value, expected, "should be equal")

    def test_get_invoice_positions(self):
        """Lies den Inhalt der Positionen"""

        self.xlsx.read_sheet("Rechnung2")
        expected = POSITIONS_EXPECTED
        value = self.xlsx.get_invoice_positions()
        MSG = "should be equal"
        print(value)
        # self.assertEqual(value.ndim, expected.ndim, "should be equal")
        self.assertTrue(np.array_equiv(value['daten'], expected), MSG)
        # type: ignore

    def test__split_dataframe_by_search_value(self):
        """Lies den Inhalt der Positionen"""

        self.xlsx.read_sheet("Rechnung2")
        expected = POSITIONS_EXPECTED
        value = self.xlsx._split_dataframe_by_search_value(
                "An:", "Pos."
            )  # pylint: disable=protected-access
        # ['daten']
        self.xlsx._change_values_to_german(value)
        test = np.r_[
            [
                ["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis",
                 "Summe"]
            ],
            value.astype(str).values]

        # self.assertEqual(value.ndim, expected.ndim, "should be equal")
        self.assertTrue(np.array_equiv(test, expected), "should be equal")
        # type: ignore

    def test__split_dataframe_by_search_value_unknown_column(self):
        """soll einen ValueError liefern"""
        self.xlsx.read_sheet("Rechnung2")
        with self.assertRaises(ValueError):
            self.xlsx._split_dataframe_by_search_value(
                "Daneben", "Pos."
            )
        try:
            self.xlsx._split_dataframe_by_search_value(
                "An:", "Pos."
            )
        except ValueError:
            self.fail('raised ValueError unexpectedly!')

    def test__split_dataframe_by_search_value_unknown_search(self):
        """soll einen ValueError liefern"""
        self.xlsx.read_sheet("Rechnung2")
        with self.assertRaises(ValueError):
            self.xlsx._split_dataframe_by_search_value(
                "An:", "Falscher Suchstring"
            )
        try:
            self.xlsx._split_dataframe_by_search_value(
                "An:", "Pos."
            )
        except ValueError:
            self.fail('raised ValueError unexpectedly!')

    def test_get_invoice_sums(self):
        """Lies die Summen aus dem Excel Sheet"""
        self.xlsx.read_sheet("Rechnung2")
        expected = "994,50 €"
        retval = self.xlsx.get_invoice_sums()
        # print(retval)
        self.assertEqual(retval[0][1], expected, "should be equal")

    def test_search_cell_right_of(self):
        """Lies die Summen aus dem Excel Sheet"""
        sums = "Unnamed: 5"
        self.xlsx.read_sheet("Rechnung2")
        expected = "1.183,46"
        with decimal.localcontext() as ctx:
            # locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
            ctx.rounding = decimal.ROUND_05UP
            _value = decimal.Decimal(self.xlsx
                                     .search_cell_right_of(sums,
                                                           'Bruttobetrag'))\
                .quantize(decimal.Decimal('1.00', ctx))
            _brutto = locale.format_string('%0.2f', _value, grouping=True)
        # print(retval)
        self.assertEqual(_brutto, expected, "should be equal")

    def test_search_cell_right_of_unknown_search_value(self):
        """Lies die Summen aus dem Excel Sheet"""
        sums = "Unnamed: 5"
        self.xlsx.read_sheet("Rechnung2")
        # print(retval)
        with self.assertRaises(ValueError):
            float(self.xlsx
                  .search_cell_right_of(sums, 'Bruttobeträgli'))
        try:
            float(self.xlsx
                  .search_cell_right_of(sums, 'Bruttobetrag'))
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_search_cell_right_of_unknown_column(self):
        """Lies die Summen aus dem Excel Sheet"""
        sums = "Falsche Spalte"
        self.xlsx.read_sheet("Rechnung2")
        # print(retval)
        with self.assertRaises(ValueError):
            float(self.xlsx
                  .search_cell_right_of(sums, 'Bruttobetrag'))
        sums = "Unnamed: 5"
        try:
            float(self.xlsx
                  .search_cell_right_of(sums, 'Bruttobetrag'))
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_get_maxLengths(self):
        """
        teste die Maximalen Längen eines DataFrames
        """
        lenArr = self.xlsx.get_maxlengths(
            pd.DataFrame(data=POSITIONS_EXPECTED[1:],
                         columns=POSITIONS_EXPECTED[0]))
        MSG = 'should be equal'
        self.assertEqual(lenArr, [4, 10, 138, 6, 7, 7, 8], MSG)

# if __name__ == "__main__":
#     unittest.main()
