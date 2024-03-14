"""
Modul excel_content_test
"""

from unittest import TestCase
import os
import numpy as np
from excel_content import ExcelContent

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
            "Email wg. Herrn R Anmeldung im AWS (hat versucht sich anzumelden mehr als \
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
            "Änderung Rehaziele im AWS und KVS-React gemäß Besprechung mit Frau S vom 01.12.2023",
            "7",
            "h",
            "75,00 €",
            "525,00 €",
        ],
        [
            "8",
            "11.01.2024",
            "Email von Hrn F. bezüglich Anpassung Rechnungsnummern: An Herrn K verwiesen",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
        ],
        [
            "9",
            "18.01.2024",
            "Prüfung der Anmeldungen im AWS nach Email vom 17.01.2024 von Hrn. F",
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
        expected = ["Tabelle1", "Rechnung2"]
        retval = self.xlsx.read_sheet_list()
        # print (retval)
        self.assertEqual(retval, expected, "Excel File should contain expected sheets")

    def test_read_sheet(self):
        """
        Lies ein Sheet aus der Excel Datei als dataFrame
        """
        self.xlsx.read_sheet("Rechnung2")
        # print(retval)
        if self.xlsx and self.xlsx.daten is not None:
            self.assertGreater(len(self.xlsx.daten), 0, "Should contain any content")

    def test_get_invoice_number(self):
        """Lies die Rechnungsnummer aus dem Excel Sheet aus"""
        self.xlsx.read_sheet("Rechnung2")
        expected = 20240001
        retval = self.xlsx.get_invoice_number()
        # print(retval)
        self.assertEqual(retval[list(retval.keys())[0]], expected, "should be equal")

    def test_get_address_of_customer(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        value = self.xlsx.get_address_of_customer()
        # print(value)
        self.assertEqual(value, expected, "should be equal")

    def test__search_anschrift(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        value = self.xlsx._search_anschrift("An:")  # pylint: disable=protected-access
        # print(value)
        self.assertEqual(value, expected, "should be equal")

    def test__get_index_of_nan(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        if self.xlsx.daten is not None:
            an = self.xlsx.daten["An:"]
            nan_idx = self.xlsx._get_index_of_nan(  # pylint: disable=protected-access
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
        # print(value)
        # self.assertEqual(value.ndim, expected.ndim, "should be equal")
        self.assertTrue(np.array_equiv(value, expected), "should be equal")  # type: ignore

    def test__split_dataframe_by_search_value(self):
        """Lies den Inhalt der Positionen"""

        self.xlsx.read_sheet("Rechnung2")
        expected = POSITIONS_EXPECTED
        value = self.xlsx._split_dataframe_by_search_value(  # pylint: disable=protected-access
            "An:", "Pos."
        )
        # print(value)
        # self.assertEqual(value.ndim, expected.ndim, "should be equal")
        self.assertTrue(np.array_equiv(value, expected), "should be equal")  # type: ignore

    def test_get_invoice_sums(self):
        """Lies die Summen aus dem Excel Sheet"""
        self.xlsx.read_sheet("Rechnung2")
        expected = "957,00 €"
        retval = self.xlsx.get_invoice_sums()
        # print(retval)
        self.assertEqual(retval[0][1], expected, "should be equal")

    def test_search_cell_right_of(self):
        """Lies die Summen aus dem Excel Sheet"""
        sums = "Unnamed: 5"
        self.xlsx.read_sheet("Rechnung2")
        expected = "1138,83 €"
        retval = f"{float(self.xlsx.search_cell_right_of(sums, 'Bruttobetrag')):.2f} €".replace(
            ".", ","
        )
        # print(retval)
        self.assertEqual(retval, expected, "should be equal")


# if __name__ == "__main__":
#     unittest.main()
