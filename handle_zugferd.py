"""
Module handle_zugferd
"""
import re

from datetime import date, datetime
from decimal import Decimal

from drafthorse.models.accounting import ApplicableTradeTax
from drafthorse.models.document import Document
from drafthorse.models.note import IncludedNote
from drafthorse.models.tradelines import LineItem
from drafthorse.models.payment import PaymentTerms
from drafthorse.models.party import TaxRegistration
from drafthorse.pdf import attach_xml
from drafthorse.models import NS_QDT


class ZugFeRD:
    """Class ZugFeRD"""

    def __init__(self):
        # Build data structure
        self.doc = Document()
        self.doc.context.guideline_parameter.id = (
            "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"
        )
        self.doc.header.type_code = "380"
        self.doc.header.name = "RECHNUNG"
        self.doc.header.issue_date_time = date.today()
        # self.doc.header.languages.add("de")
        self.debug = False
        self.first_date = None
        self.last_date = None

    def add_rgnr(self, rgnr):
        """Set Rechnungsnummer to id in header"""
        self.doc.header.id = rgnr

    def add_note(self, text):
        """Add note to notes"""
        note = IncludedNote()
        note.content.add(text)
        note.subject_code = "REG"
        self.doc.header.notes.add(note)

    def add_bundesland(self, bundesland):
        """Add Bundesland"""
        self.doc.trade.agreement.seller.address.country_subdivision = bundesland

    def add_zahlungsempfaenger(self, text):
        """set Zahlungsempfaenger to correct value"""
        self.doc.trade.settlement.payment_means.type_code = (
            "58"  # SEPA Überweisung else "ZZZ"
        )
        self.doc.trade.settlement.payment_means.information.add('Zahlung per SEPA Überweisung.')
        arr = text.split("\n")
        # self.doc.trade.settlement.payee.name = arr[0] # BR-17
        self.doc.trade.settlement.payment_means.payee_account.account_name = arr[0]
        if len(arr) > 1:
            self.doc.trade.settlement.payment_means.payee_account.iban = arr[1].split(
                " ", 1
            )[1]
        if len(arr) == 3:
            self.doc.trade.settlement.payment_means.payee_institution.bic = arr[
                2
            ].split(" ", 1)[1]

    def add_rechnungsempfaenger(self, text):
        """set Rechnungsempfänger"""
        self.doc.trade.settlement.currency_code = "EUR"
        # self.doc.trade.settlement.tax_currency_code = "EUR" # BR-53-1

        arr = text.split("\n")
        # self.doc.trade.settlement.invoicee.name = arr[0]
        self.doc.trade.agreement.buyer.name = arr[0]
        if len(arr) > 2:
            self.doc.trade.agreement.buyer.address.line_one = arr[1]
        if len(arr) > 3:
            self.doc.trade.agreement.buyer.address.line_one = arr[-2]
        if len(arr) > 1:
            self.doc.trade.agreement.buyer.address.postcode = arr[-1].split(" ", 1)[0]
            self.doc.trade.agreement.buyer.address.city_name = arr[-1].split(" ", 1)[1]
            self.doc.trade.agreement.buyer.address.country_id = "DE"

    def add_my_company(self, adr, company, kontakt, ustid):
        """Add Address of my company to zugferd"""
        self.doc.trade.agreement.seller.id = company

        arr = adr.split("\n")
        self.doc.trade.agreement.seller.name = (
            arr[0] if len(arr) > 1 else adr if len(adr) > 0 else "unbekannt"
        )
        if len(arr) > 2:
            self.doc.trade.agreement.seller.address.line_one = arr[1]
        if len(arr) > 3:
            self.doc.trade.agreement.seller.address.line_one = arr[-2]
        if len(arr) > 1:
            self.doc.trade.agreement.seller.address.postcode = arr[-1].split(" ", 1)[0]
            self.doc.trade.agreement.seller.address.city_name = arr[-1].split(" ", 1)[1]
            self.doc.trade.agreement.seller.address.country_id = "DE"

        arr = kontakt.split("\n")
        self.doc.trade.agreement.seller.contact.telephone.number = (
            arr[0].split(" ", 1)[1] if len(arr) > 0 and len(arr[0]) > 0 else " "
        )
        self.doc.trade.agreement.seller.contact.email.address = (
            arr[1].split(" ", 1)[1]
            if len(arr) > 1 and len(arr[1]) > 0 and len(arr[1].split(" ", 1)) > 0
            else " "
        )
        taxreg = TaxRegistration()
        taxreg.id = ("FC", ustid)
        self.doc.trade.agreement.seller.tax_registrations.add(taxreg)
        # self.doc.trade.agreement.seller.tax = ustid

    def add_items(self, dat):
        """add items to invoice"""
        i = 0
        # ("Pos.", "Datum", "Tätigkeit", "Menge", "Typ", "Einzel €", "Gesamt €")
        for item in dat:
            if i > 0:
                li = LineItem()
                li.document.line_id = item[0]  # Pos.
                li.product.name = item[1] + ": " + item[2]  # Datum ' ' Tätigkeit
                menge = float(item[3])
                # li.agreement.gross.basis_quantity = (
                #     Decimal("1.0000"),
                #     item[4],
                # )  # C62 == pieces
                # li.agreement.net.basis_quantity = (Decimal("1.0000"), item[4])
                einzelpreisnetto = float(item[5].split()[0].replace(",", "."))
                # einzelpreisbrutto = round(einzelpreisnetto * 1.19, 2)
                li.agreement.net.amount = Decimal(f"{einzelpreisnetto:.2f}")
                # li.agreement.gross.amount = Decimal(f"{einzelpreisnetto:.2f}") # Decimal(f"{einzelpreisbrutto:.2f}")
                li.delivery.billed_quantity = (
                    Decimal(f"{menge:.4f}"),
                    "HUR" if item[4] == "h" else "MIN",
                )  # C62 == pieces
                if item[1] and len(item[1]) == 10:
                    the_date = datetime.strptime(item[1], '%d.%m.%Y') # tatsächlicher Zeitpunkt der Tätigkeit
                    li.delivery.event.occurrence = the_date
                    if self.first_date == None:
                        self.first_date = the_date
                    else:
                        self.last_date = the_date # ich benutze nur den ersten Leistungsbezug, keinen Bereich
                li.settlement.trade_tax.type_code = "VAT"
                li.settlement.trade_tax.category_code = "S"
                li.settlement.trade_tax.rate_applicable_percent = Decimal("19.00")
                gesamt = float(item[6].split()[0].replace(",", "."))
                li.settlement.monetary_summation.total_amount = Decimal(f"{gesamt:.2f}")
                self.doc.trade.items.add(li)
            i = i + 1

    def add_gesamtsummen(self, dat):
        """add gesamtsumme to invoice"""
        netto = float(dat[0][1].split()[0].replace(",", "."))
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

        self.doc.trade.settlement.monetary_summation.line_total = Decimal(
            f"{netto:.2f}"
        )
        # self.doc.trade.settlement.monetary_summation.charge_total = Decimal("0.00")
        # self.doc.trade.settlement.monetary_summation.allowance_total = Decimal("0.00")
        self.doc.trade.settlement.monetary_summation.tax_basis_total = Decimal(
            f"{netto:.2f}"
        )
        self.doc.trade.settlement.monetary_summation.tax_total = (
            Decimal(f"{steuer:.2f}"),
            "EUR",
        )
        self.doc.trade.settlement.monetary_summation.grand_total = Decimal(
            f"{brutto:.2f}"
        )
        self.doc.trade.settlement.monetary_summation.due_amount = Decimal(
            f"{brutto:.2f}"
        )
        self.doc.trade.delivery.event.occurrence = self.first_date
        self.doc.trade.settlement.monetary_summation.charge_total = 0.00
        self.doc.trade.settlement.monetary_summation.allowance_total = 0.00

    def add_zahlungsziel(self, text, datum):
        """add zahlungsziel to zugferd"""
        terms = PaymentTerms()
        terms.description = text
        terms.due = datum
        self.doc.trade.settlement.terms.add(terms)

    def add_xml2pdf(self, in_file=None, out_file=None) -> None:
        """add xml content to out_file"""
        # Generate XML file
        xml = self.modify_xml(self.doc.serialize(schema="FACTUR-X_EXTENDED"))

        # print ('XML:', xml[:512])

        # Attach XML to an existing PDF.
        # Note that the existing PDF should be compliant to PDF/A-3!
        # You can validate this here: https://www.pdf-online.com/osa/validate.aspx
        if in_file:
            with open(in_file, "rb") as original_file:
                new_pdf_bytes = attach_xml(original_file.read(), xml, "EXTENDED")
        if self.debug:
            with open("factur-x.xml", "wb") as f:
                f.write(xml)
        if out_file:
            with open(out_file, "wb") as f:
                f.write(new_pdf_bytes)

    def modify_xml(self, xml=None):
        """insert xmlns:qdt if it is not in namespaces"""
        decoded = xml.decode('utf-8')
        searchstr = re.search(r'<rsm:CrossIndustryInvoice(.*)>', decoded).group()
        # print(searchstr)
        nsmap = searchstr.split(' ')
        _QDT = 'xmlns:qdt='
        if not _QDT in nsmap:
            QDT = _QDT + '\"' + NS_QDT + '\"'
            nsmap.insert(1, QDT)
            decoded = decoded.replace(searchstr, ' '.join(nsmap))
        # print ('MAP:', nsmap)

        return decoded.encode('utf-8')
