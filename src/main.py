from pydispatch import dispatcher
import logging
logger = logging.getLogger('pzcmdr')
import signal
import os
import asyncio
import sys
import argparse
from cmdr import RC522
from cmdr import VC0706
from cmdr import UID2Cmd
from cmdr import QRCode2Cmd
from cmdr import UIDLogger
from cmdr import JPEG2Image, Image2Gray, QRCodeScanner
from cmdr import RGB_LED
from cmdr import CmdExec

class App:
    def setup_signal_handlers(self):
        """
        Initialize the signal handlers.
        """
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, self.exit_gracefully)
        loop.add_signal_handler(signal.SIGINT, self.exit_gracefully)
        loop.add_signal_handler(signal.SIGUSR1, self.reload)
        loop.add_signal_handler(signal.SIGUSR2, self.toggle_leak_uid)
        loop.add_signal_handler(signal.SIGCHLD, self.child_exit)

    def exit_gracefully(self):
        logger.debug('cancelling tasks...')
        [task.cancel() for task in asyncio.Task.all_tasks()]
        asyncio.get_event_loop().stop()

    def reload(self):
        try:
            lookup_tables = self.load_lookup_tables()
            dispatcher.send(signal="reload", sender=dispatcher.Any, commands=lookup_tables['commands'], uids=lookup_tables['uids'], qrcodes=lookup_tables['qrcodes'])
        except:
            dispatcher.send(signal="got_error")

    def toggle_leak_uid(self):
        dispatcher.send("toggle_leak_uid")
        
    def child_exit(self):
        logger.debug('child process exit')
        os.waitpid(0, 0)

    def load_lookup_tables(self):
        """
        Load lookup tables from files.
        """
        exec_g = {}
        exec_l = {}
        try:
            exec(open(self.iddb_file).read(), exec_g, exec_l)
            exec(open(self.cmds_file).read(), exec_g, exec_l)
        except:
            dispatcher.send(signal='got_error')
        finally:
            return exec_l

    def setup_processing_components(self):
        lookup_tables = self.load_lookup_tables()
        self.rfid_reader = RC522()
        self.serial_camera = VC0706()
        self.uid2cmd = UID2Cmd(lookup_tables['uids'])
        self.qrcode2cmd = QRCode2Cmd(lookup_tables['qrcodes'])
        self.uid_logger = UIDLogger()
        self.jpeg2image = JPEG2Image()
        self.image2gray = Image2Gray()
        self.qrcode_scanner = QRCodeScanner()
        self.rgb_led = RGB_LED()
        self.cmdexec = CmdExec(lookup_tables['commands'])

    def __init__(self, iddb_file, cmds_file):
        self.iddb_file = iddb_file
        self.cmds_file = cmds_file
        logger.info('ID file is {idfile} and CMD file is {cmdfile}'.format(idfile=self.iddb_file, cmdfile=self.cmds_file))

        self.setup_signal_handlers()
        self.setup_processing_components()
        
    def run(self):
        dispatcher.send("start")

        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        finally:
            logger.debug('waiting for all tasks done...')
            loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(), return_exceptions=True))
            loop.close()

if __name__=='__main__':
    logging.basicConfig(level=logging.__dict__[os.getenv('PZCMDR_LOGLEVEL','INFO')])
    parser = argparse.ArgumentParser()
    parser.add_argument('--iddb', help='The ID to command lookup tables', default='./config/iddb.py')
    parser.add_argument('--cmds', help='The command to code lookup table', default='./config/cmds.py')
    args = parser.parse_args()
    app = App(args.iddb, args.cmds)
    app.run()

