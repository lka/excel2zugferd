"""Constants for excel2zugferd."""

P19USTG = "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."
GERMAN_DATE = "%d.%m.%Y"
KONTAKT_ERROR = (
    "Telefon: 012345-1234\noder\nE-Mail: xyz@abcdef.de\n\n" "müssen ausgefüllt sein."
)
ANSCHRIFT_ERROR = (
    "mindestens\n\nFirma\n"
    "Strasse und Hausnummer oder Postfach sowie\n"
    "PLZ und Ort\n\nmüssen befüllt sein."
)
USTID_ERROR = (
    "entweder\n\n"
    "Steuernummer: 12345/12345\nund Finanzamt: Ortsname\n\noder\n\n"
    "Umsatzsteuer-ID: DE999999999\n\nmüssen befüllt sein"
)
KONTO_ERROR = (
    "Kontoinhaber: Name des Kontos\nIBAN: DE12345678901\n"
    "BIC: XYZABCDEF\n\n müssen befüllt sein."
)
BETRIEB_ERROR = "'Betriebsbezeichnung' muss ausgefüllt sein."
NAME_ERROR = "'Name' muss ausgefüllt sein."
STEUERSATZ_ERR_MSG = (
    "'Steuersatz (in %)' darf nur aus Ziffern und" " '.' bestehen z.B. 7.5 oder 19"
)
ANSCHRIFT_POS_ERROR = (
    "Bei den Positionen für Anschrift muss sowohl"
    " Anschrift Spalte, als auch Anschrift Zeile "
    "ausgefüllt sein.\n"
    " Ansonsten müssen beide leer sein, dann wird "
    "nach 'An:' gesucht."
)
RECHNUNG_POS_ERROR = (
    "Bei den Positionen für Rechnungsnummer muss sowohl"
    " Rechnungsnummer Spalte, als auch Rechnungsnummer Zeile"
    " ausgefüllt sein.\n"
    "Ansonsten müssen beide leer sein, dann wird nach "
    "'Rechnungs-Nr:' gesucht."
)
NEGATIVE_PRICE_ERR = (
    "Position {pos}: Der Einzelpreis darf nicht negativ sein. "
    "Negative Beträge bitte über eine negative Menge eintragen."
)
STORNO_POS_ERROR = (
    "Bei den Positionen für Storno muss sowohl"
    " Storno Spalte, als auch Storno Zeile"
    " ausgefüllt sein.\n"
    "Ansonsten müssen beide leer sein."
)
RECHNUNGSDATUM_POS_ERROR = (
    "Bei den Positionen für Rechnungsdatum muss "
    "sowohl Rechnungsdatum Spalte, als auch "
    "Rechnungsdatum Zeile ausgefüllt sein.\n"
    "Ansonsten müssen beide leer sein, dann wird nach"
    " 'Rechnungsdatum:' gesucht."
)
DATUM_NOT_FOUND_ERR = (
    "Das Rechnungsdatum muss im Excel Tabellenblatt"
    " angegeben sein, wenn die Position dafür angegeben "
    "wurde."
)
NETTOSUMME_POS_ERROR = (
    "Bei den Positionen für Nettosumme muss sowohl"
    " Nettosumme Spalte, als auch Nettosumme Zeile "
    "ausgefüllt sein.\n"
    "Ansonsten müssen beide leer sein, dann wird nach "
    "'Summe' gesucht."
)
MWSTSUMME_POS_ERROR = (
    "Bei den Positionen für MwStsumme muss sowohl"
    " MwStsumme Spalte, als auch MwStsumme Zeile "
    "ausgefüllt sein.\n"
    "Ansonsten müssen beide leer sein, dann wird nach "
    "'Umsatzsteuer 19%' gesucht."
)
BRUTTOSUMME_POS_ERROR = (
    "Bei den Positionen für Bruttosumme muss sowohl"
    " Bruttosumme Spalte, als auch Bruttosumme Zeile "
    "ausgefüllt sein.\n"
    "Ansonsten müssen beide leer sein, dann wird nach "
    "'Bruttobetrag' gesucht."
)
EINZELPOSITIONEN_POS_ERR = (
    "Bei den Einzelpositionen müssen entweder alle" " oder kein Wert ausgefüllt sein."
)
UST_KEY_DEFAULT_SPALTE = "E"
ANSCHRIFT_DEFAULT_SPALTE = "A"
RGNR_DEFAULT_SPALTE = "A"
RGDATUM_DEFAULT_SPALTE = "A"
STORNO_DEFAULT_SPALTE = "A"
STORNO_DEFAULT_VALUES = (381, 384)
# ZUGFeRD type_code: Name im Dokumentkopf
STORNO_TYPE_NAMES = {381: "GUTSCHRIFTANZEIGE", 384: "KORREKTURRECHNUNG"}

EINHEITEN = {
    "h": "HUR",
    "min": "MIN",
    "Tag(e)": "DAY",
    "Monat(e)": "MON",
    "Jahr(e)": "ANN",
    "l": "LTR",
    "Liter": "LTR",
    "kg": "KGM",
    "t": "TNE",
    "m": "MTR",
    "m²": "MTK",
    "m³": "MTQ",
    "1": "C62",
    "Stk.": "C62",
    "kWh": "KWH",
    "AW": "E48",
}
LABELWIDTH = 22
TEXTWIDTH = 60
PADX = 5
PADY = 5

# Platzierung des Logos im PDF (A=wie bis Version 0.27.3, L=links, C=mittig, R=rechts)
LOGO_ALIGN_KEY = "LogoAusrichtung"
LOGO_ALIGN_DEFAULT = "A"
LOGO_ALIGN_CHOICES = {
    "Wie bisher (bis 0.27.3)": "A",
    "Links": "L",
    "Mittig": "C",
    "Rechts": "R",
}
LOGO_ALIGN_ERROR = "LogoAusrichtung muss A (wie bisher), L (links), C (mittig) oder R (rechts) sein."
