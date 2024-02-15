import os
import pandas as pd
import math
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

    def readSheetList(self):
        """Read the List of Sheets in this Excel File"""
        return self.xlsx.sheet_names

    def readSheet(self, sheetName) -> None:
        """Read the specified sheet content"""
        self.daten = self.xlsx.parse(sheetName)

    def _searchCellRightOf(self, columnName, searchValue):
        """Search in row with columnName for searchValue, return array with values right of the searchValue until next empty cell"""
        arr = self.daten.loc[self.daten[columnName] == searchValue]
        # print(arr, arr.iat[0, -1], np.NaN, math.isnan(arr.iat[0, -1]))
        return arr.iat[0, -1] if not math.isnan(arr.iat[0, -1]) else arr.iat[0, 1]

    def _getIndexOfNextNaN(self, df):
        """get first index of next NaN"""
        return next((i for i, v in enumerate(df) if v != v), -1)

    def _searchAnschrift(self, search):
        """Search in specified column until next NaN, return string with \\n joined values"""
        an = self.daten[search]
        nan_idx = self._getIndexOfNextNaN(an)  # get first index of NaN in an
        return "\n".join(an[0:nan_idx])

    def _split_dataframe_by_SearchValue(self, columnName, searchValue):
        """Search in specified column for searchValue return rows until next NaN as numpy dataFrame with all cells as strings
        replace column Datum with german date %d.%m.%Y and columns Preis and Summe as float values with Komma separated
        """
        line = self.daten[self.daten[columnName] == searchValue]
        # print(line)
        startIndex = int(line.index[0]) + 1
        tmpDf = self.daten.iloc[startIndex : len(self.daten), :]
        nan_idx = self._getIndexOfNextNaN(tmpDf[columnName])
        retVal = tmpDf[0:nan_idx]
        retVal.columns = line.loc[int(line.index[0])]
        # retVal.style.format({"Datum": lambda t: t.strftime("%d.%m.%Y")})
        try:
            # print (retVal["Datum"])
            retVal["Datum"] = pd.to_datetime(retVal["Datum"]).dt.strftime("%d.%m.%Y")
            # print (retVal["Datum"])
        except:
            pass
        # pattern = "{:.2f} €".format
        # retVal.to_string(formatters={'Preis': pattern, 'Summe': pattern})
        # print(retVal)
        retVal["Preis"] = (
            retVal["Preis"]
            .apply("{:.2f} €".format)
            .apply(lambda x: x.replace(".", ","))
        )
        retVal["Summe"] = (
            retVal["Summe"]
            .apply("{:.2f} €".format)
            .apply(lambda x: x.replace(".", ","))
        )

        return np.r_[line.values, retVal.astype(str).values]

    def getAddressOfCustomer(self):
        """returns address of customer in Excel Sheet with \\n joined values"""
        return self._searchAnschrift("An:")

    def getInvoiceNumber(self):
        """returns tuple ('InvoiceNumberText', invoiceNumber)"""
        return {"Rechnungs-Nr:": self._searchCellRightOf("An:", "Rechnungs-Nr:")}

    def getInvoicePositions(self):
        """return array of array of positions for invoice"""
        return self._split_dataframe_by_SearchValue("An:", "Pos.")

    def getInvoiceSums(self):
        SUMS = "Unnamed: 5"
        netto = "{:.2f} €".format(
            float(self._searchCellRightOf(SUMS, "Summe"))
        ).replace(".", ",")
        umsatzsteuer = "{:.2f} €".format(
            float(self._searchCellRightOf(SUMS, "Umsatzsteuer 19%"))
        ).replace(".", ",")
        brutto = "{:.2f} €".format(
            float(self._searchCellRightOf(SUMS, "Bruttobetrag"))
        ).replace(".", ",")
        return [
            ("Summe netto:", f"{netto}"),
            ("zzgl. Umsatzsteuer 19%:", f"{umsatzsteuer}"),
            ("Bruttobetrag:", f"{brutto}"),
        ]
