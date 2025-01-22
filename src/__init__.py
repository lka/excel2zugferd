import src.oberflaeche_base
import src.oberflaeche_ini
import src.oberflaeche_steuerung
import src.oberflaeche_excelpositions
import src.oberflaeche_excelsteuerung  # noqa F404


def format_ioerr(err: IOError) -> str:
    """
    format IOError corresponding to errno and string
    """
    return f"Error ({0}): {1}".format(err.errno, err.strerror)


def _normalize(arr_in: list) -> list:
    """remove empty elements of array"""
    return list(filter(None, arr_in))


def _setNoneIfEmpty(str_in: str) -> str | None:
    # print("_setNoneIfEmpty:", str_in)
    if str_in is None:
        return None
    trimmed = str_in.strip()
    trimmed = ' '.join(trimmed.split())
    return trimmed if trimmed != "" else None
