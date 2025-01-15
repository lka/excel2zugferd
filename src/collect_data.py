"""
Module collect_data
"""

from src.handle_other_objects import Konto, Steuerung, Invoice
from src.lieferant import Lieferant
from src.kunde import Kunde
from src.excel_content import ExcelContent


class InvoiceCollection(Invoice):
    """
    add functionality to Invoice class
    """
    def __init__(self, daten: ExcelContent = None,
                 stammdaten: dict = None) -> None:
        super().__init__()
        self.set_stammdaten(stammdaten)
        self.set_daten(daten)

    def set_stammdaten(self, stammdaten: dict) -> None:
        if stammdaten is not None:
            keys = stammdaten.keys()
            self.supplier = Lieferant()
            self.supplier.fill_lieferant(stammdaten)
            self.supplier_account = Konto()
            self.supplier_account.fill_konto(stammdaten, keys)
            self.management = Steuerung()
            self.management.fill_steuerung(stammdaten)

    def set_daten(self, daten: ExcelContent = None) -> None:
        if daten is not None:
            self.customer = Kunde()
            daten.get_address_of_customer(customer=self.customer)
            self.positions = daten.get_invoice_positions()
            self.sums = daten.get_invoice_sums()
            self.invoicenr = daten.get_invoice_number()
