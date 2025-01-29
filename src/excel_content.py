"""
Module excel_content
"""

import os
from datetime import datetime, time
import pandas as pd
# from src.handle_other_objects import Adresse
from src.kunde import Kunde
from src.steuerung import Steuerung
from src.constants import DATUM_NOT_FOUND_ERR, ANSCHRIFT_DEFAULT_SPALTE, \
    RGNR_DEFAULT_SPALTE, RGDATUM_REFAULT_SPALTE
import decimal
import string


class ExcelContent:
    """Handle Content of Excel Files"""

    def __init__(self, filename: str, directory: str):
        self.fn: str = filename
        self.dir: str = directory
        self.path: str = os.path.join(self.dir, self.fn)\
            if '/' not in filename else filename
        self.daten: pd.DataFrame = None
        try:
            self.xlsx = pd.ExcelFile(self.path)
            pd.options.mode.copy_on_write = True
        except FileNotFoundError:
            print(f"file not found '{self.path}'")
            pass

    def read_sheet_list(self):
        """Read the List of Sheets in this Excel File"""
        return self.xlsx.sheet_names

    def read_sheet(self, sheet_name) -> pd.DataFrame:
        """Read the specified sheet content"""
        # self.daten = self.xlsx.parse(sheet_name, header=None)
        self.daten = pd.read_excel(io=self.xlsx, sheet_name=sheet_name,
                                   header=None)
        self.daten.columns = list(string.ascii_uppercase)[0:len(self.daten
                                                                .columns)]
        self.daten.index = range(1, len(self.daten.index)+1)
        # print(self.daten)
        return self.daten

    def mapReducePositions(self, inp: pd.DataFrame, columns: list,
                           start_row: str = "1") -> pd.DataFrame:
        """maps and reduces DataFrame inp to expected columns"""
        reduced = inp.loc[int(start_row):, columns]
        noneIdx = self._get_index_of_nan(reduced[columns[0]])
        # print(f"NoneIdx = {noneIdx}\n", reduced[columns[0]])
        reduced.columns = reduced.loc[int(reduced.index[0])]
        return reduced.iloc[1:noneIdx] if noneIdx != -1 else reduced

    def _get_search_err(self, search_value: str, column_name: str) -> str:
        """return ErrorMessage for search_err"""
        return f"Ich konnte '{search_value}' in Spalte '{column_name}'\
 nicht finden."

    def _get_col_err(self, column_name: str) -> str:
        """return ErrorMessage for col_err"""
        return f"Ich konnte die Spalte '{column_name}' nicht finden."

    def _search_cell_in_column(self, column_name: str, search_value: str)\
            -> list:
        """
        Search in row with column_name for search_value,
            return array with values right of the search_value
        """
        SEARCH_ERR = ValueError(
            self._get_search_err(search_value, column_name))
        COL_ERR = ValueError(self._get_col_err(column_name))
        try:
            arr = self.daten.loc[self.daten[column_name] == search_value]
        except IndexError:
            raise SEARCH_ERR
        except KeyError:
            raise COL_ERR
        return arr

    def _check_raise(self, error_msg: str, raiseIfNotFound: bool) -> None:
        SEARCH_ERR = ValueError(error_msg)
        if raiseIfNotFound:
            raise SEARCH_ERR

    def _get_value_of_row_in_next_column(self, arr: list, col: str,
                                         error_msg: str,
                                         raiseIfNotFound: bool = True)\
            -> any:
        """return value at next cell"""
        retval = None
        try:
            idx = list(arr.columns).index(col) + 1
            retval = arr.iat[0, idx]
        except TypeError:
            self._check_raise(error_msg, raiseIfNotFound)
        except IndexError:
            self._check_raise(error_msg, raiseIfNotFound)
        if pd.isna(retval):
            retval = None
        return retval

    def search_cell_right_of(self, column_name: str, search_value: str,
                             raiseIfNotFound: bool = True) -> any:
        """
        Search in row with column_name for search_value,
            return value right of the search_value
        """
        if self.daten is None:
            return ""
        arr = self._search_cell_in_column(column_name, search_value)
        return self._get_value_of_row_in_next_column(arr,
                                                     column_name,
                                                     self._get_search_err(
                                                        search_value,
                                                        column_name),
                                                     raiseIfNotFound)

    def _get_index_of_nan(self, df: pd.DataFrame) -> int:
        """get first index of next NaN"""
        return next((i for i, v in enumerate(df) if v != v), -1)

    def _search_anschrift(self, spalte: str, zeile: str, search: str,
                          customer: Kunde) -> None:
        """
        Search in specified column until next NaN,
        and fill it into anschrift of customer
        """
        if self.daten is None:
            return None
        an = self.daten[spalte]
        fromIdx = self.daten.index.to_list().index(int(zeile)) if zeile else\
            self.daten.index[an == search].tolist()[0]
        nan_idx = self._get_index_of_nan(an)  # get first index of NaN in an
        # arr = an[fromIdx:nan_idx].to_list()
        arr = ('\n'.join(an[fromIdx:nan_idx].to_list())).splitlines()
        # print("_search_anschrift:\n", arr)
        if customer:
            customer.anschrift = arr
            customer.landeskennz = "DE"

    def _get_err_objects(self, column_name: str, search_value: str) -> list:
        SEARCH_ERR = ValueError(f"Ich konnte '{search_value}'\
 in Spalte '{column_name}' nicht finden.")
        COL_ERR = ValueError(f"Ich konnte\
 die Spalte '{column_name}' nicht finden.")
        return [SEARCH_ERR, COL_ERR]

    def _get_line_with_search_value_in_column(self, column_name: str,
                                              search_value: str)\
            -> pd.DataFrame:
        SEARCH_ERR, COL_ERR = self._get_err_objects(column_name, search_value)
        try:
            line = self.daten[self.daten[column_name] == search_value]
        except KeyError:
            raise COL_ERR
        except IndexError:
            raise SEARCH_ERR
        return line

    def _split_dataframe_by_search_value(self, column_name: str,
                                         search_value: str) -> pd.DataFrame:
        """
        Search in specified column for search_value return rows until next NaN
        as pandas dataFrame
        """
        if self.daten is None:
            return None
        line = self._get_line_with_search_value_in_column(column_name,
                                                          search_value)
        SEARCH_ERR, COL_ERR = self._get_err_objects(column_name, search_value)
        # print(line)
        try:
            start_index = int(line.index[0])  # + 1
        except IndexError:
            raise SEARCH_ERR

        tmpdf = self.daten.iloc[
            start_index : len(self.daten), :  # noqa: E203
        ]
        nan_idx = self._get_index_of_nan(tmpdf[column_name])
        retval = tmpdf[0:nan_idx]
        retval.columns = line.loc[int(line.index[0])]
        # print(retval)
        return retval

    def get_address_of_customer(self, spalte: str = ANSCHRIFT_DEFAULT_SPALTE,
                                anschrift: str = "An:",
                                customer: Kunde = None,
                                zeile: str = None):
        """returns address of customer in Excel Sheet with \\n joined values"""
        return self._search_anschrift(spalte, zeile, anschrift, customer)

    def _get_content_at(self, spalte: str, zeile: int) -> any:
        return self.daten.at[int(zeile), spalte]

    def get_invoice_number(self, spalte: str = RGNR_DEFAULT_SPALTE,
                           rg_nr: str = "Rechnungs-Nr:",
                           zeile: str = None
                           ) -> dict:
        """returns tuple ('InvoiceNumberText', invoiceNumber)"""
        theDict = {rg_nr: self._get_content_at(spalte, zeile) if zeile else
                   self.search_cell_right_of(spalte, rg_nr)}
        # self.invoice.invoicenr = theDict   # ToDo. eliminate
        return theDict

    def get_invoice_date(self, spalte: str = RGDATUM_REFAULT_SPALTE,
                         rg_date: str = "Rechnungsdatum:",
                         zeile: str = None
                         ) -> any:
        """returns tuple ('InvoiceDateText', invoiceDate)"""
        if zeile:
            value = self._get_content_at(spalte, zeile)
            if pd.isna(value):
                raise ValueError(DATUM_NOT_FOUND_ERR)
        else:
            value = self.search_cell_right_of(spalte, rg_date, False)
            if value is None:
                today = datetime.now()
                value = datetime.combine(today.date(), time.min)
        theDict = {rg_date:  value}

        return theDict

    def get_invoice_positions(self, spalte: str = "A",
                              search: str = "Pos.",
                              mgmnt: Steuerung = None
                              ) -> dict:
        """
        return pandas DataFrame with positions for invoice
        """
        if mgmnt and mgmnt.positionen_zeile:
            columns = [mgmnt.pos_spalte, mgmnt.dat_spalte,
                       mgmnt.desc_spalte, mgmnt.anz_spalte, mgmnt.typ_spalte,
                       mgmnt.preis_spalte, mgmnt.sum_spalte]
            return self.mapReducePositions(self.daten, columns,
                                           mgmnt.positionen_zeile)
        return self._split_dataframe_by_search_value(spalte, search)

    def _round(self, value, prec: int) -> decimal.Decimal:
        """round decimal to prec as in excel"""
        precStr = '1.' + '0' * prec
        rounded = (decimal.Decimal(value + 0.0000000001)
                   .quantize(decimal.Decimal(precStr),
                             rounding=decimal.ROUND_HALF_UP)
                   )
        # print("_round:", value, ' = ', rounded)
        return rounded

    def _get_netto_sum(self, spalte: str, search: str,
                       management: Steuerung) -> any:
        if (management is not None and
                management.nettosumme_zeile is not None):
            return self._get_content_at(management.nettosumme_spalte,
                                        management.nettosumme_zeile)
        else:
            return self.search_cell_right_of(spalte, search)

    def _get_ust_sum(self, spalte: str, search: str,
                     management: Steuerung) -> any:
        if (management is not None and
                management.mwstsumme_zeile is not None):
            return self._get_content_at(management.mwstsumme_spalte,
                                        management.mwstsumme_zeile)
        else:
            return self.search_cell_right_of(spalte, search)

    def _get_brutto_sum(self, spalte: str, search: str,
                        management: Steuerung) -> any:
        if (management is not None and
                management.bruttosumme_zeile is not None):
            return self._get_content_at(management.bruttosumme_spalte,
                                        management.bruttosumme_zeile)
        else:
            return self.search_cell_right_of(spalte, search)

    def get_invoice_sums(self,
                         spalte: str = "F",
                         sum: str = "Summe",
                         USt: str = "Umsatzsteuer 19%",
                         bruttobetr: str = "Bruttobetrag",
                         management: Steuerung = None
                         ):
        """return array of invoice sums"""
        netto = self._get_netto_sum(spalte, sum, management)
        umsatzsteuer = self._get_ust_sum(spalte, USt, management)
        brutto = self._get_brutto_sum(spalte, bruttobetr, management)
        return [("Summe netto:", self._round(netto, 2)),
                ("zzgl. Umsatzsteuer:", self._round(umsatzsteuer, 2)),
                ("Bruttobetrag:", self._round(brutto, 2))]
