import os
from datetime import date
from decimal import Decimal

from drafthorse.models.accounting import ApplicableTradeTax
from drafthorse.models.document import Document
from drafthorse.models.note import IncludedNote
from drafthorse.models.tradelines import LineItem
from drafthorse.models.payment import PaymentTerms
from drafthorse.models.party import TaxRegistration
from drafthorse.pdf import attach_xml

class ZugFeRD:
    def __init__(self):
        # Build data structure
        self.doc = Document()
        self.doc.context.guideline_parameter.id = (
            "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"
        )
        self.doc.header.type_code = "380"
        self.doc.header.name = "RECHNUNG"
        self.doc.header.issue_date_time = date.today()
        self.doc.header.languages.add("de")
        self.debug = False

    def add_rgNr(self, rgNr):        
        self.doc.header.id = rgNr

    def add_note(self, text):
        note = IncludedNote()
        note.content.add(text)
        self.doc.header.notes.add(note)

    def add_zahlungsempfaenger(self, text):
        self.doc.trade.settlement.payment_means.type_code = "58" # SEPA Überweisung else "ZZZ"
        arr = text.split("\n")
        self.doc.trade.settlement.payee.name = arr[0]
        self.doc.trade.settlement.payment_means.payee_account.account_name = arr[0]
        if len(arr) > 1:
            self.doc.trade.settlement.payment_means.payee_account.iban = arr[1].split(' ', 1)[1]
        if len(arr) == 3:
            self.doc.trade.settlement.payment_means.payee_institution.bic = arr[2].split(" ", 1)[1]

    def add_rechnungsempfaenger(self, text):
        self.doc.trade.settlement.currency_code = "EUR"

        arr = text.split('\n')
        self.doc.trade.settlement.invoicee.name = arr[0]
        self.doc.trade.agreement.buyer.name = arr[0]
        if len(arr) > 2:
            self.doc.trade.agreement.buyer.address.line_one = arr[1]
        if len(arr) > 3:
            self.doc.trade.agreement.buyer.address.line_two = arr[2]
        if len(arr) > 1:
            self.doc.trade.agreement.buyer.address.postcode = arr[-1].split(" ", 1)[0]
            self.doc.trade.agreement.buyer.address.city_name = arr[-1].split(" ", 1)[1]
            self.doc.trade.agreement.buyer.address.country_id = "DE"

    def add_myCompany(self, adr, company, kontakt, ustid):
        self.doc.trade.agreement.seller.id = company

        arr = adr.split("\n")
        self.doc.trade.agreement.seller.name = arr[0] if len(arr) > 1 else adr
        if len(arr) > 2:
            self.doc.trade.agreement.seller.address.line_one = arr[1]
        if len(arr) > 3:
            self.doc.trade.agreement.seller.address.line_two = arr[2]
        if len(arr) > 1:
            self.doc.trade.agreement.seller.address.postcode = arr[-1].split(" ", 1)[0]
            self.doc.trade.agreement.seller.address.city_name = arr[-1].split(' ', 1)[1]
            self.doc.trade.agreement.seller.address.country_id = "DE"

        arr = kontakt.split('\n')
        self.doc.trade.agreement.seller.contact.telephone.number = arr[0].split(' ', 1)[1]
        self.doc.trade.agreement.seller.contact.email.address = arr[1].split(' ', 1)[1]
        taxreg = TaxRegistration()
        taxreg.id = ("FC", ustid)
        self.doc.trade.agreement.seller.tax_registrations.add (taxreg)
        # self.doc.trade.agreement.seller.tax = ustid

    def add_items(self, dat):
        i = 0
        # ("Pos.", "Datum", "Tätigkeit", "Menge", "Typ", "Einzel €", "Gesamt €")
        for item in dat:
            if i > 0:
                li = LineItem()
                li.document.line_id = item[0] # Pos.
                li.product.name = item[1] + ': ' + item[2] # Datum ' ' Tätigkeit
                menge = float(item[3])
                # li.agreement.gross.basis_quantity = (
                #     Decimal("1.0000"),
                #     item[4],
                # )  # C62 == pieces
                # li.agreement.net.basis_quantity = (Decimal("1.0000"), item[4])
                einzelpreisnetto = float(item[5].split()[0].replace(",", "."))
                li.agreement.net.amount = Decimal(f"{einzelpreisnetto:.2f}")
                li.agreement.gross.amount = Decimal(f"{einzelpreisnetto:.2f}")
                li.delivery.billed_quantity = (
                    Decimal(f"{menge:.4f}"),
                    "HUR" if item[4] == "h" else "MIN",
                )  # C62 == pieces
                li.settlement.trade_tax.type_code = "VAT"
                li.settlement.trade_tax.category_code = "S"
                li.settlement.trade_tax.rate_applicable_percent = Decimal("19.00")
                gesamt = float(item[6].split()[0].replace(',', '.'))
                li.settlement.monetary_summation.total_amount = Decimal(f"{gesamt:.2f}")
                self.doc.trade.items.add(li)
            i = i + 1

    def add_gesamtsummen(self, dat):

        netto = float(dat[0][1].split()[0].replace(',', '.'))
        steuer = float(dat[1][1].split()[0].replace(",", "."))
        brutto = float(dat[2][1].split()[0].replace(",", "."))

        trade_tax = ApplicableTradeTax()
        trade_tax.calculated_amount = Decimal(f"{steuer:.2f}")
        trade_tax.basis_amount = Decimal(f"{netto:.2f}")
        trade_tax.type_code = "VAT"
        trade_tax.category_code = "S"
        # trade_tax.exemption_reason_code = 'VATEX-EU-AE'
        trade_tax.rate_applicable_percent = Decimal("19.00")
        self.doc.trade.settlement.trade_tax.add(trade_tax)

        self.doc.trade.settlement.monetary_summation.line_total = Decimal(f"{netto:.2f}")
        # self.doc.trade.settlement.monetary_summation.charge_total = Decimal("0.00")
        # self.doc.trade.settlement.monetary_summation.allowance_total = Decimal("0.00")
        self.doc.trade.settlement.monetary_summation.tax_basis_total = Decimal(
            f"{netto:.2f}"
        )
        self.doc.trade.settlement.monetary_summation.tax_total = (Decimal(f"{steuer:.2f}"), "EUR")
        self.doc.trade.settlement.monetary_summation.grand_total = Decimal(f"{brutto:.2f}")
        self.doc.trade.settlement.monetary_summation.due_amount = Decimal(
            f"{brutto:.2f}"
        )

    def add_zahlungsziel(self, text, datum):
        terms = PaymentTerms()
        terms.description = text
        terms.due = datum
        self.doc.trade.settlement.terms.add(terms)

    def add_xml2pdf(self, inFile=None, outFile=None) -> None:
        # Generate XML file
        xml = self.doc.serialize(schema="FACTUR-X_EXTENDED")

        # print (xml)

        # Attach XML to an existing PDF.
        # Note that the existing PDF should be compliant to PDF/A-3!
        # You can validate this here: https://www.pdf-online.com/osa/validate.aspx
        if inFile:
            with open(inFile, "rb") as original_file:
                new_pdf_bytes = attach_xml(original_file.read(), xml, 'EXTENDED')
        if self.debug:
            with open('factur-x.xml', 'wb') as f:
                f.write(xml)
        if outFile:
            with open(outFile, "wb") as f:
                f.write(new_pdf_bytes)
