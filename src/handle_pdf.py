"""
Module handle_pdf
"""

# -*- coding: utf8 -*-

from datetime import datetime, timedelta
import os
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode, OutputIntentSubType
from src.excel_content import ExcelContent
import src.handle_zugferd as handle_zugferd
import src.handle_girocode as gc
from src.handle_other_objects import Adresse, Konto, Steuerung
import math

GERMAN_DATE = "%d.%m.%Y"
P19USTG = "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."


class PDF(FPDF):
    """
    Base Class for my PDF
    """

    def __init__(self, footer_txt: str = ""):
        super().__init__()
        self.footer_txt = footer_txt
        self.table_lines = None
        self.table_head_color = None
        self.table_head = None
        self.table_fill_color = None
        self.table_widths = None
        self.sum_table_widths = None

    def footer(self) -> None:
        """
        declare a footer for the pdf file
        """
        if len(self.footer_txt) == 0:
            return
        self.set_y(-15)
        self.set_font_size(size=8)
        self.cell(
            0,
            1,
            self.footer_txt,
            align="C",
        )
        self.ln()
        self.set_font(None, "I", 8)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")

    def header(self) -> None:
        if not hasattr(self, "title"):
            return
        # Setting font: origin font bold 15
        self.set_font(None, "B", 15)
        # Calculating width of title and setting cursor position:
        width = self.get_string_width(self.title) + 6
        # self.set_x((210 - width) / 2)
        self.set_x(25)
        # Setting colors for frame, background and text:
        # self.set_draw_color(0, 80, 180)
        # self.set_fill_color(230, 230, 0)
        # self.set_text_color(220, 50, 50)
        # Setting thickness of the frame (1 mm)
        self.set_line_width(1)
        # Printing title:
        self.cell(
            width,
            9,
            self.title,
            # border=1,
            new_x="LMARGIN",
            new_y="NEXT",
            align="L",
            # fill=True,
        )
        # Performing a line break:
        self.ln()

    def print_faltmarken(self) -> None:
        """
        prints Falt- und Lochmarkierungen
        """
        self.line(4, 105, 8, 105)
        self.line(3, 148.5, 6, 148.5)  # Lochmarke
        self.line(4, 210, 8, 210)

    def print_absender(self, adress: str) -> None:
        """
        prints Absenderdaten
        """
        self.start_section("Absender", 0)
        self.set_xy(140, 25.5)
        self.set_font_size(12)
        self.multi_cell(105, 5, adress)
        self.set_xy(25, 60.5)
        self.set_font(None, "U", size=6)
        self.cell(105, 1, adress.replace("\n", ", "))
        self.ln()

    def print_bundesland(self, bundesland: str) -> None:
        """
        prints Bundesland
        """
        self.start_section("Bundesland", 0)
        self.set_xy(140, 54.5)
        self.set_font(None, "", 10)
        self.cell(105, 1, bundesland)

    def print_kleinunternehmerregelung(self, grund: str) -> None:
        """
        prints Begründung Kleinunternehmerregelung
        """
        self.start_section("Kleinunternehmen")
        self.set_xy(25, 105)
        self.set_font(None, "", 10)
        self.cell(105, 1, grund)

    def print_kontakt(self, daten: str) -> None:
        """
        prints Kontakt
        """
        self.start_section("Kontakt", 0)
        self.set_xy(140, 60)
        self.set_font(None, "", size=10)
        self.multi_cell(105, 5, daten)

    def print_adress(self, adress: str) -> None:
        """
        prints Empfänger
        """
        self.start_section("Empfänger", 0)
        self.set_xy(25, 63.6)
        self.set_font_size(12)
        self.multi_cell(105, 5, adress)
        self.ln()

    def print_bezug(self, text: str) -> None:
        """
        prints Betreffzeile
        """
        self.start_section("Betreff", 0)
        self.set_xy(25, 97.4)
        self.set_font(None, "B", size=12)
        self.cell(None, None, text)
        self.ln()

    def _printTableHeader(self):
        """set table Header"""
        self.start_section("Rechnungspositionen", 0)
        self.set_xy(25, 110)
        self.set_font(None, "", size=10)
        if self.table_lines:
            self.set_draw_color(self.table_lines)
        else:
            self.set_draw_color(0, 0, 255)
        self.set_line_width(0.3)

    def _getHeadingsStyle(self):
        """return headings_style"""
        return FontFace(
            emphasis="BOLD",
            color=self.table_head_color if self.table_head_color else 255,
            fill_color=self.table_head if self.table_head else (255, 100, 0),
        )

    def _getCellFillColor(self):
        return (
                self.table_fill_color if self.table_fill_color
                else (244, 235, 255)
            )

    def _calcColWidths(self, lengths: list) -> list:
        retval = None
        if lengths:
            arr = []
            for index, val in enumerate(lengths):
                # index 2 ist die Spalte
                # Bezeichnung, die ich als
                # eine variable Spalte haben möchte
                if index != 2:
                    arr.append(math.ceil(val * 2.4))
            fixeBreite = sum(arr)
            variableBreite = self._getTableWidth() - fixeBreite
            if variableBreite > 1:
                arr.insert(2, variableBreite)
                retval = arr
        return retval

    def _getColWidths(self, lengths: list) -> tuple:
        default = (10, 21, 68, 16, 15, 16, 19)
        arr = self._calcColWidths(lengths)
        return tuple(arr) if arr else default
        # return (
        #         self.table_widths
        #         if hasattr(self, "table_widths")
        #         else
        #           return (10, 21, 68, 16, 15, 16, 19)
        #         # wird in der abgeleiteten Klasse Pdf gesetzt !!!
        #     )

    def _getTableWidth(self) -> int:
        return 165
        # return (sum(self.table_widths) if self.table_widths
        #         else 165)

    def print_positions(self, arr: list, lengths: list = None) -> None:
        """
        prints Table with Positions
        """
        self._printTableHeader()
        with self.table(
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_color=self._getCellFillColor(),
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=self._getColWidths(lengths),
            text_align=(
                "CENTER",
                "LEFT",
                "LEFT",
                "CENTER",
                "CENTER",
                "RIGHT",
                "RIGHT",
            ),
            align="RIGHT",
            headings_style=self._getHeadingsStyle(),
            line_height=5.5,
            width=self._getTableWidth(),
            padding=(2, 0, 2, 0),
            v_align="TOP",
        ) as table:
            for data_row in arr:
                table.row(data_row)

    def _printSummenHeader(self) -> None:
        self.start_section("Rechnungssumme", 0)
        self.set_x(153)
        self.ln()
        self.set_font(None, "", size=10)
        if self.table_lines:
            self.set_draw_color(self.table_lines)
        else:
            self.set_draw_color(255, 0, 255)
        self.set_line_width(0.3)

    def _getTableFillColor(self) -> tuple:
        return (
                self.table_fill_color
                if hasattr(self, "table_fill_color")
                else (244, 235, 255)
            )

    def _getSummenColWidths(self) -> tuple:
        return (self.sum_table_widths if self.sum_table_widths
                else (50, 22))

    def _getSummenTableWidth(self) -> int:
        return sum(self.sum_table_widths) if self.sum_table_widths else 72

    def print_summen(self, arr: list) -> None:
        """
        print Summen
        """
        self._printSummenHeader()
        # headings_style = FontFace(emphasis="BOLD", color=255,
        # fill_color=self.table_head
        # if hasattr(self, "table_head")
        # else (255, 100, 0))
        with self.table(
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_color=self._getTableFillColor(),
            cell_fill_mode=TableCellFillMode.ROWS,
            col_widths=self._getSummenColWidths(),
            text_align=(
                "RIGHT",
                "RIGHT",
            ),
            first_row_as_headings=False,
            align="RIGHT",
            # headings_style=headings_style,
            line_height=5.5,
            width=self._getSummenTableWidth(),
            padding=(2, 0, 2, 0),
            v_align="TOP",
        ) as table:
            for data_row in arr:
                table.row(data_row)
        self.ln()

    def print_abspann(self, text: str) -> None:
        """
        print Abspann
        """
        self.ln()
        self.ln()
        self.start_section("Abspann", 0)
        self.set_font_size(12)
        self.multi_cell(0, None, text)
        self.ln()

    def print_logo(self, fn: str) -> None:
        """
        print Logo
        """
        if fn is None:
            return
        self.start_section("Logo", 0)
        rect1 = 27, 30, 20, 20
        self.set_draw_color(255)
        self.rect(*rect1)
        self.image(fn, *rect1, keep_aspect_ratio=True)
        self.set_draw_color(0)

    def print_qrcode(self, img: object) -> None:
        """
        print qrcode
        """
        if img is None:
            return
        # rect1 = 27, 30, 20, 20
        self.start_section("GiroCode", 0)
        self.set_draw_color(255)
        # self.rect(*rect1)
        self.image(img.get_image(), w=30, h=30,
                   keep_aspect_ratio=True)
        self.set_draw_color(0)
        self.set_x(28)
        self.set_font(None, "B", size=10)
        self.cell(80, 1, 'Bezahlen via GiroCode')
        self.set_font(None, "", size=10)

    def uniquify(self, path: str, appendix: str = None) -> str:
        """
        make unique Path from filename
        """
        fn, ext = os.path.splitext(path)
        counter = 1

        if appendix is not None:
            equal = False
            for i in range(len(appendix)-1):
                equal |= (appendix[-(i+1)] == fn[-(i+1)])
            fn = f"{fn}{appendix}" if not equal else fn
            path = f"{fn}" + ext

        while os.path.exists(path):
            path = f"{fn} ({str(counter)})" + ext
            counter += 1
        return path


