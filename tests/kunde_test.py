"""
Modul Kunde Test
"""

import unittest
from src.kunde import Kunde
from src import _setNoneIfEmpty

ADRESSFELD = [
    "Mustermann GmbH & CoKG",
    "Vertrieb",
    "Frau Müller",
    "In der Musterstr. 17a",
    "12345 Musterstadt"
]


class TestAdresse(unittest.TestCase):
    """
    Test Class for Class Adresse
    """
    def test_get_anschrift_kunde(self):
        """Tests get_anschrift of Kunde"""
        adr = Kunde()
        MSG = 'should be filled'
        BEZ = "Mustermann GmbH & CoKG"
        NAME = 'Frau Müller'
        ZUS = 'Vertrieb'
        ORT = 'Musterstadt'
        PLZ = '12345'
        STR = 'In der Musterstr.'
        HNR = '17a'

        adr.anschrift = ADRESSFELD
        self.assertEqual(adr.anschrift,
                         f"{BEZ}\n{ZUS}\n{NAME}\n{STR} {HNR}\n{PLZ} {ORT}",
                         MSG)
        adr.adresszusatz = _setNoneIfEmpty("")
        self.assertEqual(adr.anschrift,
                         f"{BEZ}\n{NAME}\n{STR} {HNR}\n{PLZ} {ORT}", MSG)

    def test_set_anschrift_kunde_throws_ValueError(self):
        """
        Test that anschrift throws ValueError on failure
        """
        kunde = Kunde()
        with self.assertRaises(ValueError):
            kunde.anschrift = []
        zeile6 = "Zu viele Zeilen"
        adr = ADRESSFELD
        adr.append(zeile6)
        # print(adr)
        with self.assertRaises(ValueError):
            kunde.anschrift = adr
