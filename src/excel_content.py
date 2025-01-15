"""
Module excel_content
"""

import os
import math
import pandas as pd
# from src.handle_other_objects import Adresse
from src.kunde import Kunde
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
        self.daten = self.xlsx.parse(sheet_name, header=None)
        self.daten.columns = list(string.ascii_uppercase)[0:len(self.daten
                                                                .columns)]
        self.daten.index = range(1, len(self.daten.index)+1)
        # print(self.daten)
        return self.daten

    def mapReducePositions(self, inp: pd.DataFrame, columns: list)\
            -> pd.DataFrame:
        """maps and reduces DataFrame inp to expected columns"""
        return inp[columns]

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

    def _truncate_array_at_next_empty_cell(self, arr: list, error_msg: str)\
            -> list:
        """return array truncated at next empty cell"""
        SEARCH_ERR = ValueError(error_msg)
        retval = []
        try:
            retval = arr.iat[0, -1] if not math.isnan(arr.iat[0, -1]) else \
                arr.iat[0, 1]
        except TypeError:
            raise SEARCH_ERR
        except IndexError:
            raise SEARCH_ERR
        return retval

    def search_cell_right_of(self, column_name: str, search_value: str)\
            -> list:
        """
        Search in row with column_name for search_value,
            return array with values right of the search_value
            until next empty cell
        """
        if self.daten is None:
            return ""
        arr = self._search_cell_in_column(column_name, search_value)
        return self._truncate_array_at_next_empty_cell(arr,
                                                       self._get_search_err(
                                                           search_value,
                                                           column_name))

    def _get_index_of_nan(self, df: pd.DataFrame) -> int:
        """get first index of next NaN"""
        return next((i for i, v in enumerate(df) if v != v), -1)

    def _search_anschrift(self, spalte: str, search: str,
                          customer: Kunde) -> None:
        """
        Search in specified column until next NaN,
        and fill it into anschrift of customer
        """
        if self.daten is None:
            return None
        an = self.daten[spalte]
        fromIdx = self.daten.index[an == search].tolist()[0]  # + 1
        nan_idx = self._get_index_of_nan(an)  # get first index of NaN in an
        arr = an[fromIdx:nan_idx].to_list()
        # print("_search_anschrift:\n", arr)
        if customer:
            customer.anschrift = arr
            customer.landeskennz = "DE"

    def _split_dataframe_by_search_value(self, column_name: str,
                                         search_value: str) -> dict:
        """
        Search in specified column for search_value return rows until next NaN
        as pandas dataFrame
        """
        if self.daten is None:
            return None
        SEARCH_ERR = ValueError(f"Ich konnte '{search_value}'\
 in Spalte '{column_name}' nicht finden.")
        COL_ERR = ValueError(f"Ich konnte\
 die Spalte '{column_name}' nicht finden.")
        try:
            line = self.daten[self.daten[column_name] == search_value]
        except KeyError:
            raise COL_ERR
        except IndexError:
            raise SEARCH_ERR
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

    def get_address_of_customer(self, spalte: str = "A",
                                anschrift: str = "An:",
                                customer: Kunde = None):
        """returns address of customer in Excel Sheet with \\n joined values"""
        return self._search_anschrift(spalte, anschrift, customer)

    def get_invoice_number(self, spalte: str = "A",
                           rg_nr: str = "Rechnungs-Nr:"
                           ) -> dict:
        """returns tuple ('InvoiceNumberText', invoiceNumber)"""
        theDict = {rg_nr: self.search_cell_right_of(spalte, rg_nr)}
        # self.invoice.invoicenr = theDict   # ToDo. eliminate
        return theDict

    def get_invoice_positions(self, spalte: str = "A",
                              search: str = "Pos.",
                              ) -> dict:
        """
        return pandas DataFrame with positions for invoice
        """
        return self._split_dataframe_by_search_value(spalte, search)

    def _round(self, value, prec: int) -> decimal.Decimal:
        """round decimal to prec as in excel"""
        precStr = '1.' + '0' * prec
        return (decimal.Decimal(value)
                .quantize(decimal.Decimal(precStr),
                          rounding=decimal.ROUND_05UP)
                )

    def get_invoice_sums(self,
                         spalte: str = "F",
                         sum: str = "Summe",
                         USt: str = "Umsatzsteuer 19%",
                         bruttobetr: str = "Bruttobetrag",
                         ):
        """return array of invoice sums"""
        netto = self._round(self.search_cell_right_of(spalte, sum), 2)
        umsatzsteuer = self._round(self.search_cell_right_of(spalte, USt), 2)
        brutto = self._round(self.search_cell_right_of(spalte, bruttobetr), 2)
        return [("Summe netto:", netto),
                ("zzgl. Umsatzsteuer:", umsatzsteuer),
                ("Bruttobetrag:", brutto)]
