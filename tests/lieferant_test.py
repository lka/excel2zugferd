"""
Module Test Lieferant
"""

import unittest
from src.lieferant import Lieferant


STAMMDATEN = {
    "Betriebsbezeichnung": "Max Mustermann - Software",
    "Ansprechpartner": "Max Mustermann",
    "Abteilung": "Softwareentwicklung",
    "Strasse": "Musterstr.",
    "Hausnummer": "17a",
    "PLZ": "12345",
    "Ort": "Musterstadt",
    "Bundesland": "Baden-Württemberg",
    "Telefon": "01234-1234567",
    "Email": "max@mustermann.de",
    "Name": "Max Mustermann",
    "Steuernummer": "12345/12345",
    "Finanzamt": "Musterstadt",
    "Verzeichnis": "C:/Users/xxx/Documents",
    "Zahlungsziel": "14",
    "Steuersatz": "7.5",
    "Kontoinhaber": "Max Mustermann",
    "IBAN": "DEXX YYYY ZZZZ AAAA BBBB CC",
    "BIC": "XYZBCAY",
    "Name": "Max Mustermann",
    "Steuernummer": "12345/12345",
    "Finanzamt": "Musterstadt",
    "Verzeichnis": "C:/Users/xxx/Documents",
    "Zahlungsziel": "14",
    "ZugFeRD": "Ja",
}


