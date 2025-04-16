"""
Module handle_pdf
"""

# -*- coding: utf8 -*-

from datetime import datetime
import os
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode, OutputIntentSubType
from fpdf.output import PDFICCProfileObject

# import src.handle_zugferd as handle_zugferd
import src.handle_girocode as gc
import pandas as pd
import numpy as np
from src.invoice_collection import InvoiceCollection
import math
import locale
import decimal
from src.constants import P19USTG, GERMAN_DATE

LEFTofABSENDER = 135


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

    def _set_section(
        self, section: str, x: float, y: float, style: str, size: int
    ) -> None:
        """sets section, xy position, font"""
        if section is not None:
            self.start_section(section)
        self.set_xy(x, y)
        self.set_font(None, style, size)

    def print_absender(self, adress: str) -> None:
        """
        prints Absenderdaten
        """
        self._set_section("Absender", LEFTofABSENDER, 25.5, "", 11)
        arr = adress.splitlines()
        self.multi_cell(0, 5, "\n".join(arr[1:]))
        self._set_section("Abs-kurz", 25, 60.5, "U", 6)
        abs_kurz = ", ".join([arr[0], arr[-2], arr[-1]])
        self.cell(105, 1, abs_kurz)
        self.ln()

    def print_bundesland(self, bundesland: str) -> None:
        """
        prints Bundesland
        """
        self._set_section("Bundesland", LEFTofABSENDER, 54.5, "", 10)
        self.cell(105, 1, bundesland)

    def print_leistungszeitraum(self, von: str, bis: str) -> None:
        """
        prints Rechnungszeitraum
        """
        self._set_section("Leistungszeitraum", 25, 105, "", 10)
        self.cell(105, 1, f"Leistungszeitraum: {von} - {bis}")

    def print_kontakt(self, daten: str) -> None:
        """
        prints Kontakt
        """
        self._set_section("Kontakt", LEFTofABSENDER, 60, "", 10)
        self.multi_cell(105, 5, daten)

    def print_adress(self, adress: str) -> None:
        """
        prints Empfänger
        """
        self._set_section("Empfänger", 25, 63.6, "", 12)
        self.multi_cell(105, 5, adress)
        self.ln()

    def print_bezug(self, text: str) -> None:
        """
        prints Betreffzeile
        """
        self._set_section("Betreff", 25, 97.4, "B", 12)
        self.cell(None, None, text)
        self.ln()

    def _printTableHeader(self):
        """set table Header"""
        self._set_section("Rechnungspositionen", 25, 110, "", 10)
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
        return self.table_fill_color if self.table_fill_color else (244, 235, 255)

    def _set_variable_Breite(self, arr: list) -> list:
        fixeBreite = sum(arr)
        variableBreite = self._getTableWidth() - fixeBreite
        if variableBreite > 1:
            arr.insert(2, variableBreite)
            return arr
        return None

    def _calcColWidths(self, lengths: list) -> list:
        if lengths:
            arr = []
            for index, val in enumerate(lengths):
                # index 2 ist die Spalte
                # Bezeichnung, die ich als
                # eine variable Spalte haben möchte
                if index != 2:
                    arr.append(math.ceil(val * (2.4 if val > 3 else 2.9)))
        return self._set_variable_Breite(arr)

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
        last = None
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
                if data_row[1] == "":  # Datum
                    data_row[1] = last
                last = data_row[1]
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
        return self.sum_table_widths if self.sum_table_widths else (50, 22)

    def _getSummenTableWidth(self) -> int:
        return sum(self.sum_table_widths) if self.sum_table_widths else 72

    def print_summen(self, arr: list) -> None:
        """
        print Summen
        """
        # print(arr)
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

    def print_kleinunternehmerregelung(self, grund: str) -> None:
        """
        prints Begründung Kleinunternehmerregelung
        """
        self.start_section("Kleinunternehmen", 0)
        self.cell(105, 1, grund)
        self.ln(2)

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
        self.image(img.get_image(), w=30, h=30, keep_aspect_ratio=True)
        self.set_draw_color(0)
        self.set_x(28)
        self.set_font(None, "B", size=10)
        self.cell(80, 1, "Bezahlen via GiroCode")
        self.set_font(None, "", size=10)

    def uniquify(self, path: str, appendix: str = None) -> str:
        """
        make unique Path from filename
        """
        fn, ext = os.path.splitext(path)
        counter = 1

        if appendix is not None:
            equal = False
            for i in range(len(appendix) - 1):
                equal |= appendix[-(i + 1)] == fn[-(i + 1)]
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

    def __init__(self, logo_fn=None) -> None:
        super().__init__()
        self.logo_fn = logo_fn
        self.qrcode_img = None
        self.invoice: InvoiceCollection = None
        self.set_fonts_and_other_stuff()
        locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

    def set_fonts_and_other_stuff(self) -> None:
        """
        import and embed TTF Font to use € in text
        """
        self.add_font(
            "dejavu-sans", style="", fname="./_internal/Fonts/DejaVuSansCondensed.ttf"
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
        with open(os.path.join("_internal", "sRGB2014.icc"), "rb") as iccp_file:
            icc_profile = PDFICCProfileObject(
                contents=iccp_file.read(), n=3, alternate="DeviceRGB"
            )
        self.set_output_intent(
            OutputIntentSubType.PDFA,
            "sRGB",
            "IEC 61966-2-1:1999",
            "http://www.color.org",
            icc_profile,
            "sRGB2014 (v2)",
        )

    def fill_header(self) -> None:
        """
        populate header with data
        """
        self.set_title(self.invoice.supplier.betriebsbezeichnung)
        self.footer_txt = self.invoice.supplier_account.oneliner()
        self.set_author(self.invoice.supplier.name)

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
        self.print_absender(self.invoice.supplier.anschrift)
        bundesland = self.invoice.supplier.bundesland
        if bundesland and len(bundesland) > 0:
            self.print_bundesland(bundesland)
        self.print_kontakt(
            self.invoice.supplier.kontakt + "\n\n" + self.invoice.supplier.umsatzsteuer
        )

    def _fill_girocode(self, brutto, rg_nr, datum):
        girocode = gc.Handle_Girocode(
            self.invoice.supplier_account.bic,
            self.invoice.supplier_account.iban,
            self.invoice.supplier_account.name,
        )
        self.qrcode_img = girocode.girocodegen(
            brutto, f"{list(rg_nr.keys())[0]} {list(rg_nr.values())[0]} vom {datum}"
        )
        self.print_qrcode(self.qrcode_img)

    def _fill_kleinunternehmen(self) -> None:
        if self.invoice.management.is_kleinunternehmen:
            self.print_kleinunternehmerregelung(P19USTG)

    def get_maxlengths(self, df: pd.DataFrame) -> list:
        """
        get array with max string length of each column in pandas DataFrame
        """
        lenArr = []
        # print("get_maxlengths:\n", df)
        for c in df:
            theLength = max(df[c].astype(str).map(len).max(), len(c))
            # print('Max length of column %s: %s' % (c, theLength))
            lenArr.append(theLength)
        return lenArr

    def _currency(self, amount: float | decimal.Decimal) -> str:
        """return str as locale currency"""
        return locale.currency(amount, grouping=True)

    def get_von_bis_dates(self) -> list:
        """get min and max dates from positions

        Returns:
            list: min and max as list
        """
        df = self.invoice.positions
        retval = df.copy()
        headers = list(df.columns)
        retval[headers[1]] = pd.to_datetime(
            retval[headers[1]], errors="ignore"  # Datum
        )
        von = min(retval[headers[1]])
        bis = max(retval[headers[1]])
        return [von, bis]

    def _set_first_datum(self, df: pd.DataFrame, headers: list) -> None:
        """I expect Datum at second position in df"""
        if df.loc[df[headers[1]].index[0], headers[1]] == "":
            df.loc[df[headers[1]].index[0], headers[1]] = list(
                self.invoice.invoicedate.values()
            )[0].strftime(GERMAN_DATE)

    def _change_values_to_german(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        replace column Datum with german date %d.%m.%Y and columns Anzahl,
        Preis and Summe as float values with Komma separated
        """
        retval = df.copy()
        headers = list(df.columns)
        # retval.style.format({datum: lambda t: t.strftime("%d.%m.%Y")
        #                      if len(t) > 0 else ""})
        retval[headers[1]] = pd.to_datetime(
            retval[headers[1]], errors="ignore"  # Datum
        ).dt.strftime(GERMAN_DATE)
        # substitute NaN by ""
        retval[headers[1]] = retval[headers[1]].fillna("")
        self._set_first_datum(retval, headers)
        # print("_change_values_to_german:\n", retval)
        retval[headers[3]] = retval[headers[3]].apply("{:n}".format)  # Anzahl
        retval[headers[5]] = retval[headers[5]].apply(  # Preis
            lambda x: self._currency(x)
        )
        retval[headers[6]] = retval[headers[6]].apply(  # Summe
            lambda x: self._currency(x)
        )
        return retval

    def get_invoice_positions(self, positions: pd.DataFrame = None) -> dict:
        """
        return dict with array of array of positions for invoice
        and maxlengths of columns
        {'daten': np.r_[], 'maxlengths': []}
        """
        retval = self._change_values_to_german(positions)
        # print(retval)
        lenArr = self.get_maxlengths(retval)
        # print(lenArr)

        # return {'daten': np.r_[line.values, retval.astype(str).values],
        return {
            "daten": np.r_[[retval.columns], retval.astype(str).values],
            "maxlengths": lenArr,
        }

    def _fill_positions(self) -> None:
        # print(self.split_dataframe_by_SearchValue(AN, "Pos."))
        theDict = self.get_invoice_positions(self.invoice.positions)
        if len(theDict) > 0:
            self.print_positions(theDict["daten"], theDict["maxlengths"])

    def _fill_abspann(self, brutto: str, ueberweisungsdatum: datetime) -> None:
        abspann = (
            self.invoice.management.abspann
            if self.invoice.management.abspann
            and len(self.invoice.management.abspann) > 1
            else (
                "Mit freundlichen Grüßen\n" + self.invoice.supplier.name
                if self.invoice.supplier.name
                else ""
            )
        )
        self.print_abspann(
            f"Bitte überweisen Sie den Betrag von {brutto} bis zum \
{ueberweisungsdatum.strftime(GERMAN_DATE)} auf \
u.a. Konto.\n\n{abspann}"
        )

    def _get_value(self, tuple) -> str:
        _, v = tuple
        return v

    def _toLocaleFloatStr(self, inp: str) -> str:
        """convert string witch float to locale float string"""
        return locale.format_string("%.f", float(inp), grouping=True)

    def get_invoice_sums(self):
        """return array of invoice sums"""
        netto = self._get_value(self.invoice.sums[0])
        umsatzsteuer = self._get_value(self.invoice.sums[1])
        brutto = self._get_value(self.invoice.sums[-1])
        satz = self._toLocaleFloatStr(self.invoice.supplier.steuersatz)
        UST = f"zzgl. Umsatzsteuer {satz}%:"
        return [
            ("Summe netto:", self._currency(netto)),
            (UST, self._currency(umsatzsteuer)),
            ("Bruttobetrag:", self._currency(brutto)),
        ]

    def fill_pdf(self, invoice: InvoiceCollection) -> None:
        """
        set own data
        """
        self.invoice = invoice
        self.fill_header()

        self.print_adress(self.invoice.customer.anschrift)
        rg_nr = self.invoice.invoicenr  # _get_rg_nr()
        # today = datetime.now()
        datum = list(invoice.invoicedate.values())[0]
        von, bis = self.get_von_bis_dates()
        ueberweisungsdatum = self.invoice.supplier.get_ueberweisungsdatum(datum)

        self.print_bezug(
            f"{list(rg_nr.keys())[0]} {list(rg_nr.values())[0]} vom\
 {datum.strftime(GERMAN_DATE)}"
        )

        self.print_leistungszeitraum(
            von.strftime(GERMAN_DATE), bis.strftime(GERMAN_DATE)
        )
        self._fill_positions()

        summen = self.get_invoice_sums()
        brutto = self._get_value(summen[-1])
        self.print_summen(summen)

        self._fill_kleinunternehmen()
        # if self.lieferantensteuerung.create_xml:
        #     self.fill_xml(rg_nr, summen, brutto, ueberweisungsdatum, datum)
        self._fill_abspann(brutto, ueberweisungsdatum)

        if self.invoice.management.create_girocode:
            self._fill_girocode(
                locale.atof(brutto.strip(" €")), rg_nr, datum.strftime(GERMAN_DATE)
            )