class Pdf(PDF):
    """
    Klasse Pdf
    """

    def __init__(self, daten, stammdaten, logo_fn=None)\
            -> None:
        super().__init__()
        # print(daten)
        # print("----------")
        # print(stammdaten)
        self.logo_fn = logo_fn
        self.daten = daten if isinstance(daten, ExcelContent) else None
        self.stammdaten = stammdaten if stammdaten is not None else {}
        self.qrcode_img = None
        self.lieferant = Adresse()
        self.lieferantenkonto = Konto()
        self.lieferantensteuerung = Steuerung()
        self.empfaenger = Adresse()
        self.lieferant.fill_lieferant(stammdaten)
        self.lieferantensteuerung.fill_steuerung(stammdaten)
        self.lieferantenkonto.fill_konto(stammdaten)
        self.set_fonts_and_other_stuff()

    def set_fonts_and_other_stuff(self) -> None:
        """
        import and embed TTF Font to use € in text
        """
        self.add_font(
            "dejavu-sans", style="",
            fname="./_internal/Fonts/DejaVuSansCondensed.ttf"
        )
        self.add_font(
            "dejavu-sans",
            style="b",
            fname="./_internal/Fonts/DejaVuSansCondensed-Bold.ttf",
        )
        self.add_font(
            "dejavu-sans",
            style="i",
            fname="./_internal/Fonts/DejaVuSansCondensed-Oblique.ttf",
        )
        self.add_font(
            "dejavu-sans",
            style="bi",
            fname="./_internal/Fonts/DejaVuSansCondensed-BoldOblique.ttf",
        )
        # use the font imported
        self.set_font("dejavu-sans")
        self.set_lang("de_DE")
        # set left, top and right margin for document
        self.set_margins(25, 16.9, 20)
        self.set_output_intents(
            OutputIntentSubType.PDFA,
            "sRGB",
            "IEC 61966-2-1:1999",
            "http://www.color.org",
            FPDF.dest_output_profile(
                fn=os.path.join("_internal", "sRGB2014.icc"), N=3,
                alternate="DeviceRGB"
            ),
            "sRGB2014 (v2)",
        )

    def demo(self) -> None:
        """
        Demo for creation of Pdf
        """
        today = datetime.now()
        german_date = "%d.%m.%Y"
        datum = today.strftime(german_date)
        ueberweisungsdatum = (today + timedelta(days=14)).strftime(german_date)
        # self = self()

        #
        self.table_head = (
            255  # white fill-color of Table Header (30, 144, 255)
            # DodgerBlue1
        )
        self.table_head_color = 0  # black text-color of Table Header
        self.table_lines = 0  # black (0, 0, 255)  # Blue
        self.table_fill_color = 220  # lightgrey
        self.table_widths = (10, 21, 68, 16, 15, 16, 19)
        # (11, 22, 61, 16, 20, 21, 21)
        self.table_lines = 120  # darkgrey

        self.set_title("Max Mustermann - Softwareentwicklung")
        self.footer_txt = (
            "Max Mustermann, IBAN: DE 6472482348234234248794, \
                BIC: BICOFINSTITUTE"
        )
        self.set_author("M. Mustermann")
        self.add_page()
        self.print_faltmarken()
        self.print_absender(
            "Max Mustermann\nSoftwareentwicklung\nDorfstr. 712\n\
                65432 Musterdorf"
        )
        self.print_kontakt(
            "Tel.: 0813-12345678\nEMail: max@mustermann.de\n\nSteuer-Nr: \
                081519/987543\nFinanzamt Musterdorf"
        )
        self.print_adress(
            "Empfängerfirma GmbH\nFrau Anette Musterfrau\nDorfstr. 10\n\
                65432 Musterdorf"
        )
        self.print_bezug(f"Rechnung Nr. 123456 vom {datum}")

        self.print_positions(
            [
                ("Pos.", "Datum", "Tätigkeit", "Menge", "Typ", "Einzel €",
                 "Gesamt €"),
                (
                    "1",
                    "01.01.2024",
                    "Irgendwas, das länger ist als zwei Zeilen in der Ausgabe \
                        mit einer Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "10 Min.",
                    "22.00",
                    "22.00",
                ),
                (
                    "2",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "3",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "4",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "5",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "6",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "7",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "8",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "9",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer\
                          Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "10",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "1",
                    "h",
                    "75.00",
                    "75.00",
                ),
                (
                    "11",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "2",
                    "10 Min.",
                    "22.00",
                    "44.00",
                ),
                (
                    "12",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "2",
                    "10 Min.",
                    "22.00",
                    "44.00",
                ),
                (
                    "13",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "2",
                    "10 Min.",
                    "22.00",
                    "44.00",
                ),
                (
                    "14",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "2",
                    "10 Min.",
                    "22.00",
                    "44.00",
                ),
                (
                    "15",
                    "02.01.2024",
                    "Irgendwas, das länger ist als eine Zeilen und einer \
                        Dokumentation dessen, was geleistet wurde.",
                    "2",
                    "10 Min.",
                    "22.00",
                    "44.00",
                ),
            ]
        )

        self.print_summen(
            [
                ("Summe Netto:", "1.540,00 €"),
                ("zzgl. Umsatzsteuer 19%:", "84,98 €"),
                ("Gesamt:", "1.690,98 €"),
            ]
        )

        self.print_abspann(
            f"Bitte überweisen Sie den Betrag von 1.690,98 € bis zum \
{ueberweisungsdatum} auf u.a. Konto.\
\n\nMit freundlichen Grüßen\nMax Mustermann",
        )

        self.output("hello_world.pdf")

    def fill_header(self) -> None:
        """
        populate header with data
        """
        self.set_title(self.lieferant.betriebsbezeichnung)
        self.footer_txt = self.lieferantenkonto.oneliner()
        self.set_author(self.lieferant.name)

        self.table_head = (
            255  # white fill-color of Table Header (30, 144, 255)
            # DodgerBlue1
        )
        self.table_head_color = 10  # 0  # black text-color of Table Header
        self.table_lines = 0  # black (0, 0, 255)  # Blue
        self.table_fill_color = 220  # lightgrey
        self.table_widths = (10, 21, 61, 16, 15, 21, 21)
        # (11, 22, 61, 16, 20, 21, 21)
        self.table_lines = 120  # darkgrey

        self.add_page()
        self.print_faltmarken()
        self.print_logo(self.logo_fn)
        self.print_absender(self.lieferant.get_anschrift())
        bundesland = self.lieferant.bundesland
        if len(bundesland) > 0:
            self.print_bundesland(bundesland)
        self.print_kontakt(
            self.lieferant.get_kontakt() + "\n\n" +
            self.lieferant.get_umsatzsteuer()
        )

    def fill_lieferant_to_note(self) -> None:
        """
        populate note with addressfields for ZugFeRD
        """
        txt = (
            self.lieferant.get_anschrift()
            + "\n"
            + self.lieferant.get_kontakt()
            + "\n"
            + self.lieferant.get_umsatzsteuer()
        )
        self.zugferd.add_note(txt)

    def _fill_girocode(self, brutto, rg_nr, datum):
        girocode = gc.Handle_Girocode(self.lieferantenkonto.bic,
                                      self.lieferantenkonto.iban,
                                      self.lieferantenkonto.name)
        self.qrcode_img = girocode.girocodegen(
            float(brutto.split(' ')[0].replace(',', '.')),
            f"{rg_nr['key']} {rg_nr['value']} vom {datum}")
        self.print_qrcode(self.qrcode_img)

    def _fill_kleinunternehmen(self) -> None:
        if self.lieferantensteuerung.is_kleinunternehmen:
            self.print_kleinunternehmerregelung(P19USTG)

    def _get_ueberweisungsdatum(self, today: datetime) -> datetime:
        return (
            today
            + timedelta(
                days=int(
                    self.lieferant.zahlungsziel
                    if self.lieferant.zahlungsziel > ""
                    else "0"
                )
            )
        )

    def _get_rg_nr(self) -> list:
        rg_nr = self.daten.get_invoice_number() if self.daten else {}
        return {'key': list(rg_nr.keys())[0],
                'value': rg_nr[list(rg_nr.keys())[0]]}

    def _get_the_tax(self) -> str:
        return "0.00" if self.lieferantensteuerung.is_kleinunternehmen\
                        else "19.00"

    def _fill_positions(self) -> None:
        # print(self.split_dataframe_by_SearchValue(AN, "Pos."))
        theDict = self.daten.get_invoice_positions() if self.daten else []
        if len(theDict) > 0:
            self.print_positions(theDict['daten'], theDict['maxlengths'])

    def _fill_invoice_positions_in_xml(self) -> None:
        """fills invoice positions into ZugFeRD"""
        theDict = self.daten.get_invoice_positions() if self.daten else []
        if len(theDict) > 0:
            df = theDict['daten']
            self.zugferd.add_items(df, self._get_the_tax())

    def _fill_abspann(self, brutto: str, ueberweisungsdatum: datetime) -> None:
        abspann = (
            self.lieferantensteuerung.abspann
            if len(self.lieferantensteuerung.abspann) > 1
            else "Mit freundlichen Grüßen\n" + self.lieferant.name
        )
        self.print_abspann(
            f"Bitte überweisen Sie den Betrag von {brutto} bis zum \
{ueberweisungsdatum.strftime(GERMAN_DATE)} auf u.a. Konto.\n\n{abspann}"
        )

    def fill_xml(self, rg_nr: list, an: str, summen: list,
                 brutto: str, ueberweisungsdatum: datetime,
                 datum: str) -> None:
        """
        fills data into ZugFeRD part
        """
        self.zugferd = handle_zugferd.ZugFeRD()
        kleinunternehmen = self.lieferantensteuerung.is_kleinunternehmen
        self.zugferd.add_zahlungsempfaenger(
            self.lieferantenkonto.multiliner())

        self.fill_lieferant_to_note()
        self.zugferd.add_my_company(self.lieferant)
        self.zugferd.add_rgnr(f"{rg_nr['value']}")
        self.zugferd.add_rechnungsempfaenger(an)
        self._fill_invoice_positions_in_xml()
        self.zugferd.add_gesamtsummen(summen,
                                      self._get_the_tax(),
                                      P19USTG if kleinunternehmen else None)
        self.zugferd.add_zahlungsziel(
            f"Bitte überweisen Sie den Betrag von {brutto} bis zum",
            ueberweisungsdatum,
        )
        self.zugferd.add_verwendungszweck(rg_nr, datum)

    def fill_pdf(self) -> None:
        """
        set own data
        """
        self.fill_header()

        self._fill_kleinunternehmen()
        an = self.daten.get_address_of_customer() if self.daten else ""
        self.print_adress(an)
        rg_nr = self._get_rg_nr()
        today = datetime.now()
        datum = today.strftime(GERMAN_DATE)
        ueberweisungsdatum = self._get_ueberweisungsdatum(today)

        self.print_bezug(
            f"{rg_nr['key']} {rg_nr['value']} vom {datum}"
        )

        self._fill_positions()
        summen = self.daten.get_invoice_sums() if self.daten else []
        brutto = summen[-1][-1]
        self.print_summen(summen)
        if self.lieferantensteuerung.create_xml:
            self.fill_xml(rg_nr, an, summen, brutto, ueberweisungsdatum, datum)
        self._fill_abspann(brutto, ueberweisungsdatum)

        if self.lieferantensteuerung.create_girocode:
            self._fill_girocode(brutto, rg_nr, datum)
