P19USTG = "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."
GERMAN_DATE = "%d.%m.%Y"
KONTAKT_ERROR = "Telefon: 012345-1234\noder\nE-Mail: xyz@abcdef.de\n\n\
müssen ausgefüllt sein."
ANSCHRIFT_ERROR = "mindestens\n\nFirma\n\
Strasse und Hausnummer oder Postfach sowie\n\
PLZ und Ort\n\nmüssen befüllt sein."
USTID_ERROR = "entweder\n\n\
Steuernummer: 12345/12345\nund Finanzamt: Ortsname\n\noder\n\n\
Umsatzsteuer-ID: DE999999999\n\nmüssen befüllt sein"
KONTO_ERROR = "Kontoinhaber: Name des Kontos\nIBAN: DE12345678901\n\
BIC: XYZABCDEF\n\n müssen befüllt sein."
BETRIEB_ERROR = "'Betriebsbezeichnung' muss ausgefüllt sein."
NAME_ERROR = "'Name' muss ausgefüllt sein."
ZZIEL_ERROR = "'Zahlungsziel' muss ausgefüllt sein."
STEUERSATZ_ERR_MSG = "'Steuersatz (in %)' darf nur aus Ziffern und\
 '.' bestehen z.B. 7.5 oder 19"


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
