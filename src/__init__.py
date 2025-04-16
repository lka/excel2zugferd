import os
import src.oberflaeche_base
import src.oberflaeche_excel2zugferd
import src.oberflaeche_ini
import src.oberflaeche_steuerung
import src.oberflaeche_excelpositions
import src.oberflaeche_excelsteuerung  # noqa F404


def _normalize(arr_in: list) -> list:
    """remove empty elements of array"""
    return list(filter(None, arr_in))


def _setNoneIfEmpty(str_in: str) -> str | None:
    # print("_setNoneIfEmpty:", str_in)
    if str_in is None:
        return None
    trimmed = str_in.strip()
    trimmed = " ".join(trimmed.split())
    return trimmed if trimmed != "" else None


def logo_fn() -> str:
    return os.path.join(
        os.getenv("APPDATA"), "excel2zugferd", "logo.jpg"  # type: ignore
    )
