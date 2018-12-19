"""
wiim.qrcode

Generate QRCode

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

import os
import qrcode
from PIL import Image
from io import BytesIO

dirname = os.path.dirname(__file__)
logo = Image.open(os.path.join(dirname, 'static/icons/96/wiim_boxborder.png'))
logo = logo.convert("RGBA")


def generate(data):
    # QRCode options
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )

    # set content
    qr.add_data(data)
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
    im.save(img_io, 'PNG')
    img_io.seek(0)
    # im.show()  # show final qrcode image

    return img_io
