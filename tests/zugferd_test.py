"""
Modul zugferd_test
"""

import unittest
import os
from datetime import datetime, timedelta
import src.handle_zugferd as handle_zugferd
import src.handle_pdf as handle_pdf
from src.handle_other_objects import Adresse
import decimal


class TestZugFerd(unittest.TestCase):
    """Testclass for zugferd tests"""

    def setUp(self) -> None:
        self.zugferd = handle_zugferd.ZugFeRD()
        self.pdf = handle_pdf.Pdf(None, None)
        self.mydebug = None
        return super().setUp()

    def test_modify_xml(self):
        """Test that xmlns:qdt is added"""
        xml = "<?xml version='1.0' encoding='UTF-8'?>\
<rsm:CrossIndustryInvoice xmlns:ram=\
\"urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100\"\
 xmlns:rsm=\"urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100\" \
xmlns:udt=\"urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100\">\
  <rsm:ExchangedDocumentContext>\
    <ram:GuidelineSpecifiedDocumentContextParameter>\
      <ram:ID>urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended</ram:ID>\
    </ram:GuidelineSpecifiedDocumentContextParameter>\
  </rsm:ExchangedDocumentContext>\
</rsm:CrossIndustryInvoice>".encode('utf-8')
        mod_xml = self.zugferd.modify_xml(xml).decode('utf-8')
        count = mod_xml.count('xmlns:qdt=')
        self.assertEqual(count, 1, 'should only be 1')
        # self.assertIn('show me the content of mod_xml', mod_xml)

    def test_modify_xml_already_in(self):
        """Test that xmlns:qdt is added"""
        xml = "<?xml version='1.0' encoding='UTF-8'?>\
<rsm:CrossIndustryInvoice xmlns:qdt=\
\"urn:un:unece:uncefact:data:standard:QualifiedDataType:100\" xmlns:ram=\
\"urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100\"\
 xmlns:rsm=\"urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100\" \
xmlns:udt=\"urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100\">\
  <rsm:ExchangedDocumentContext>\
    <ram:GuidelineSpecifiedDocumentContextParameter>\
      <ram:ID>urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended</ram:ID>\
    </ram:GuidelineSpecifiedDocumentContextParameter>\
  </rsm:ExchangedDocumentContext>\
</rsm:CrossIndustryInvoice>".encode('utf-8')
        mod_xml = self.zugferd.modify_xml(xml).decode('utf-8')
        count = mod_xml.count('xmlns:qdt=')
        self.assertEqual(count, 1, 'should only be 1')
        # self.assertIn('show me the content of mod_xml', mod_xml)

    def test_add_items(self):
        """test that add_items doesn't throw any exception"""
        data = [
                ['Pos.', 'Datum', 'Tätigkeit', 'Anzahl', 'Typ', 'Preis',
                 'Summe'],
                ['1', '2024-01-01 00:00:00',
                    'WhatsApp wg. Netzteil für USB-Server', '1', '10 Min.',
                    '22',
                    '22'],
                ['2', '2024-01-02 00:00:00',
                    'Telefonat wg. KVSiServer (steht in der Doku)', '1',
                    '10 Min.',
                    '22', '22'],
                ['3', '2024-01-03 00:00:00',
                    'Telefonat wg. KVSiServer (steht in der Doku)', '1',
                    '10 Min.',
                    '22', '22'],
                ['4', '2024-01-03 00:00:00',
                    'Bewerbungsgespräch mit Frau A und B', '2', 'h', '75',
                    '150'],
                ['5', '',
                    'Anfahrt dazu', '1', 'h', '75',
                    '75'],
                ]
        try:
            self.zugferd.add_items(data, "19.00")
        except Exception:
            self.fail("raised Exceptionr unexpectedly!")

    def test_add_xml2pdf(self):
        """
        check whether demo creates the file hello_world.pdf
        """
        try:
            os.remove("hello_world_zugferd.pdf")
        except OSError:
            pass
        try:
            os.remove("hello_world.pdf")
        except OSError:
            pass

        daten = {
                    "Anschrift": "Max Mustermann\nSoftware\nMusterstr. 17a\
\n12345 Musterstadt",
                    "Betriebsbezeichnung": "Max Mustermann - Software",
                    "Bundesland": "Baden-Württemberg",
                    "Kontakt": "Tel.: 01234-1234567\nEmail: max@mustermann.de",
                    "Name": "Max Mustermann",
                    "Umsatzsteuer": "Steuernummer: 12345/12345\
\nFinanzamt Musterstadt",
                    "Verzeichnis": "C:/Users/xxx/Documents",
                    "Zahlungsziel": "14",
                }
        lieferant = Adresse()
        lieferant.fill_lieferant(daten)

        # create pdf infile
        self.pdf.demo()
        self.assertTrue(os.path.isfile("hello_world.pdf"))

        self.zugferd.add_rgnr("2024000000000123")
        self.zugferd.add_note(
            "Max Mustermann - Softwareentwicklung\nMusterstr. 1\n\
                12345 Musterstadt"
        )
        self.zugferd.add_rechnungsempfaenger(
            "Musterfrauen GmbH & CoKG\nAnette Musterfrau\nAm Bild 19\n\
                98766 Unterschleißheim"
        )
        self.zugferd.add_zahlungsempfaenger(
            "Max Mustermann\nIBAN: DE97 xxx xxx xxx xxx xxx xxx\n\
                BIC: SOLADES1XYZ"
        )
        self.zugferd.add_my_company(lieferant)
        self.zugferd.add_items(
            [
                ("Pos.", "Datum", "Tätigkeit", "Menge", "Typ", "Einzel €",
                 "Gesamt €"),
                (
                    "1",
                    "2024-01-01 00:00:00",
                    "Irgendwas, das länger ist als zwei Zeilen in der Ausgabe \
                        mit einer Dokumentation dessen, was geleistet wurde.",
                    "3",
                    "10 Min.",
                    "22.00",
                    "66.00",
                ),
                (
                    "2",
                    "2024-01-02 00:00:00",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "3",
                    "2024-01-02 00:00:00",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "4",
                    "2024-01-02 00:00:00",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "5",
                    "2024-01-02 00:00:00",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "6",
                    "2024-01-02 00:00:00",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
            ], "19.0"
        )

        self.zugferd.add_gesamtsummen(
            [
                decimal.Decimal("1540.00"),
                decimal.Decimal("84.98"),
                decimal.Decimal("1690.98"),
            ], "19.0"
        )

        self.zugferd.add_zahlungsziel(
            "Zahlbar ohne Abschlag bis", datetime.now() +
            timedelta(days=int(14))
        )
        self.zugferd.add_xml2pdf("hello_world.pdf", "hello_world_zugferd.pdf")
        self.assertTrue(os.path.isfile("hello_world_zugferd.pdf"))

        if self.mydebug is None:
            try:
                os.remove("hello_world_zugferd.pdf")
            except OSError:
                pass
            try:
                os.remove("hello_world.pdf")
            except OSError:
                pass


# if __name__ == "__main__":
#     unittest.main()
