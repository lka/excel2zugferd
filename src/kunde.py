"""
Modul Kunde
"""

from src.adresse import Adresse
from src.constants import ANSCHRIFT_ERROR
import src


class Kunde(Adresse):

    def __init__(self):
        super().__init__()

    @property
    def anschrift(self) -> str:
        return super().anschrift

    @anschrift.setter
    def anschrift(self, arr: list) -> None:
        self._check_dimensions_of_arr(arr)
        # print(arr)
        self.betriebsbezeichnung = src._setNoneIfEmpty(arr[0])
        if len(arr) == 5:
            self.adresszusatz = src._setNoneIfEmpty(arr[1])
            self.name = src._setNoneIfEmpty(arr[2])
        elif len(arr) == 4:
            self.name = src._setNoneIfEmpty(arr[1])
        self._fill_str_hnr(src._setNoneIfEmpty(arr[-2]))
        self._fill_plz_ort(src._setNoneIfEmpty(arr[-1]))

    # def _fill_adresszeile1(self, zeile1: str) -> None:
    #     if len(zeile1) == 0:
    #         raise ValueError(ANSCHRIFT_ERROR)
    #     self.anschrift_line1 = zeile1

    def _check_dimensions_of_arr(self, arr: list) -> None:
        if arr is None or len(arr) < 3 or len(arr) > 5:
            raise ValueError(ANSCHRIFT_ERROR)

    def _fill_postfach(self, postfach):
        sub = src._normalize(postfach.rsplit(" ", 1))
        if len(sub) == 2:
            self.postfach = sub[1]
        else:
            raise ANSCHRIFT_ERROR

    def _fill_str_hnr(self, strasse):
        if "Postfach" in strasse:
            self._fill_postfach(strasse)
        else:
            sub = src._normalize(strasse.rsplit(" ", 1))
            self.strasse = sub[0]
            if len(sub) == 2:
                self.hausnummer = sub[1]

    def _fill_plz_ort(self, ort):
        sub = src._normalize(ort.split(" ", 1))
        self.plz = sub[0]
        if len(sub) == 2:
            self.ort = sub[1]
        else:
            raise ValueError(ANSCHRIFT_ERROR)
