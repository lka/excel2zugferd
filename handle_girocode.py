"""
Module handle_girocode
"""
import qrcode


# replace german umlauts
def uml2ascii(str):
    uml_dict = {
        'Ä': 'Ae',
        'ä': 'ae',
        'Ö': 'Oe',
        'ö': 'oe',
        'Ü': 'Ue',
        'ü': 'ue',
        'ß': 'ss',
    }

    for u in uml_dict.keys():
        str = str.replace(u, uml_dict[u])

    return str


QR_SIZE = 4
QR_BORDER = 10


class Handle_Girocode:
    """
    Class Handle_Girocode
    """

    def __init__(self, bic: str, iban: str, receiver: str,
                 verbose: bool = False):
        if not (isinstance(bic, (str)) and len(bic) > 0):
            raise ValueError(f"parameter BIC as string \
expected but got {bic}")
        self.bic = bic[:11]
        if not (isinstance(iban, (str)) and len(iban) > 0):
            raise ValueError(f"parameter IBAN as string \
expected but got {iban}")
        self.iban = iban[:34]
        if not (isinstance(receiver, (str)) and len(receiver) > 0):
            raise ValueError(f"parameter receiver as string \
expected but got {receiver}")
        self.receiver = uml2ascii(receiver)[:70]
        self.verbose = verbose
        self.qrdata = None

    def girocodegen(self, amount: float, purpose: str):
        """generate qrcode"""
        # first line is static
        qrdata = 'BCD\n001\n2\nSCT\n'
        qrdata += self.bic + '\n'
        qrdata += self.receiver + '\n'
        qrdata += self.iban + '\n'
        qrdata += 'EUR' + str(abs(amount)) + '\n'
        qrdata += '\n\n' + uml2ascii(purpose)[:140] + '\n'

        if self.verbose:
            self.qrdata = qrdata

        qr = qrcode.QRCode(box_size=QR_SIZE, border=QR_BORDER)
        qr.add_data(qrdata)

        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
