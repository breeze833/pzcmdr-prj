import logging
from pydispatch import dispatcher
from PIL import Image
import zbar
import numpy as np
import io
import asyncio

class JPEG2Image:
    """
    Decode the JPEG bytes to a PIL Image object.
    It listens to the signal "captured_jpeg" to get the JPEG data.
    When the decoded result is ready, it is sent as the parameter to the signal "got_image".
    """
    def __init__(self):
        dispatcher.connect(self.decode, signal='captured_jpeg')

    def decode(self, jpeg_data):
        img = Image.open(io.BytesIO(jpeg_data))
        dispatcher.send('got_image', self, img)

class Image2Gray:
    """
    Convert an Image to a gray-level Image.
    It listens to the signal "got_image" to get the image.
    When the conversion is done, it sends the gray-level image as the parameter to the signal "got_gray".
    """
    def __init__(self):
        dispatcher.connect(self.convert, signal='got_image')

    def convert(self, image_data):
        gray = image_data.convert('L')
        dispatcher.send('got_gray', self, gray)

class QRCodeScanner:
    """
    Scan an image to search for code.
    The scanning library is zbar.
    It listens for the signal "got_gray" to get the gray-level image data.

    When a QR-Code is detected, it is sent as the parameter to the signal "got_qrcode".
    """
    def __init__(self):
        self.scanner = zbar.Scanner()
        dispatcher.connect(self.scan, signal='got_gray')

    async def _scan(self, gray):
        """
        The handler for extracting QRCode from the image.
        The scanning operation would be a long task. Therefore it is executed in a separate thread.
        Currently, we only raise a signal when QR-Code is detected.

        Argument:
        gray -- The gray-level Image object.
        """
        result = await asyncio.get_event_loop().run_in_executor(None, self.scanner.scan, np.asarray(gray))
        #logging.debug('image scanned')
        for sym in result:
            if sym.type=='QR-Code':
                logging.debug('QR-Code detected')
                dispatcher.send('got_qrcode', self, sym.data)

    def scan(self, img_data):
        asyncio.ensure_future(self._scan(img_data))
