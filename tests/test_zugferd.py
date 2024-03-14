"""
Testmodul for zugferd
"""

import unittest
import os
from datetime import datetime, timedelta
from zugferd import ZugFeRD


class TestZugFerd(unittest.TestCase):
    """Testclass for zugferd tests"""

    def setUp(self) -> None:
        self.zugferd = ZugFeRD()
        self.mydebug = None
        return super().setUp()

    def test_add_xml2pdf(self):
        """
        check whether demo creates the file hello_world.pdf
        """
        try:
            os.remove("hello_world_zugferd.pdf")
        except OSError:
            pass

        self.zugferd.add_rgnr("2024000000000123")
        self.zugferd.add_note(
            "Max Mustermann - Softwareentwicklung\nMusterstr. 1\n12345 Musterstadt"
        )
        self.zugferd.add_rechnungsempfaenger(
            "Musterfrauen GmbH & CoKG\nAnette Musterfrau\nAm Bild 19\n98766 Unterschleißheim"
        )
        self.zugferd.add_zahlungsempfaenger(
            "Max Mustermann\nIBAN: DE97 xxx xxx xxx xxx xxx xxx\nBIC: SOLADES1XYZ"
        )
        self.zugferd.add_my_company(
            "Max Mustermann\nMusterstr. 1\n12345 Musterstadt",
            "Max Mustermann - Softwareentwicklung",
            "Tel.: 01234-123456789\nEmail: max@mustermann.de",
            "12345/6789",
        )
        self.zugferd.add_items(
            [
                ("Pos.", "Datum", "Tätigkeit", "Menge", "Typ", "Einzel €", "Gesamt €"),
                (
                    "1",
                    "01.01.2024",
                    "Irgendwas, das länger ist als zwei Zeilen in der Ausgabe mit \
einer Dokumentation dessen, was geleistet wurde.",
                    "3",
                    "10 Min.",
                    "22,00",
                    "66,00",
                ),
                (
                    "2",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer Dokumentation \
dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75,00",
                    "75,00",
                ),
                (
                    "3",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer Dokumentation \
dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75,00",
                    "75,00",
                ),
                (
                    "4",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer Dokumentation \
dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75,00",
                    "75,00",
                ),
                (
                    "5",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer Dokumentation \
dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75,00",
                    "75,00",
                ),
                (
                    "6",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer Dokumentation \
dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75,00 €",
                    "75,00 €",
                ),
            ]
        )

        self.zugferd.add_gesamtsummen(
            [
                ("Summe Netto:", "1540,00 €"),
                ("zzgl. Umsatzsteuer 19%:", "84,98 €"),
                ("Gesamt:", "1690,98 €"),
            ]
        )

        self.zugferd.add_zahlungsziel(
            "Zahlbar ohne Abschlag bis", datetime.now() + timedelta(days=int(14))
        )
        yield self.zugferd.add_xml2pdf("hello_world.pdf", "hello_world_zugferd.pdf")
        self.assertTrue(os.path.isfile("hello_world_zugferd.pdf"))
        self.assertTrue(os.path.isfile("hello_world.pdf"))

        if self.mydebug is None:
            try:
                os.remove("hello_world_zugferd.pdf")
            except OSError:
                pass
            try:
                os.remove("hello_world.pdf")
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
