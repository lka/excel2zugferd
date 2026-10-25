"""Modul zugferd_test."""

# from locale import currency
from types import SimpleNamespace
import unittest

# import os
# from datetime import datetime, timedelta
import src.handle_zugferd as handle_zugferd
import src.handle_pdf as handle_pdf

# from src.handle_other_objects import Adresse
# from src.lieferant import Lieferant
import decimal


class TestZugFerd(unittest.TestCase):
    """Testclass for zugferd tests."""

    def setUp(self) -> None:
        self.zugferd = handle_zugferd.ZugFeRD()
        self.pdf = handle_pdf.Pdf()
        self.mydebug = None
        return super().setUp()

    @unittest.skip("not more necessary testing this")
    def test_modify_xml(self):
        """Test that xmlns:qdt is added."""
        xml = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\
<rsm:CrossIndustryInvoice xmlns:ram=\
"urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"\
 xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" \
xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100">\
  <rsm:ExchangedDocumentContext>\
    <ram:GuidelineSpecifiedDocumentContextParameter>\
      <ram:ID>urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended</ram:ID>\
    </ram:GuidelineSpecifiedDocumentContextParameter>\
  </rsm:ExchangedDocumentContext>\
</rsm:CrossIndustryInvoice>'.encode(
            "utf-8"
        )
        mod_xml = self.zugferd.modify_xml(xml).decode("utf-8")
        count = mod_xml.count("xmlns:qdt=")
        self.assertEqual(count, 1, "should only be 1")
        # self.assertIn('show me the content of mod_xml', mod_xml)

    @unittest.skip("not more necessary testing this")
    def test_modify_xml_already_in(self):
        """Test that xmlns:qdt is added"""
        xml = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\
<rsm:CrossIndustryInvoice xmlns:qdt=\
"urn:un:unece:uncefact:data:standard:QualifiedDataType:100" xmlns:ram=\
"urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"\
 xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" \
xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100">\
  <rsm:ExchangedDocumentContext>\
    <ram:GuidelineSpecifiedDocumentContextParameter>\
      <ram:ID>urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended</ram:ID>\
    </ram:GuidelineSpecifiedDocumentContextParameter>\
  </rsm:ExchangedDocumentContext>\
