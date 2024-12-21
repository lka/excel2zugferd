"""
Module excel_content
"""

import os
import math
import pandas as pd
import numpy as np
from src.handle_other_objects import Adresse
import locale
import decimal


class ExcelContent:
    """Handle Content of Excel Files"""

    def __init__(self, filename: str, directory: str):
        self.fn: str = filename
        self.dir: str = directory
        self.path: str = os.path.join(self.dir, self.fn)
        self.daten: pd.DataFrame = None
        self.invoice_poitions: pd.DataFrame = None
        self.customer = Adresse()
        self.summen = None
        try:
            self.xlsx = pd.ExcelFile(self.path)
            pd.options.mode.copy_on_write = True
        except FileNotFoundError:
            pass
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

    def read_sheet_list(self):
        """Read the List of Sheets in this Excel File"""
        return self.xlsx.sheet_names

    def read_sheet(self, sheet_name) -> None:
        """Read the specified sheet content"""
        self.daten = self.xlsx.parse(sheet_name)

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

    def _get_index_of_nan(self, df) -> int:
        """get first index of next NaN"""
        return next((i for i, v in enumerate(df) if v != v), -1)

    def _search_anschrift(self, search: str) -> None:
        """
        Search in specified column until next NaN,
        and fill it into anschrift of customer
        """
        if self.daten is None:
            return None
        an = self.daten[search]
        nan_idx = self._get_index_of_nan(an)  # get first index of NaN in an
        arr = an[0:nan_idx].to_list()
        self.customer.anschrift = arr
        self.customer.landeskennz = "DE"
        # return "\n".join(arr)

    def get_maxlengths(self, df: pd.DataFrame) -> list:
        """
        get array with max string length of each column in pandas DataFrame
        """
        lenArr = []
        for c in df:
            theLength = max(df[c].astype(str).map(len).max(), len(c))
            # print('Max length of column %s: %s' % (c, theLength))
            lenArr.append(theLength)
        return lenArr

    def _currency(self, amount: float | decimal.Decimal) -> str:
        """return str as locale currency"""
        return locale.currency(amount, grouping=True)

    def _change_values_to_german(self, df: pd.DataFrame,
                                 datum: str = "Datum",
                                 preis: str = "Preis",
                                 summe: str = "Summe",
                                 anzahl: str = "Anzahl") -> None:
        """
        replace column Datum with german date %d.%m.%Y and columns Preis and
        Summe as float values with Komma separated"""
        retval = df
        # retval.style.format({datum: lambda t: t.strftime("%d.%m.%Y")
        #                      if len(t) > 0 else ""})
        retval[datum] = pd.to_datetime(retval[datum],
                                       errors="ignore").dt.strftime("%d.%m.%Y")
        retval[datum] = retval[datum].fillna("")  # substitute NaN by ""
        # pd.describe_option("styler.format.decimal")
        # pd.set_option("styler.format.decimal", ",")
        # pd.describe_option("styler.format.decimal")
        # pd.options.styler.format.thousands = "."
        # print(retval[datum])
        # pattern = "{:.2f} €".format
        # retval.to_string(formatters={preis: pattern, summe: pattern})
        # print(retval)
        retval[anzahl] = (
            retval[anzahl]
            .apply("{:n}".format)
            # .apply(lambda x: x.replace(".", ","))
            # .apply(lambda x: locale.format_string('%.2g', x))
        )
        retval[preis] = (
            retval[preis]
            # .apply("{:.2f} €".format)
            # .apply(lambda x: x.replace(".", ","))
            .apply(lambda x: self._currency(x))
        )
        retval[summe] = (
            retval[summe]
            # .apply("{:.2f} €".format)
            # .apply(lambda x: x.replace(".", ","))
            .apply(lambda x: self._currency(x))
        )

    def _split_dataframe_by_search_value(self, column_name: str,
                                         search_value: str) -> dict:
        """
        Search in specified column for search_value return rows until next NaN
        as numpy dataFrame with all cells as strings, append
        maxlengths of columns to dict as {'daten': np.r_[], 'maxlengths': []}
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
            start_index = int(line.index[0]) + 1
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

    def get_address_of_customer(self, anschrift: str = "An:"):
        """returns address of customer in Excel Sheet with \\n joined values"""
        return self._search_anschrift(anschrift)

    def get_invoice_number(self, spalte: str = "An:",
                           rg_nr: str = "Rechnungs-Nr:"):
        """returns tuple ('InvoiceNumberText', invoiceNumber)"""
        return {rg_nr: self.search_cell_right_of(spalte, rg_nr)}

    def get_invoice_positions(self, spalte: str = "An:",
                              search: str = "Pos.") -> dict:
        """
        return dict with array of array of positions for invoice
        and maxlengths of columns
        {'daten': np.r_[], 'maxlengths': []}
        """
        retval = self._split_dataframe_by_search_value(spalte, search)
        self.invoice_poitions = np.r_[[retval.columns],
                                      retval.astype(str).values]
        self._change_values_to_german(retval)
        # print(retval)
        lenArr = self.get_maxlengths(retval)
        # print(lenArr)

        # return {'daten': np.r_[line.values, retval.astype(str).values],
        return {'daten': np.r_[[retval.columns], retval.astype(str).values],
                'maxlengths': lenArr}

    def _round(self, value, prec: int) -> decimal.Decimal:
        """round decimal to prec as in excel"""
        precStr = '1.' + '0' * prec
        return (decimal.Decimal(value)
                .quantize(decimal.Decimal(precStr),
                          rounding=decimal.ROUND_05UP)
                )

    def get_invoice_sums(self,
                         spalte: str = "Unnamed: 5",
                         sum: str = "Summe",
                         USt: str = "Umsatzsteuer 19%",
                         bruttobetr: str = "Bruttobetrag"):
        """return array of invoice sums"""
        netto = self._round(self.search_cell_right_of(spalte, sum), 2)
        umsatzsteuer = self._round(self.search_cell_right_of(spalte, USt), 2)
        brutto = self._round(self.search_cell_right_of(spalte, bruttobetr), 2)
        self.summen = [netto,
                       umsatzsteuer,
                       brutto]  # saved for for xml
        return [
            ("Summe netto:", self._currency(netto)),
            ("zzgl. Umsatzsteuer 19%:", self._currency(umsatzsteuer)),
            ("Bruttobetrag:", self._currency(brutto))
        ]