class TestLieferant(unittest.TestCase):
    """
    Test Class for Class Lieferant
    """

    def test_get_anschrift_lieferant(self):
        """Tests get_anschrift of Lieferant"""
        adr = Lieferant()
        MSG = "should be filled"
        BEZ = "Software AG"
        NAME = "Max Mustermann"
        AN1 = "Maximilian Mustermann"
        ZUS = "Berichtswesen"
        ORT = "Musterstadt"
        PLZ = "12345"
        STR = "Musterstrasse"
        HNR = "17a"
        TEL = "01234 5678 456"
        FAX = "01234 5678 457"
        MAIL = "mustermann@telekom.de"
        COUNTY = "Baden Württemberg"
        adr.betriebsbezeichnung = BEZ
        adr.name = NAME
        adr.anschrift_line1 = AN1
        adr.ort = ORT
        adr.plz = PLZ
        adr.strasse = STR
        adr.hausnummer = HNR
        adr.email = MAIL
        adr.telefon = TEL
        adr.fax = FAX
        adr.bundesland = COUNTY
        self.assertEqual(adr.anschrift, f"{BEZ}\n{NAME}\n{STR} {HNR}\n{PLZ} {ORT}", MSG)
        adr.adresszusatz = ZUS
        self.assertEqual(
            adr.anschrift, f"{BEZ}\n{ZUS}\n{NAME}\n{STR} {HNR}\n{PLZ} {ORT}", MSG
        )

    def test_get_kontakt(self):
        """Tests get_kontakt"""
        adr = Lieferant()
        TEL = "01234 5678 456"
        FAX = "01234 5678 457"
        MAIL = "mustermann@telekom.de"
        adr.telefon = TEL
        adr.email = MAIL
        self.assertEqual(adr.kontakt, f"Tel.: {TEL}\nE-Mail: {MAIL}")
        adr.fax = FAX
        self.assertEqual(adr.kontakt, f"Tel.: {TEL}\nFax: {FAX}\nE-Mail: {MAIL}")

    def test_get_umsatzsteuer(self):
        """Tests get_umsatzsteuer"""
        adr = Lieferant()
        AMT = "Finanzamt Musterstadt"
        USTNR = "12345/12345"
        adr.steuernr = USTNR
        adr.finanzamt = AMT
        self.assertEqual(adr.umsatzsteuer, f"Steuernummer: {USTNR}\nFinanzamt: {AMT}")

    def test_get_umsatzsteuer_ID(self):
        """Tests get_umsatzsteuer with Umsatzsteuer-ID"""
        adr = Lieferant()
        USTNR = "DE123456789"
        adr.steuerid = USTNR
        self.assertEqual(adr.umsatzsteuer, f"Umsatzsteuer-ID: {USTNR}")

    def test__fill_umsatzsteuer(self):
        """Tests _fill_umsatzsteuer with Steuernummer"""
        MSG = "should be equal"
        adr = Lieferant()
        AMT = "Musterstadt"
        USTNR = "12345/12345"
        adr._fill_umsatzsteuer(
            {"Steuernummer": USTNR, "Finanzamt": AMT}, ["Steuernummer", "Finanzamt"]
        )
        self.assertEqual(adr.steuernr, USTNR, MSG)
        self.assertEqual(adr.finanzamt, AMT, MSG)
        self.assertIsNone(adr.steuerid)

    def test__fill_umsatzsteuer_ID_withoutAMT(self):
        """Tests _fill_umsatzsteuer with Umsatzsteuer-ID"""
        MSG = "should be equal"
        adr = Lieferant()
        USTNR = "DE123456789"
        adr._fill_umsatzsteuer({"UmsatzsteuerID": USTNR}, ["UmsatzsteuerID"])
        self.assertEqual(adr.steuerid, USTNR, MSG)
        self.assertIsNone(adr.finanzamt)
        self.assertIsNone(adr.steuernr)

    def test__fill_umsatzsteuer_ID(self):
        """Tests _fill_umsatzsteuer with Umsatzsteuer-ID"""
        MSG = "should be equal"
        adr = Lieferant()
        AMT = "Musterstadt"
        USTNR = "DE123456789"
        adr._fill_umsatzsteuer(
            {"UmsatzsteuerID": USTNR, "Finanzamt": AMT}, ["UmsatzsteuerID", "Finanzamt"]
        )
        self.assertEqual(adr.steuerid, USTNR, MSG)
        self.assertIsNone(adr.finanzamt)
        self.assertIsNone(adr.steuernr)

    def test__fill_steuersatz(self):
        """Test _fill_steuersatz with correct value"""
        MSG = "should be equal"
        adr = Lieferant()
        daten = {"Steuersatz": "19"}
        EXPECTED = "19.00"
        adr._fill_steuersatz(daten)
        self.assertEqual(adr.steuersatz, EXPECTED, MSG)

    def test_fill_lieferant(self):
        """
        Tests that procedure fill_lieferant works
        """
        MSG = "Should be equal"
        daten = STAMMDATEN
        lieferant = Lieferant()
        lieferant.fill_lieferant(daten)
        self.assertEqual(lieferant.name, "Max Mustermann", MSG)
        self.assertEqual(lieferant.adresszusatz, "Softwareentwicklung", MSG)
        self.assertEqual(
            lieferant.betriebsbezeichnung, "Max Mustermann - Software", MSG
        )
        self.assertEqual(lieferant.bundesland, "Baden-Württemberg", MSG)
        self.assertEqual(lieferant.email, "max@mustermann.de", MSG)
        self.assertIsNone(lieferant.fax, MSG)
        self.assertEqual(lieferant.finanzamt, "Musterstadt", MSG)
        self.assertEqual(lieferant.hausnummer, "17a", MSG)
        self.assertEqual(lieferant.ort, "Musterstadt", MSG)
        self.assertEqual(lieferant.plz, "12345", MSG)
        self.assertEqual(lieferant.steuernr, "12345/12345", MSG)
        self.assertEqual(lieferant.strasse, "Musterstr.", MSG)
        self.assertEqual(lieferant.telefon, "01234-1234567", MSG)
        self.assertEqual(lieferant.zahlungsziel, "14", MSG)
        self.assertEqual(lieferant.steuersatz, "7.50", MSG)

    def test_fill_lieferant_throws_cond1(self):
        """
        Tests that wrong Anschrift in Stammdaten throws ValueError
        """
        daten = STAMMDATEN | {
            "Steuersatz": "19",
        }
        lieferant = Lieferant()
        daten["Betriebsbezeichnung"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Betriebsbezeichnung"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Betriebsbezeichnung"] = "Software AG"
        daten["Strasse"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Hausnummer"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Postfach"] = "12345"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
        daten["Strasse"] = "An der Musterstrasse"
        daten["Hausnummer"] = "17a"
        daten["Postfach"] = None
        daten["PLZ"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["PLZ"] = "12345"
        daten["Ort"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Ort"] = "Musterstadt (Ortsteil Klein)"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond2(self):
        """
        Tests that wrong Betriebsbezeichnung in Stammdaten throws ValueError
        """
        daten = STAMMDATEN | {
            "Steuersatz": None,
        }
        lieferant = Lieferant()
        daten["Betriebsbezeichnung"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Betriebsbezeichnung"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Betriebsbezeichnung"] = "Max Mustermann - Software"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond4(self):
        """
        Tests that wrong Betriebsbezeichnung in Stammdaten throws ValueError
        """
        daten = STAMMDATEN | {
            "Steuersatz": None,
        }
        lieferant = Lieferant()
        expected = "Software AG"
        MSG = "should be equal"
        daten["Betriebsbezeichnung"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Betriebsbezeichnung"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Betriebsbezeichnung"] = "Software\nAG"
        lieferant.fill_lieferant(daten)
        self.assertEqual(lieferant.betriebsbezeichnung, expected, MSG)
        daten["Betriebsbezeichnung"] = "Max Mustermann"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond5(self):
        """
        Tests that wrong Umsatzsteuer in Stammdaten throws ValueError
        """
        daten = STAMMDATEN | {
            "Steuersatz": None,
        }
        lieferant = Lieferant()
        daten["Finanzamt"] = None
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Finanzamt"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Finanzamt"] = "\n"
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Finanzamt"] = ""
        with self.assertRaises(ValueError):
            lieferant.fill_lieferant(daten)
        daten["Finanzamt"] = "Musterstadt"
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")

    def test_fill_lieferant_throws_cond6(self):
        """
        Tests that no Steuersatz / Zahlungsziel in Stammdaten
        throws no ValueError
        """
        daten = STAMMDATEN | {
            "Steuersatz": "",
            "Zahlungsziel": "",
        }
        lieferant = Lieferant()
        try:
            lieferant.fill_lieferant(daten)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