</rsm:CrossIndustryInvoice>'.encode(
            "utf-8"
        )
        mod_xml = self.zugferd.modify_xml(xml).decode("utf-8")
        count = mod_xml.count("xmlns:qdt=")
        self.assertEqual(count, 1, "should only be 1")
        # self.assertIn('show me the content of mod_xml', mod_xml)

    def test_add_items(self):
        """test that add_items doesn't throw any exception"""
        data = [
            ["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe"],
            [
                "1",
                "2024-01-01 00:00:00",
                "WhatsApp wg. Netzteil für USB-Server",
                "1",
                "10 Min.",
                "22",
                "22",
            ],
            [
                "2",
                "2024-01-02 00:00:00",
                "Telefonat wg. KVSiServer (steht in der Doku)",
                "1",
                "10 Min.",
                "22",
                "22",
            ],
            [
                "3",
                "2024-01-03 00:00:00",
                "Telefonat wg. KVSiServer (steht in der Doku)",
                "1",
                "10 Min.",
                "22",
                "22",
            ],
            [
                "4",
                "2024-01-03 00:00:00",
                "Bewerbungsgespräch mit Frau A und B",
                "2",
                "h",
                "75",
                "150",
            ],
            ["5", "", "Anfahrt dazu", "1", "h", "75", "75"],
        ]
        try:
            self.zugferd.add_items(data, "19.00")
        except Exception:
            self.fail("raised Exceptionr unexpectedly!")

    def test__collect_tax_free_position(self):
        """Pos. werden je Steuertyp in einer Liste gesammelt"""
        self.zugferd._collect_tax_free_position(3, "2")
        self.zugferd._collect_tax_free_position(3, "5")
        self.zugferd._collect_tax_free_position(4, "7")
        self.assertEqual(
            self.zugferd.tax_free_positions,
            {3: ["2", "5"], 4: ["7"]},
            "should be equal",
        )

    def test__format_positions(self):
        """mindestens 3 fortlaufende Pos. werden als Bereich dargestellt"""
        fmt = self.zugferd._format_positions
        self.assertEqual(fmt([]), "", "leer")
        self.assertEqual(fmt(["4"]), "4", "eine")
        self.assertEqual(fmt(["1", "2"]), "1, 2", "zwei sind noch kein Bereich")
        self.assertEqual(fmt(["1", "2", "3"]), "1-3", "Bereich")
        self.assertEqual(fmt(["1", "2", "3", "5"]), "1-3, 5", "Bereich und einzeln")
        self.assertEqual(fmt(["2", "4", "5", "6", "9"]), "2, 4-6, 9", "Mitte")
        self.assertEqual(fmt(["8", "9", "10", "11"]), "8-11", "mehrstellig")
        self.assertEqual(fmt(["1", "3", "5"]), "1, 3, 5", "Lücken")
        self.assertEqual(fmt(["1", "2", "3", "A"]), "1-3, A", "Text bleibt Text")

    def _items_with_tax_types(self) -> list:
        """Positionen mit Steuertyp in item[7], 'nan' = ohne Steuertyp"""
        head = ["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe", "Steuer"]
        date = "2024-01-01 00:00:00"
        return [
            head,
            ["1", date, "mit 19%", "1", "h", "22", "22", "1"],
            ["2", date, "durchlaufend", "1", "h", "55", "55", "3"],
            ["3", date, "durchlaufend", "1", "h", "75", "75", "3"],
            ["4", date, "Bildung", "1", "h", "10", "10", "4"],
            ["5", date, "ohne Steuertyp", "1", "h", "5", "5", "nan"],
        ]

    def test_add_items_collects_tax_free_positions(self):
        """steuerfreie Pos. werden je Steuertyp (item[7]) gesammelt"""
        self.zugferd.invoice = SimpleNamespace(
            invoice_tax={
                1: [0.19, 1001, 190.19],
                3: [0, 130, "Durchlaufender Posten"],
                4: [0, 10, "Steuerfreie Bildungsleistung"],
            }
        )
        self.zugferd.add_items(self._items_with_tax_types(), "19.00")
        self.assertEqual(
            self.zugferd.tax_free_positions,
            {3: ["2", "3"], 4: ["4"]},
            "should be equal",
        )

    def test_add_items_without_tax_free_positions(self):
        """ohne steuerfreie Zeilen bleibt das Ergebnis leer; Aufrufe addieren nicht"""
        self.zugferd.invoice = SimpleNamespace(
            invoice_tax={1: [0.19, 1001, 190.19], 3: [0, 130, "Durchlaufender Posten"]}
        )
        data = self._items_with_tax_types()
        self.zugferd.add_items([data[0], data[1]], "19.00")
        self.assertEqual(self.zugferd.tax_free_positions, {}, "should be equal")
        self.zugferd.add_items([data[0], data[2]], "19.00")
        self.zugferd.add_items([data[0], data[3]], "19.00")
        self.assertEqual(
            self.zugferd.tax_free_positions, {3: ["3"]}, "wird bei jedem Aufruf neu"
        )

    def _trade_taxes(self) -> list:
        """(Netto, Steuer, Satz, Grund) aller ApplicableTradeTax im Dokument"""
        return [
            (
                str(tax.basis_amount._value),
                str(tax.calculated_amount._value),
                str(tax.rate_applicable_percent._value),
                tax.exemption_reason._text or None,
            )
            for tax in self.zugferd.doc.trade.settlement.trade_tax.children
        ]

    def test__add_tax_free_positions_if_needed_taxed_and_one_tax_free(self):
        """Steuersatz != 0 einzeln, Steuersatz 0 mit einem Typ wie bisher"""
        self.zugferd.invoice = SimpleNamespace(
            invoice_tax={
                1: [0.19, 1001, 190.19],
                2: [0.07, 151, 10.57],
                3: [0, 130, "Durchlaufender Posten"],
                4: [0, 0, "Steuerfreie Bildungsleistung"],
            }
        )
        self.zugferd._add_tax_free_positions_if_needed()
        self.assertEqual(
            self._trade_taxes(),
            [
                ("1001.00", "190.19", "19.00", None),
                ("151.00", "10.57", "7.00", None),
                ("130.00", "0.00", "0.00", "Durchlaufender Posten"),
            ],
            "Typ 4 hat Netto 0 und wird nicht eingetragen",
        )

    def test__add_tax_free_positions_if_needed_several_tax_free(self):
        """mehrere Steuertypen mit Satz 0: Summe der Netto, Gründe mit Pos."""
        self.zugferd.invoice = SimpleNamespace(
            invoice_tax={
                1: [0.19, 1001, 190.19],
                3: [0, 130, "Durchlaufender Posten"],
                4: [0, 10, "Steuerfreie Bildungsleistung"],
            }
        )
        self.zugferd.tax_free_positions = {3: ["2", "3"], 4: ["4"]}
        self.zugferd._add_tax_free_positions_if_needed()
        self.assertEqual(
            self._trade_taxes(),
            [
                ("1001.00", "190.19", "19.00", None),
                (
                    "140.00",
                    "0.00",
                    "0.00",
                    "Pos. 2, 3: Durchlaufender Posten (Netto 130.00 EUR); "
                    "Pos. 4: Steuerfreie Bildungsleistung (Netto 10.00 EUR)",
                ),
            ],
            "should be equal",
        )

    def _item_reasons(self) -> list:
        """Befreiungsgrund jeder Position (None = keiner)"""
        return [
            item.settlement.trade_tax.exemption_reason._text or None
            for item in self.zugferd.doc.trade.items.children
        ]

    def test_add_items_reason_equals_trade_tax_reason_several_tax_free(self):
        """bei mehreren steuerfreien Typen haben Positionen und E-Zeile
        denselben zusammengesetzten Grund"""
        self.zugferd.invoice = SimpleNamespace(
            invoice_tax={
                1: [0.19, 22, 4.18],
                3: [0, 130, "Durchlaufender Posten"],
                4: [0, 10, "Steuerfreie Bildungsleistung"],
            }
        )
        self.zugferd.add_items(self._items_with_tax_types(), "19.00")
        self.zugferd._add_tax_free_positions_if_needed()
        reason = (
            "Pos. 2, 3: Durchlaufender Posten (Netto 130.00 EUR); "
            "Pos. 4: Steuerfreie Bildungsleistung (Netto 10.00 EUR)"
        )
        self.assertEqual(
            self._item_reasons(), [None, reason, reason, reason, None], "Positionen"
        )
        self.assertEqual(
            [tax[3] for tax in self._trade_taxes() if tax[2] == "0.00"],
            [reason],
            "E-Zeile",
        )

    def test_add_items_reason_equals_trade_tax_reason_one_tax_free(self):
        """bei einem steuerfreien Typ bleibt es der eigene Grund"""
        self.zugferd.invoice = SimpleNamespace(
            invoice_tax={
                1: [0.19, 22, 4.18],
                3: [0, 130, "Durchlaufender Posten"],
                4: [0, 0, "Steuerfreie Bildungsleistung"],
            }
        )
        self.zugferd.add_items(self._items_with_tax_types(), "19.00")
        self.zugferd._add_tax_free_positions_if_needed()
        self.assertEqual(
            self._item_reasons(),
            [None, "Durchlaufender Posten", "Durchlaufender Posten",
             "Steuerfreie Bildungsleistung", None],
            "Typ 4 hat Netto 0: Position behält ihren eigenen Grund",
        )
        self.assertEqual(
            [tax[3] for tax in self._trade_taxes() if tax[2] == "0.00"],
            ["Durchlaufender Posten"],
            "E-Zeile",
        )

    def test_add_items_kleinunternehmer_reason_equals_trade_tax_reason(self):
        """Positionen ohne Steuertyp bekommen bei Satz 0.00 den Grund der
        Steuerzeile (Kleinunternehmerregelung)"""
        data = [
            ["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe"],
            ["1", "2024-01-01 00:00:00", "eins", "1", "h", "22", "22"],
            ["2", "2024-01-02 00:00:00", "zwei", "1", "h", "75", "75"],
        ]
        grund = "Kleinunternehmerregelung"
        self.zugferd.add_items(data, "0.00", grund)
        self.zugferd.add_applicable_trade_tax(
            decimal.Decimal("97.00"), decimal.Decimal("0.00"), "0.00", grund
        )
        self.assertEqual(self._item_reasons(), [grund, grund], "Positionen")
        self.assertEqual([tax[3] for tax in self._trade_taxes()], [grund], "E-Zeile")

    def test_add_items_without_default_reason_for_taxed_items(self):
        """bei Steuersatz != 0.00 wird kein Grund eingetragen"""
        data = [
            ["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe"],
            ["1", "2024-01-01 00:00:00", "eins", "1", "h", "22", "22"],
        ]
        self.zugferd.add_items(data, "19.00", "Kleinunternehmerregelung")
        self.assertEqual(self._item_reasons(), [None], "kein Grund")

    def test__add_tax_free_positions_if_needed_nothing_to_add(self):
        """ohne Nettosumme > 0 wird nichts eingetragen"""
        self.zugferd.invoice = SimpleNamespace(
            invoice_tax={3: [0, 0, "Durchlaufender Posten"]}
        )
        self.zugferd._add_tax_free_positions_if_needed()
        self.assertEqual(self._trade_taxes(), [], "should be empty")

    #     @unittest.skip("no way of currently testing this")
    #     def test_add_xml2pdf(self):
    #         """
    #         check whether demo creates the file hello_world.pdf
    #         """
    #         try:
    #             os.remove("hello_world_zugferd.pdf")
    #         except OSError:
    #             pass
    #         try:
    #             os.remove("hello_world.pdf")
    #         except OSError:
    #             pass

    #         daten = {
    #                     "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
    # \n12345 Musterstadt",
    #                     "Betriebsbezeichnung": "Max Mustermann - Software",
    #                     "Bundesland": "Baden-Württemberg",
    #                     "Kontakt": "Tel.: 01234-1234567\
    # \nEmail: max@mustermann.de",
    #                     "Name": "Max Mustermann",
    #                     "Umsatzsteuer": "Steuernummer: 12345/12345\
    # \nFinanzamt Musterstadt",
    #                     "Verzeichnis": "C:/Users/xxx/Documents",
    #                     "Zahlungsziel": "14",
    #                 }
    #         lieferant = Lieferant()
    #         lieferant.fill_lieferant(daten)

    #         # create pdf infile
    #         # self.pdf.demo()
    #         self.assertTrue(os.path.isfile("hello_world.pdf"))

    #         self.zugferd.add_rgnr("2024000000000123")
    #         self.zugferd.add_note(
    #             "Max Mustermann - Softwareentwicklung\nMusterstr. 1\n\
    #                 12345 Musterstadt"
    #         )
    #         self.zugferd.add_rechnungsempfaenger(
    #             "Musterfrauen GmbH & CoKG\nAnette Musterfrau\nAm Bild 19\n\
    #                 98766 Unterschleißheim"
    #         )
    #         self.zugferd.add_zahlungsempfaenger(
    #             "Max Mustermann\nIBAN: DE97 xxx xxx xxx xxx xxx xxx\n\
    #                 BIC: SOLADES1XYZ"
    #         )
    #         self.zugferd.add_my_company(lieferant)
    #         self.zugferd.add_items(
    #             [
    #                 ("Pos.", "Datum", "Tätigkeit", "Menge", "Typ", "Einzel €",
    #                  "Gesamt €"),
    #                 (
    #                     "1",
    #                     "2024-01-01 00:00:00",
    #                     "Irgendwas, das länger ist als zwei\
    #  Zeilen in der Ausgabe mit einer Dokumentation dessen,\
    #  was geleistet wurde.",
    #                     "3",
    #                     "10 Min.",
    #                     "22.00",
    #                     "66.00",
    #                 ),
    #                 (
    #                     "2",
    #                     "2024-01-02 00:00:00",
    #                     "Irgendwas, das länger ist als eine Zeilen und einer \
    #                         Dokumentation dessen, was geleistet wurde.",
    #                     "1",
    #                     "h",
    #                     "75.00",
    #                     "75.00",
    #                 ),
    #                 (
    #                     "3",
    #                     "2024-01-02 00:00:00",
    #                     "Irgendwas, das länger ist als eine Zeilen und einer \
    #                         Dokumentation dessen, was geleistet wurde.",
    #                     "1",
    #                     "h",
    #                     "75.00",
    #                     "75.00",
    #                 ),
    #                 (
    #                     "4",
    #                     "2024-01-02 00:00:00",
    #                     "Irgendwas, das länger ist als eine Zeilen und einer \
    #                         Dokumentation dessen, was geleistet wurde.",
    #                     "1",
    #                     "h",
    #                     "75.00",
    #                     "75.00",
    #                 ),
    #                 (
    #                     "5",
    #                     "2024-01-02 00:00:00",
    #                     "Irgendwas, das länger ist als eine Zeilen und einer \
    #                         Dokumentation dessen, was geleistet wurde.",
    #                     "1",
    #                     "h",
    #                     "75.00",
    #                     "75.00",
    #                 ),
    #                 (
    #                     "6",
    #                     "2024-01-02 00:00:00",
    #                     "Irgendwas, das länger ist als eine Zeilen und einer \
    #                         Dokumentation dessen, was geleistet wurde.",
    #                     "1",
    #                     "h",
    #                     "75.00",
    #                     "75.00",
    #                 ),
    #             ], "19.0"
    #         )

    #         self.zugferd.add_gesamtsummen(
    #             [
    #                 ("netto:", decimal.Decimal("1540.00")),
    #                 ("USt.:", decimal.Decimal("84.98")),
    #                 ("brutto:", decimal.Decimal("1690.98")),
    #             ], "19.0"
    #         )

    #         self.zugferd.add_zahlungsziel(
    #             "Zahlbar ohne Abschlag bis", datetime.now() +
    #             timedelta(days=int(14))
    #         )
    #         self.zugferd.add_xml2pdf("hello_world.pdf",
    #               "hello_world_zugferd.pdf")
    #         self.assertTrue(os.path.isfile("hello_world_zugferd.pdf"))

    #         if self.mydebug is None:
    #             try:
    #                 os.remove("hello_world_zugferd.pdf")
    #             except OSError:
    #                 pass
    #             try:
    #                 os.remove("hello_world.pdf")
    #             except OSError:
    #                 pass

    def test__get_einheit(self):
        """Teste die Rückgabe der Einheit"""
        MSG = "should be equal"
        self.assertEqual(self.zugferd._get_einheit("nix"), "C62", MSG)
        self.assertEqual(self.zugferd._get_einheit("kg"), "KGM", MSG)

    def test__add_gesamtsumme(self):
        """Test that add_gesamtsumme doesn't throw any exception."""
        data = [
                    ("netto:", decimal.Decimal("1540.00")),
                    ("USt.:", decimal.Decimal("84.00")),
                    ("brutto:", decimal.Decimal("1690.00")),
                ]
        try:
            self.zugferd.add_gesamtsummen(data)
        except Exception:
            self.fail("raised Exception unexpectedly!")
        self.assertEqual(
            str(self.zugferd.doc.trade.settlement.monetary_summation.grand_total),
            str(decimal.Decimal("1690.00")) + " None", "Grand_total should be equal"
        )
        self.assertEqual(
            str(self.zugferd.doc.trade.settlement.monetary_summation.tax_basis_total),
            str(decimal.Decimal("1540.00")) + " None", "Tax_basis_total should be equal"
        )
        self.assertEqual(
            str(self.zugferd.doc.trade.settlement.monetary_summation.tax_total),
            str(decimal.Decimal("84.00")) + " EUR", "Tax_total should be equal"
        )

# if __name__ == "__main__":
#     unittest.main()
