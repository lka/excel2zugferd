import unittest
import os
import excelContent
import numpy as np

adressExpected = "\n".join(
    [
        "Kunde Hans Mustermann GmbH",
        "Frau Mustermann",
        "Musterstr. 10",
        "12345 Musterstadt",
    ]
)

posistionsExpected = np.array(
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
            "Anmeldung im AWS von Patienten mit falscher MassnahmeID verbessert. Gemäß Email Fr. S.",
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
            "Email von Hrn. F bzgl. KVS Downtime und Funktion im Saal. (Kein KVS, keine Funktion im Saal)",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
        ],
    ]
)


class test_ExcelContent(unittest.TestCase):
    def setUp(self) -> None:
        self.fn = 'TestRechnung.xlsx'
        self.dir = '.'
        self.path = os.path.join(self.dir, self.fn)
        self.xlsx = excelContent.ExcelContent(self.fn, self.dir)
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_readSheetList(self):
        """
        Teste, ob der Inhalt einer Excel-Datei gelesen werden kann
        """
        expected = ['Tabelle1', 'Rechnung2']
        retVal = self.xlsx.readSheetList()
        # print (retVal)
        self.assertEqual(retVal, expected, "Excel File should contain expected sheets")

    def test_readSheet(self):
        """
        Lies ein Sheet aus der Excel Datei als dataFrame
        """
        self.xlsx.readSheet('Rechnung2')
        # print(retVal)
        self.assertGreater(len(self.xlsx.daten), 0, 'Should contain any content')

    def test_getInvoiceNumber(self):
        """Lies die Rechnungsnummer aus dem Excel Sheet aus"""
        self.xlsx.readSheet("Rechnung2")
        expected = 20240001
        retVal = self.xlsx.getInvoiceNumber()
        # print(retVal)
        self.assertEqual(retVal[list(retVal.keys())[0]], expected, "should be equal")

    def test_getAddressOfCustomer(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        self.xlsx.readSheet("Rechnung2")
        expected = adressExpected
        value = self.xlsx.getAddressOfCustomer()
        # print(value)
        self.assertEqual(value, expected, "should be equal")

    def test__searchAnschrift(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        self.xlsx.readSheet("Rechnung2")
        expected = adressExpected
        value = self.xlsx._searchAnschrift('An:')
        # print(value)
        self.assertEqual(value, expected, "should be equal")

    def test__getIndexOfNextNaN(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        self.xlsx.readSheet("Rechnung2")
        expected = adressExpected
        an = self.xlsx.daten["An:"]
        nan_idx = self.xlsx._getIndexOfNextNaN(an)
        value = "\n".join(an[0:nan_idx])
        # print(value)
        self.assertEqual(value, expected, "should be equal")

    def test_getInvoicePositions(self):
        """Lies den Inhalt der Positionen"""

        self.xlsx.readSheet("Rechnung2")
        expected = posistionsExpected
        value = self.xlsx.getInvoicePositions()
        # print(value)
        # self.assertEqual(value.ndim, expected.ndim, "should be equal")
        self.assertTrue(np.array_equiv(value, expected), "should be equal")

    def test__split_dataframe_by_SearchValue(self):
        """Lies den Inhalt der Positionen"""

        self.xlsx.readSheet("Rechnung2")
        expected = posistionsExpected
        value = self.xlsx._split_dataframe_by_SearchValue("An:", "Pos.")
        # print(value)
        # self.assertEqual(value.ndim, expected.ndim, "should be equal")
        self.assertTrue(np.array_equiv(value, expected), "should be equal")

    def test_getInvoiceSums(self):
        """Lies die Summen aus dem Excel Sheet"""
        self.xlsx.readSheet("Rechnung2")
        expected = "957,00 €"
        retVal = self.xlsx.getInvoiceSums()
        # print(retVal)
        self.assertEqual(retVal[0][1], expected, "should be equal")

    def test__searchCellRightOf(self):
        """Lies die Summen aus dem Excel Sheet"""
        SUMS = "Unnamed: 5"
        self.xlsx.readSheet("Rechnung2")
        expected = "1138,83 €"
        retVal = "{:.2f} €".format(
            float(self.xlsx._searchCellRightOf(SUMS, "Bruttobetrag"))
        ).replace(".", ",")
        # print(retVal)
        self.assertEqual(retVal, expected, "should be equal")


if __name__ == '__main__':
    unittest.main()
