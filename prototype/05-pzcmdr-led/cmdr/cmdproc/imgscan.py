import logging
from pydispatch import dispatcher
from PIL import Image
import zbar
import numpy as np
import io

class ImageScanner:
    """
    Scan an image to search for code.
    The scanning library is zbar.
    It listens for the signal "captured_image" to get the image data.

    When a QR-Code is detected, it is sent as the parameter to the signal "got_qrcode".
    """
    def __init__(self):
        self.scanner = zbar.Scanner()
        dispatcher.connect(self.scan, signal='captured_image')

    def scan(self, img_data):
        """
        The handler for extracting QRCode from the image.
        Currently, we only raise a signal when QR-Code is detected.

        Argument:
        img_data -- The byte sequence of the image data.
        """
        img = Image.open(io.BytesIO(img_data))
        gray = img.convert('L')
        result = self.scanner.scan(np.asarray(gray))
        for sym in result:
            if sym.type=='QR-Code':
                dispatcher.send('got_qrcode', self, sym.data)
