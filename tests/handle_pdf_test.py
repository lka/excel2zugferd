"""
Modul handle_pdf_test
"""

import os
from pathlib import Path
import unittest
import numpy as np
import src.handle_pdf as handle_pdf
from src.excel_content import ExcelContent

# Tabellenblatt 3 (Index) "Rechnung div. Steuern" in TestRechnung.xlsx
POSITIONS_DIV_STEUERN_EXPECTED = np.array(
    [
        ["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe", "Steuer"],
        [
            "1",
            "01.01.2024",
            "WhatsApp wg. Netzteil für USB-Server",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
            "1",
        ],
        [
            "2",
            "02.01.2024",
            "Telefonat wg. KVSiServer (steht in der Doku)",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
            "1",
        ],
        ["3", "03.01.2024", "Taxifahrt", "1", "Stk.", "55,00 €", "55,00 €", "2"],
        [
            "4",
            "03.01.2024",
            "Bewerbungsgespräch mit Frau A und B",
            "2",
            "h",
            "75,00 €",
            "150,00 €",
            "1",
        ],
        [
            "5",
            "04.01.2024",
            "Email wg. Herrn R Anmeldung im AWS (hat versucht sich anzumelden mehr als 120 Tage vor Beginn der Reha, steht in der Logdatei im W2k19-fs)",
            "1",
            "10 Min.",
            "22,00 €",
            "22,00 €",
            "1",
        ],
        [
            "6",
            "05.01.2024",
            "Anmeldung im AWS von Patienten mit falscher MassnahmeID verbessert. Gemäß Email Fr. S.",
            "1",
            "h",
            "75,00 €",
            "75,00 €",
            "1",
        ],
        [
            "7",
            "11.01.2024",
            "Änderung Rehaziele im AWS und KVS-React gemäß Besprechung mit Frau S vom 01.12.2023",
            "7",
            "h",
            "75,00 €",
            "525,00 €",
            "1",
        ],
        ["8", "11.01.2024", "TÜV", "1", "Stk.", "130,00 €", "130,00 €", "3"],
        [
            "9",
            "18.01.2024",
            "Prüfung der Anmeldungen im AWS nach Email vom 17.01.2024 von Hrn. F",
            "1",
            "h",
            "75,00 €",
            "75,00 €",
            "1",
        ],
        ["10", "", "Anfahrt dazu per Taxi", "1", "Stk.", "96,00 €", "96,00 €", "2"],
        [
            "11",
            "18.01.2024",
            "Programmiertätigkeiten",
            "5",
            "AW",
            "22,00 €",
            "110,00 €",
            "1",
        ],
    ]
)


class TestHandlePdf(unittest.TestCase):
    """
    Test Class for handling pdf
    """

    def setUp(self) -> None:
        self.pdf = handle_pdf.Pdf()
        return super().setUp()

    def test_get_invoice_positions_div_steuern(self):
        """
        Positionen aus Tabellenblatt 3 (mit Steuer-Spalte) müssen im
        Rückgabewert dieselben Daten wie in der Tabelle enthalten
        """
        xlsx = ExcelContent("TestRechnung.xlsx", ".")
        xlsx.read_sheet(3)
        positions = xlsx.get_invoice_positions()
        value = self.pdf.get_invoice_positions(positions)
        self.assertEqual(
            value["daten"].tolist(),
            POSITIONS_DIV_STEUERN_EXPECTED.tolist(),
            "should be equal",
        )
        self.assertEqual(
            value["maxlengths"], [4, 10, 138, 6, 7, 8, 8, 6], "should be equal"
        )

    def test_uniquify(self):
        """
        Check whether uniquify counts up filename if file already exists
        """
        fn = "testUniquify.pdf"
        expected = "testUniquify (1).pdf"
        try:
            Path(fn).touch()
        except OSError:
            pass
        retval = self.pdf.uniquify(fn)
        self.assertEqual(retval, expected, "should be equal")
        try:
            os.remove(fn)
        except OSError:
            pass

    def test_uniquify_appendix(self):
        """
        Check whether uniquify counts up filename if file already exists
        """
        fn = "testUniquify.pdf"
        expected = "testUniquify_E.pdf"
        try:
            Path(fn).touch()
        except OSError:
            pass
        retval = self.pdf.uniquify(fn, "_E")
        self.assertEqual(retval, expected, "should be equal")
        try:
            os.remove(fn)
        except OSError:
            pass

    def test_uniquify_appendix_with_already_existant_appendix(self):
        """
        Check whether uniquify counts up filename if file already exists
        without appending already existant appendix
        """
        fn = "testUniquify_E.pdf"
        expected = "testUniquify_E (1).pdf"
        try:
            Path(fn).touch()
        except OSError:
            pass
        retval = self.pdf.uniquify(fn, "_E")
        self.assertEqual(retval, expected, "should be equal")
        try:
            os.remove(fn)
        except OSError:
            pass


# if __name__ == "__main__":
#     unittest.main()
