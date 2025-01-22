"""
Module collect_data
"""

from src.invoice import Invoice
from src.konto import Konto
from src.steuerung import Steuerung
from src.lieferant import Lieferant
from src.kunde import Kunde
from src.excel_content import ExcelContent
from src.constants import ANSCHRIFT_DEFAULT_SPALTE, RGNR_DEFAULT_SPALTE, \
    RGDATUM_REFAULT_SPALTE


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
            spalte = self.management.anschrift_spalte if self.\
                management.anschrift_spalte else ANSCHRIFT_DEFAULT_SPALTE
            daten.get_address_of_customer(spalte=spalte,
                                          zeile=self.management.
                                          anschrift_zeile,
                                          customer=self.customer
                                          )
            self.positions = daten.get_invoice_positions(mgmnt=self.management)
            self.sums = daten.get_invoice_sums(management=self.management)
            spalte = self.management.rechnung_spalte if self.\
                management.rechnung_spalte else RGNR_DEFAULT_SPALTE
            self.invoicenr = daten.get_invoice_number(spalte=spalte,
                                                      zeile=self.management.
                                                      rechnung_zeile)
            spalte = self.management.datum_spalte if self.\
                management.datum_spalte else RGDATUM_REFAULT_SPALTE
            self.invoicedate = daten.get_invoice_date(spalte=spalte,
                                                      zeile=self.management.
                                                      datum_zeile)
