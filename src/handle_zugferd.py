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

from src.handle_other_objects import Adresse


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
        if bundesland:
            self.doc.trade.agreement.seller\
                .address.country_subdivision = bundesland

    def add_zahlungsempfaenger(self, text):
        """set Zahlungsempfaenger to correct value"""
        self.doc.trade.settlement.payment_means.type_code = (
            "58"  # SEPA Überweisung else "ZZZ"
        )
        self.doc.trade.settlement.payment_means.information.add(
            'Zahlung per SEPA Überweisung.'
            )
        arr = text.split("\n")
        # self.doc.trade.settlement.payee.name = arr[0] # BR-17
        self.doc.trade.settlement.payment_means\
            .payee_account.account_name = arr[0]
        if len(arr) > 1:
            self.doc.trade.settlement.payment_means.payee_account\
                .iban = arr[1].split(" ", 1)[1]
        if len(arr) == 3:
            self.doc.trade.settlement.payment_means.payee_institution\
                .bic = arr[2].split(" ", 1)[1]

    def _add_buyer_from_text(self, text: str) -> None:
        arr = text.split("\n")
        # self.doc.trade.settlement.invoicee.name = arr[0]
        self.doc.trade.agreement.buyer.name = arr[0]
        if len(arr) > 2:
            self.doc.trade.agreement.buyer.address.line_one = arr[1]
        if len(arr) > 3:
            self.doc.trade.agreement.buyer.address.line_one = arr[-2]
        if len(arr) > 1:
            self.doc.trade.agreement.buyer.address\
                .postcode = arr[-1].split(" ", 1)[0]
            self.doc.trade.agreement.buyer.address\
                .city_name = arr[-1].split(" ", 1)[1]

    def _add_str_hnr(self, buyer: Adresse) -> None:
        if buyer.postfach is not None:  # BT-50
            self.doc.trade.agreement.buyer.address.line_one =\
                'Postfach: ' + buyer.postfach
        elif buyer.strasse is not None:  # BT-50
            self.doc.trade.agreement.buyer.address.line_one =\
                buyer.strasse + ' ' + buyer.hausnummer

    def _add_plz_ort(self, buyer: Adresse) -> None:
        if buyer.plz is not None:  # BT-53
            self.doc.trade.agreement.buyer.address\
                .postcode = buyer.plz
        if buyer.ort is not None:  # BT-52
            self.doc.trade.agreement.buyer.address\
                .city_name = buyer.ort

    def _add_buyer_from_object(self, buyer: Adresse) -> None:
        if buyer.anschrift_line1 is not None:  # BT-44
            self.doc.trade.agreement.buyer.name = buyer.anschrift_line1
        if buyer.adresszusatz is not None:  # BT-51
            self.doc.trade.agreement.buyer.address.line_two =\
                buyer.adresszusatz
        self._add_str_hnr(buyer)
        self._add_plz_ort(buyer)

    def add_rechnungsempfaenger(self, text: str, adr: Adresse = None):
        """set Rechnungsempfänger"""
        self.doc.trade.settlement.currency_code = "EUR"
        # self.doc.trade.settlement.tax_currency_code = "EUR" # BR-53-1
        if adr is not None:
            self._add_buyer_from_object(adr)
        else:
            self._add_buyer_from_text(text)
        self.doc.trade.agreement.buyer.address.country_id = "DE"

    def _add_my_adresse(self, lieferant: Adresse):
        self.doc.trade.agreement.seller.id = lieferant.betriebsbezeichnung

        self.doc.trade.agreement.seller.name = lieferant.betriebsbezeichnung
        if lieferant.adresszusatz:
            self.doc.trade.agreement.\
                seller.address.line_two = lieferant.adresszusatz
        if lieferant.postfach:
            self.doc.trade.agreement.seller.address\
                .line_two = lieferant.postfach
        else:
            self.doc.trade.agreement.\
                seller.address.line_one = (
                    lieferant.strasse + ' ' + lieferant.hausnummer
                )
        self.doc.trade.agreement.seller.address\
            .postcode = lieferant.plz
        self.doc.trade.agreement.seller.address\
            .city_name = lieferant.ort
        self.doc.trade.agreement.seller.address.country_id = "DE"

    def _add_my_kontakt(self, lieferant: Adresse):
        if lieferant.name:
            self.doc.trade.agreement.seller.\
                contact.person_name = lieferant.name
        if lieferant.telefon:
            self.doc.trade.agreement.seller.\
                contact.telephone.number = lieferant.telefon
        if lieferant.fax:
            self.doc.trade.agreement.seller.\
                contact.telephone.fax.number = lieferant.fax
        if lieferant.email:
            self.doc.trade.agreement.seller.\
                contact.email.address = lieferant.email

    def add_my_company(self, lieferant: Adresse):
        """Add Address of my company to zugferd"""
        self._add_my_adresse(lieferant)
        self._add_my_kontakt(lieferant)
        self.add_bundesland(lieferant.bundesland)
        taxreg = TaxRegistration()
        taxreg.id = ("VA", lieferant.steuerid)\
            if lieferant.steuerid else ("FC", lieferant.steuernr)
        self.doc.trade.agreement.seller.tax_registrations.add(taxreg)
        # self.doc.trade.agreement.seller.tax = ustid

    def add_verwendungszweck(self, rg_nr: str, datum: str) -> None:
        """Add Verwendungszweck to zugferd BT-83"""
        self.doc.trade.settlement.payment_reference =\
            f"{rg_nr['key']} {rg_nr['value']} vom {datum}"

    def _fillPosAndNameOfLi(self, li: LineItem, item: list) -> None:
        li.document.line_id = item[0]  # Pos.
        # Datum + ': ' + Tätigkeit
        # li.product.name = item[1] + ": " + item[2]
        li.product.name = item[2]

    def _replaceCommaWithDot(self, item: str) -> float:
        return float(item.split()[0].replace(",", "."))

    def _setTaxInLi(self, li: LineItem, item: str, the_tax: str) -> None:
        li.settlement.trade_tax.type_code = "VAT"
        li.settlement.trade_tax\
            .category_code = "E" if the_tax == "0.00" else "S"
        li.settlement.trade_tax\
            .rate_applicable_percent = Decimal(the_tax)
        gesamt = self._replaceCommaWithDot(item)
        li.settlement.monetary_summation\
            .total_amount = Decimal(f"{gesamt:.2f}")

    def _set_date(self, item: str) -> datetime:
        if item == 'nan' or item == "":
            return self.last_date if self.last_date is not None\
                else datetime.today()
        else:
            return datetime.strptime(item, '%Y-%m-%d %H:%M:%S')

    def _setOccurrenceInLi(self, li: LineItem, item: str) -> None:
        if item is not None:
            the_date = self._set_date(item)
            # BG-26
            li.settlement.period.start = the_date  # BT-134
            li.settlement.period.end = the_date  # BT-135
            if self.first_date is None:
                self.first_date = the_date
            self.last_date = the_date

    def add_items(self, dat, the_tax: str):
        """add items to invoice"""
        # ("Pos.", "Datum", "Tätigkeit", "Menge", "Typ",
        #  "Einzel €", "Gesamt €")
        for i, item in enumerate(dat):
            if i > 0:
                li = LineItem()
                self._fillPosAndNameOfLi(li, item)
                menge = float(item[3])
                einzelpreisnetto = float(item[5])
                # self._replaceCommaWithDot(item[5])
                li.agreement.net.amount = Decimal(f"{einzelpreisnetto:.2f}")
                li.delivery.billed_quantity = (
                    Decimal(f"{menge:.4f}"),
                    "HUR" if item[4] == "h" else "MIN",
                )  # C62 == pieces
                self._setOccurrenceInLi(li, item[1])
                self._setTaxInLi(li, item[6], the_tax)
                self.doc.trade.items.add(li)

    def add_gesamtsummen(self, dat, the_tax: str,
                         steuerbefreiungsgrund: str = None) -> None:
        """add gesamtsumme to invoice"""
        netto = dat[0]
        steuer = dat[1]
        brutto = dat[2]

        trade_tax = ApplicableTradeTax()
        trade_tax.calculated_amount = steuer
        trade_tax.basis_amount = netto
        trade_tax.type_code = "VAT"
        trade_tax.category_code = "E" if the_tax == "0.00" else 'S'
        # trade_tax.exemption_reason_code = 'VATEX-EU-AE'
        trade_tax.rate_applicable_percent = Decimal(the_tax)
        if steuerbefreiungsgrund:
            trade_tax.exemption_reason = steuerbefreiungsgrund
        self.doc.trade.settlement.trade_tax.add(trade_tax)

        self.doc.trade.settlement.monetary_summation.line_total = netto
        # self.doc.trade.settlement.monetary_summation\
        #   .charge_total = Decimal("0.00")
        # self.doc.trade.settlement.monetary_summation\
        #   .allowance_total = Decimal("0.00")
        self.doc.trade.settlement.monetary_summation.tax_basis_total = netto
        self.doc.trade.settlement.monetary_summation.tax_total = (
            steuer,
            "EUR",
        )
        self.doc.trade.settlement.monetary_summation.grand_total = brutto
        self.doc.trade.settlement.monetary_summation.due_amount = brutto
        self.doc.trade.delivery.event.occurrence = self.first_date
        self.doc.trade.settlement.monetary_summation.charge_total = 0.00
        self.doc.trade.settlement.monetary_summation.allowance_total = 0.00
        # BG-14 - Rechnungszeitraum
        self.doc.trade.settlement.period.start = self.first_date  # BT-73
        self.doc.trade.settlement.period.end = self.last_date  # BT-74

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
        # You can validate this here:
        #   https://www.pdf-online.com/osa/validate.aspx
        if in_file:
            with open(in_file, "rb") as original_file:
                new_pdf_bytes = attach_xml(original_file.read(),
                                           xml, "EXTENDED")
        if self.debug:
            with open("factur-x.xml", "wb") as f:
                f.write(xml)
        if out_file:
            with open(out_file, "wb") as f:
                f.write(new_pdf_bytes)

    def modify_xml(self, xml=None):
        """insert xmlns:qdt if it is not in namespaces"""
        decoded = xml.decode('utf-8')
        searchstr = re.search(r'<rsm:CrossIndustryInvoice(.*)>',
                              decoded).group()
        # print(searchstr)
        nsmap = searchstr.split(' ')
        _QDT = 'xmlns:qdt='
        QDT = _QDT + '\"' + NS_QDT + '\"'
        if QDT not in nsmap:
            nsmap.insert(1, QDT)
            decoded = decoded.replace(searchstr, ' '.join(nsmap))
        # print ('MAP:', nsmap)

        return decoded.encode('utf-8')
