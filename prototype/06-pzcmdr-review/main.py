from pydispatch import dispatcher
import logging
import signal
import os
import asyncio
import sys
from cmdr import RC522
from cmdr import VC0706
from cmdr import UID2Cmd
from cmdr import QRCode2Cmd
from cmdr import UIDLogger
from cmdr import ImageScanner
from cmdr import RGB_LED
from cmdr import CmdExec

class SysSigHandler:
    def __init__(self, iddb_file, cmds_file):
        """
        Initialize the signal handlers.

        Arguments:
        iddb_file -- The path to the ID-to-Cmd lookup table.
        cmds_file -- The path to the Cmd-to-ExecCode lookup table.
        """
        self.iddb_file = iddb_file
        self.cmds_file = cmds_file
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, self.exit_gracefully)
        loop.add_signal_handler(signal.SIGINT, self.exit_gracefully)
        loop.add_signal_handler(signal.SIGUSR1, self.reload)
        loop.add_signal_handler(signal.SIGUSR2, self.toggle_leak_uid)
        loop.add_signal_handler(signal.SIGCHLD, self.child_exit)
    def exit_gracefully(self):
        logging.debug('cancelling tasks...')
        [task.cancel() for task in asyncio.Task.all_tasks()]
        asyncio.get_event_loop().stop()
    def reload(self):
        try:
            lookup_tables = load_lookup_tables(self.iddb_file, self.cmds_file)
            dispatcher.send(signal="reload", sender=dispatcher.Any, commands=lookup_tables['commands'], uids=lookup_tables['uids'], qrcodes=lookup_tables['qrcodes'])
        except:
            dispatcher.send(signal="got_error")
    def toggle_leak_uid(self):
        dispatcher.send("toggle_leak_uid")
    def child_exit(self):
        logging.debug('child process exit')
        os.waitpid(0, 0)

def load_lookup_tables(iddb_file, cmds_file):
    exec_g = {}
    exec_l = {}
    try:
        exec(open(iddb_file).read(), exec_g, exec_l)
        exec(open(cmds_file).read(), exec_g, exec_l)
    except:
        dispatcher.send(signal='got_error')
    finally:
        return exec_l

def main(log_level=logging.INFO):
    logging.basicConfig(level=log_level)

    iddb_file = './iddb.py'
    cmds_file = './cmds.py'

    lookup_tables = None
    try:
        iddb_file = sys.argv[1]
        cmds_file = sys.argv[2]
    except:
        pass
    finally:
        lookup_tables = load_lookup_tables(iddb_file, cmds_file)
        logging.info('ID file is {idfile} and CMD file is {cmdfile}'.format(idfile=iddb_file, cmdfile=cmds_file))

    loop = asyncio.get_event_loop()

    sig_handlers = SysSigHandler(iddb_file, cmds_file)

    rfid_reader = RC522()
    serial_camera = VC0706()
    uid2cmd = UID2Cmd(lookup_tables['uids'])
    qrcode2cmd = QRCode2Cmd(lookup_tables['qrcodes'])
    uid_logger = UIDLogger()
    image_scanner = ImageScanner()
    rgb_led = RGB_LED()
    cmdexec = CmdExec(lookup_tables['commands'])

    dispatcher.send("start_rfid_reader")
    dispatcher.send("start_capture")

    try:
        loop.run_forever()
    finally:
        logging.debug('waiting for all tasks done...')
        loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(), return_exceptions=True))
        loop.close()

if __name__=='__main__':
    main(log_level=logging.__dict__[os.getenv('PZCMDR_LOGLEVEL','INFO')])
