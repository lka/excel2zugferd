"""
Module excel_content
"""

import os
import math
import pandas as pd
import numpy as np


class ExcelContent:
    """Handle Content of Excel Files"""

    def __init__(self, filename, directory):
        self.fn = filename
        self.dir = directory
        self.path = os.path.join(self.dir, self.fn)
        self.daten = None
        try:
            self.xlsx = pd.ExcelFile(self.path)
            pd.options.mode.copy_on_write = True
        except FileNotFoundError:
            pass

    def read_sheet_list(self):
        """Read the List of Sheets in this Excel File"""
        return self.xlsx.sheet_names

    def read_sheet(self, sheet_name) -> None:
        """Read the specified sheet content"""
        self.daten = self.xlsx.parse(sheet_name)

    def search_cell_right_of(self, column_name, search_value):
        """
        Search in row with column_name for search_value, 
            return array with values right of the search_value
            until next empty cell
        """
        if self.daten is None:
            return ""
        arr = self.daten.loc[self.daten[column_name] == search_value]
        # print(arr, arr.iat[0, -1], np.NaN, math.isnan(arr.iat[0, -1]))
        return arr.iat[0, -1] if not math.isnan(arr.iat[0, -1]) else \
            arr.iat[0, 1]

    def _get_index_of_nan(self, df) -> int:
        """get first index of next NaN"""
        return next((i for i, v in enumerate(df) if v != v), -1)

    def _search_anschrift(self, search):
        """
        Search in specified column until next NaN, 
        return string with \\n joined values
        """
        if self.daten is None:
            return None
        an = self.daten[search]
        nan_idx = self._get_index_of_nan(an)  # get first index of NaN in an
        return "\n".join(an[0:nan_idx])

    def _split_dataframe_by_search_value(self, column_name: str,
                                         search_value: str):
        """
        Search in specified column for search_value return rows until next NaN
        as numpy dataFrame with all cells as strings
        replace column Datum with german date %d.%m.%Y and columns Preis and
        Summe as float values with Komma separated
        """
        if self.daten is None:
            return None
        line = self.daten[self.daten[column_name] == search_value]
        # print(line)
        start_index = int(line.index[0]) + 1
        tmpdf = self.daten.iloc[
            start_index : len(self.daten), :  # noqa: E203
        ]
        nan_idx = self._get_index_of_nan(tmpdf[column_name])
        retval = tmpdf[0:nan_idx]
        retval.columns = line.loc[int(line.index[0])]
        # retval.style.format({"Datum": lambda t: t.strftime("%d.%m.%Y")})
        # print (retval["Datum"])
        retval["Datum"] = pd.to_datetime(retval["Datum"], errors="coerce").dt\
            .strftime("%d.%m.%Y")
        # print (retval["Datum"])
        # pattern = "{:.2f} €".format
        # retval.to_string(formatters={'Preis': pattern, 'Summe': pattern})
        # print(retval)
        retval["Preis"] = (
            retval["Preis"]
            .apply("{:.2f} €".format)
            .apply(lambda x: x.replace(".", ","))
        )
        retval["Summe"] = (
            retval["Summe"]
            .apply("{:.2f} €".format)
            .apply(lambda x: x.replace(".", ","))
        )

        return np.r_[line.values, retval.astype(str).values]

    def get_address_of_customer(self):
        """returns address of customer in Excel Sheet with \\n joined values"""
        return self._search_anschrift("An:")

    def get_invoice_number(self):
        """returns tuple ('InvoiceNumberText', invoiceNumber)"""
        return {"Rechnungs-Nr:": self.search_cell_right_of("An:",
                                                           "Rechnungs-Nr:")}

    def get_invoice_positions(self):
        """return array of array of positions for invoice"""
        return self._split_dataframe_by_search_value("An:", "Pos.")

    def get_invoice_sums(self):
        """return array of invoice sums"""
        sums = "Unnamed: 5"
        netto = (
            f"{float(self.search_cell_right_of(sums, 'Summe')):.2f} €"
            .replace(".", ",")
        )
        _mwst = float(self.search_cell_right_of(sums, 'Umsatzsteuer 19%'))
        umsatzsteuer = (
            f"{_mwst:.2f} €".replace(".", ",")
        )
        brutto = (
            f"{float(self.search_cell_right_of(sums, 'Bruttobetrag')):.2f} €"
            .replace(".", ",")
        )
        return [
            ("Summe netto:", f"{netto}"),
            ("zzgl. Umsatzsteuer 19%:", f"{umsatzsteuer}"),
            ("Bruttobetrag:", f"{brutto}"),
        ]
