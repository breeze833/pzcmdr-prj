from pydispatch import dispatcher
import logging

class QRCode2Cmd:
    """
    Lookup the command by the given QR-Code.
    It listens to the signal "got_qrcode" and send the command with the signal "got_cmd".
    It also listens to the signal "reload" to reload the QR-Code lookup table.
    """
    def __init__(self, qrcodes={}):
        """
        Initialize the lookup component.

        Argument:
        qrcodes -- The lookup table from qrcode to command.
        """
        self.qrcodes = qrcodes
        dispatcher.connect(self.find_cmd, signal="got_qrcode")
        dispatcher.connect(self.reload, signal="reload")

    def find_cmd(self, qrcode):
        cmd = None
        try:
            cmd = self.qrcodes[qrcode][0]
            dispatcher.send("got_cmd", self, cmd)
        except KeyError:
            logging.warning('QR-Code not found')
            dispatcher.send("got_error", self, qrcode)

    def reload(self, qrcodes):
        """
        Reload the lookup table.

        Argument:
        qrcodes -- The lookup table from qrcode to command.
        """
        self.qrcodes = qrcodes
        logging.info('QR-Code lookup table reloaded')
