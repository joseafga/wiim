"""
wiim.qrcode

Generate QRCode

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

import qrcode
from PIL import Image
from io import BytesIO

logo = Image.open('wiim/static/images/logo/wiim_boxborder.png')
logo = logo.convert("RGBA")


def generate(type, id):
    # QRCode options
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )

    # set content
    qr.add_data(type + ':' + str(id))
    qr.make(fit=True)

    # create QRCode image
    im = qr.make_image().convert("RGB")

    # logo image configuration
    size = (80, 80)
    coods = tuple(map(lambda x, y: int((x - y) / 2), im.size, size))
    region = logo.resize(size, Image.BILINEAR)
    # place logo in qrcode image
    im.paste(region, coods)

    # get file bytes
    img_io = BytesIO()
    im.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    # im.show()  # show final qrcode image

    return img_io
