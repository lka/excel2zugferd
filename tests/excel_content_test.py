"""
Modul excel_content_test
"""

from unittest import TestCase
from datetime import datetime, time
import os
from types import SimpleNamespace
import numpy as np
import pandas as pd
from src.excel_content import ExcelContent
from src.invoice_collection import InvoiceCollection
from src.kunde import Kunde
import src.handle_pdf as pdf
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
        ],
        [
            "12",
            "18.01.2024",
            "Programmiertätigkeiten",
            "5",
            "AW",
            "22,00 €",
            "110,00 €",
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
        expected = ["Tabelle1", "Rechnung2", "Rechnung für Kleinunternehmen", "Rechnung div. Steuern",
            "Gutschriftanzeige", "Gutschriftanzeige negativ", "Korrekturrechnung"]
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

    def test_get_invoice_number_at_spalte_zeile(self):
        """Lies die Rechnungsnummer aus dem Excel Sheet aus"""
        self.xlsx.read_sheet("Rechnung2")
        expected = 20240001
        retval = self.xlsx.get_invoice_number(spalte="B", zeile="7")
        # print(retval)
        self.assertEqual(retval[list(retval.keys())[0]], expected, "should be equal")

    def test_get_invoice_date_found(self):
        """Lies das Rechnungsdatum aus dem Excel Sheet aus"""
        self.xlsx.read_sheet("Rechnung2")
        expected = datetime(2024, 1, 30, 0, 0)
        retval = self.xlsx.get_invoice_date()
        print(retval)
        self.assertEqual(retval[list(retval.keys())[0]], expected, "should be equal")

    def test_get_invoice_date_not_found(self):
        """Lies das Rechnungsdatum aus dem Excel Sheet aus"""
        self.xlsx.read_sheet("Rechnung2")
        today = datetime.now()
        expected = datetime.combine(today.date(), time.min)
        retval = self.xlsx.get_invoice_date(spalte="C")
        print(retval)
        self.assertEqual(retval[list(retval.keys())[0]], expected, "should be equal")

    def test_get_invoice_date_not_found_with_zeile(self):
        """Lies das Rechnungsdatum aus dem Excel Sheet aus"""
        self.xlsx.read_sheet("Rechnung2")
        expected = datetime(2024, 1, 30, 0, 0)
        # retval = self.xlsx.get_invoice_date(spalte="A", zeile="8")
        with self.assertRaises(ValueError):
            self.xlsx.get_invoice_date(spalte="D", zeile="8")
        try:
            retval = self.xlsx.get_invoice_date(spalte="B", zeile="8")
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

        print(retval)
        self.assertEqual(retval[list(retval.keys())[0]], expected, "should be equal")

    def test_get_address_of_customer(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        MSG = "should be equal"
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        customer = Kunde()
        self.xlsx.get_address_of_customer(customer=customer)
        # print(value)
        self.assertEqual(customer.anschrift, expected, MSG)

    def test__search_anschrift(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        MSG = "should be equal"
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        customer = Kunde()
        self.xlsx._search_anschrift(
            "A", None, "An:", customer=customer
        )  # pylint: disable=protected-access
        # print(customer.anschrift)
        self.assertEqual(customer.anschrift, expected, MSG)

    def test__search_anschrift_Spalte_Zeile(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        MSG = "should be equal"
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        customer = Kunde()
        self.xlsx._search_anschrift(
            "A", "2", "An:", customer=customer
        )  # pylint: disable=protected-access
        # print(customer.anschrift)
        self.assertEqual(customer.anschrift, expected, MSG)

    def test__search_anschrift_object(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet in das Adresse Objekt
        """
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        exp_arr = expected.splitlines()
        MSG = "should be equal"
        customer = Kunde()
        self.xlsx._search_anschrift(
            "A", None, "An:", customer=customer
        )  # pylint: disable=protected-access
        # print(value)
        self.assertEqual(customer.anschrift, expected, MSG)
        # print(repr(kunde))
        self.assertEqual(customer.betriebsbezeichnung, exp_arr[0], MSG)
        self.assertEqual(customer.name, exp_arr[1], MSG)
        self.assertEqual(customer.strasse, exp_arr[2].split(" ")[0], MSG)
        self.assertEqual(customer.hausnummer, exp_arr[2].split(" ")[1], MSG)
        self.assertEqual(customer.plz, exp_arr[3].split(" ")[0], MSG)
        self.assertEqual(customer.ort, exp_arr[3].split(" ")[1], MSG)
        self.assertEqual(customer.landeskennz, "DE", MSG)

    def test__get_index_of_nan(self):
        """
        Lies die Anschrift des Kunden aus dem Excel Sheet
        """
        self.xlsx.read_sheet("Rechnung2")
        expected = ADDRESS_EXPECTED
        if self.xlsx.daten is not None:
            an = self.xlsx.daten["A"]
            fromIdx = self.xlsx.daten.index[an == "An:"].tolist()[0]  # + 1
            nan_idx = self.xlsx._get_index_of_nan(  # pylint: disable=protected-access
                an
            )
            value = "\n".join(an[fromIdx:nan_idx])
            # print(value)
            self.assertEqual(value, expected, "should be equal")

    def test_get_invoice_positions(self):
        """Lies den Inhalt der Positionen"""

        self.xlsx.read_sheet("Rechnung2")
        expected = POSITIONS_EXPECTED
        retval = self.xlsx.get_invoice_positions()
        myPdf = pdf.Pdf()
        value = myPdf.get_invoice_positions(retval)
        MSG = "should be equal"
        # print(value)
        # self.assertEqual(value.ndim, expected.ndim, "should be equal")
        self.assertTrue(np.array_equiv(value["daten"], expected), MSG)
        # type: ignore

    def test_get_tax_values_without_sheet(self):
        """ohne gelesenes Tabellenblatt soll ein leeres dict geliefert werden"""
        self.assertEqual(self.xlsx.get_tax_values(), {}, "should be equal")

    def test_get_tax_values_unknown_search_value(self):
        """bei unbekanntem Suchwert soll ein leeres dict geliefert werden"""
        self.xlsx.read_sheet(3)
        retval = self.xlsx.get_tax_values(search="gibt es nicht")
        self.assertEqual(retval, {}, "should be equal")

    def test_get_tax_values_unknown_column(self):
        """bei unbekannter Spalte soll ein ValueError ausgelöst werden"""
        self.xlsx.read_sheet(3)
        with self.assertRaises(ValueError):
            self.xlsx.get_tax_values(spalte="Z")

    def test_get_tax_values_div_steuern(self):
        """
        Tabellenblatt 3 (Index) "Rechnung div. Steuern": die Zeilen unter
        "Umsatzsteueraufschlüsselung:" in Spalte E: die Nummer der Steuerart
        (Spalte E) ist der Schlüssel, der Wert ist die Liste
        [Steuersatz (F), Nettobetrag (G), Steuerbetrag oder Begründung (H)]
        Die Daten stammen aus der festen Testdatei testdaten_steuern.xlsx.
        """
        xlsx = ExcelContent(
            os.path.join(os.path.dirname(__file__), "testdaten_steuern.xlsx"), "."
        )
        xlsx.read_sheet(3)
        expected = {
            1: [0.19, 1001, 190.19],
            2: [0.07, 151, 10.57],
            3: [0, 130, "Durchlaufender Posten im Sinne von § 10 Abs. 1 Satz 6 UStG"],
            4: [0, 150, "Steuerfreie Bildungsleistung gemäß § 4 Nr. 21 UStG"],
        }
        retval = xlsx.get_tax_values()
        self.assertEqual(retval, expected, "should be equal")

    def _read_div_steuern(self) -> ExcelContent:
        xlsx = ExcelContent(
            os.path.join(os.path.dirname(__file__), "testdaten_steuern.xlsx"), "."
        )
        xlsx.read_sheet(3)
        return xlsx

    def test_get_tax_values_with_zeile(self):
        """mit zeile und spalte müssen dieselben Werte wie über search kommen"""
        xlsx = self._read_div_steuern()
        header = xlsx._search_cell_in_column("E", "Umsatzsteueraufschlüsselung:")
        first_row = int(header.index[0]) + 1
        retval = xlsx.get_tax_values(spalte="E", zeile=str(first_row))
        self.assertEqual(retval, xlsx.get_tax_values(), "should be equal")
        self.assertEqual(len(retval), 4, "should be equal")

    def test_get_tax_values_with_mgmnt(self):
        """zeile und spalte aus mgmnt haben Vorrang vor search"""
        xlsx = self._read_div_steuern()
        header = xlsx._search_cell_in_column("E", "Umsatzsteueraufschlüsselung:")
        mgmnt = SimpleNamespace(
            umsatzsteueraufschluesselung_zeile=str(int(header.index[0]) + 1), umsatzsteueraufschluesselung_spalte="E"
        )
        retval = xlsx.get_tax_values(spalte="Z", mgmnt=mgmnt, search="gibt es nicht")
        self.assertEqual(retval, xlsx.get_tax_values(), "should be equal")

    def test_get_tax_values_unknown_zeile(self):
        """eine nicht vorhandene Zeile soll einen ValueError auslösen"""
        xlsx = self._read_div_steuern()
        with self.assertRaises(ValueError):
            xlsx.get_tax_values(spalte="E", zeile="9999")

    def _xlsx_with_storno(self, rows: list) -> ExcelContent:
        """ExcelContent ohne Datei, Sheet aus rows (Spalten A..E, Zeilen ab 1)"""
        xlsx = ExcelContent("gibt_es_nicht.xlsx", ".")
        xlsx.daten = pd.DataFrame(
            rows, columns=list("ABCDE"), index=range(1, len(rows) + 1)
        )
        return xlsx

    def test_get_storno_values_gutschrift(self):
        """Suche über den Code (Feld 2) in der Spalte rechts von spalte"""
        xlsx = self._xlsx_with_storno(
            [
                ["Rechnung", np.nan, np.nan, np.nan, np.nan],
                ["Gutschrift", 381.0, 20240001.0, datetime(2024, 1, 30), np.nan],
            ]
        )
        self.assertEqual(
            xlsx.get_storno_values(),
            ["Gutschrift", 381, "20240001", "30.01.2024"],
            "should be equal",
        )

    def test_get_storno_values_korrekturrechnung(self):
        """variabler Text in Feld 1, Code 384, Strings bleiben Strings"""
        xlsx = self._xlsx_with_storno(
            [["Korrekturrechnung", 384, "RG-17", "15.12.2023", np.nan]]
        )
        self.assertEqual(
            xlsx.get_storno_values(),
            ["Korrekturrechnung", 384, "RG-17", "15.12.2023"],
            "should be equal",
        )

    def test_get_storno_values_other_spalte(self):
        """mit spalte='C' stehen die Felder in C bis F"""
        xlsx = self._xlsx_with_storno(
            [[np.nan, np.nan, "Gutschrift", 381, "RG-1"]]
        )
        xlsx.daten["F"] = "01.01.2024"
        self.assertEqual(
            xlsx.get_storno_values(spalte="C"),
            ["Gutschrift", 381, "RG-1", "01.01.2024"],
            "should be equal",
        )

    def test_get_storno_values_not_found(self):
        """kein Code vorhanden: None"""
        xlsx = self._xlsx_with_storno([["Rechnung", np.nan, np.nan, np.nan, np.nan]])
        self.assertIsNone(xlsx.get_storno_values(), "should be None")

    def test_get_storno_values_without_sheet(self):
        """ohne Sheet: None"""
        self.assertIsNone(self.xlsx.get_storno_values(), "should be None")

    def test_get_storno_values_with_zeile(self):
        """mit zeile wird direkt in dieser Zeile gelesen"""
        xlsx = self._xlsx_with_storno(
            [
                ["x", 999, "x", "x", np.nan],
                ["Gutschrift", 381, "RG-1", "01.01.2024", np.nan],
            ]
        )
        self.assertEqual(
            xlsx.get_storno_values(zeile="2"),
            ["Gutschrift", 381, "RG-1", "01.01.2024"],
            "should be equal",
        )

    def test_get_storno_values_with_zeile_empty_code(self):
        """mit zeile, aber leerem Code: None"""
        xlsx = self._xlsx_with_storno([[np.nan] * 5])
        self.assertIsNone(xlsx.get_storno_values(zeile="1"), "should be None")

    def test_get_storno_values_with_zeile_invalid_code(self):
        """mit zeile und unbekanntem Code: ValueError"""
        xlsx = self._xlsx_with_storno([["Gutschrift", 123, "RG-1", "x", np.nan]])
        with self.assertRaises(ValueError):
            xlsx.get_storno_values(zeile="1")

    def test_get_storno_values_empty_invoice_number_is_switch(self):
        """leere Rechnungsnummer: kein Storno, None ohne Fehler"""
        xlsx = self._xlsx_with_storno([["Gutschrift", 381, np.nan, "x", np.nan]])
        self.assertIsNone(xlsx.get_storno_values(), "should be None")
        self.assertIsNone(xlsx.get_storno_values(zeile="1"), "should be None")
        xlsx = self._xlsx_with_storno([["Gutschrift", 123, "  ", "x", np.nan]])
        self.assertIsNone(xlsx.get_storno_values(zeile="1"), "should be None")

    def test_get_storno_values_missing_date(self):
        """Rechnungsnummer gefüllt, Rechnungsdatum leer: ValueError"""
        xlsx = self._xlsx_with_storno([["Gutschrift", 381, "RG-1", np.nan, np.nan]])
        with self.assertRaises(ValueError):
            xlsx.get_storno_values()

    def test_get_storno_values_invalid_date_format(self):
        """Rechnungsdatum als Text nicht im Format TT.MM.JJJJ: ValueError"""
        for value in ("2024-02-01", "1.2.24", "gestern"):
            xlsx = self._xlsx_with_storno([["Gutschrift", 381, "RG-1", value, np.nan]])
            with self.assertRaises(ValueError, msg=value):
                xlsx.get_storno_values()

    def test_get_storno_values_date_with_spaces(self):
        """Leerzeichen um das Datum werden entfernt"""
        xlsx = self._xlsx_with_storno([["Gutschrift", 381, "RG-1", " 01.02.2024 ", np.nan]])
        self.assertEqual(xlsx.get_storno_values()[3], "01.02.2024", "should be equal")

    def test_get_storno_values_date_normalized(self):
        """einstellige Tage und Monate werden auf TT.MM.JJJJ ergänzt"""
        xlsx = self._xlsx_with_storno([["Gutschrift", 381, "RG-1", "1.2.2024", np.nan]])
        self.assertEqual(xlsx.get_storno_values()[3], "01.02.2024", "should be equal")

    def test_get_storno_values_with_zeile_empty_code_and_number(self):
        """mit zeile, Rechnungsnummer gefüllt, Code leer: ValueError"""
        xlsx = self._xlsx_with_storno([["Gutschrift", np.nan, "RG-1", "x", np.nan]])
        with self.assertRaises(ValueError):
            xlsx.get_storno_values(zeile="1")

    def test_get_storno_values_with_mgmnt(self):
        """storno_spalte und storno_zeile aus mgmnt haben Vorrang"""
        xlsx = self._xlsx_with_storno(
            [["Gutschrift", 381, "RG-1", "01.01.2024", np.nan]]
        )
        mgmnt = SimpleNamespace(storno_zeile="1", storno_spalte="A")
        self.assertEqual(
            xlsx.get_storno_values(spalte="Z", mgmnt=mgmnt),
            ["Gutschrift", 381, "RG-1", "01.01.2024"],
            "should be equal",
        )

    def test__to_number_text_with_comma(self):
        """Text mit Komma (auch mit Tausenderpunkt, €, Leerzeichen) wird zur Zahl"""
        cases = {
            "144,84": 144.84,
            "22,00 €": 22.0,
            "1.149,86 €": 1149.86,
            " 22 ": 22.0,
            "-10,5": -10.5,
            "22.5": 22.5,
            "1 234,50 €": 1234.5,
        }
        for text, expected in cases.items():
            self.assertEqual(self.xlsx._to_number(text), expected, text)

    def test__to_number_keeps_numbers_and_unreadable(self):
        """echte Zahlen, NaN, None und nicht lesbare Texte bleiben unverändert"""
        for value in (22, 22.5, -3, 0):
            self.assertEqual(self.xlsx._to_number(value), value, str(value))
        self.assertIs(type(self.xlsx._to_number(22)), int, "int should stay int")
        self.assertTrue(np.isnan(self.xlsx._to_number(np.nan)), "nan should stay nan")
        self.assertIsNone(self.xlsx._to_number(None), "None should stay None")
        for text in ("Preis", "abc", "", "1,2,3"):
            self.assertEqual(self.xlsx._to_number(text), text, text)

    def _xlsx_with_positions(self, rows: list) -> ExcelContent:
        header = ["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe"]
        data = [header] + rows + [[np.nan] * 7]
        xlsx = ExcelContent("gibt_es_nicht.xlsx", ".")
        xlsx.daten = pd.DataFrame(
            data, columns=list("ABCDEFG"), index=range(1, len(data) + 1)
        )
        return xlsx

    def test_get_invoice_positions_text_numbers(self):
        """Anzahl, Preis und Summe als Text mit Komma werden zu Zahlen"""
        xlsx = self._xlsx_with_positions(
            [
                [1, "x", "A", "2", "h", "144,84", "289,68 €"],
                [2, "x", "B", "1,5", "h", "10,00 €", "15,00 €"],
            ]
        )
        positions = xlsx.get_invoice_positions()
        self.assertEqual(positions["Anzahl"].tolist(), [2.0, 1.5], "should be equal")
        self.assertEqual(positions["Preis"].tolist(), [144.84, 10.0], "should be equal")
        self.assertEqual(positions["Summe"].tolist(), [289.68, 15.0], "should be equal")

    def test_get_invoice_positions_pure_numbers_unchanged(self):
        """reine Zahlen bleiben unverändert"""
        xlsx = self._xlsx_with_positions(
            [
                [1, "x", "A", 2, "h", 144.84, 289.68],
                [2, "x", "B", 1.5, "h", 10, 15],
            ]
        )
        positions = xlsx.get_invoice_positions()
        self.assertEqual(positions["Anzahl"].tolist(), [2, 1.5], "should be equal")
        self.assertEqual(positions["Preis"].tolist(), [144.84, 10], "should be equal")
        self.assertEqual(positions["Summe"].tolist(), [289.68, 15], "should be equal")
        # auch die Darstellung als Text (1 bleibt 1, nicht 1.0)
        self.assertEqual(positions["Anzahl"].astype(str).tolist(), ["2", "1.5"])
        self.assertEqual(positions["Summe"].astype(str).tolist(), ["289.68", "15"])

    def test_get_invoice_positions_only_text_columns_are_converted(self):
        """nur Spalten mit Text werden umgewandelt, Zahlenspalten bleiben wie sie sind"""
        xlsx = self._xlsx_with_positions(
            [
                [1, "x", "A", 1, "h", "10,5", 10],
                [2, "x", "B", 2, "h", "20", 40],
            ]
        )
        positions = xlsx.get_invoice_positions()
        self.assertEqual(positions["Anzahl"].astype(str).tolist(), ["1", "2"])
        self.assertEqual(positions["Summe"].astype(str).tolist(), ["10", "40"])
        self.assertEqual(positions["Preis"].tolist(), [10.5, 20.0], "should be equal")

    def test_get_invoice_positions_other_columns_unchanged(self):
        """Pos., Datum, Tätigkeit und Typ werden nicht angefasst"""
        xlsx = self._xlsx_with_positions([[1, "1,5", "Text 2,5", "2", "h", "1", "2"]])
        positions = xlsx.get_invoice_positions()
        self.assertEqual(
            positions.iloc[0, [0, 1, 2, 4]].tolist(), [1, "1,5", "Text 2,5", "h"]
        )

    def test_get_invoice_positions_text_numbers_with_mgmnt(self):
        """auch über feste Spalten (Steuerung) werden Text-Zahlen umgewandelt"""
        xlsx = self._xlsx_with_positions(
            [[1, "x", "A", "2", "h", "144,84", "289,68"]]
        )
        mgmnt = SimpleNamespace(
            positionen_zeile="1",
            pos_spalte="A", dat_spalte="B", desc_spalte="C", anz_spalte="D",
            typ_spalte="E", preis_spalte="F", sum_spalte="G", steuer_spalte=None,
        )
        positions = xlsx.get_invoice_positions(mgmnt=mgmnt)
        self.assertEqual(positions["Preis"].tolist(), [144.84], "should be equal")
        self.assertEqual(positions["Anzahl"].tolist(), [2.0], "should be equal")

    def test_get_invoice_positions_text_prices_pass_price_check(self):
        """Text-Preise lösen in der Preisprüfung keinen Fehler mehr aus"""
        xlsx = self._xlsx_with_positions(
            [[1, "x", "A", "2", "h", "144,84", "289,68"]]
        )
        InvoiceCollection()._check_prices(xlsx.get_invoice_positions())
        xlsx = self._xlsx_with_positions(
            [[1, "x", "A", "2", "h", "-144,84", "-289,68"]]
        )
        with self.assertRaises(ValueError):
            InvoiceCollection()._check_prices(xlsx.get_invoice_positions())

    def test__split_dataframe_by_search_value(self):
        """Lies den Inhalt der Positionen"""

        self.xlsx.read_sheet("Rechnung2")
        expected = POSITIONS_EXPECTED
        value = self.xlsx._split_dataframe_by_search_value(
            "A", "Pos."
        )  # pylint: disable=protected-access
        # ['daten']
        myPdf = pdf.Pdf()
        retval = myPdf._change_values_to_german(value)
        test = np.r_[
            [["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe"]],
            retval.astype(str).values,
        ]

        # self.assertEqual(value.ndim, expected.ndim, "should be equal")
        self.assertTrue(np.array_equiv(test, expected), "should be equal")
        # type: ignore

    def test__split_dataframe_by_search_value_unknown_column(self):
        """soll einen ValueError liefern"""
        self.xlsx.read_sheet("Rechnung2")
        with self.assertRaises(ValueError):
            self.xlsx._split_dataframe_by_search_value("Daneben", "Pos.")
        try:
            self.xlsx._split_dataframe_by_search_value("A", "Pos.")
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test__split_dataframe_by_search_value_unknown_search(self):
        """soll einen ValueError liefern"""
        self.xlsx.read_sheet("Rechnung2")
        with self.assertRaises(ValueError):
            self.xlsx._split_dataframe_by_search_value("A", "Falscher Suchstring")
        try:
            self.xlsx._split_dataframe_by_search_value("A", "Pos.")
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_get_invoice_sums(self):
        """Lies die Summen aus dem Excel Sheet"""
        self.xlsx.read_sheet("Rechnung2")
        expected = 1104.50
        retval = self.xlsx.get_invoice_sums()
        # print(retval)
        self.assertEqual(float(retval[0][1]), expected, "should be equal")

    def test_search_cell_right_of(self):
        """Lies die Summen aus dem Excel Sheet"""
        sums = "F"
        self.xlsx.read_sheet("Rechnung2")
        expected = "1.314,36"
        with decimal.localcontext() as ctx:
            # locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
            ctx.rounding = decimal.ROUND_HALF_UP
            _value = decimal.Decimal(
                self.xlsx.search_cell_right_of(sums, "Bruttobetrag") + 0.000000001
            ).quantize(decimal.Decimal("1.00", ctx))
            _brutto = locale.format_string("%0.2f", _value, grouping=True)
        # print(retval)
        self.assertEqual(_brutto, expected, "should be equal")

    def test_search_cell_right_of_unknown_search_value(self):
        """Lies die Summen aus dem Excel Sheet"""
        sums = "F"
        self.xlsx.read_sheet("Rechnung2")
        # print(retval)
        with self.assertRaises(ValueError):
            float(self.xlsx.search_cell_right_of(sums, "Bruttobeträgli"))
        try:
            float(self.xlsx.search_cell_right_of(sums, "Bruttobetrag"))
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_search_cell_right_of_unknown_column(self):
        """Lies die Summen aus dem Excel Sheet"""
        sums = "G"
        self.xlsx.read_sheet("Rechnung2")
        # print(retval)
        with self.assertRaises(ValueError):
            float(self.xlsx.search_cell_right_of(sums, "Bruttobetrag"))
        sums = "F"
        try:
            float(self.xlsx.search_cell_right_of(sums, "Bruttobetrag"))
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_get_maxLengths(self):
        """
        teste die Maximalen Längen eines DataFrames
        """
        myPdf = pdf.Pdf()
        lenArr = myPdf.get_maxlengths(
            pd.DataFrame(data=POSITIONS_EXPECTED[1:], columns=POSITIONS_EXPECTED[0])
        )
        MSG = "should be equal"
        self.assertEqual(lenArr, [4, 10, 138, 6, 7, 7, 8], MSG)

    def test_mapReducePositions(self):
        """
        Test of remapping and reducing positions in DataFrame
        """
        expected_columns = ["B", "D", "E", "F", "I", "G", "H"]
        expected = pd.DataFrame(
            data=(
                [
                    "1",
                    "01.01.2024",
                    "WhatsApp wg. Netzteil für USB-Server",
                    "1",
                    "10 Min.",
                    "22",
                    "22",
                ],
            ),
            columns=["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe"],
            index=[2],
        )
        entered = pd.DataFrame(
            data=(
                [
                    "unusable",
                    "Pos.",
                    "unusable",
                    "Datum",
                    "Tätigkeit",
                    "Anzahl",
                    "Preis",
                    "Summe",
                    "Typ",
                ],
                [
                    "NaN",
                    "1",
                    "NaN",
                    "01.01.2024",
                    "WhatsApp wg. Netzteil für USB-Server",
                    "1",
                    "22",
                    "22",
                    "10 Min.",
                ],
            ),
            columns=["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            index=[1, 2],
        )
        entered = entered.reindex([1, 2, 3])
        print("entered:\n", entered)
        retVal = self.xlsx.mapReducePositions(entered, expected_columns)
        print("retVal:\n", retVal)
        print("expected:\n", expected)
        self.assertTrue(expected.equals(retVal), "should be True")


# if __name__ == "__main__":
#     unittest.main()
