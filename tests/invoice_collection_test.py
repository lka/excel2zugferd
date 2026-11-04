"""
Tests for Module invoice_collection
"""

from unittest import TestCase
import pandas as pd
from unittest.mock import MagicMock
from src.constants import STORNO_DEFAULT_SPALTE
from src.excel_content import ExcelContent
from src.invoice_collection import InvoiceCollection
from src.steuerung import Steuerung


class TestInvoiceCollection(TestCase):
    """TestClass for InvoiceCollection"""

    def _positions(self, preis="22"):
        return pd.DataFrame(
            [
                ["1", "2024-01-01", "A", "1", "h", "22", "22"],
                ["2", "2024-01-02", "B", "1", "h", preis, preis],
            ],
            columns=["Pos.", "Datum", "Tätigkeit", "Anzahl", "Typ", "Preis", "Summe"],
        )

    def _collection(self, storno_return, spalte=None, zeile=None, positions=None):
        collection = InvoiceCollection()
        collection.management = Steuerung()
        # werden sonst erst durch fill_steuerung gesetzt
        collection.management.datum_spalte = None
        collection.management.datum_zeile = None
        collection.management.storno_spalte = spalte
        collection.management.storno_zeile = zeile
        daten = MagicMock(spec=ExcelContent)
        daten.get_storno_values.return_value = storno_return
        daten.get_invoice_positions.return_value = (
            positions if positions is not None else self._positions()
        )
        collection.set_daten(daten)
        return collection, daten

    def test_storno_is_none_by_default(self):
        """ohne Daten ist storno None"""
        self.assertIsNone(InvoiceCollection().storno, "should be None")

    def test_set_daten_storno_none(self):
        """liefert get_storno_values None, ist storno None"""
        collection, _ = self._collection(None)
        self.assertIsNone(collection.storno, "should be None")

    def test_set_daten_storno_list(self):
        """liefert get_storno_values eine Liste, steht sie in storno"""
        values = ["Gutschrift", 381, "R-001", "01.02.2024"]
        collection, daten = self._collection(values)
        self.assertEqual(collection.storno, values, "should be equal")
        daten.get_storno_values.assert_called_once_with(
            spalte=STORNO_DEFAULT_SPALTE,
            zeile=None,
            mgmnt=collection.management,
        )

    def test_set_daten_storno_spalte_zeile_from_management(self):
        """storno_spalte und storno_zeile aus der Steuerung werden übergeben"""
        collection, daten = self._collection(None, spalte="C", zeile="5")
        daten.get_storno_values.assert_called_once_with(
            spalte="C", zeile="5", mgmnt=collection.management
        )

    def test_set_daten_negative_price_raises(self):
        """negativer Einzelpreis: ValueError schon beim Einlesen mit Positionsnummer"""
        with self.assertRaises(ValueError) as ctx:
            self._collection(None, positions=self._positions("-10"))
        self.assertIn("Position 2", str(ctx.exception), "should contain position")
        self.assertIn("Einzelpreis", str(ctx.exception), "should contain Einzelpreis")

    def test_set_daten_price_zero_or_empty_is_allowed(self):
        """Preis 0 oder leer ist kein negativer Preis"""
        positions = self._positions("0")
        positions.loc[0, "Preis"] = float("nan")
        try:
            self._collection(None, positions=positions)
        except ValueError:
            self.fail("raised ValueError unexpectedly!")
