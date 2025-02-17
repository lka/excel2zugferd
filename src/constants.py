P19USTG = u"Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."
GERMAN_DATE = "%d.%m.%Y"
KONTAKT_ERROR = (u"Telefon: 012345-1234\noder\nE-Mail: xyz@abcdef.de\n\n"
                 u"müssen ausgefüllt sein.")
ANSCHRIFT_ERROR = (u"mindestens\n\nFirma\n"
                   "Strasse und Hausnummer oder Postfach sowie\n"
                   "PLZ und Ort\n\nmüssen befüllt sein.")
USTID_ERROR = ("entweder\n\n"
               "Steuernummer: 12345/12345\nund Finanzamt: Ortsname\n\noder\n\n"
               u"Umsatzsteuer-ID: DE999999999\n\nmüssen befüllt sein")
KONTO_ERROR = (u"Kontoinhaber: Name des Kontos\nIBAN: DE12345678901\n"
               u"BIC: XYZABCDEF\n\n müssen befüllt sein.")
BETRIEB_ERROR = u"'Betriebsbezeichnung' muss ausgefüllt sein."
NAME_ERROR = "'Name' muss ausgefüllt sein."
STEUERSATZ_ERR_MSG = (u"'Steuersatz (in %)' darf nur aus Ziffern und"
                      " '.' bestehen z.B. 7.5 oder 19")
ANSCHRIFT_POS_ERROR = (u"Bei den Positionen für Anschrift muss sowohl"
                       " Anschrift Spalte, als auch Anschrift Zeile "
                       "ausgefüllt sein.\n"
                       " Ansonsten müssen beide leer sein, dann wird "
                       "nach 'An:' gesucht.")
RECHNUNG_POS_ERROR = (u"Bei den Positionen für Rechnungsnummer muss sowohl"
                      " Rechnungsnummer Spalte, als auch Rechnungsnummer Zeile"
                      " ausgefüllt sein.\n"
                      "Ansonsten müssen beide leer sein, dann wird nach "
                      "'Rechnungs-Nr:' gesucht.")
RECHNUNGSDATUM_POS_ERROR = (u"Bei den Positionen für Rechnungsdatum muss "
                            "sowohl Rechnungsdatum Spalte, als auch "
                            u"Rechnungsdatum Zeile ausgefüllt sein.\n"
                            u"Ansonsten müssen beide leer sein, dann wird nach"
                            " 'Rechnungsdatum:' gesucht.")
DATUM_NOT_FOUND_ERR = (u"Das Rechnungsdatum muss im Excel Tabellenblatt"
                       " angegeben sein, wenn die Position dafür angegeben "
                       "wurde.")
NETTOSUMME_POS_ERROR = (u"Bei den Positionen für Nettosumme muss sowohl"
                        " Nettosumme Spalte, als auch Nettosumme Zeile "
                        u"ausgefüllt sein.\n"
                        u"Ansonsten müssen beide leer sein, dann wird nach "
                        "'Summe' gesucht.")
MWSTSUMME_POS_ERROR = (u"Bei den Positionen für MwStsumme muss sowohl"
                       " MwStsumme Spalte, als auch MwStsumme Zeile "
                       u"ausgefüllt sein.\n"
                       u"Ansonsten müssen beide leer sein, dann wird nach "
                       "'Umsatzsteuer 19%' gesucht.")
BRUTTOSUMME_POS_ERROR = (u"Bei den Positionen für Bruttosumme muss sowohl"
                         " Bruttosumme Spalte, als auch Bruttosumme Zeile "
                         u"ausgefüllt sein.\n"
                         u"Ansonsten müssen beide leer sein, dann wird nach "
                         "'Bruttobetrag' gesucht.")
EINZELPOSITIONEN_POS_ERR = (u"Bei den Einzelpositionen müssen entweder alle"
                            " oder kein Wert ausgefüllt sein.")
ANSCHRIFT_DEFAULT_SPALTE = "A"
RGNR_DEFAULT_SPALTE = "A"
RGDATUM_REFAULT_SPALTE = "A"

EINHEITEN = {
    'h': 'HUR',
    'min': 'MIN',
    'Tag(e)': 'DAY',
    'Monat(e)': 'MON',
    'Jahr(e)': 'ANN',
    'l': 'LTR',
    'Liter': 'LTR',
    'kg': 'KGM',
    't': 'TNE',
    'm': 'MTR',
    'm²': 'MTK',
    'm³': 'MTQ',
    '1': 'C62',
    'Stk.': 'C62',
    'kWh': 'KWH'
    }
LABELWIDTH = 22
TEXTWIDTH = 60
PADX = 5
PADY = 5
